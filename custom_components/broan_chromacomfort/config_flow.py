"""Config flow for Broan ChromaComfort integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

try:
    from bleak import BleakScanner
except ImportError:
    _LOGGER.error("Bleak not installed; please check requirements in manifest.json")


class BroanChromaComfortConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Broan ChromaComfort."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow."""
        # If user clicked refresh button, restart scan
        if user_input is not None:
            if user_input.get("refresh"):
                return await self.async_step_user()
            # User selected a device
            return self.async_create_entry(
                title="Broan ChromaComfort", data={"device_mac": user_input["device_mac"]}
            )

        # Scan for nearby BLE devices
        devices = await BleakScanner.discover()
        options = {d.address: d.name for d in devices if d.name and "ChromaComfort" in d.name}

        # Build schema
        if options:
            schema = vol.Schema({
                vol.Required("device_mac"): vol.In(options),
                vol.Optional("refresh", default=False): bool
            })
            description = {"options": ", ".join(options.values())}
        else:
            # No devices found — only show refresh button
            schema = vol.Schema({
                vol.Optional("refresh", default=False): bool
            })
            description = {"error": "No devices found nearby."}

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders=description
        )
