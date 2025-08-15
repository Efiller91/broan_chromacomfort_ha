"""Config flow for Broan ChromaComfort integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

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

        if user_input is not None:
            # User selected a device from dropdown
            if user_input.get("refresh_scan"):
                # User clicked "Refresh" — restart scan
                return await self.async_step_user()
            return self.async_create_entry(title="Broan ChromaComfort", data=user_input)

        # Scan for nearby BLE devices
        devices = await BleakScanner.discover()
        options = {d.address: d.name for d in devices if d.name and "ChromaComfort" in d.name}

        if not options:
            _LOGGER.warning("No Broan ChromaComfort devices found")
            # Show a minimal form with refresh
            return self.async_show_form(
                step_id="user",
                description_placeholders={"error": "No devices found nearby."},
                data_schema=vol.Schema({
                    vol.Required("refresh_scan", default=False): bool
                })
            )

        # Build dropdown schema
        schema = vol.Schema({
            vol.Required("device_mac"): vol.In(options),
            vol.Required("refresh_scan", default=False): bool
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={"options": ", ".join(options.values())}
        )
