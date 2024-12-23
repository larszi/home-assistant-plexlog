from asyncio import sleep
import asyncio
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from pymodbus.client import ModbusTcpClient
from homeassistant.const import CONF_PORT, CONF_IP_ADDRESS

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=20)

class ModbusCoordinator(DataUpdateCoordinator):
    """Modbus coordinator."""
    # Registers to read from the modbus device
    registers_to_read = [0, 1, 2, 3, 36, 37, 38]

    _data: dict[int, int] = {}
    
    def __init__(self, hass, config):
        """Initialize coordinator."""

        self.ip_address = config.data[CONF_IP_ADDRESS]
        self.port = config.data[CONF_PORT]
        _LOGGER.info("Creating coordinator with ip %s and port %s", self.ip_address, self.port)

        super().__init__(
            hass,
            _LOGGER,
            name="Plexlogger Modbus Coordinator",
            update_interval=timedelta(seconds=20),
            always_update=True
        )
        modbusClient = ModbusTcpClient(host=self.ip_address, port=self.port)
        modbusClient.connect()

        self._modbusClient = modbusClient

    

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """

        try:
            if not self._modbusClient.connected:
                _LOGGER.error("Modbus client is not connected")
            
        except Exception as e:
            _LOGGER.error("An error occurred while _async_setup: %s", e)


    async def _async_update_data(self):
        #TODO: this need a bit of clean up
        """Fetch data from API endpoint. """

        try:
            # Try to read old power usage, this will fail if it's the first time we read data
            old_power_usage = None
            try: 
                old_power_usage = self._data[3]
            except KeyError:
                old_power_usage = 0

            # Read all registers from modbus device
            for register in self.registers_to_read:
                self._data[register] = await self.read_one_input_register(register)

            # Calculate power usage
            current_solar_power = self._data[1]
            current_power_usage = self._data[3]
            current_battery_power_one = self._data[37]
            current_battery_power_two = self._data[38]
            battery_usage = 0

             # Handle bad data by current_power_usage being too high
            if current_power_usage > old_power_usage + 25000:
                # We have bad data, use the old value
                current_power_usage = old_power_usage
                self._data[3] = old_power_usage

            # If batt_reg_one is 0, then the battery discharging, amount will be in reg_two
            if current_battery_power_one == 0:
                battery_usage = -current_battery_power_two
            # If batt_reg_one is != 0, then the battery charging, amount will be the difference between reg_one and reg_two
            else:
                battery_usage = current_battery_power_one - current_battery_power_two

            power_usage = current_power_usage - current_solar_power  - abs(battery_usage)
            self._data[100] = power_usage
            self._data[101] = -battery_usage

        except Exception as e:
            _LOGGER.error("An error occurred e: %s", e)


    def getRegisterValue(self, register):
        """Fetch data from internal data dict."""
        return self._data[register]
    

    async def read_one_input_register(self, register):
        """Read one input register."""
        try:
            registerValue = self._modbusClient.read_input_registers(register, count=1).registers[0]
        except BrokenPipeError:
            _LOGGER.error("Broken pipe error will try to reconnect")
            self._modbusClient.close()
            self._modbusClient.connect()
            _LOGGER.error("Reconnected to modbus")
        # Sleep to avoid modbus error
        await asyncio.sleep(0.02)
        if registerValue is not None:
            return registerValue
        else:
            _LOGGER.error("Failed to read register at %s", register)
            return None
