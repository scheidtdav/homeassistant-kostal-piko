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
    'inverter_power_consumption' : ['Inverter Power Consumption', 'W', 'mdi:power-plug', 83888128],
    'inverter_power_input' : ['Power Input', 'W', 'mdi:current-dc', 33556736],
    'string1_voltage' : ['Voltage String 1', 'V', 'mdi:flash', 33555202],
    'string1_current' : ['Current String 1', 'A', 'mdi:current-dc', 33555201],
    'string1_power' : ['Power String 1', 'W', 'mdi:solar-power', 33555203],
    'string2_voltage' : ['Voltage String 2', 'V', 'mdi:flash', 33555458],
    'string2_current' : ['Current String 2', 'A', 'mdi:current-dc', 33555457],
    'string2_power' : ['Power String 2', 'W', 'mdi:solar-power', 33555459],
    'string3_voltage' : ['Voltage String 3', 'V', 'mdi:flash', 33555714],
    'string3_current' : ['Current String 3', 'A', 'mdi:current-dc', 33555713],
    'string3_power' : ['Power String 3', 'W', 'mdi:solar-power', 33555715],
    'battery_voltage' : ['Battery Voltage', 'V', 'mdi:battery-charging-70', 33556226],
    'battery_charge' : ['Battery Charge', '%', 'mdi:car-battery', 33556229],
    'battery_charging_current' : ['Battery Charging Current', 'A', 'mdi:current-dc', 33556238],
    'battery_charging' : ['Battery Charging', '', 'mdi:battery-positive', 33556230],
    'battery_charge_cycles' : ['Battery Charge Cycles', '', 'mdi:battery-heart', 33556228],
    'battery_temperature' : ['Battery Temperature', '°C', 'mdi:thermometer', 33556227],
    'home_consumption_solar' : ['Home Consumption from Solar', 'W', 'mdi:solar-power', 83886336],
    'home_consumption_battery' : ['Home Consumption from Battery', 'W', 'mdi:battery-negative', 83886592],
    'home_consumption_grid' : ['Home Consumption from Grid', 'W', 'mdi:power-plug', 83886848],
    'home_consumption_phase1' : ['Home Consumption on Phase 1', 'W', 'mdi:power-plug', 83887106],
    'home_consumption_phase2' : ['Home Consumption on Phase 2', 'W', 'mdi:power-plug', 83887362],
    'home_consumption_phase3' : ['Home Consumption on Phase 3', 'W', 'mdi:power-plug', 83887618],
    'feed_in_power' : ['Feed In Power', 'W', 'mdi:currency-usd', 67109120],
    'feed_in_regulation' : ['Regulation of Feed In', '%', '', 67110144],
    'grid_frequency' : ['Grid Frequency', 'Hz', '', 67110400],
    'grid_power_factor' : ['Grid Power Factor', '', 67110656],
    'phase1_voltage' : ['Voltage Phase 1', 'V', 'mdi:flash', 67109378],
    'phase1_feed_in_current' : ['Feed In Current Phase 1', 'A', 'mdi:power-ac', 67109377],
    'phase1_feed_in_power' : ['Feed In Power Phase 1', 'A', 'mdi:power-ac', 67109379],
    'phase2_voltage' : ['Voltage Phase 2', 'V', 'mdi:flash', 67109634],
    'phase2_feed_in_current' : ['Feed In Current Phase 2', 'A', 'mdi:power-ac', 67109633],
    'phase2_feed_in_power' : ['Feed In Power Phase 2', 'A', 'mdi:power-ac', 67109635],
    'phase3_voltage' : ['Voltage Phase 3', 'V', 'mdi:flash', 67109890],
    'phase3_feed_in_current' : ['Feed In Current Phase 3', 'A', 'mdi:power-ac', 67109889],
    'phase3_feed_in_power' : ['Feed In Power Phase 3', 'A', 'mdi:power-ac', 67109891],
    'power_yield_today' : ['Power Yield Today', 'Wh', 'mdi:solar-power', 251658754],
    'yield_consumption_today' : ['Yield Consumption Today', 'Wh', 'mdi:chart-donut', 251659266],
    'yield_consumption_rate_today' : ['Yield Consumption Rate Today', '%', 'mdi:chart-donut', 251659278],
    'home_consumption_today' : ['Home Consumption Today', 'Wh', 'mdi:chart-donut', 251659010],
    'self_reliance_rate_today' : ['Self-Reliance Rate Today', '%', 'mdi:chart-donut', 251659279],
    'power_yield_total' : ['Power Yield Total', 'kWh', 'mdi:solar-power', 251658753],
    'yield_consumption_total' : ['Yield Consumption Total', 'kWh', 'mdi:chart-donut', 251659265],
    'yield_consumption_rate_total' : ['Yield Consumption Rate Total', '%', 'mdi:chart-donut', 251659280],
    'home_consumption_total' : ['Home Consumption Total', 'kWh', 'mdi:chart-donut', 251659009],
    'self_reliance_rate_total' : ['Self-Reliance Rate Total', '%', 'mdi:chart-donut', 251659281],
    'uptime' : ['Total Uptime', 'h', 'mdi:clock-outline', 251658496]
}

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
                first = False
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
            new_state = dev._state

            for item in self.data:
                if item["dxsId"] == SENSOR_TYPES[dev.type][3]:
                    new_state = self.get_state_for_sensor_from_value(item["dsxId"], item["value"])
            
                if new_state != dev._state:
                    dev._state = new_state
                    tasks.append(dev.async_update_ha_state())

        if tasks:
            await asyncio.wait(tasks)

    def get_state_for_sensor_from_value(self, id, value):
        if id == SENSOR_TYPES['battery_charging'][3]:
            return True if value == 0 else False
        else:
            return value