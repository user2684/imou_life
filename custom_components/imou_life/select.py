"""Switch platform for Imou."""
from collections.abc import Callable
import logging

from homeassistant.components.select import ENTITY_ID_FORMAT, SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .entity import ImouEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


# async def async_setup_entry(hass, entry, async_add_devices):
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: Callable
):
    """Configure platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device = coordinator.device
    sensors = []
    for sensor_instance in device.get_sensors_by_platform("select"):
        sensor = ImouSelect(coordinator, entry, sensor_instance, ENTITY_ID_FORMAT)
        sensors.append(sensor)
        coordinator.entities.append(sensor)
        _LOGGER.debug(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouSelect(ImouEntity, SelectEntity):
    """imou select class."""

    @property
    def current_option(self):
        """Return current option."""
        return self.sensor_instance.get_current_option()

    @property
    def options(self):
        """Return available options."""
        return self.sensor_instance.get_available_options()

    async def async_select_option(self, option: str) -> None:
        """Se the option."""
        # control the switch
        await self.sensor_instance.async_select_option(option)
        # save the new state to the state machine (otherwise will be reset by HA and set to the correct value only upon the next update)
        self.async_write_ha_state()
        _LOGGER.debug(
            "[%s] Set %s to %s",
            self.device.get_name(),
            self.sensor_instance.get_description(),
            option,
        )
