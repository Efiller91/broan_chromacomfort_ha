import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_POLL_INTERVAL
import re

class ChromaComfortConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            device_mac = user_input.get("device_mac")
            poll_interval = user_input.get("poll_interval", DEFAULT_POLL_INTERVAL)
            if not re.fullmatch(r"([0-9A-Fa-f]{12}|([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", device_mac):
                errors["device_mac"] = "invalid_mac"
            elif poll_interval < 1:
                errors["poll_interval"] = "invalid_poll_interval"
            else:
                return self.async_create_entry(
                    title=f"ChromaComfort {device_mac[-6:]}",
                    data={"device_mac": device_mac, "poll_interval": poll_interval}
                )

        data_schema = vol.Schema({
            vol.Required("device_mac"): str,
            vol.Optional("poll_interval", default=DEFAULT_POLL_INTERVAL): int
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
