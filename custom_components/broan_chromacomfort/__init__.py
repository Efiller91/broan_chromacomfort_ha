"""ChromaComfort integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, PLATFORMS
from .ble import ChromaComfortBLE
from .fan import ChromaComfortFan
from .light import ChromaComfortLight
from .switch import ChromaComfortSwitch

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ChromaComfort from a config entry."""
    device_mac = entry.data["device_mac"]

    # Initialize BLE client
    ble_client = ChromaComfortBLE(device_mac)
    await ble_client.connect()
    hass.data[DOMAIN]["ble_client"] = ble_client

    # Forward setup to platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    ble_client: ChromaComfortBLE = hass.data[DOMAIN].get("ble_client")
    if ble_client:
        await ble_client.disconnect()

    unload_ok = []
    for platform in PLATFORMS:
        result = await hass.config_entries.async_forward_entry_unload(entry, platform)
        unload_ok.append(result)

    hass.data[DOMAIN].pop("ble_client", None)
    return all(unload_ok)
