"""Light platform for Broan ChromaComfort."""
from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS, SUPPORT_COLOR
from .const import DOMAIN
from .__init__ import ChromaComfortBLE

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the light entity."""
    ble_client: ChromaComfortBLE = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortLight(ble_client)])

class ChromaComfortLight(LightEntity):
    """Representation of the light."""

    def __init__(self, ble_client: ChromaComfortBLE):
        self._ble_client = ble_client
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
        brightness = kwargs.get("brightness", self._brightness)
        color = kwargs.get("rgb_color", self._rgb_color)
        self._brightness = brightness
        self._rgb_color = color
        # Send BLE commands
        await self._ble_client.send_cmd(11, *color, dimmer=int(brightness/255*100))
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble_client.send_cmd(12)  # deactivate favorite color
        self.async_write_ha_state()
