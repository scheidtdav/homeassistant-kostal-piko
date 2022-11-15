"""Constants for the Kostal Piko integration."""
from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntityDescription,
)
from homeassistant.const import (
    ATTR_BATTERY_LEVEL,
    ATTR_STATE,
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
import kostal

DOMAIN = "kostal_piko"

CONDITION_MAP_BATTERY_STATUS = {0: "Charging", 1: "Discharging"}

CONDITION_MAP_INVERTER_STATUS = {0: "", 1: "", 2: "Starting", 3: "Feed-In"}

# Defines all possible sensors
SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    # Analog Input sensors
    SensorEntityDescription(
        key=str(kostal.ActualAnalogInputs.ANALOG1),
        name="Analog Input 1",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualAnalogInputs.ANALOG2),
        name="Analog Input 2",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualAnalogInputs.ANALOG3),
        name="Analog Input 3",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualAnalogInputs.ANALOG4),
        name="Analog Input 4",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Battery sensors
    SensorEntityDescription(
        key=str(kostal.ActualBattery.VOLTAGE),
        name="Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualBattery.CHARGE),
        name="Battery Charge",
        native_unit_of_measurement=ATTR_BATTERY_LEVEL,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualBattery.CURRENT),
        name="Battery Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualBattery.CURRENT_DIR),
        name="Battery Current Direction",
        native_unit_of_measurement=ATTR_STATE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualBattery.CHARGE_CYCLES),
        name="ChargeCycles",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualBattery.TEMPERATURE),
        name="Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Grid sensors
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_OUTPUT_POWER),
        name="Output Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_FREQ),
        name="Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_COS_PHI),
        name="CosPhi",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_LIMITATION),
        name="Limitation",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_VOLTAGE_L1),
        name="Voltage L1",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_CURRENT_L1),
        name="Current L1",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_POWER_L1),
        name="Power L1",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_VOLTAGE_L2),
        name="Voltage L2",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_CURRENT_L2),
        name="Current L2",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_POWER_L2),
        name="Power L2",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_VOLTAGE_L3),
        name="Voltage L3",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_CURRENT_L3),
        name="Current L3",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGrid.GRID_POWER_L3),
        name="Power L3",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Home sensors
    SensorEntityDescription(
        key=str(kostal.ActualHome.ACT_HOME_CONSUMPTION_SOLAR),
        name="Home Consumption Solar",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualHome.ACT_HOME_CONSUMPTION_BATTERY),
        name="Home Consumption Battery",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualHome.ACT_HOME_CONSUMPTION_GRID),
        name="Home Consumption Grid",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualHome.PHASE_SELECTIVE_CONSUMPTION_L1),
        name="Home Consumption L1",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualHome.PHASE_SELECTIVE_CONSUMPTION_L2),
        name="Home Consumption L2",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualHome.PHASE_SELECTIVE_CONSUMPTION_L3),
        name="Home Consumption L3",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.Home.DC_POWER_PV),
        name="DC Power PV",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.Home.AC_POWER),
        name="AC Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.Home.OWN_CONSUMPTION),
        name="Self Consumption",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.Home.BATTERY_STATE_OF_CHARGE),
        name="Battery State of Charge",
        native_unit_of_measurement=ATTR_BATTERY_LEVEL,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.Home.OPERATING_STATUS),
        name="Operating Status",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # PVGenerator sensors
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_1_VOLTAGE),
        name="DC 1 Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_1_CURRENT),
        name="DC 1 Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_1_POWER),
        name="DC 1 Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_2_VOLTAGE),
        name="DC 2 Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_2_CURRENT),
        name="DC 2 Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_2_POWER),
        name="DC 2 Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_3_VOLTAGE),
        name="DC 3 Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_3_CURRENT),
        name="DC 3 Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualGenerator.DC_3_POWER),
        name="DC 3 Power",
        native_unit_of_measurement=POWER_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # S0 sensors
    SensorEntityDescription(
        key=str(kostal.ActualSZeroIn.S0_IN_PULSE_COUNT),
        name="S0 in Pulses",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.ActualSZeroIn.LOG_INTERVAL),
        name="Log Interval",
        native_unit_of_measurement=TIME_SECONDS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Device Information sensors
    # SensorEntityDescription(
    #     key=str("16779267"),
    #     name="Version UI",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16779265"),
    #     name="Version FW",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16779266"),
    #     name="Version HW",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16779268"),
    #     name="Version PAR",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16777728"),
    #     name="Serial Number",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16777472"),
    #     name="Article Number",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16779522"),
    #     name="Country Settings Name",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16779521"),
    #     name="Country Settings Version",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16780288"),
    #     name="Unknown",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16777984"),
    #     name="Inverter Name",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # SensorEntityDescription(
    #     key=str("16780544"),
    #     name="Inverter Type",
    #     state_class=STATE_CLASS_MEASUREMENT,
    # ),
    # Daily statistics sensors
    SensorEntityDescription(
        key=str(kostal.StatisticDay.YIELD),
        name="Daily Yield",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticDay.HOME_CONSUMPTION),
        name="Daily Home Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticDay.SELF_CONSUMPTION),
        name="Daily Self Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticDay.SELF_CONSUMPTION_RATE),
        name="Daily Self Consumption Rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticDay.AUTONOMY_DEGREE),
        name="Daily Autonomy Degree",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    # Total statistics sensors
    SensorEntityDescription(
        key=str(kostal.StatisticTotal.YIELD),
        name="Total Yield",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticTotal.OPERATING_TIME),
        name="Total Operating Time",
        native_unit_of_measurement=TIME_HOURS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticTotal.HOME_CONSUMPTION),
        name="Total Home Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticTotal.SELF_CONSUMPTION),
        name="Total Self Consumption",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticTotal.SELF_CONSUMPTION_RATE),
        name="Total Self Consumption Rate",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=str(kostal.StatisticTotal.AUTONOMY_DEGREE),
        name="Total Autonomy Degree",
        native_unit_of_measurement=PERCENTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
)
