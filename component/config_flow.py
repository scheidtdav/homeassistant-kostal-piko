import logging
import voluptuous as vol
import kostal

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_BASE, CONF_HOST, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO add tests to be accepted to into core

SETUP_SCHEMA = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

async def test_connection(hass: HomeAssistant, data) -> str:
    """Tests the connection to the inverter and returns its name"""
    session = async_get_clientsession(hass)
    inverter = kostal.Piko(
        session, data["host"], data["username"], data["password"])
    # TODO replace the serial number with the inverter name once implemented in pykostal
    res = await inverter._Piko__fetch_dxs_entry(kostal.const.InfoVersions["SerialNumber"])
    return f"Kostal Piko Inverter {res.value}"

class KostalPikoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for the Kostal Piko inverter."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the user initiating the flow via the user interface. 
        Will ask for host, username and password."""
        errors = {}

        if user_input is not None:
            try:
                inverter_name = await test_connection(self.hass, user_input)
            # TODO handle auth error with correct message
            # except SOMEERROR as err:
            # _LOGGER.error(...)
            # errors[CONF_BASE] = "auth"
            except ValueError as err:
                _LOGGER.error(
                    "Kostal Piko api returned unknown value: %s", err)
                errors[CONF_BASE] = "unknown"
            except ConnectionError as err:
                _LOGGER.error(
                    "Could not connect to Kostal Piko api: %s", err)
                errors[CONF_HOST] = "cannot_connect"
            except Exception as err:
                _LOGGER.error(
                    "Unknown error: %s", err)
                errors[CONF_BASE] = "unknown"

            if not errors:
                return self.async_create_entry(title=inverter_name, data=user_input)

        return self.async_show_form(step_id="user", data_schema=SETUP_SCHEMA, errors=errors)
