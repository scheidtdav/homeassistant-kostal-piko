# Kostal Piko 8.0 BA
A custom component to get the readings of a Kostal Piko 8.0 BA inverter

```
sensor:
  - platform: kostal_piko
    host: !secret kostal_host
    monitored_conditions:
      - inverter_status
```
