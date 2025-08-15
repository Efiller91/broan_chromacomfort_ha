"""Switch platform for ChromaComfort."""

from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .bluetooth import rgb_on_cmd, rgb_off_cmd

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    ble_client = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortSwitch(ble_client)])

class ChromaComfortSwitch(SwitchEntity):
    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._ble.send_command(rgb_on_cmd())
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        await self._ble.send_command(rgb_off_cmd())
        self._is_on = False
