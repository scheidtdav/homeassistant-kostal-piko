# Home Assistant Kostal Piko

<div align="center">
[![release_badge](https://img.shields.io/github/release/scheidtdav/homeassistant-kostal-piko.svg?style=for-the-badge)](https://github.com/scheidtdav/homeassistant-kostal-piko/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
</div>

A custom Home Assistant integration for certain Kostal Piko solar inverters.

---

This integration provides Home Assistant with the data that can be obtained from the inverters built-in web portal.
It was tested with the following inverters:
- Piko 8.0 BA running FW v2.30 / UI v6.41

There are a number of sensors provided to Home Assistant. 
Due to limitations of the api of the inverter it is recommended to disable sensor entities that are not required.

<details>
<summary>Click to see the sensors provided by the integration</summary>

- Analog inputs
  - Analog Input 1
  - Analog Input 2
  - Analog Input 3
  - Analog Input 4
- Battery
  - Voltage
  - Charge
  - Current
  - Charging State
  - Charge Cycles
  - Temperature
- Grid
  - Output Power
  - Frequency
  - Power Factor
  - Limitation
  - Voltage L1, L2, L3
  - Current L1, L2, L3
  - Power L1, L2, L3
- House
  - Consumption from solar
  - Consumption from battery
  - Consumption from grid
  - Consumption on L1, L2, L3
- Home
  - Total DC input power
  - Self consumption
  - Operating state
- Generator
  - Current, Voltage and Power of DC inputs 1, 2 and 3
- S0 input
  - Pulse count
  - Log interval
- Statistics
  - Todays yield
  - Todays home consumption, self consumption and self consumption rate
  - Todays degree of autonomy 
  - Total yield
  - Total home consumption, total self consumption and total self consumption rate
  - Total degree of autonomy
  - Total operating time

</details>

## Installation

### HACS
The recommended way is through [HACS](https://hacs.xyz).
Add this repository as a custom repository by going to HACS > Integrations, click the three dots in the top right corner and select custom repositories. Insert the link to this repository and choose integration as the category.
Once added, search for "Kostal Piko" and install the integration.

## Contributing

Any help is appreciated.
Please leave feedback if you tested the integration with an inverter (or firmware) that hasn't been tested yet.

### Versioning

This integration uses [CalVer](https://calver.org/) for versioning.
The scheme is YY.0M.MICRO.

## Core Integration

As of November 2022 the work for an initial version is done with the goal to have this implemented in [Home Assistant Core](https://github.com/home-assistant/core).

Relevant pull requests:
- https://github.com/home-assistant/brands/pull/3869
- https://github.com/home-assistant/home-assistant.io/pull/25002
- https://github.com/home-assistant/core/pull/82391

## Acknowledgements

Many thanks to [Giel Janssens](https://github.com/gieljnssns) for creating a [Kostal component](https://github.com/gieljnssns/kostalpiko-sensor-homeassistant) and inspiring me to create my own for this different version of the api.
Also thanks to [Andreas Rehn](https://github.com/DAMEK86) for creating [pykostal](https://github.com/DAMEK86/pykostal) on top of which this component builds.
