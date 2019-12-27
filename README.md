# Kostal Piko 8.0 BA
A custom component to get the readings of a Kostal Piko 8.0 BA inverter

```
sensor:
  - platform: kostal-piko
    host: !secret kostal_host
    username: !secret kostal_username
    password: !secret kostal_password
    monitored_conditions:
      - current_power
      - total_energy
      - daily_energy
      - string1_voltage
      - string1_current
      - string2_voltage
      - string2_current
      - l1_voltage
      - l1_power
      - l2_voltage
      - l2_power
      - l3_voltage
      - l3_power
```
