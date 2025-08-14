"""Fan entity for Broan ChromaComfort."""
from __future__ import annotations

import logging
from homeassistant.components.fan import FanEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([BroanFan()])


class BroanFan(FanEntity):
    """Representation of the ChromaComfort fan."""

    def __init__(self):
        self._is_on = False

    @property
    def name(self):
        return "Broan ChromaComfort Fan"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        _LOGGER.info("Turning on ChromaComfort fan")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        _LOGGER.info("Turning off ChromaComfort fan")
        self._is_on = False
        self.async_write_ha_state()
