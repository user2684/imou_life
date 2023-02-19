"""Sensor platform for Imou."""
from collections.abc import Callable
import logging

from homeassistant.components.sensor import ENTITY_ID_FORMAT
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
    for sensor_instance in device.get_sensors_by_platform("sensor"):
        sensor = ImouSensor(coordinator, entry, sensor_instance, ENTITY_ID_FORMAT)
        sensors.append(sensor)
        coordinator.entities.append(sensor)
        _LOGGER.debug(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouSensor(ImouEntity):
    """imou sensor class."""

    @property
    def device_class(self) -> str:
        """Device device class."""
        if self.sensor_instance.get_name() == "lastAlarm":
            return "timestamp"
        return None

    @property
    def unit_of_measurement(self) -> str:
        """Provide unit of measurement."""
        if self.sensor_instance.get_name() == "storageUsed":
            return "%"
        if self.sensor_instance.get_name() == "battery":
            return "%"
        return None

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.sensor_instance.get_state() is None:
            self.entity_available = False
        return self.sensor_instance.get_state()
