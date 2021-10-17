"""Kostal Piko sensors."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from homeassistant.components.switch import SensorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the Kostal Piko platform with its sensors"""
    piko = hass.data[DOMAIN][entry.entry_id]
    entities = []


class KostalPikoSensor(CoordinatorEntity, SensorEntity):
    """A Kostal Piko sensor updated using a DataUpdateCoordinator."""
