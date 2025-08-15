"""Switch platform for ChromaComfort integration."""

from homeassistant.components.switch import SwitchEntity
from .ble import ChromaComfortBLE

class ChromaComfortSwitch(SwitchEntity):
    """Representation of a ChromaComfort Switch."""

    def __init__(self, ble: ChromaComfortBLE, name="Wall RGB"):
        self._ble = ble
        self._is_on = False
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        CMD = bytes([58, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0])
        await self._ble.send_command(CMD)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        CMD = bytes([58, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0])
        await self._ble.send_command(CMD)
        self.async_write_ha_state()

    async def async_refresh_state(self):
        """Fetch latest state from BLE device."""
        await self._ble.refresh_state()
