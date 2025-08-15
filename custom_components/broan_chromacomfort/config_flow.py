"""Config flow for ChromaComfort integration."""

import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
import re

class ChromaComfortConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChromaComfort."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            device_mac = user_input.get("device_mac")
            if not re.fullmatch(r"([0-9A-Fa-f]{12}|([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", device_mac):
                errors["device_mac"] = "invalid_mac"
            else:
                return self.async_create_entry(
                    title=f"ChromaComfort {device_mac[-6:]}",
                    data={"device_mac": device_mac}
                )

        data_schema = vol.Schema({vol.Required("device_mac"): str})
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
