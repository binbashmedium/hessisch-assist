from homeassistant.components.conversation import (
    AbstractConversationProvider,
    ConversationResult,
)
from homeassistant.core import HomeAssistant
import logging
from .dialect import convert_to_hessisch

_LOGGER = logging.getLogger(__name__)

DOMAIN = "hessisch_assist"


async def async_setup(hass: HomeAssistant, config: dict):
    """Register the Hessisch conversation agent."""
    provider = HessischConversationProvider(hass)

    # WICHTIG: Provider registrieren
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["provider"] = provider

    # Conversation registriert es systemweit
    hass.components.conversation.async_register_provider(provider)

    _LOGGER.info("Hessisch Assist Conversation Provider geladen.")
    return True


class HessischConversationProvider(AbstractConversationProvider):
    """Frankfurter/Hessischer Dialekt-Provider."""

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.id = DOMAIN
        self.name = "Hessisch Assist"

    async def async_process(self, text, context=None):
        """Process conversation and return dialect response."""

        # original Antwort holen
        result = await self.hass.services.async_call(
            "conversation",
            "process",
            {"text": text},
            blocking=True,
            return_response=True,
        )

        original_text = result.get("response", "")

        # in Dialekt umwandeln
        dialect_text = convert_to_hessisch(original_text)

        return ConversationResult(text=dialect_text)
        
