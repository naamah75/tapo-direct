"""Tapo Direct integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from kasa import AuthenticationError, KasaException

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, PLATFORMS
from .coordinator import TapoDirectCoordinator
from .device import close_device, connect_device

type TapoDirectConfigEntry = ConfigEntry[TapoDirectCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: TapoDirectConfigEntry) -> bool:
    """Set up Tapo Direct from a config entry."""
    try:
        device = await connect_device(dict(entry.data))
    except AuthenticationError as err:
        raise ConfigEntryAuthFailed from err
    except KasaException as err:
        raise ConfigEntryNotReady(str(err)) from err

    coordinator = TapoDirectCoordinator(
        hass,
        entry,
        device,
        timedelta(
            seconds=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
        ),
    )
    entry.runtime_data = coordinator
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: TapoDirectConfigEntry) -> bool:
    """Unload a Tapo Direct config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await close_device(entry.runtime_data.device)
    return unloaded
