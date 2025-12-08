"""Conversation provider that converts responses into Frankfurt dialect."""
from __future__ import annotations

from typing import Iterable

from homeassistant.components.conversation import (
    AbstractConversationProvider,
    ConversationResult,
)
from homeassistant.core import Context, HomeAssistant

from .dialect import convert_to_frankfurt


class FrankfurtConversationProvider(AbstractConversationProvider):
    """Conversation provider that wraps the default provider and adds dialect."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the provider."""
        self.hass = hass

    @property
    def id(self) -> str:  # pragma: no cover - interface property
        """Return stable id for the provider."""
        return "frankfurt_assist"

    @property
    def name(self) -> str:  # pragma: no cover - interface property
        """Return display name for the provider."""
        return "Frankfurt Assist"

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

        original = result.get("response", "")
        dialect = convert_to_frankfurt(str(original))

        return ConversationResult(text=dialect)
