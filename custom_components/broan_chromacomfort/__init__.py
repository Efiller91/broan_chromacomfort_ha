"""ChromaComfort integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .fan import ChromaComfortFan
from .light import ChromaComfortLight
from .switch import ChromaComfortSwitch
from .ble import ChromaComfortBLE  # Your BLE wrapper using ESP32 commands

PLATFORMS = ["fan", "light", "switch"]

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    device_mac = entry.data.get("device_mac")
    if not device_mac:
        return False

    # Initialize BLE client
    ble_client = ChromaComfortBLE(device_mac)
    hass.data[DOMAIN]["ble_client"] = ble_client
    await ble_client.connect()  # make sure your ble.py has an async connect()

    # Forward entry setup to all platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Unload all platforms
    unload_ok = []
    for platform in PLATFORMS:
        result = await hass.config_entries.async_forward_entry_unload(entry, platform)
        unload_ok.append(result)

    # Disconnect BLE
    ble_client: ChromaComfortBLE = hass.data[DOMAIN].get("ble_client")
    if ble_client:
        await ble_client.disconnect()

    # Remove from hass.data
    hass.data[DOMAIN].pop("ble_client", None)

    return all(unload_ok)
