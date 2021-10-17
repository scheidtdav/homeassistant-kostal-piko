"""The Kostal Piko API."""
import logging
from datetime import timedelta
from collections import defaultdict
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_call_later
from kostal import Piko, const as PikoConst
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class PikoApi:
    """Kostal Piko API"""

    def __init__(self, hass, config_entry):
        """Creates a new piko api instance."""
        self.hass = hass
        self.config_entry = config_entry

        self.api = None
        self.device_info = {}

    @property
    def host(self) -> str:
        """Returns the host"""
        return self.config_entry.data[CONF_HOST]

    @property
    def api(self) -> Piko:
        """Return the Plenticore API client."""
        return self._api

    async def async_setup(self) -> bool:
        """Set up the API client for communicating with the inverter."""
        try:
            self._api = Piko(async_get_clientsession(self.hass),
                             self.host, self.config_entry.data[CONF_PASSWORD])
        except ValueError as err:
            _LOGGER.error("Error creating api: %s", err)
            return False

        # get some device info to check the connection and know more about the inverter
        try:
            res = await self._api.__fetch_dxs_entry([PikoConst.InfoVersions['SerialNumber'], PikoConst.InfoVersions['VersionFW'], PikoConst.InfoVersions['ArticleNumber']])

            self.device_info = {
                "identifiers": {(DOMAIN, res[0])},
                "manufacturer": "Kostal",
                "model": f"Piko {res[2]}",
                "sw_version": {res[1]},
            }
        except Exception as err:
            _LOGGER.info(
                "Error connecting to the inverter for initial setup: %s", err)
            return False

        return True
