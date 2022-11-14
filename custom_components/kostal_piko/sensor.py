"""Kostal Piko sensors."""
import logging
from . import PikoUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.switch import SensorEntity

# from kostal import const as PikoConst
import kostal

from homeassistant.components.sensor import ATTR_STATE_CLASS, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ACTUAL_ANALOG_SENSOR_TYPES,
    ACTUAL_BATTERY_SENSOR_TYPES,
    ACTUAL_GRID_SENSOR_TYPES,
    ACTUAL_HOUSE_SENSOR_TYPES,
    ACTUAL_PVGENERATOR_SENSOR_TYPES,
    ACTUAL_SZEROIN_SENSOR_TYPES,
    DOMAIN,
    HOME_SENSOR_TYPES,
    INFO_INVERTER_SENSOR_TYPES,
    INFO_VERSIONS_SENSOR_TYPES,
    STATISTIC_DAY_SENSOR_TYPES,
    STATISTIC_TOTAL_SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the Kostal Piko platform with its sensors"""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        KostalPikoSensor(coordinator, description) for description in SENSOR_TYPES
    )
    return True


class KostalPikoSensor(CoordinatorEntity[PikoUpdateCoordinator], SensorEntity):
    """A Kostal Piko sensor updated using a DataUpdateCoordinator."""

    def __init__(self, coordinator, description):
        """Create a new KostalPikoSensor entity for inverter data."""
        super().__init__(coordinator)
        self.entity_description = description

    async def async_added_to_hass(self) -> None:
        """Register this entity on the Update Coordinator."""
        await super().async_added_to_hass()
        self.coordinator.start_fetch_data(self.dxs_id)

    async def async_will_remove_from_hass(self) -> None:
        """Unregister this entity from the Update Coordinator."""
        self.coordinator.stop_fetch_data(self.dxs_id)
        await super().async_will_remove_from_hass()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            super().available
            and self.coordinator.data is not None
            and self.dxs_id in self.coordinator.data
        )

    @property
    def unique_id(self) -> str:
        """Return the unique id of this Sensor Entity."""
        return f"{self.piko_const_name}_{self.piko_const_value}_{vars(PikoConst)[self.piko_const_name][self.piko_const_value]}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self.dxs_id]
        self.async_write_ha_state()
