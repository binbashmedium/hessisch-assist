"""Hessisch Assist custom conversation agent."""
from __future__ import annotations

from homeassistant.components.conversation.models import (
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
)
from homeassistant.core import HomeAssistant

from .dialect import convert_to_hessisch


class HessischAgent(AbstractConversationAgent):
    """A conversation agent that converts HA replies to Hessisch dialect."""

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.id = "hessisch_assist"
        self.name = "Hessisch Assist"

    @property
    def supported_languages(self):
        return ["de"]

    async def async_prepare(self, language: str) -> None:
        """Prepare the agent for a specific language."""
        return

    async def async_process(
        self, user_input: ConversationInput, conversation_id: str | None
    ) -> ConversationResult:
        """Process user input through the default agent, then hessisch-ify it."""

        # Call the default agent
        default = self.hass.components.conversation.async_get_agent(
            self.hass, None
        )
        if default is None:
            return ConversationResult(text="Fehler: Kein Standard-Agent.")

        result = await default.async_process(user_input, conversation_id)

        # Extract plain text
        text = result.response_text or ""

        # Convert to Hessisch
        return ConversationResult(text=convert_to_hessisch(text))
        
