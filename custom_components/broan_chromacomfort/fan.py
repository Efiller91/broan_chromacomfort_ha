"""Fan platform for Broan ChromaComfort."""
from homeassistant.components.fan import FanEntity, SUPPORT_PRESET_MODE
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the fan entity."""
    device_mac = entry.data["device_mac"]
    async_add_entities([ChromaComfortFan(device_mac)])

class ChromaComfortFan(FanEntity):
    """Representation of the Broan ChromaComfort Fan."""

    def __init__(self, mac):
        self._mac = mac
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        # TODO: Send BLE command to turn fan on

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        # TODO: Send BLE command to turn fan off
