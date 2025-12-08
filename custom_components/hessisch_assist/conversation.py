"""Conversation provider that converts answers to Hessisch dialect."""
from __future__ import annotations

from typing import Iterable

from homeassistant.components.conversation import (
    AbstractConversationProvider,
    ConversationResult,
)
from homeassistant.core import Context, HomeAssistant

from .dialect import convert_to_hessisch


class HessischConversationProvider(AbstractConversationProvider):
    """Conversation provider that wraps the default provider and adds dialect."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the provider."""
        self.hass = hass
        self.id = "hessisch_assist"
        self.name = "Hessisch Assist"

    @property
    def supported_languages(self) -> Iterable[str]:  # pragma: no cover - interface property
        """Return supported languages."""
        return ["de", "de-DE"]

    async def async_process(self, text: str, context: Context | None) -> ConversationResult:
        """Process a conversation request and return a dialect response."""

        result = await self.hass.services.async_call(
            "conversation",
            "process",
            {"text": text},
            blocking=True,
            return_response=True,
        )

        original = result.get("response", "") if isinstance(result, dict) else ""
        dialect = convert_to_hessisch(str(original))

        return ConversationResult(text=dialect)
