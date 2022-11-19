"""Binary sensor platform for Imou."""
from collections.abc import Callable
import logging

from homeassistant.components.binary_sensor import ENTITY_ID_FORMAT, BinarySensorEntity
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
    for sensor_instance in device.get_sensors_by_platform("binary_sensor"):
        sensor = ImouBinarySensor(coordinator, entry, sensor_instance, ENTITY_ID_FORMAT)
        sensors.append(sensor)
        coordinator.entities.append(sensor)
        _LOGGER.debug(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouBinarySensor(ImouEntity, BinarySensorEntity):
    """imou binary sensor class."""

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self.sensor_instance.is_on()

    @property
    def device_class(self) -> str:
        """Device device class."""
        if self.sensor_instance.get_name() == "motionAlarm":
            return "motion"
        return None
