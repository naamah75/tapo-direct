"""Diagnostics support for Tapo Direct."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import TapoDirectConfigEntry

TO_REDACT = {
    "device_id",
    "host",
    "ip",
    "ip_addr",
    "mac",
    "password",
    "rssi",
    "ssid",
    "username",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: TapoDirectConfigEntry,
) -> dict[str, Any]:
    """Return safely redacted diagnostics for a config entry."""
    device = entry.runtime_data.device
    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "device": async_redact_data(
            {
                "alias": device.alias,
                "model": device.model,
                "is_on": device.is_on,
                "sys_info": dict(device.sys_info),
            },
            TO_REDACT,
        ),
        "transport": {
            "device_family": "SMART.TAPOBULB",
            "encryption": "KLAP",
            "login_version": 2,
            "https": False,
            "port": 80,
        },
    }
