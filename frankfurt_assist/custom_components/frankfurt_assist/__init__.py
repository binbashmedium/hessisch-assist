"""Frankfurt Assist integration setup."""
from __future__ import annotations

from homeassistant.components import conversation
from homeassistant.core import HomeAssistant

from .conversation import FrankfurtConversationProvider

DOMAIN = "frankfurt_assist"
ENTRYPOINT = "conversation"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Frankfurt Assist conversation provider."""

    provider = FrankfurtConversationProvider(hass)
    hass.data.setdefault(DOMAIN, {})["provider"] = provider

    if hasattr(conversation, "async_register_provider"):
        await conversation.async_register_provider(hass, provider)
    elif hasattr(conversation, "async_set_agent"):
        conversation.async_set_agent(hass, provider)
    else:
        return False

    return True
