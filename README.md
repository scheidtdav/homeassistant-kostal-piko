# Kostal Piko 8.0 BA
![Build Status](https://github.com/scheidtdav/kostal-piko-80-ba/workflows/pythonapp.yml/badge.svg)

A custom component to get the readings of a Kostal Piko 8.0 BA inverter

```
sensor:
  - platform: kostal_piko
    host: !secret kostal_host
    monitored_conditions:
      - inverter_status
```
