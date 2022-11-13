"""Kostal Piko custom component."""
import logging
from datetime import timedelta
from typing import Dict

from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from kostal import Piko, const as PikoConst

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kostal Piko from a config entry."""
    host = entry.data[CONF_HOST]
    user = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    try:
        piko = Piko(async_get_clientsession(hass), host, user, password)
    except Exception as err:
        raise ConfigEntryNotReady from err

    coordinator = PikoUpdateCoordinator(hass, piko)
    await coordinator.async_config_entry_first_refresh()    

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Kostal Piko from a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
    return 

class PikoUpdateCoordinator(DataUpdateCoordinator):
    """Get the latest data from the Kostal Piko Inverter."""

    def __init__(self, hass: HomeAssistant, piko: Piko, update_interval = timedelta(seconds=1)) -> None:
        """Initialize the coordinator."""
        self.hass = hass
        self.piko: Piko = piko
        self._fetch = list()

        super().__init__(
            self.hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval)

    def start_fetch_data(self, dxs_id: int) -> None:
        """Adds the given dxs_id to the data that is being fetched."""
        self._fetch.append(dxs_id)

    def stop_fetch_data(self, dxs_id: int) -> None:
        """Removes the given dxs_id from the data that is being fetched."""
        self._fetch.remove(dxs_id)

    async def _async_update_data(self) -> Dict[int, str]:
        """Fetch data from API endpoint."""
        if not self._fetch:
            return {}

        try:
            data = await self.piko.fetch_props(self._fetch)
            return {
                dxs_id: {
                    v.value
                }
                for dxs_id, v in data
            }
        except Exception as err:
            raise UpdateFailed(err) from err
