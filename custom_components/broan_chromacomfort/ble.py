"""BLE client for ChromaComfort."""

import asyncio
from bleak import BleakClient
from .bluetooth import fan_on_bytes, fan_off_bytes, light_on_bytes, light_off_bytes, rgb_on_bytes, rgb_off_bytes

CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

class ChromaComfortBLE:
    """BLE wrapper using ESP32 commands."""

    def __init__(self, mac: str):
        self.mac = mac
        self.client = BleakClient(mac)

    async def connect(self):
        """Connect to the BLE device."""
        await self.client.connect()

    async def disconnect(self):
        """Disconnect from the BLE device."""
        if self.client.is_connected:
            await self.client.disconnect()

    async def send_command(self, cmd: bytes):
        """Send raw bytes to the device."""
        if self.client.is_connected:
            await self.client.write_gatt_char(CHARACTERISTIC_UUID, cmd)

    # Fan commands
    async def fan_on(self):
        await self.send_command(fan_on_bytes())

    async def fan_off(self):
        await self.send_command(fan_off_bytes())

    # Light commands
    async def light_on(self):
        await self.send_command(light_on_bytes())

    async def light_off(self):
        await self.send_command(light_off_bytes())

    # RGB commands
    async def rgb_on(self, r: int, g: int, b: int, brightness: int = 100):
        await self.send_command(rgb_on_bytes(r, g, b, brightness))

    async def rgb_off(self):
        await self.send_command(rgb_off_bytes())
