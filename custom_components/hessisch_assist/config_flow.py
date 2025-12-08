from homeassistant import config_entries

DOMAIN = "conversation_hessisch"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, info=None):
        return self.async_create_entry(title="Hessisch Assist Agent", data={})
        
