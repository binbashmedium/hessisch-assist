from homeassistant import config_entries
from . import DOMAIN

class HessischAssistConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle setup."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """User initiated setup."""
        if user_input is not None:
            return self.async_create_entry(title="Hessisch Assist", data={})

        return self.async_show_form(step_id="user")
        
