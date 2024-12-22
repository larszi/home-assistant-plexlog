"""The plexlog integration."""

from __future__ import annotations
import asyncio
import logging
from .const import DOMAIN

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr  # Add this import
from . import plexlogger

PLATFORMS: list[Platform] = [Platform.SENSOR]


type PlexloggerEntry = ConfigEntry[plexlogger.Plexlogger]

async def async_setup_entry(hass: HomeAssistant, entry: PlexloggerEntry) -> bool:
    """Set up Plexlogger from a config entry."""

    entry.runtime_data = plexlogger.Plexlogger(hass, entry.data["ip_address"], entry.data["port"])

    if entry.runtime_data._modbus_client is None:
        return False

    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.data["ip_address"])},
        manufacturer="Plexlogger",
        name="Plexlogger Solar Gateway",
        model="PL-100",
        sw_version="1.0",
    )

    hass.config_entries.async_update_entry(entry, title="Plexlog")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True



async def async_unload_entry(hass: HomeAssistant, entry: PlexloggerEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
