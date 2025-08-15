"""Bluetooth commands wrapper (optional helper)."""

# For now all BLE commands go directly via ble.py send_command
# You can add helpers to build the bytes per ESP32 commands

def fan_on_command() -> bytes:
    return bytes([58, 0, 0, 0, 1] + [0]*12)

def fan_off_command() -> bytes:
    return bytes([58, 0, 0, 0, 2] + [0]*12)

def light_on_command() -> bytes:
    return bytes([58, 0, 0, 0, 3] + [0]*12)

def light_off_command() -> bytes:
    return bytes([58, 0, 0, 0, 4] + [0]*12)

def rgb_on_command() -> bytes:
    return bytes([58, 0, 0, 0, 5] + [0]*12)

def rgb_off_command() -> bytes:
    return bytes([58, 0, 0, 0, 6] + [0]*12)
