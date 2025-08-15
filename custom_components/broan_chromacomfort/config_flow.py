"""Config flow for Broan ChromaComfort - manual MAC entry."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class ChromaComfortFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChromaComfort."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Create entry with the MAC address
            return self.async_create_entry(
                title=f"ChromaComfort {user_input['device_mac']}",
                data=user_input,
            )

        # Show form asking user to enter device MAC
        data_schema = vol.Schema({
            vol.Required("device_mac"): str
        })
        return self.async_show_form(step_id="user", data_schema=data_schema)
