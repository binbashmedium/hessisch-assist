"""Conversation agent that converts Home Assistant replies to Hessisch dialect."""
from __future__ import annotations

from typing import Any, Literal
import re

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

    # ------------------------------------------------------------------------
    # Required abstract properties
    # ------------------------------------------------------------------------

    @property
    def id(self) -> str:
        """Unique agent ID."""
        return self._entry.entry_id

    @property
    def name(self) -> str:
        """Human-readable agent name."""
        return self._entry.title or "Hessisch Assist"

    @property
    def supported_languages(self) -> set[str] | Literal["*"]:
        """Support all languages (Hessisch applies only to text content)."""
        return MATCH_ALL

    # ------------------------------------------------------------------------
    # Core Conversation Handler
    # ------------------------------------------------------------------------

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Handle a conversation turn via HA's internal agent and translate the reply."""

        # -------------------------------------------------------------
        # 1. Original agent ausführen (Home Assistant built-in agent)
        # -------------------------------------------------------------
        base_result: ConversationResult = await async_converse(
            hass=self.hass,
            text=user_input.text,
            conversation_id=user_input.conversation_id,
            context=user_input.context,
            language=user_input.language,
            agent_id=HOME_ASSISTANT_AGENT,
        )

        # If HA produced no response → do nothing
        if base_result.response is None:
            return base_result

        response = base_result.response

        # -------------------------------------------------------------
        # 2. PRIORITÄT 1: response_text (LLM / Smart Assist)
        # -------------------------------------------------------------
        try:
            if getattr(base_result, "response_text", None):
                base_result.response_text = convert_to_hessisch(
                    base_result.response_text
                )
        except Exception:
            pass  # Never break assist flow

        # -------------------------------------------------------------
        # 3. PRIORITÄT 2: speech.plain.speech
        # -------------------------------------------------------------
        try:
            plain: dict[str, Any] = response.speech.get("plain", {})
            if "speech" in plain and plain["speech"]:
                plain["speech"] = convert_to_hessisch(plain["speech"])
        except Exception:
            pass

        # -------------------------------------------------------------
        # 4. PRIORITÄT 3: speech.ssml (Text-to-Speech pipelines)
        # -------------------------------------------------------------
        try:
            ssml = response.speech.get("ssml")
            if ssml:
                # Remove tags → convert text → reinsert
                text_only = re.sub("<[^>]+>", "", ssml)
                if text_only.strip():
                    ssml = ssml.replace(text_only, convert_to_hessisch(text_only))
                    response.speech["ssml"] = ssml
        except Exception:
            pass

        return base_result
        
