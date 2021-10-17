"""Constants for the Kostal Piko integration."""
from typing import Callable, Final
from homeassistant.components.sensor import (
    SensorEntityDescription, STATE_CLASS_MEASUREMENT)
from homeassistant.const import PERCENTAGE

DOMAIN = "kostal_piko"

# Defines all possible sensors
# TODO Add all sensors the pykostal library offers
SENSOR_TYPES: Final[SensorEntityDescription] = (
    SensorEntityDescription(
        dxs_id="33556229",
        name="Battery Charge",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT
    )
)
