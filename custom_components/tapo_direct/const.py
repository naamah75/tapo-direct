"""Constants for Tapo Direct."""

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "tapo_direct"
PLATFORMS = [Platform.LIGHT]
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 10
DEFAULT_TIMEOUT = 10
UPDATE_INTERVAL = timedelta(seconds=DEFAULT_UPDATE_INTERVAL)
