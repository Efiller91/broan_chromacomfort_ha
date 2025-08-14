"""Light entity for Broan ChromaComfort."""
from __future__ import annotations

import logging
from homeassistant.components.light import LightEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([BroanLight()])


class BroanLight(LightEntity):
    """Representation of the ChromaComfort light."""

    def __init__(self):
        self._is_on = False

    @property
    def name(self):
        return "Broan ChromaComfort Light"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        _LOGGER.info("Turning on ChromaComfort light")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        _LOGGER.info("Turning off ChromaComfort light")
        self._is_on = False
        self.async_write_ha_state()
