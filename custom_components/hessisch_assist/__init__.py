"""Hessisch Assist conversation agent integration."""
from __future__ import annotations

from homeassistant.components.conversation import async_set_agent, async_unset_agent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .conversation import HessischConversationAgent

DOMAIN = "hessisch_assist"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Hessisch Assist (no YAML config)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hessisch Assist from a config entry."""
    agent = HessischConversationAgent(hass, entry)
    async_set_agent(hass, entry, agent)
    hass.data[DOMAIN][entry.entry_id] = agent
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Hessisch Assist config entry."""
    async_unset_agent(hass, entry)
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
    
