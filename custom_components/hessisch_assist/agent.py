from homeassistant.components.conversation.models import (
    AbstractConversationAgent,
    ConversationInput,
    ConversationResult,
)

from homeassistant.core import HomeAssistant

from .dialect import convert_to_hessisch


class HessischAgent(AbstractConversationAgent):

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.id = "conversation_hessisch"
        self.name = "Hessisch Assist"

    @property
    def supported_languages(self):
        return ["de"]

    async def async_prepare(self, language: str) -> None:
        return

    async def async_process(
        self, user_input: ConversationInput, conversation_id: str | None
    ) -> ConversationResult:

        # call default agent
        default_agent = self.hass.components.conversation.async_get_agent(
            self.hass, None
        )
        result = await default_agent.async_process(user_input, conversation_id)

        text = result.response_text or ""

        return ConversationResult(text=convert_to_hessisch(text))
      
