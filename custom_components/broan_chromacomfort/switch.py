"""ChromaComfort switch platform."""

from homeassistant.components.switch import SwitchEntity

class ChromaComfortSwitch(SwitchEntity):
    """ChromaComfort Switch entity."""

    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._ble.turn_on_wall_rgb()
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble.turn_off_wall_rgb()
        self._is_on = False
        self.async_write_ha_state()
