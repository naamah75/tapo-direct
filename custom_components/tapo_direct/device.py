"""Direct KLAP v2 device helpers for Tapo Direct."""

from __future__ import annotations

from typing import Any

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from kasa import Credentials, Device, DeviceConfig
from kasa.deviceconfig import (
    DeviceConnectionParameters,
    DeviceEncryptionType,
    DeviceFamily,
)

from .const import DEFAULT_TIMEOUT


def build_device_config(data: dict[str, Any]) -> DeviceConfig:
    """Build the known-working direct KLAP v2 connection configuration."""
    return DeviceConfig(
        host=data[CONF_HOST],
        credentials=Credentials(data[CONF_USERNAME], data[CONF_PASSWORD]),
        connection_type=DeviceConnectionParameters(
            device_family=DeviceFamily.SmartTapoBulb,
            encryption_type=DeviceEncryptionType.Klap,
            login_version=2,
            https=False,
            http_port=80,
        ),
        timeout=DEFAULT_TIMEOUT,
    )


async def connect_device(data: dict[str, Any]) -> Device:
    """Connect directly without discovery and populate initial state."""
    device = await Device.connect(config=build_device_config(data))
    await device.update()
    return device


async def close_device(device: Device | None) -> None:
    """Close a device transport when it exists."""
    if device is not None:
        await device.protocol.close()
