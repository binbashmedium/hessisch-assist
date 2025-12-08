"""Conversation agent that converts answers to Hessisch dialect."""
from __future__ import annotations

from typing import Any, Literal

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
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant

from .dialect import convert_to_hessisch


class HessischConversationAgent(AbstractConversationAgent):
    """Conversation agent that wraps the default agent and adds Hessisch dialect."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self._entry = entry

    @property
    def id(self) -> str:
        """Return the unique id of the agent."""
        return self._entry.entry_id

    @property
    def name(self) -> str:
        """Return the human readable name of the agent."""
        return self._entry.title or "Hessisch Assist"

    @property
    def supported_languages(self) -> set[str] | Literal["*"]:
        """Return languages supported by this agent."""
        # Wir hängen uns nur hinter den Standard-Agent – alle Sprachen erlaubt.
        return MATCH_ALL

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Handle a conversation turn via the built-in agent and translate the reply."""
        # 1. Erst den Home-Assistant-Standardagenten ausführen
        base_result: ConversationResult = await async_converse(
            hass=self.hass,
            text=user_input.text,
            conversation_id=user_input.conversation_id,
            context=user_input.context,
            language=user_input.language,
            agent_id=HOME_ASSISTANT_AGENT,
        )

        # Wenn keine Antwort vorhanden ist, nichts anfassen
        if base_result.response is None:
            return base_result

        response = base_result.response

        # 2. Plain-Text der Antwort ins Hessische umschreiben
        try:
            # Struktur entspricht dem /api/conversation/process-Result:
            # response.speech["plain"]["speech"] -> Text
            plain: dict[str, Any] = response.speech.get("plain", {})  # type: ignore[assignment]
            original_text: str = plain.get("speech") or ""
            if original_text:
                plain["speech"] = convert_to_hessisch(original_text)
        except Exception:
            # Sicherheit: lieber Originalantwort lassen als Assist crashen
            return base_result

        return base_result
        
