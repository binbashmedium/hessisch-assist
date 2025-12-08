"""Conversation agent that converts answers to Hessisch dialect."""
from __future__ import annotations

from typing import Any

from homeassistant.components.conversation import (
    HOME_ASSISTANT_AGENT,
    async_converse,
)
from homeassistant.components.conversation.models import (
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .dialect import convert_to_hessisch


class HessischConversationAgent(AbstractConversationAgent):
    """Conversation agent that wraps the default agent and adds Hessisch dialect."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self._entry = entry
        # ID und Name, wie HA sie im UI anzeigt
        self.id = entry.entry_id
        self.name = entry.title or "Hessisch Assist"
        # Wir akzeptieren alle Sprachen; Hessisch macht bei Deutsch am meisten Sinn
        # MATCH_ALL wäre sauberer, ist aber hier nicht zwingend notwendig.
        self.supported_languages = {"*"}

    async def async_process(
        self,
        user_input: ConversationInput,
    ) -> ConversationResult:
        """Handle a conversation turn via the built-in agent and translate the reply."""

        # 1. Standard-Home-Assistant-Agent aufrufen, NICHT uns selbst
        base_result: ConversationResult = await async_converse(
            hass=self.hass,
            text=user_input.text,
            conversation_id=user_input.conversation_id,
            context=user_input.context,
            language=user_input.language,
            agent_id=HOME_ASSISTANT_AGENT,
        )

        # 2. Wenn keine Antwort da ist, einfach zurückgeben
        if base_result.response is None:
            return base_result

        response = base_result.response

        # 3. Plain-Speech-Text ins Hessische umschreiben
        try:
            # Struktur entspricht dem, was das Conversation-API per /api/conversation/process liefert:
            # response.speech["plain"]["speech"] -> Text
            plain: dict[str, Any] = response.speech.get("plain", {})
            original_text: str = plain.get("speech") or ""
            if original_text:
                plain["speech"] = convert_to_hessisch(original_text)
        except Exception:
            # Wenn sich intern mal was ändert, lieber gar nicht ändern als crashen
            return base_result

        return base_result
        
