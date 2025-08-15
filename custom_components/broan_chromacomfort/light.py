"""Light platform for ChromaComfort."""

from homeassistant.components.light import (
    LightEntity,
    LightEntityFeature,
    ColorMode,
)
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up light from a config entry."""
    ble_client = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortLight(ble_client)], True)

class ChromaComfortLight(LightEntity):
    """Representation of the ChromaComfort RGB light."""

    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._brightness = 255
        self._rgb = (255, 255, 255)

    @property
    def name(self):
        return "ChromaComfort Light"

    @property
    def is_on(self):
        return self._is_on

    @property
    def supported_features(self):
        return LightEntityFeature.BRIGHTNESS | LightEntityFeature.RGB_COLOR

    @property
    def color_mode(self):
        return ColorMode.RGB

    @property
    def brightness(self):
        return self._brightness

    @property
    def rgb_color(self):
        return self._rgb

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        if "brightness" in kwargs:
            self._brightness = kwargs["brightness"]
        if "rgb_color" in kwargs:
            self._rgb = kwargs["rgb_color"]
        await self._ble.set_light(
            self._is_on, self._brightness, self._rgb
        )
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble.set_light(self._is_on)
        self.async_write_ha_state()
