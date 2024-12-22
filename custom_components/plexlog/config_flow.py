"""Config flow for the plexlog integration."""

from __future__ import annotations
from pymodbus.client import ModbusTcpClient

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PORT, CONF_IP_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
import ipaddress

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Required(CONF_PORT): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    _LOGGER.info("Validating the provided data")

    # Check that the Port is a number
    try:
        data[CONF_PORT] = int(data[CONF_PORT])
    except ValueError:
        raise CannotConnect("Invalid port number")
    
    # Check that the IP address is valid
    try:
        ipaddress.ip_address(data[CONF_IP_ADDRESS])
    except ValueError:
        raise CannotConnect("Invalid IP address")
    
    try:
        modbusClient = ModbusTcpClient(host=data[CONF_IP_ADDRESS], port=data[CONF_PORT])
        modbusClient.connect()
        modbusClient.close()
    except:
        raise CannotConnect("Failed to connect to Modbus Client")


    hass.data[DOMAIN] = {
        'ip_address': data[CONF_IP_ADDRESS],
        'port':       data[CONF_PORT]
    }

    # Return info that you want to store in the config entry.
    return {"title": "Plexlogger"}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for plexlog."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                identifier = (DOMAIN, info["title"])
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(identifier)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
