"""Fan entity for Broan ChromaComfort."""
from __future__ import annotations

import logging
from homeassistant.components.fan import FanEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .bluetooth import connect_to_device

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Broan ChromaComfort fan."""
    async_add_entities([BroanFan(entry.data["device_mac"])])


class BroanFan(FanEntity):
    """Representation of the ChromaComfort fan."""

    def __init__(self, mac: str):
        self._is_on = False
        self._mac = mac

    @property
    def name(self):
        return "Broan ChromaComfort Fan"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        _LOGGER.info("Turning on ChromaComfort fan")
        success = await connect_to_device(self._mac)
        if success:
            self._is_on = True
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        _LOGGER.info("Turning off ChromaComfort fan")
        success = await connect_to_device(self._mac)
        if success:
            self._is_on = False
            self.async_write_ha_state()
