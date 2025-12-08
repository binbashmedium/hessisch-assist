"""Config flow for Hessisch Assist."""
from __future__ import annotations

from homeassistant import config_entries

from . import DOMAIN


class HessischAssistConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hessisch Assist."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Start the config flow."""
        if user_input is not None:
            return self.async_create_entry(title="Hessisch Assist", data={})

        return self.async_show_form(step_id="user", data_schema=None)
        
