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
    """Hessisch dialect conversation provider."""

    @property
    def provider_type(self) -> str:
        """Declare provider type."""
        return "local"

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.id = "hessisch_assist"
        self.name = "Hessisch Assist"

    @property
    def supported_languages(self) -> list[str]:
        return ["de"]

    async def async_process(
        self, text: str, context: ConversationInput | None = None
    ) -> ConversationResult:

        result = await self.hass.services.async_call(
            "conversation",
            "process",
            {"text": text},
            blocking=True,
            return_response=True,
        )

        try:
            original = result["response"]["speech"]["plain"]["speech"]
        except Exception:
            original = ""

        return ConversationResult(
            text=convert_to_hessisch(original)
        )
        
