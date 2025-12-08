"""Conversation provider that converts answers to Hessisch dialect."""
from __future__ import annotations

from homeassistant.components.conversation import (
    AbstractConversationProvider,
    ConversationResult,
)
from homeassistant.core import HomeAssistant

from .dialect import convert_to_hessisch


class HessischConversationProvider(AbstractConversationProvider):
    """Conversation provider that wraps the default provider and adds dialect."""

    def __init__(self, hass):
        self.hass = hass
        self.id = "hessisch_assist"
        self.name = "Hessisch Assist"

    async def async_process(self, text, context):
        result = await self.hass.services.async_call(
            "conversation",
            "process",
            {"text": text},
            blocking=True,
            return_response=True
        )
        original = result.get("response", "")
        dialect = convert_to_hessisch(original)
        return ConversationResult(text=dialect)
