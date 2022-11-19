"""Binary sensor platform for Imou."""
from collections.abc import Callable
import logging

from homeassistant.components.button import ENTITY_ID_FORMAT, ButtonEntity
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
    for sensor_instance in device.get_sensors_by_platform("button"):
        sensor = ImouButton(coordinator, entry, sensor_instance, ENTITY_ID_FORMAT)
        sensors.append(sensor)
        coordinator.entities.append(sensor)
        _LOGGER.debug(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouButton(ImouEntity, ButtonEntity):
    """imou button class."""

    async def async_press(self) -> None:
        """Handle the button press."""
        # press the button
        await self.sensor_instance.async_press()
        _LOGGER.debug(
            "[%s] Pressed %s",
            self.device.get_name(),
            self.sensor_instance.get_description(),
        )
        # ask the coordinator to refresh data to all the sensors
        if self.sensor_instance.get_name() == "refreshData":
            await self.coordinator.async_request_refresh()
        # refresh the motionAlarm sensor
        if self.sensor_instance.get_name() == "refreshAlarm":
            # update the motionAlarm sensor
            await self.coordinator.device.get_sensor_by_name(
                "motionAlarm"
            ).async_update()
            # ask HA to update its state based on the new value
            for entity in self.coordinator.entities:
                if entity.sensor_instance.get_name() in "motionAlarm":
                    await entity.async_update_ha_state()

    @property
    def device_class(self) -> str:
        """Device device class."""
        if self.sensor_instance.get_name() == "restartDevice":
            return "restart"
        return None
