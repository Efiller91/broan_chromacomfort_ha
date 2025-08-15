"""ChromaComfort integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging

from .const import DOMAIN
from .ble import ChromaComfortBLE
from .fan import ChromaComfortFan
from .light import ChromaComfortLight
from .switch import ChromaComfortSwitch

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["fan", "light", "switch"]

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    mac = entry.data["device_mac"]
    poll_interval = entry.data.get("poll_interval", 5)

    ble_client = ChromaComfortBLE(mac)
    await ble_client.connect()

    async def async_update_data():
        try:
            return await ble_client.get_status()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ChromaComfort",
        update_method=async_update_data,
        update_interval=timedelta(seconds=poll_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN]["coordinator"] = coordinator
    hass.data[DOMAIN]["ble_client"] = ble_client

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = []
    for platform in PLATFORMS:
        result = await hass.config_entries.async_forward_entry_unload(entry, platform)
        unload_ok.append(result)

    ble_client: ChromaComfortBLE = hass.data[DOMAIN].get("ble_client")
    if ble_client:
        await ble_client.disconnect()

    hass.data[DOMAIN].pop("coordinator", None)
    hass.data[DOMAIN].pop("ble_client", None)
    return all(unload_ok)
