"""The Kostal Piko integration."""
import asyncio
from datetime import timedelta
import logging
from typing import Dict

from aiohttp.client_exceptions import ClientError
from kostal import Piko, const as PikoConst

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kostal Piko from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = PikoUpdateCoordinator(
        hass, _LOGGER, DOMAIN, entry, timedelta(seconds=10)
    )

    if not await coordinator.async_setup():
        return False

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Kostal Piko from a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok


class PikoUpdateCoordinator(DataUpdateCoordinator):
    """Get the latest data from the Kostal Piko Inverter."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        name: str,
        entry: ConfigEntry,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator object."""
        super().__init__(
            hass,
            logger=logger,
            name=name,
            update_interval=update_interval,
        )
        self.hass = hass
        self.config_entry: ConfigEntry = entry
        self._client = None
        # self._fetch = list()

    @property
    def host(self) -> str:
        """Return the host of the Plenticore inverter."""
        return self.config_entry.data[CONF_HOST]

    @property
    def client(self) -> Piko:
        """Return the Plenticore API client."""
        return self._client

    async def async_setup(self) -> bool:
        """Set up Plenticore API client."""
        self._client = Piko(
            async_get_clientsession(self.hass),
            url=self.host,
            username=self.config_entry.data[CONF_USERNAME],
            password=self.config_entry.data[CONF_PASSWORD],
        )
        try:
            # get Inverter Information to test connection
            infoInverter = await self._client.get_info_inverter()
        except (ClientError, asyncio.TimeoutError, ConnectionError, ValueError) as err:
            _LOGGER.error("Error connecting to %s - %s", self.host, err)
            raise ConfigEntryNotReady from err
        else:
            _LOGGER.debug("Log-in successfully to %s", self.host)

        self._shutdown_remove_listener = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, self._async_shutdown
        )

        # get some device meta data
        infoVersions = await self._client.get_info_versions()

        self.device_info = {
            "identifiers": {
                (DOMAIN, infoVersions["InfoVersions"]["SerialNumber"]["value"])
            },
            "manufacturer": "Kostal",
            "model": infoInverter["InfoInverter"]["InverterType"]["value"],
            "name": infoInverter["InfoInverter"]["InverterName"]["value"],
            "sw_version": "FW: {}".format(
                infoVersions["InfoVersions"]["VersionFW"]["value"]
            )
            + " HW: {}".format(infoVersions["InfoVersions"]["VersionHW"]["value"])
            + " UI: {}".format(infoVersions["InfoVersions"]["VersionUI"]["value"]),
        }

        return True

    async def _async_shutdown(self, event):
        """Call from Homeassistant shutdown event."""
        # unset remove listener otherwise calling it would raise an exception
        self._shutdown_remove_listener = None
        await self.async_unload()

    async def async_unload(self) -> None:
        """Unload the Plenticore API client."""
        if self._shutdown_remove_listener:
            self._shutdown_remove_listener()

        _LOGGER.debug("Logged out from %s", self.host)

    def start_fetch_data(self, dxs_id: int) -> None:
        """Adds the given dxs_id to the data that is being fetched."""
        self._fetch.append(dxs_id)

    def stop_fetch_data(self, dxs_id: int) -> None:
        """Removes the given dxs_id from the data that is being fetched."""
        self._fetch.remove(dxs_id)

    async def async_update_data(self) -> dict:
        client = self._client
        if client is None:
            return {}

        data = await client.get_all
        return data
