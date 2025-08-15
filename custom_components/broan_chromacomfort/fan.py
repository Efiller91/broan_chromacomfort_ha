"""Fan platform for ChromaComfort."""

from homeassistant.components.fan import FanEntity, SUPPORT_ON_OFF
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

class ChromaComfortFan(FanEntity):
    """Representation of the ChromaComfort fan."""

    def __init__(self, hass, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._name = "ChromaComfort Fan"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def supported_features(self):
        return SUPPORT_ON_OFF

    async def async_turn_on(self, **kwargs):
        await self._ble.turn_fan(True)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble.turn_fan(False)
        self._is_on = False
        self.async_write_ha_state()
