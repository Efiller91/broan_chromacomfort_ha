"""Bluetooth helper for Broan ChromaComfort."""
import logging
from bleak import BleakClient, BleakError

_LOGGER = logging.getLogger(__name__)

# Real UUIDs from ESP32 reverse-engineered project
LIGHT_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
FAN_CHAR_UUID   = "0000fff2-0000-1000-8000-00805f9b34fb"

async def connect_to_device(mac_address: str) -> bool:
    """Test connection to the Bluetooth device."""
    try:
        async with BleakClient(mac_address) as client:
            if client.is_connected:
                _LOGGER.info("Connected to %s", mac_address)
                return True
            else:
                _LOGGER.error("Failed to connect to %s", mac_address)
                return False
    except BleakError as e:
        _LOGGER.error("Bluetooth connection failed: %s", e)
        return False

async def turn_on_light(mac_address: str):
    """Turn on the ChromaComfort light."""
    try:
        async with BleakClient(mac_address) as client:
            await client.write_gatt_char(LIGHT_CHAR_UUID, bytearray([0x01]))
            _LOGGER.info("Light turned on for %s", mac_address)
    except BleakError as e:
        _LOGGER.error("Failed to turn on light: %s", e)

async def turn_off_light(mac_address: str):
    """Turn off the ChromaComfort light."""
    try:
        async with BleakClient(mac_address) as client:
            await client.write_gatt_char(LIGHT_CHAR_UUID, bytearray([0x00]))
            _LOGGER.info("Light turned off for %s", mac_address)
    except BleakError as e:
        _LOGGER.error("Failed to turn off light: %s", e)

async def turn_on_fan(mac_address: str):
    """Turn on the ChromaComfort fan."""
    try:
        async with BleakClient(mac_address) as client:
            await client.write_gatt_char(FAN_CHAR_UUID, bytearray([0x01]))
            _LOGGER.info("Fan turned on for %s", mac_address)
    except BleakError as e:
        _LOGGER.er_
