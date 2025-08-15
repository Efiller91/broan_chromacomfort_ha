"""Broan ChromaComfort integration."""
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via configuration.yaml (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the integration from config flow entry."""
    hass.data.setdefault(DOMAIN, {})
    device_mac = entry.data["device_mac"]
    hass.data[DOMAIN]["device_mac"] = device_mac

    # Register platforms
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "fan")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "light")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "fan")
    await hass.config_entries.async_forward_entry_unload(entry, "light")
    return True
