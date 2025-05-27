"""Config flow for Nanjing Water integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    CONF_OPENID,
    CONF_ACCOUNT,
    CONF_JSLUID,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

class NanjingWaterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nanjing Water."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the input
                if not user_input[CONF_OPENID]:
                    raise InvalidOpenID
                if not user_input[CONF_ACCOUNT]:
                    raise InvalidAccount
                if not user_input[CONF_JSLUID]:
                    raise InvalidJSLUID
                
                # Validate update interval
                update_interval = user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
                if not isinstance(update_interval, (int, float)) or update_interval < 1:
                    raise InvalidUpdateInterval

                # Check if already configured
                await self.async_set_unique_id(user_input[CONF_ACCOUNT])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Nanjing Water {user_input[CONF_ACCOUNT]}",
                    data={
                        CONF_OPENID: user_input[CONF_OPENID],
                        CONF_ACCOUNT: user_input[CONF_ACCOUNT],
                        CONF_JSLUID: user_input[CONF_JSLUID],
                        CONF_UPDATE_INTERVAL: update_interval,
                    },
                )
            except InvalidOpenID:
                errors["base"] = "invalid_openid"
            except InvalidAccount:
                errors["base"] = "invalid_account"
            except InvalidJSLUID:
                errors["base"] = "invalid_jsluid"
            except InvalidUpdateInterval:
                errors["base"] = "invalid_update_interval"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_OPENID): str,
                    vol.Required(CONF_ACCOUNT): str,
                    vol.Required(CONF_JSLUID): str,
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=DEFAULT_UPDATE_INTERVAL,
                        description="Update interval in hours (minimum 1 hour)"
                    ): int,
                }
            ),
            errors=errors,
        )

class InvalidOpenID(HomeAssistantError):
    """Error to indicate invalid OpenID."""

class InvalidAccount(HomeAssistantError):
    """Error to indicate invalid account."""

class InvalidJSLUID(HomeAssistantError):
    """Error to indicate invalid JSLUID."""

class InvalidUpdateInterval(HomeAssistantError):
    """Error to indicate invalid update interval."""