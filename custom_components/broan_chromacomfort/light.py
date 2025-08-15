"""ChromaComfort light platform."""

from homeassistant.components.light import LightEntity, LightEntityFeature, ColorMode

class ChromaComfortLight(LightEntity):
    """ChromaComfort Light entity."""

    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._brightness = 0
        self._rgb_color = (0, 0, 0)

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def rgb_color(self):
        return self._rgb_color

    @property
    def supported_color_modes(self):
        return {ColorMode.RGB, ColorMode.BRIGHTNESS}

    @property
    def color_mode(self):
        return ColorMode.RGB if self._rgb_color != (0, 0, 0) else ColorMode.BRIGHTNESS

    async def async_turn_on(self, **kwargs):
        brightness = kwargs.get("brightness", self._brightness)
        rgb = kwargs.get("rgb_color", self._rgb_color)

        if rgb:
            await self._ble.set_rgb(*rgb)
            self._rgb_color = rgb
        else:
            await self._ble.activate_fav_color(brightness)
            self._brightness = brightness

        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble.deactivate_fav_color()
        self._is_on = False
        self.async_write_ha_state()
