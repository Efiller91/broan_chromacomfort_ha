"""ChromaComfort fan platform."""

from homeassistant.components.fan import FanEntity, FanEntityFeature

class ChromaComfortFan(FanEntity):
    """ChromaComfort Fan entity."""

    def __init__(self, ble_client):
        self._ble = ble_client
        self._is_on = False
        self._speed = None

    @property
    def supported_features(self):
        return FanEntityFeature.SET_SPEED

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, speed=None, **kwargs):
        await self._ble.send_cmd(cmd_type=1)  # 1 = fan on
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._ble.send_cmd(cmd_type=2)  # 2 = fan off
        self._is_on = False
        self.async_write_ha_state()

    async def async_set_speed(self, speed: str):
        speed_map = {"low": 10, "medium": 30, "high": 60}
        await self._ble.send_cmd(cmd_type=0, dimmer=speed_map.get(speed, 30))
        self._speed = speed
        self.async_write_ha_state()
