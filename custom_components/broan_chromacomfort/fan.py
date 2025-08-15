"""Fan platform for ChromaComfort."""

from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

SPEEDS = ["low", "medium", "high"]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up fan from a config entry."""
    ble_client = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortFan(ble_client)], True)

class ChromaComfortFan(FanEntity):
    """Representation of the ChromaComfort fan."""

    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._speed = "medium"

    @property
    def name(self):
        return "ChromaComfort Fan"

    @property
    def is_on(self):
        return self._is_on

    @property
    def speed(self):
        return self._speed

    @property
    def speed_list(self):
        return SPEEDS

    async def async_turn_on(self, speed=None, **kwargs):
        self._is_on = True
        if speed:
            self._speed = speed
        await self._ble.set_fan(self._is_on, self._speed)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble.set_fan(self._is_on)
        self.async_write_ha_state()
