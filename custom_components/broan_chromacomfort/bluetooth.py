"""Bluetooth helper for Broan ChromaComfort."""
import logging
from bleak import BleakClient

_LOGGER = logging.getLogger(__name__)

async def connect_to_device(mac_address: str):
    """Connect to the Bluetooth device."""
    try:
        async with BleakClient(mac_address) as client:
            _LOGGER.info("Connected to %s", mac_address)
            # Add read/write BLE code here
            return True
    except Exception as e:
        _LOGGER.error("Bluetooth connection failed: %s", e)
        return False
