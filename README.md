# Kostal Piko 8.0 BA
![Build Status](https://github.com/scheidtdav/kostal-piko-80-ba/workflows/Flake8%20Lint/badge.svg)

A custom component to get the readings of a Kostal Piko 8.0 BA inverter

## Installation

tba

## Usage
Simply add the following lines to your `configuration.yaml` file.
Make sure to select the monitored conditions you are interested in to not bloat your entities :)

```
sensor:
  - platform: kostal_piko
    host: !secret kostal_host
    monitored_conditions:
      - inverter_status
      - inverter_power_consumption
      - inverter_power_input
      - string1_voltage
      - string1_current
      - string1_power
      - string2_voltage
      - string2_current
      - string2_power
      - string3_voltage
      - string3_current
      - string3_power
      - battery_voltage
      - battery_charge
      - battery_charging_current
      - battery_charging
      - battery_charge_cycles
      - battery_temperature
      - home_consumption_solar
      - home_consumption_battery
      - home_consumption_grid
      - home_consumption_phase1
      - home_consumption_phase2
      - home_consumption_phase3
      - feed_in_power
      - feed_in_regulation
      - grid_frequency
      - grid_power_factor
      - phase1_voltage
      - phase1_feed_in_current
      - phase1_feed_in_power
      - phase2_voltage
      - phase2_feed_in_current
      - phase2_feed_in_power
      - phase3_voltage
      - phase3_feed_in_current
      - phase3_feed_in_power
      - power_yield_today
      - yield_consumption_today
      - yield_consumption_rate_today
      - home_consumption_today
      - self_reliance_rate_today
      - power_yield_total
      - yield_consumption_total
      - yield_consumption_rate_total
      - home_consumption_total
      - self_reliance_rate_total
      - uptime
```

## Contributing

The component has only been tested on a Kostal Piko 8.0 BA inverter.
Other inverters of the same series _should_ work, but testing needs to be done.

## Acknowledgements

Thanks to everyone creating open source software and special thanks to all the people contributing to [Home Assistant](www.home-assistant.io), making it as awesome as it is.

Many thanks to [Giel Janssens](https://github.com/gieljnssns) for creating a [Kostal component](https://github.com/gieljnssns/kostalpiko-sensor-homeassistant) and inspiring me to create my own for this different version of the api.
