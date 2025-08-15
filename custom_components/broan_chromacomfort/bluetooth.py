"""Bluetooth helper for ChromaComfort."""

# This file can contain helper functions for parsing or sending BLE packets.
# For now, we just import the byte commands from ESP32 firmware.

def fan_on_bytes():
    return bytes([58, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])

def fan_off_bytes():
    return bytes([58, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0])

def light_on_bytes():
    return bytes([58, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0])

def light_off_bytes():
    return bytes([58, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0])

def rgb_on_bytes(r, g, b, brightness):
    return bytes([58, 0, 0, 0, 0, r, g, b, 5, brightness, 0, 0, 0, 0, 0, 0, 0])

def rgb_off_bytes():
    return bytes([58, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0])
