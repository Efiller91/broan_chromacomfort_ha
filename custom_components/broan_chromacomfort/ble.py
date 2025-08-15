"""BLE client for ChromaComfort."""

from bleak import BleakClient

CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

class ChromaComfortBLE:
    """BLE wrapper using the ESP32 command set."""

    def __init__(self, mac: str):
        self.mac = mac
        self.client = BleakClient(mac)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        if self.client.is_connected:
            await self.client.disconnect()

    async def send_command(self, cmd: bytes):
        if self.client.is_connected:
            await self.client.write_gatt_char(CHAR_UUID, cmd)

    async def get_status(self):
        """Return a dictionary with fan, light, wall_rgb, brightness."""
        # Minimal status polling
        if not self.client.is_connected:
            await self.connect()
        # Example: request a status packet from device
        # You can replace this with the exact BLE command that queries device
        # For now, simulate reading (replace with actual read_gatt_char if available)
        return {"fan": False, "light": False, "wall_rgb": False, "brightness": 255}
