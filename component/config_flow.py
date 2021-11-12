import logging

from kostal import Piko
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_BASE, CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO add tests to be accepted to into core


class PikoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for the Kostal Piko inverter."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step asking for host, username and password."""
        errors = {}

        data_schema = {
            vol.Optional(
                CONF_HOST, description={"suggested_value": "http://192.168.178.xx"}
            ): str,
            vol.Optional(CONF_USERNAME, default="pvserver"): str,
            vol.Optional(CONF_PASSWORD, default="pvwr"): str,
        }

        if user_input is not None:
            try:
                inverter_name = await test_connection(self.hass, user_input)
            except ValueError as err:
                _LOGGER.error("Kostal Piko api returned unknown value: %s", err)
                errors[CONF_BASE] = "unknown"
            except ConnectionError as err:
                _LOGGER.error("Could not connect to Kostal Piko api: %s", err)
                errors[CONF_HOST] = "cannot_connect"
            except Exception as err:
                _LOGGER.error("Unknown error: %s", err)
                errors[CONF_BASE] = "unknown"

            if not errors:
                return self.async_create_entry(title=inverter_name, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )


async def test_connection(hass: HomeAssistant, data) -> str:
    """Tests the connection to the inverter and returns its name"""
    _LOGGER.info("Test Connection to Piko inverter.")
    session = async_get_clientsession(hass)

    inverter = Piko(session, data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD])

    # TODO replace the serial number with the inverter name once implemented in pykostal
    res = await inverter.get_info_inverter()

    _LOGGER.info(
        "Found Kostal inverter " + res["InfoInverter"]["InverterName"]["value"]
    )

    return "Kostal Piko Inverter {}".format(
        res["InfoInverter"]["InverterName"]["value"]
    )
