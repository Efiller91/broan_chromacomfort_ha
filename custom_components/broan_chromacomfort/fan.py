"""Fan platform for ChromaComfort."""

from homeassistant.components.fan import FanEntity
from .const import DOMAIN
from .bluetooth import fan_on_cmd, fan_off_cmd

SPEEDS = ["low", "medium", "high"]

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    ble_client = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortFan(ble_client)])

class ChromaComfortFan(FanEntity):
    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._speed = None

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, speed=None, **kwargs):
        await self._ble.send_command(fan_on_cmd())
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        await self._ble.send_command(fan_off_cmd())
        self._is_on = False

    @property
    def speed(self):
        return self._speed

    @property
    def speed_count(self):
        return len(SPEEDS)
