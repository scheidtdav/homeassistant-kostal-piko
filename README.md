# Home Assistant Kostal Piko

Home Assistant Component for Kostal Piko Inverters.
**As of October 2021 this is work in progress with the goal to have this implemented in [Home Assistant Core](https://github.com/home-assistant/core).**

## TODOs

- [x] Handle authentication errors in config flow with appropiate message
- [x] Test config flow
- [x] Translate config flow (at least to german, because thats what I know)
- [ ] ~~Implement update coordinators `async_config_entry_first_refresh`~~ Turns out there is no need...
- [x] Add all possible sensors in the const `SENSOR_TYPES`
- [x] Implement device info in sensors.py `async_setup_entry`
- [x] Replace magic numbers of sensor entities with const from pykostal
- [ ] Add integration to [home-assistant/brands](https://github.com/home-assistant/brands)
- [x] Implement connection test properly
- [x] Abort config flow if necessary
- [ ] Inverter Name and Make for config entry

## Acknowledgements

Thanks to everyone creating open source software and special thanks to all the people contributing to [Home Assistant](www.home-assistant.io), making it as awesome as it is.

Many thanks to [Giel Janssens](https://github.com/gieljnssns) for creating a [Kostal component](https://github.com/gieljnssns/kostalpiko-sensor-homeassistant) and inspiring me to create my own for this different version of the api.
Also thanks to [Andreas Rehn](https://github.com/DAMEK86) for creating [pykostal](https://github.com/DAMEK86/pykostal) on top of which this component builds.
