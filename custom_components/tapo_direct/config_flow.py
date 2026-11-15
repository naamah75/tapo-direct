"""Config flow for Tapo Direct."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from kasa import AuthenticationError, KasaException

from .const import DOMAIN
from .device import close_device, connect_device


class TapoDirectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tapo Direct."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial configuration step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})
            device = None
            try:
                device = await connect_device(user_input)
            except AuthenticationError:
                errors["base"] = "invalid_auth"
            except KasaException:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(device.device_id)
                self._abort_if_unique_id_configured(
                    updates={CONF_HOST: user_input[CONF_HOST]},
                )
                return self.async_create_entry(
                    title=device.alias or f"Tapo {device.model}",
                    data=user_input,
                )
            finally:
                await close_device(device)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                },
            ),
            errors=errors,
        )
