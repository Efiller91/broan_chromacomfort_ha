"""Config flow for Broan ChromaComfort integration."""

import re
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_MAC

class ChromaComfortConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChromaComfort."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters the MAC address."""
        errors = {}

        if user_input is not None:
            device_mac = user_input.get(CONF_MAC)
            # Accept plain 12-digit or colon-separated MAC
            if not re.fullmatch(r"([0-9A-Fa-f]{12}|([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", device_mac):
                errors[CONF_MAC] = "invalid_mac"
            else:
                # Normalize to colon-separated uppercase: FC:58:FA:75:F8:66
                device_mac = device_mac.upper()
                if len(device_mac) == 12:
                    device_mac = ":".join(device_mac[i:i+2] for i in range(0, 12, 2))
                return self.async_create_entry(
                    title=f"ChromaComfort {device_mac[-8:]}",  # last 3 bytes
                    data={CONF_MAC: device_mac}
                )

        data_schema = vol.Schema(
            {vol.Required(CONF_MAC): str}
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
