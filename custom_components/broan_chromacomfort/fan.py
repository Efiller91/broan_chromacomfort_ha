"""Fan platform for ChromaComfort integration."""

from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED
from .ble import ChromaComfortBLE

class ChromaComfortFan(FanEntity):
    """Representation of the ChromaComfort Fan."""

    def __init__(self, ble: ChromaComfortBLE):
        self._ble = ble
        self._is_on = False
        self._speed = None
        self._attr_supported_features = SUPPORT_SET_SPEED

    @property
    def is_on(self):
        return self._is_on

    @property
    def speed(self):
        return self._speed

    @property
    def speed_list(self):
        return ["low", "medium", "high"]

    async def async_turn_on(self, speed=None, **kwargs):
        if speed:
            self._speed = speed
        self._is_on = True
        CMD = bytes([58, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        await self._ble.send_command(CMD)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        CMD = bytes([58, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0])
        await self._ble.send_command(CMD)
        self.async_write_ha_state()

    async def async_refresh_state(self):
        """Fetch latest state from BLE device."""
        await self._ble.refresh_state()
