from datetime import timedelta
import logging
import random
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from pymodbus.client import ModbusTcpClient
from . import PlexloggerEntry



_LOGGER = logging.getLogger(__name__)


SCAN_INTERVAL = timedelta(seconds=25)

current_power_usage_global = None
solar_power_global = None
battery_usage_global = None

async def async_setup_entry(hass, entry: PlexloggerEntry, async_add_entities):
    """Set up the Plexlogger sensors."""
    _LOGGER.info("Setting up the Plexlogger sensors" )

    async_add_entities([SolarPower(entry)])
    async_add_entities([SolarPowerReg2(entry)])
    async_add_entities([CurrentPowerUsage(entry)])
    async_add_entities([CurrentPowerUsageReg1(entry)])
    async_add_entities([BatteryState(entry)])
    async_add_entities([NetworkUsage(entry)])
    async_add_entities([BatteryUsage(entry)])

class SolarPower(Entity):
    """Representation of a Solar Sensor."""

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:solar-power-variant"

    def __init__(self,entry):
        """Initialize the sensor."""
        self._state = None
        self._entry = entry

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Current Solar Power"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "W"

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "unique_device_id"

    @property
    def entity_info(self):
        """Return entity specific information."""
        return {"foo": "bar"}

    async def async_update(self):
        """Fetch new state data for the sensor."""
        result = self._entry.runtime_data._modbus_client.read_input_registers(0, count=1)
        self._state = result.registers[0]
        # Update the global variable for calculating the total power usage
        global solar_power_global
        solar_power_global = self._state

class SolarPowerReg2(Entity):
    """Representation of a Solar Sensor."""

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:solar-power-variant"

    def __init__(self,entry):
        """Initialize the sensor."""
        self._state = None
        self._entry = entry

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Current Solar Power Bank 2"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "W"

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "solarpowerreg2"

    @property
    def entity_info(self):
        """Return entity specific information."""
        return {"foo": "bar"}

    async def async_update(self):
        """Fetch new state data for the sensor."""
        result = self._entry.runtime_data._modbus_client.read_input_registers(1, count=1)
        self._state = result.registers[0]

class CurrentPowerUsage(Entity):
    """Representation of PowerUsage Sensor."""

    def __init__(self, entry):
        """Initialize the sensor."""
        self._state = None
        self._entry = entry

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Current Power Usage"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "W"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "current_power_usage"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:flash"

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    async def async_update(self):
        """Fetch new state data for the sensor."""
        result = self._entry.runtime_data._modbus_client.read_input_registers(3, count=1)

        if result is not None:
            self._state = result.registers[0]
            # Update the global variable for calculating the total power usage
            global current_power_usage_global
            current_power_usage_global = self._state
        else:
            _LOGGER.error("Failed to read current power usage from Modbus Client")
            self._state = None

class CurrentPowerUsageReg1(Entity):
    """Representation of PowerUsage Sensor."""

    def __init__(self, entry):
        """Initialize the sensor."""
        self._state = None
        self._entry = entry

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Current Power Usage Reg 1"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "W"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "current_power_usage_reg_1"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:flash"

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    async def async_update(self):
        """Fetch new state data for the sensor."""
        result = self._entry.runtime_data._modbus_client.read_input_registers(2, count=1)

        if result is not None:
            self._state = result.registers[0]
        else:
            _LOGGER.error("Failed to read current power usage from Modbus Client")
            self._state = None

class BatteryState(Entity):
    """Representation of Battery State Sensor."""

    def __init__(self, entry):
        """Initialize the sensor."""
        self._state = None
        self._entry = entry

    @property
    def icon(self):
        if self._state is None:
            return "mdi:battery-unknown"
        else:
            if self._state > 90:
                return "mdi:battery"
            elif self._state > 80:
                return "mdi:battery-90"
            elif self._state > 70:
                return "mdi:battery-80"
            elif self._state > 60:
                return "mdi:battery-70"
            elif self._state > 50:
                return "mdi:battery-60"
            elif self._state > 40:
                return "mdi:battery-50"
            elif self._state > 30:
                return "mdi:battery-40"
            elif self._state > 20:
                return "mdi:battery-30"
            elif self._state > 10:
                return "mdi:battery-20"
            else:
                return "mdi:battery-10"

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Battery State"
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "battery_state"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        result = self._entry.runtime_data._modbus_client.read_input_registers(36, count=1)
        if result is not None:
            self._state = result.registers[0]
        else:
            _LOGGER.error("Failed to read battery state from Modbus Client")
        

class NetworkUsage(Entity):
    """Representation of Network Usage Sensor."""

    def __init__(self, entry):
        """Initialize the sensor."""
        self._state = None
        self._entry = entry

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Network Usage"
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "W"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "network_usage"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self._state is not None and self._state < 0:
            return "mdi:transmission-tower-import"
        else:
            return "mdi:transmission-tower-export"

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    async def async_update(self):
        """Fetch new state data for the sensor."""
        global current_power_usage_global, solar_power_global, battery_usage_global
        if current_power_usage_global is not None and solar_power_global is not None and battery_usage_global is not None:
            self._state = current_power_usage_global - solar_power_global - battery_usage_global
        else:
            self._state = None


class BatteryUsage(Entity):
    """Representation of Battery Usage Sensor."""

    def __init__(self, entry):
        """Initialize the BatteryUsage sensor."""
        self._state = None
        self._entry = entry

    @property
    def name(self):
        """Return the name of the BatteryUsage sensor."""
        return "Battery Usage"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "W"

    @property
    def state(self):
        """Return the state of the BatteryUsage sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return "battery_usage"

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self._state is not None and self._state < 0:
            return "mdi:battery-arrow-up"
        else:
            return "mdi:battery-arrow-down"
    
    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Update the state from the API
        result_reg_one = self._entry.runtime_data._modbus_client.read_input_registers(37, count=1)
        result_reg_two = self._entry.runtime_data._modbus_client.read_input_registers(38, count=1)

        # If batt_reg_one is 0, then the battery discharging, amount will be in reg_two
        if result_reg_one.registers[0] == 0:
            self._state = -battery_usage
        # If batt_reg_one is != 0, then the battery charging, amount will be the difference between reg_one and reg_two
        else:
            battery_usage = result_reg_one.registers[0] - result_reg_two.registers[0]

        # Update the global variable for calculating the total battery usage
        global battery_usage_global
        battery_usage_global = self._state

