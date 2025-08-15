"""Switch platform for ChromaComfort."""

from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switch from a config entry."""
    ble_client = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortSwitch(ble_client)], True)

class ChromaComfortSwitch(SwitchEntity):
    """Representation of the ChromaComfort wall RGB switch."""

    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False

    @property
    def name(self):
        return "ChromaComfort Wall RGB"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        await self._ble.set_rgb(True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble.set_rgb(False)
        self.async_write_ha_state()
