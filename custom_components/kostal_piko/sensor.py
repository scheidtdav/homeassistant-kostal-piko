"""
Support for the Kostal Piko 8.0 BA inverter.
"""
import asyncio
import logging
from random import randrange

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_HOST, CONF_MONITORED_CONDITIONS)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_call_later
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    'inverter_status' : ['Inverter Status', '', 'mdi:information-outline', 16780032],


    #'operating_mode' : ['Operating Mode', '', ''],
    #'solar_generator_power': ['Solar generator power', 'W', 'mdi:solar-power'],
    #'consumption_phase_1': ['Consumption phase 1', 'W', 'mdi:power-socket-eu'],
    #'consumption_phase_2': ['Consumption phase 2', 'W', 'mdi:power-socket-eu'],
    #'consumption_phase_3': ['Consumption phase 3', 'W', 'mdi:power-socket-eu'],
    #'current_power': ['Current power', 'W', 'mdi:solar-power'],
    #'total_energy': ['Total energy', 'kWh', 'mdi:solar-power'],
    #'daily_energy': ['Daily energy', 'kWh', 'mdi:solar-power'],
    #'string1_voltage': ['String 1 voltage', 'V', 'mdi:current-ac'],
    #'string1_current': ['String 1 current', 'A', 'mdi:flash'],
    #'string2_voltage': ['String 2 voltage', 'V', 'mdi:current-ac'],
    #'string2_current': ['String 2 current', 'A', 'mdi:flash'],
    #'string3_voltage': ['String 3 voltage', 'V', 'mdi:current-ac'],
    #'string3_current': ['String 3 current', 'A', 'mdi:flash'],
    #'l1_voltage': ['L1 voltage', 'V', 'mdi:current-ac'],
    #'l1_power': ['L1 power', 'W', 'mdi:power-plug'],
    #'l2_voltage': ['L2 voltage', 'V', 'mdi:current-ac'],
    #'l2_power': ['L2 power', 'W', 'mdi:power-plug'],
    #'l3_voltage': ['L3 voltage', 'V', 'mdi:current-ac'],
    #'l3_power': ['L3 power', 'W', 'mdi:power-plug'],
    #'battery_charge' : ['Battery Charge', '%', 'mdi:car-battery'],
    #'charge_cycle_count' : ['Battery Cycle Count', '', 'mdi:battery-heart'],
    #'battery_temp' : ['Battery Temperature', '°C', 'mdi:thermometer'],
    #'battery_voltage' : ['Battery Voltage', 'V', 'mdi:current-dc'],
    #'battery_current' : ['Battery Current', 'A', 'mdi:flash'],
    #'battery_is_charging' : ['Battery Charging', '', 'mdi:battery-charging-100'],
    #'system_current_total_consumption': ['Current Total Consumption', 'W', 'mdi:power-socket-eu'],
    #'solar_self_consumption' : ['Current Consumption of Self-Harvested', 'W', 'mdi:power-socket-eu']
}

#JSON_KEYS = {
#    'operating_mode' : 16780032,
#    'solar_generator_power' : 33556736,
#    'string1_voltage' : 33555202,
#    'string1_current' : 33555201,
#    'string1_power' : 33555203,
#    'string2_voltage' : 33555458,
#    'string2_current' : 33555457,
#    'string2_power' : 33555459,
#    'string3_voltage' : 33555714,
#    'string3_current' : 33555713,
#    'string3_power' : 33555715,
#    'current_power' : 67109120,
#    'actot_Hz' : 67110400,
#    'actot_cos' : 67110656,
#    'actot_limitation' : 67110144,
#    'l1_voltage' : 67109378,
#    'l1_current' : 67109377,
#    'l1_power' : 67109379,
#    'l2_voltage' : 67109634,
#    'l2_current' : 67109633,
#    'l2_power' : 67109635,
#    'l3_voltage' : 67109890,
#    'l3_current' : 67109889,
#    'l3_power' : 67109891,
#    'daily_energy' : 251658754,
#    'total_energy' : 251658753,
#    'operationtime_h' : 251658496,
#    'battery_charge' : 33556229,
#    'charge_cycle_count' : 33556228,
#    'battery_temp' : 33556227,
#    'battery_voltage' : 33556226,
#    'battery_current' : 33556238,
#    'battery_is_charging' : 33556230,
#    'system_current_total_consumption': 83886848,
#    'solar_self_consumption' : 83888128
#    }

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_MONITORED_CONDITIONS):
        vol.All(cv.ensure_list, [vol.In(list(SENSOR_TYPES))])
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Kostal Piko 8.0 BA inverter platform."""

    dev = []
    for sensor_type in config[CONF_MONITORED_CONDITIONS]:
        dev.append(InverterSensor(sensor_type))

    async_add_entities(dev)

    inverter = Piko80BA(hass, dev, config[CONF_HOST], config[CONF_MONITORED_CONDITIONS])
    await inverter.fetching_data()

class InverterSensor(Entity):
    """Representation of a Piko 8.0 BA inverter sensor."""

    def __init__(self, sensor_type):
        """Initialize the sensor."""
        self.type = sensor_type
        self._name = SENSOR_TYPES[self.type][0]
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name}"

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

class Piko80BA:
    """Allows getting the latest data from a Piko 8.0 BA and updates the states."""

    def __init__(self, hass, devices, host, monitored_conditions):
        """Initializes the data object."""
        self._url = f"{host}/api/dxs.json"

        first = True
        for condition in monitored_conditions:
            if first:
                self._url += f"?dxsEntries={SENSOR_TYPES[condition][3]}"
            else:
                self._url += f"&dxsEntries={SENSOR_TYPES[condition][3]}"

        self.devices = devices
        self.data = {}
        self.hass = hass

    async def fetching_data(self, *_):
        """Get the latest data from the inverter for all monitored conditions."""

        def try_again(err: str):
            """Retry in 5 to 10 minutes."""
            minutes = 5 + randrange(6)
            _LOGGER.error("Retrying in %i minutes: %s", minutes, err)
            async_call_later(self.hass, minutes * 60, self.fetching_data)

        try:
            websession = async_get_clientsession(self.hass)
            with async_timeout.timeout(10):
                resp = await websession.get(self._url)
            if resp.status != 200:
                try_again(f"{resp.url} returned {resp.status}")
                return
            text = await resp.text()

        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            try_again(err)
            return
        
        import json

        try:
            self.data = (json.loads(text))["dxsEntries"]
        except Exception as err:
            try_again(err)
            return

        await self.updating_devices()
        async_call_later(self.hass, 1*60, self.fetching_data)

    async def updating_devices(self, *_):
        """Find the current data from self.data."""
        if not self.data:
            return

        tasks = []
        for dev in self.devices:
            for item in self.data:
                if item["dxsId"] == SENSOR_TYPES[dev.type][3]:
                    new_state = item["value"]
            
                if new_state != dev._state:
                    dev._state = new_state
                    tasks.append(dev.async_update_ha_state())

        if tasks:
            await asyncio.wait(tasks)