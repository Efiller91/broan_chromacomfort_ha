"""ChromaComfort integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .fan import ChromaComfortFan
from .light import ChromaComfortLight
from .switch import ChromaComfortSwitch
from .ble import ChromaComfortBLE  # <- Make sure ble.py exists with this class

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    mac = entry.data.get("device_mac")
    if not mac:
        return False

    # Initialize BLE client
    ble_client = ChromaComfortBLE(mac)
    hass.data[DOMAIN]["ble_client"] = ble_client

    # Forward setup to each platform
    await hass.config_entries.async_forward_entry_setups(entry, ["fan", "light", "switch"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unloads(
        entry, ["fan", "light", "switch"]
    )

    ble_client: ChromaComfortBLE = hass.data[DOMAIN].get("ble_client")
    if ble_client:
        await ble_client.disconnect()

    return all(unload_ok)
