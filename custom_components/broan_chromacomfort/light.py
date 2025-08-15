"""Light platform for ChromaComfort integration."""

from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, SUPPORT_COLOR
from .ble import ChromaComfortBLE

class ChromaComfortLight(LightEntity):
    """Representation of the ChromaComfort Light."""

    def __init__(self, ble: ChromaComfortBLE):
        self._ble = ble
        self._is_on = False
        self._brightness = 0
        self._color = (0, 0, 0)
        self._attr_supported_features = SUPPORT_BRIGHTNESS | SUPPORT_COLOR

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def rgb_color(self):
        return self._color

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        brightness = kwargs.get("brightness", 255)
        rgb = kwargs.get("rgb_color", (255, 255, 255))
        self._brightness = brightness
        self._color = rgb
        CMD = bytes([58, 0, 0, 0, 0, rgb[0], rgb[1], rgb[2], 5, brightness, 0, 0, 0, 0, 0, 0, 0])
        await self._ble.send_command(CMD)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        CMD = bytes([58, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0])
        await self._ble.send_command(CMD)
        self.async_write_ha_state()

    async def async_refresh_state(self):
        """Fetch latest state from BLE device."""
        await self._ble.refresh_state()
