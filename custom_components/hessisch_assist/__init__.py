"""Hessisch Assist integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .conversation import HessischConversationProvider

DOMAIN = "hessisch_assist"


async def async_setup(hass: HomeAssistant, config: dict):
    """Legacy setup – does nothing."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Hessisch Assist using config entry."""
    provider = HessischConversationProvider(hass)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN]["provider"] = provider

    hass.components.conversation.async_register_provider(provider)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Hessisch Assist."""
    provider = hass.data.get(DOMAIN, {}).get("provider")

    if provider:
        hass.components.conversation.async_unregister_provider(provider)

    hass.data.pop(DOMAIN, None)

    return True
    
