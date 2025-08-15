"""Light platform for ChromaComfort."""

from homeassistant.components.light import LightEntity, ColorMode
from .const import DOMAIN

class ChromaComfortLight(LightEntity):
    """Representation of the main light."""

    def __init__(self, hass, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._brightness = 255
        self._rgb = (255, 255, 255)
        self._name = "ChromaComfort Light"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def color_mode(self):
        return ColorMode.RGB

    @property
    def rgb_color(self):
        return self._rgb

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        if "brightness" in kwargs:
            self._brightness = kwargs["brightness"]
        if "rgb_color" in kwargs:
            self._rgb = kwargs["rgb_color"]
            await self._ble.set_rgb(*self._rgb)
        await self._ble.set_light(self._is_on, self._brightness)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble.set_light(False)
        self.async_write_ha_state()
