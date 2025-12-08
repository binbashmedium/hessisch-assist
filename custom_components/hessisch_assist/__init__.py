"""Hessisch Assist integration setup."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .conversation import HessischConversationProvider

DOMAIN = "hessisch_assist"


def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Hessisch Assist conversation provider."""
    provider = HessischConversationProvider(hass)
    hass.data.setdefault(DOMAIN, {})["provider"] = provider
    hass.components.conversation.async_register_provider(provider)

    return True
