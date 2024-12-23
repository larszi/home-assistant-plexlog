from datetime import timedelta
import logging
import random

from homeassistant.components.actiontec.model import Device
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import ModbusCoordinator
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

    _LOGGER.info("Setting up ModbusCoordinator with entrt %s", entry.entry_id)  
    coordinator: ModbusCoordinator = hass.data[DOMAIN][
            entry.entry_id
        ].coordinator
    
    entities = [
        SolarPowerRegOne(coordinator, entry),
        SolarPowerRegTwo(coordinator, entry),
        CurrentPowerUsageOne(coordinator, entry),
        CurrentPowerUsageTwo(coordinator, entry),
        BatteryState(coordinator, entry),
        BatteryUsage(coordinator, entry),
        NetworkUsage(coordinator, entry),
    ]
    async_add_entities(entities)



class SolarPowerRegOne(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:solar-power-variant"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Solar Power Register One"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}-solar_power_reg_one"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

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
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "0"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(0)
        self.async_write_ha_state()

class SolarPowerRegTwo(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:solar-power-variant"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Solar Power Register Two"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-solar_power_reg_two"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

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
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "1"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(1)
        self.async_write_ha_state()

class CurrentPowerUsageOne(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:flash"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Current Power Usage Register One"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-current_power_usage_one"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

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
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "2"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(2)
        self.async_write_ha_state()

class CurrentPowerUsageTwo(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:flash"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Current Power Usage Register Two"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-current_power_usage_two"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

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
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "3"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(3)
        self.async_write_ha_state()

class BatteryState(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None

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
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Battery State"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}-battery_state"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"
    
    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._entry.runtime_data._ip_address)},
        }
    @property
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "36"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(36)
        self.async_write_ha_state()

class NetworkUsage(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self._state is not None and self._state < 0:
            return "mdi:transmission-tower-import"
        else:
            return "mdi:transmission-tower-export"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Network Usage"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-network_usage"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

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
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "100"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(100)
        self.async_write_ha_state()        

class BatteryUsage(CoordinatorEntity, SensorEntity):
    """Implementation of a sensor."""

    def __init__(self, coordinator: ModbusCoordinator, device) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)
        self._entry = device
        self._state = None


    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self._state is not None and self._state < 0:
            return "mdi:battery-arrow-up"
        else:
            return "mdi:battery-arrow-down"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Battery Usage"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        return f"{DOMAIN}-battery_usage"
    
    @property
    def device_class(self) -> str:
        """Return device class."""
        return SensorDeviceClass.POWER

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
    def entity_info(self):
        """Return entity specific information."""
        return {"Register": "101"}
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        self._state = self.coordinator.getRegisterValue(101)
        self.async_write_ha_state() 
