"""Light entity for Broan ChromaComfort."""
from __future__ import annotations

import logging
from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .bluetooth import turn_on_light, turn_off_light

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Broan ChromaComfort light."""
    async_add_entities([BroanLight(entry.data["device_mac"])])


class BroanLight(LightEntity):
    """Representation of the ChromaComfort light."""

    def __init__(self, mac: str):
        self._is_on = False
        self._mac = mac

    @property
    def name(self):
        return "Broan ChromaComfort Light"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        _LOGGER.info("Turning on ChromaComfort light")
        await turn_on_light(self._mac)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        _LOGGER.info("Turning off ChromaComfort light")
        await turn_off_light(self._mac)
        self._is_on = False
        self.async_write_ha_state()
