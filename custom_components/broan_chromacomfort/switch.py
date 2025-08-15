"""Switch platform for ChromaComfort Wall RGB."""

from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

class ChromaComfortSwitch(SwitchEntity):
    """Representation of the wall RGB switch."""

    def __init__(self, hass, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._name = "ChromaComfort Wall RGB"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._ble.turn_wall_rgb(True)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble.turn_wall_rgb(False)
        self._is_on = False
        self.async_write_ha_state()
