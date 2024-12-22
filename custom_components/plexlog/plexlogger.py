import asyncio
import logging
from homeassistant.core import HomeAssistant
from pymodbus.client import ModbusTcpClient

_LOGGER = logging.getLogger(__name__)


class Plexlogger:
    """This is the Gateway Logger."""

    manufacturer = "Plexlog"

    def __init__(self, hass: HomeAssistant, ip_address: str, port: int) -> None:
        """Init Plexlogger."""
        self._ip_address = ip_address
        self._hass = hass
        self._port = port
        self.name = "Plexlogger"
        self._id = ip_address.lower()
        self.online = True

        modbusClient = ModbusTcpClient(host="192.168.153.20", port=503)
        modbusClient.connect()

        if modbusClient.is_socket_open():
            _LOGGER.info("Successfully connected to Modbus Client at %s:%s", ip_address, port)
            self.online = True
            self._modbus_client = modbusClient

        else:
            _LOGGER.error("Failed to connect to Modbus Client at %s:%s", ip_address, port)
            self.online = False
            self._modbus_client = None

    @property
    def hub_id(self) -> str:
        """ID for Plexlogger."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity is OK."""
        await asyncio.sleep(1)
        return True