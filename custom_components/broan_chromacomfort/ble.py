"""BLE client for ChromaComfort."""

import asyncio
from bleak import BleakClient

class ChromaComfortBLE:
    """BLE wrapper using ESP32 commands."""

    def __init__(self, mac: str):
        self.mac = mac
        self.client = BleakClient(mac)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        if self.client.is_connected:
            await self.client.disconnect()

    async def send_command(self, cmd: bytes):
        """Send raw bytes to the device."""
        if self.client.is_connected:
            CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
            await self.client.write_gatt_char(CHARACTERISTIC_UUID, cmd)
