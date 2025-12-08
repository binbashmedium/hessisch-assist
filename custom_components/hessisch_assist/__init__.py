"""Hessisch Assist Agent integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.components.conversation import async_set_agent, async_unset_agent

from .conversation import HessischAgent

DOMAIN = "hessisch_assist"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Hessisch Assist agent."""
    agent = HessischAgent(hass)

    # Register our agent
    async_set_agent(hass, entry, agent)

    hass.data.setdefault(DOMAIN, {})["agent"] = agent
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Hessisch Assist agent."""
    async_unset_agent(hass, entry)

    hass.data.pop(DOMAIN, None)
    return True
    
