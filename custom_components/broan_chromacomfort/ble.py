"""BLE client for ChromaComfort device."""

import asyncio
from bleak import BleakClient

# Device UUIDs (from ESP32 project)
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

class ChromaComfortBLE:
    """Handles BLE communication with ChromaComfort fan/light."""

    def __init__(self, mac: str):
        self.mac = self._normalize_mac(mac)
        self.client: BleakClient | None = None

    def _normalize_mac(self, mac: str) -> str:
        mac = mac.upper().replace(":", "")
        return ":".join(mac[i:i+2] for i in range(0, 12, 2))

    async def connect(self):
        """Connect to the BLE device."""
        self.client = BleakClient(self.mac)
        await self.client.connect()

    async def disconnect(self):
        """Disconnect from the BLE device."""
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def _send_packet(self, data: bytes):
        """Send raw packet over BLE."""
        if not self.client or not self.client.is_connected:
            raise ConnectionError("BLE device not connected")
        await self.client.write_gatt_char(CHAR_UUID, data)

    def _to_ha_brightness(self, b: int) -> int:
        """Convert 0-100 to 0-255 HA brightness."""
        return int(b / 100 * 255)

    def _from_ha_brightness(self, b: int) -> int:
        """Convert HA 0-255 brightness to 0-100."""
        return int(b / 255 * 100)

    async def turn_fan(self, on: bool):
        code = bytes([58, 17, 0, 64, 1 if on else 2] + [0]*12)
        await self._send_packet(code)

    async def set_light(self, on: bool, brightness: int = 255):
        b = self._from_ha_brightness(brightness)
        code = bytes([58, 17, 0, 64, 11 if on else 12, b] + [0]*11)
        await self._send_packet(code)

    async def set_rgb(self, r: int, g: int, b: int):
        # Apply gamma correction
        r = int(255 * (r / 255)**4)
        g = int(255 * (g / 255)**4)
        b = int(255 * (b / 255)**4)
        code = bytes([58, 17, 0, 64, 5, r, g, b] + [0]*9)
        await self._send_packet(code)

    async def turn_wall_rgb(self, on: bool):
        code = bytes([58, 17, 0, 64, 5 if on else 6] + [0]*12)
        await self._send_packet(code)
