"""Broan ChromaComfort integration for Home Assistant."""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Broan ChromaComfort from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Normally here you would initialize your Bluetooth connection
    _LOGGER.info("Broan ChromaComfort setup complete for entry: %s", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Broan ChromaComfort integration")
    return True
