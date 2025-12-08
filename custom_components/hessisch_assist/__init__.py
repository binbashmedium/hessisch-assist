"""Hessisch Assist integration setup."""
from __future__ import annotations

from homeassistant.core import HomeAssistant

from .conversation import HessischConversationProvider

DOMAIN = "hessisch_assist"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Hessisch Assist conversation provider."""

    provider = HessischConversationProvider(hass)
    hass.data[DOMAIN] = provider

    await hass.components.conversation.async_register_provider(provider)

    return True
