"""Config flow for Hessisch Assist."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN


class HessischAssistConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hessisch Assist."""

    VERSION = 1

    async def async_step_user(self, info=None) -> FlowResult:
        """User initiated setup."""
        return self.async_create_entry(title="Hessisch Assist", data={})
      
