"""Conversation provider that converts answers to Hessisch dialect."""
from __future__ import annotations

from homeassistant.components.conversation import (
    AbstractConversationProvider,
    ConversationInput,
    ConversationResult,
)
from homeassistant.core import HomeAssistant

from .dialect import convert_to_hessisch


class HessischConversationProvider(AbstractConversationProvider):
    """Conversation provider that wraps the default provider and adds dialect."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.id = "hessisch_assist"
        self.name = "Hessisch Assist"

    @property
    def supported_languages(self) -> list[str]:
        """Supported languages."""
        return ["de"]

    async def async_process(
        self, text: str, context: ConversationInput | None = None
    ) -> ConversationResult:
        """Process a request via default conversation service and return Hessisch reply."""

        result = await self.hass.services.async_call(
            "conversation",
            "process",
            {"text": text},
            blocking=True,
            return_response=True,
        )

        # Extract proper response text for HA 2024.10+
        try:
            orig
            
