"""Hessisch Assist integration setup."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .conversation import HessischConversationProvider

DOMAIN = "hessisch_assist"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Legacy setup — do nothing. Real setup happens in async_setup_entry."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hessisch Assist through UI config entry."""

    provider = HessischConversationProvider(hass)
    hass.data.setdefault(DOMAIN, {})["provider"] = provider

    # Register conversation provider
    hass.components.conversation.async_register_provider(provider)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration entry."""
    provider = hass.data.get(DOMAIN, {}).get("provider")
    if provider:
        hass.components.conversation.async_unregister_provider(provider)

    hass.data.pop(DOMAIN, None)
    return True
    
