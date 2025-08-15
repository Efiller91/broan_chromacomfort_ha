"""Fan platform for Broan ChromaComfort."""
from homeassistant.components.fan import FanEntity
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from .__init__ import ChromaComfortBLE

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the fan entity."""
    ble_client: ChromaComfortBLE = hass.data[DOMAIN]["ble_client"]
    async_add_entities([ChromaComfortFan(ble_client)])

class ChromaComfortFan(FanEntity):
    """Representation of the fan."""

    def __init__(self, ble_client: ChromaComfortBLE):
        self._ble_client = ble_client
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._ble_client.send_cmd(1)  # fan ON
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble_client.send_cmd(2)  # fan OFF
        self._is_on = False
        self.async_write_ha_state()
