"""Light platform for Broan ChromaComfort."""
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, SUPPORT_COLOR
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the light entity."""
    device_mac = entry.data["device_mac"]
    async_add_entities([ChromaComfortLight(device_mac)])

class ChromaComfortLight(LightEntity):
    """Representation of the Broan ChromaComfort Light."""

    def __init__(self, mac):
        self._mac = mac
        self._is_on = False
        self._brightness = 255
        self._rgb_color = (255, 255, 255)

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
    def supported_features(self):
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        if "brightness" in kwargs:
            self._brightness = kwargs["brightness"]
        if "rgb_color" in kwargs:
            self._rgb_color = kwargs["rgb_color"]
        # TODO: Send BLE command to turn light on / set brightness / color

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        # TODO: Send BLE command to turn light off
