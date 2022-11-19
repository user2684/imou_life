"""Class to manage fetching data from the API."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from imouapi.device import ImouDevice
from imouapi.exceptions import ImouException

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ImouDataUpdateCoordinator(DataUpdateCoordinator):
    """Implement the DataUpdateCoordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: ImouDevice,
        scan_interval: int,
    ) -> None:
        """Initialize."""
        self.device = device
        self.scan_inteval = scan_interval
        self.platforms = []
        self.entities = []
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=self.scan_inteval),
        )
        _LOGGER.debug(
            "Initialized coordinator. Scan internal %d seconds", self.scan_inteval
        )

    async def _async_update_data(self):
        """HA calls this every DEFAULT_SCAN_INTERVAL to run the update."""
        try:
            return await self.device.async_get_data()
        except ImouException as exception:
            _LOGGER.error(exception.to_string())
            raise UpdateFailed() from exception
