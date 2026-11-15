"""Data coordinator for Tapo Direct."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from kasa import AuthenticationError, Device, KasaException

from .device import close_device, connect_device

_LOGGER = logging.getLogger(__name__)


class TapoDirectCoordinator(DataUpdateCoordinator[None]):
    """Poll and reconnect one directly configured Tapo light."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        device: Device,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"tapo_direct-{device.host}",
            config_entry=entry,
            update_interval=update_interval,
        )
        self.device = device

    async def _async_update_data(self) -> None:
        """Update data, reconnecting once after a transport failure."""
        try:
            await self.device.update()
            return
        except AuthenticationError as err:
            raise ConfigEntryAuthFailed from err
        except KasaException:
            _LOGGER.debug("Direct update failed; reconnecting once", exc_info=True)

        try:
            await close_device(self.device)
            self.device = await connect_device(dict(self.config_entry.data))
        except AuthenticationError as err:
            raise ConfigEntryAuthFailed from err
        except KasaException as err:
            raise UpdateFailed(f"Direct KLAP v2 update failed: {err}") from err
