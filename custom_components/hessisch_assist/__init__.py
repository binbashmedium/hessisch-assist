"""Hessisch Assist integration setup."""
from __future__ import annotations

from homeassistant.components import conversation
from homeassistant.core import HomeAssistant

from .conversation import HessischConversationProvider

DOMAIN = "hessisch_assist"
ENTRYPOINT = "conversation"


ASYNC_SETUP_ERROR = "Failed to register Hessisch Assist conversation provider"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Hessisch Assist conversation provider."""

    provider = HessischConversationProvider(hass)
    hass.data.setdefault(DOMAIN, {})["provider"] = provider

    if hasattr(conversation, "async_register_provider"):
        await conversation.async_register_provider(hass, provider)
    elif hasattr(conversation, "async_set_agent"):
        conversation.async_set_agent(hass, provider)
    else:
        raise RuntimeError(ASYNC_SETUP_ERROR)

    return True
