from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.components.conversation import async_set_agent, async_unset_agent

from .agent import HessischAgent


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    agent = HessischAgent(hass)
    async_set_agent(hass, entry, agent)
    hass.data.setdefault("conversation_hessisch", {})["agent"] = agent
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    async_unset_agent(hass, entry)
    hass.data.pop("conversation_hessisch", None)
    return True
    
