from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

# TODO add tests to be accepted to into core


class PikoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for the Kostal Piko inverter."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step asking for host, username and password."""
        errors = {}

        data_schema = {
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
        }

        if user_input is not None:
            # TODO validate user input

            if not errors:
                return self.async_create_entry(title=user_input["host"], data=user_input)

        return self.async_show_form(step_id="init", data_schema=vol.Schema(data_schema))
