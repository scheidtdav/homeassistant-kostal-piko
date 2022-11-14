"""Constants for the Kostal Piko integration."""
from typing import Callable, Final

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntityDescription,
)
from homeassistant.const import (
    ATTR_BATTERY_CHARGING,
    ATTR_BATTERY_LEVEL,
    ATTR_STATE,
    ATTR_VOLTAGE,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_WATT_HOUR,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_WATT,
    TEMP_CELSIUS,
    TIME_HOURS,
    TIME_SECONDS,
)

DOMAIN = "kostal_piko"

CONDITION_MAP_BATTERY_STATUS = {0: "Charging", 1: "Discharging"}

CONDITION_MAP_INVERTER_STATUS = {0: "", 1: "", 2: "Starting", 3: "Feed-In"}

# Defines all possible sensors
SENSOR_TYPES = tuple[SensorEntityDescription, ...] = (
    # Analog Input sensors
    SensorEntityDescription(
        key="167772417",
        name="Analog Input 1",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="167772673",
        name="Analog Input 2",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="167772929",
        name="Analog Input 3",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="167773185",
        name="Analog Input 4",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Battery sensors
    SensorEntityDescription(
        key="33556226",
        name="Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556229",
        name="Battery Charge",
        native_unit_of_measurement=ATTR_BATTERY_LEVEL,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556238",
        name="Battery Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556230",
        name="Battery Status",
        native_unit_of_measurement=ATTR_STATE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556228",
        name="ChargeCycles",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556227",
        name="Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Grid sensors
    SensorEntityDescription(
        key="67109120",
        name="Output Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67110400",
        name="Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67110656",
        name="CosPhi",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67110144",
        name="Limitation",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109378",
        name="Voltage L1",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109377",
        name="Current L1",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109379",
        name="Power L1",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109634",
        name="Voltage L2",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109633",
        name="Current L2",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109635",
        name="Power L2",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109890",
        name="Voltage L3",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109633",
        name="Current L3",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109635",
        name="Power L3",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Home sensors
    SensorEntityDescription(
        key="83886336",
        name="Home Consumption Solar",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="83886592",
        name="Home Consumption Battery",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="83886848",
        name="Home Consumption Grid",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="83887106",
        name="Home Consumption L1",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="83887362",
        name="Home Consumption L2",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="83887618",
        name="Home Consumption L3",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556736",
        name="DC Power PV",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="67109120",
        name="AC Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="83888128",
        name="Self Consumption",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33556229",
        name="Battery State of Charge",
        native_unit_of_measurement=ATTR_BATTERY_LEVEL,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="16780032",
        name="Operating Status",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # PVGenerator sensors
    SensorEntityDescription(
        key="33555202",
        name="DC 1 Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555201",
        name="DC 1 Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555203",
        name="DC 1 Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555458",
        name="DC 2 Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555457",
        name="DC 2 Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555459",
        name="DC 2 Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555714",
        name="DC 3 Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555713",
        name="DC 3 Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="33555715",
        name="DC 3 Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # S0 sensors
    SensorEntityDescription(
        key="184549632",
        name="S0 in Pulses",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="184549632",
        name="Log Interval",
        native_unit_of_measurement=TIME_SECONDS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Device Information sensors
    # SensorEntityDescription(
    #     key="16779267",
    #     name="Version UI",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16779265",
    #     name="Version FW",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16779266",
    #     name="Version HW",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16779268",
    #     name="Version PAR",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16777728",
    #     name="Serial Number",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16777472",
    #     name="Article Number",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16779522",
    #     name="Country Settings Name",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16779521",
    #     name="Country Settings Version",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16780288",
    #     name="Unknown",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16777984",
    #     name="Inverter Name",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key="16780544",
    #     name="Inverter Type",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # Daily statistics sensors
    SensorEntityDescription(
        key="251658754",
        name="Daily Yield",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659010",
        name="Daily Home Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659266",
        name="Daily Self Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659278",
        name="Daily Self Consumption Rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659279",
        name="Daily Autonomy Degree",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Total statistics sensors
    SensorEntityDescription(
        key="251658753",
        name="Total Yield",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251658753",
        name="Total Operating Time",
        native_unit_of_measurement=TIME_HOURS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659009",
        name="Total Home Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659265",
        name="Total Self Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659280",
        name="Total Self Consumption Rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key="251659281",
        name="Total Autonomy Degree",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
)