"""Broan ChromaComfort integration using manual MAC entry."""
import logging
from bleak import BleakClient
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

WRITE_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

class ChromaComfortBLE:
    """BLE helper to send commands to the fan/light device."""

    def __init__(self, mac):
        self.mac = mac
        self.client = BleakClient(mac)
        self.connected = False

    async def connect(self):
        if not self.connected:
            await self.client.connect()
            self.connected = True

    async def disconnect(self):
        if self.connected:
            await self.client.disconnect()
            self.connected = False

    async def send_cmd(self, cmd_type, r=0, g=0, b=0, dimmer=0):
        """Send a 17-byte BLE command."""
        await self.connect()
        packet = bytearray(17)
        packet[0] = 5         # version
        packet[1] = 0         # ctrl_cmd_1
        packet[2] = 64        # ctrl_cmd_2
        packet[3] = cmd_type  # type
        packet[4] = r
        packet[5] = g
        packet[6] = b
        packet[7] = dimmer
        packet[8] = 1         # sweep_color_value_1
        packet[9] = 24        # sweep_color_value_2
        # bytes 10-16 remain 0
        await self.client.write_gatt_char(WRITE_CHAR_UUID, packet)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via configuration.yaml (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the integration from config flow entry."""
    hass.data.setdefault(DOMAIN, {})
    device_mac = entry.data["device_mac"]
    hass.data[DOMAIN]["ble_client"] = ChromaComfortBLE(device_mac)

    # Forward setup to platforms
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "fan")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "light")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "fan")
    await hass.config_entries.async_forward_entry_unload(entry, "light")
    await hass.config_entries.async_forward_entry_unload(entry, "switch")
    ble_client: ChromaComfortBLE = hass.data[DOMAIN].get("ble_client")
    if ble_client:
        await ble_client.disconnect()
    return True
