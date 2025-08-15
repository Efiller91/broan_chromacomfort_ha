"""Config flow for Broan ChromaComfort integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ChromaComfortConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChromaComfort."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters the MAC address."""
        errors = {}

        if user_input is not None:
            device_mac = user_input.get("device_mac")
            # Basic validation: MAC should be 12 hex digits or 6 pairs separated by ":"
            import re
            if not re.fullmatch(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", device_mac):
                errors["device_mac"] = "invalid_mac"
            else:
                # Create the entry
                return self.async_create_entry(
                    title=f"ChromaComfort {device_mac[-6:]}",  # last 3 bytes for title
                    data={"device_mac": device_mac}
                )

        # Show the form
        data_schema = vol.Schema(
            {
                vol.Required("device_mac"): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
