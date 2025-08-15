from homeassistant.components.fan import FanEntity, FanEntityFeature
from . import DOMAIN

class ChromaComfortFan(FanEntity):
    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._ble.send_command(b'\x3A\x00\x00\x00\x01' + b'\x00'*12)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble.send_command(b'\x3A\x00\x00\x00\x02' + b'\x00'*12)
        self._is_on = False
        self.async_write_ha_state()

    @property
    def supported_features(self):
        return FanEntityFeature.ON_OFF
