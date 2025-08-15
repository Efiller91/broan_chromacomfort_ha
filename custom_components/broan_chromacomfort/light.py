from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import DOMAIN

class ChromaComfortLight(LightEntity):
    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._brightness = 255

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self._brightness = kwargs.get("brightness", 255)
        await self._ble.send_command(b'\x3A\x00\x00\x00\x03' + b'\x00'*12)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble.send_command(b'\x3A\x00\x00\x00\x04' + b'\x00'*12)
        self.async_write_ha_state()

    @property
    def supported_color_modes(self):
        return {ColorMode.BRIGHTNESS}
