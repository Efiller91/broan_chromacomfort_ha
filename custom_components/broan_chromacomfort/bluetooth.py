"""Bluetooth commands for ChromaComfort."""

def _build_packet(cmd_type: int, r=0, g=0, b=0, brightness=0) -> bytes:
    packet = [58] + [0]*15
    packet[-1] = cmd_type
    packet[10] = r
    packet[11] = g
    packet[12] = b
    packet[13] = brightness
    return bytes(packet)

def fan_on_cmd() -> bytes:
    return _build_packet(1)

def fan_off_cmd() -> bytes:
    return _build_packet(2)

def light_on_cmd() -> bytes:
    return _build_packet(3)

def light_off_cmd() -> bytes:
    return _build_packet(4)

def rgb_on_cmd() -> bytes:
    return _build_packet(5)

def rgb_off_cmd() -> bytes:
    return _build_packet(6)

def activate_fav_color_cmd(brightness: int) -> bytes:
    return _build_packet(11, brightness=brightness)

def deactivate_fav_color_cmd() -> bytes:
    return _build_packet(12)

def set_rgb_cmd(r: int, g: int, b: int) -> bytes:
    return _build_packet(13, r, g, b)
