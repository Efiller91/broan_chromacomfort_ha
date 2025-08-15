"""Config flow for Broan ChromaComfort."""
import logging
from homeassistant import config_entries
from homeassistant.helpers import selector

from bleak import BleakScanner
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ChromaComfortFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChromaComfort."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        devices = []

        # Scan for BLE devices
        found_devices = await BleakScanner.discover(timeout=3.0)
        for d in found_devices:
            if "ChromaComfort" in d.name:
                devices.append({"label": f"{d.name} ({d.address})", "value": d.address})

        if user_input is not None:
            # User selected a device
            return self.async_create_entry(title=user_input["device_mac"], data=user_input)

        if not devices:
            devices = [{"label": "No devices found. Press Submit to retry.", "value": ""}]

        return self.async_show_form(
            step_id="user",
            data_schema=selector.SelectSelector(
                selector_type=selector.SelectSelector(
                    options=[d["value"] for d in devices]
                )
            ),
            errors=errors,
        )
