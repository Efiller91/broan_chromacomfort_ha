"""Light platform for ChromaComfort."""

from homeassistant.components.light import LightEntity
from .const import DOMAIN
from .bluetooth import (
    light_on_cmd,
    light_off_cmd,
    activate_fav_color_cmd,
    deactivate_fav_color_cmd,
    set_rgb_cmd,
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    ble_client = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortLight(ble_client)])

class ChromaComfortLight(LightEntity):
    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._brightness = 255
        self._rgb = (255, 255, 255)

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def rgb_color(self):
        return self._rgb

    async def async_turn_on(self, **kwargs):
        rgb = kwargs.get("rgb_color")
        brightness = kwargs.get("brightness", 255)

        if rgb:
            self._rgb = rgb
            await self._ble.send_command(set_rgb_cmd(*rgb))
            await self._ble.send_command(activate_fav_color_cmd(brightness))
        else:
            await self._ble.send_command(light_on_cmd())

        self._is_on = True
        self._brightness = brightness

    async def async_turn_off(self, **kwargs):
        await self._ble.send_command(deactivate_fav_color_cmd())
        await self._ble.send_command(light_off_cmd())
        self._is_on = False
