from homeassistant.components.switch import SwitchEntity

class ChromaComfortSwitch(SwitchEntity):
    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        await self._ble.send_command(b'\x3A\x00\x00\x00\x05' + b'\x00'*12)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        await self._ble.send_command(b'\x3A\x00\x00\x00\x06' + b'\x00'*12)
        self.async_write_ha_state()
