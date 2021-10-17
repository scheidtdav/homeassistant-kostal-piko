"""The Kostal Piko integration."""
import logging
from datetime import timedelta
from typing import Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from kostal import Piko, const as PikoConst

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kostal Piko from a config entry."""
    coordinator = PikoUpdateCoordinator(hass, entry)
    # await coordinator.async_setup()
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

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, update_interval: timedelta) -> None:
        """Initialize the coordinator object."""
        super().__init__(
            self.hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
            update_method=async_update_data,
        )
        self.hass = hass
        self.config: ConfigEntry = entry
        self._api = None
        self._fetch = list()

    def start_fetch_data(self, dxs_id: int) -> None:
        """Adds the given dxs_id to the data that is being fetched."""
        self._fetch.append(dxs_id)

    def stop_fetch_data(self, dxs_id: int) -> None:
        """Removes the given dxs_id from the data that is being fetched."""
        self._fetch.remove(dxs_id)

    async def async_update_data(self) -> Dict[int, str]:
        api = self._api
        if not self._fetch or api is None:
            return {}

        # TODO Currenty pykostal does not support passing in an array
        # to fetch multiple dxsIds at a time, so this won't work
        data = await self._api._Piko__fetch_dxs_entry(self._fetch)
        return {
            dxs_id: {
                v.value
            }
            for dxs_id, v in data
        }
