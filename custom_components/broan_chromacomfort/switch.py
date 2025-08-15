"""Wall RGB switch for Broan ChromaComfort."""
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .__init__ import ChromaComfortBLE

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the wall RGB switch entity."""
    ble_client: ChromaComfortBLE = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortWallRGB(ble_client)])

class ChromaComfortWallRGB(SwitchEntity):
    """Representation of the wall RGB LED switch."""

    def __init__(self, ble_client: ChromaComfortBLE):
        self._ble_client = ble_client
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._ble_client.send_cmd(5)  # Turn on wall RGB
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble_client.send_cmd(6)  # Turn off wall RGB
        self._is_on = False
        self.async_write_ha_state()
