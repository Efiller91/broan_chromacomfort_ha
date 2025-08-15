"""Minimal BLE helper for ChromaComfort."""

import asyncio

class ChromaComfortBLE:
    """Simulated BLE client for ChromaComfort."""

    def __init__(self, mac: str):
        self.mac = mac
        self.connected = False

    async def connect(self):
        """Simulate BLE connection."""
        await asyncio.sleep(1)
        self.connected = True

    async def disconnect(self):
        """Simulate BLE disconnect."""
        await asyncio.sleep(0.5)
        self.connected = False

    async def send_cmd(self, cmd_type: int, dimmer: int = 0):
        """Send a generic command to the fan/light."""
        # In the real implementation, send BLE packet here
        await asyncio.sleep(0.1)
        print(f"Command sent: type={cmd_type}, dimmer={dimmer}")

    async def activate_fav_color(self, brightness: int):
        """Activate favorite color with brightness."""
        await self.send_cmd(cmd_type=5, dimmer=brightness)

    async def deactivate_fav_color(self):
        """Deactivate favorite color."""
        await self.send_cmd(cmd_type=12)

    async def set_rgb(self, r: int, g: int, b: int):
        """Set RGB color on the light."""
        await self.send_cmd(cmd_type=5)
        print(f"RGB set to {r},{g},{b}")

    async def turn_on_wall_rgb(self):
        """Turn on wall RGB light."""
        await self.send_cmd(cmd_type=5)

    async def turn_off_wall_rgb(self):
        """Turn off wall RGB light."""
        await self.send_cmd(cmd_type=6)
