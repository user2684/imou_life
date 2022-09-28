"""Switch platform for Imou."""
import logging
from collections.abc import Callable
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from imouapi.exceptions import ImouException

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)


# async def async_setup_entry(hass, entry, async_add_devices):
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: Callable
):
    """Configure platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device = coordinator.device
    sensors = []
    for sensor_instance in coordinator.device.get_sensors("switch"):
        sensor = ImouSwitch(coordinator, entry, sensor_instance)
        sensors.append(sensor)
        _LOGGER.info(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouSwitch(CoordinatorEntity, SwitchEntity):
    """imou switch class."""

    def __init__(self, coordinator, config_entry, sensor_instance):
        """Initialize."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.device = coordinator.device
        self.sensor_instance = sensor_instance

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "_" + self.sensor_instance.get_name()

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": self.device.get_name(),
            "model": self.device.get_model(),
            "manufacturer": self.device.get_manufacturer(),
            "sw_version": self.device.get_firmware(),
            "hw_version": self.device.get_device_id(),
        }

    @property
    def available(self) -> bool:
        """Device available."""
        return self.coordinator.device.is_online()

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        # control the switch
        await self.sensor_instance.async_turn_on()
        # save the new state to the state machine (otherwise will be reset by HA and set to the correct value only upon the nexy update)
        self.async_write_ha_state()
        _LOGGER.info(
            "[%s] Turned %s ON",
            self.device.get_name(),
            self.sensor_instance.get_description(),
        )

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        # control the switch
        await self.sensor_instance.async_turn_off()
        # save the new state to the state machine (otherwise will be reset by HA and set to the correct value only upon the nexy update)
        self.async_write_ha_state()
        _LOGGER.info(
            "[%s] Turned %s OFF",
            self.device.get_name(),
            self.sensor_instance.get_description(),
        )

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self.device.get_name()} {self.sensor_instance.get_description()}"

    @property
    def icon(self):
        """Return the icon of this entity."""
        return self.sensor_instance.get_icon()

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.sensor_instance.is_on()

    async def async_added_to_hass(self):
        """Entity added to HA (at startup or when re-enabled)."""
        await super().async_added_to_hass()
        _LOGGER.debug("%s added to HA", self.name)
        self.sensor_instance.set_enabled(True)
        # request an update of this sensor
        if self.device.is_online():
            try:
                await self.sensor_instance.async_update()
            except ImouException as exception:
                _LOGGER.error(exception.to_string())

    async def async_will_remove_from_hass(self):
        """Entity removed from HA (when disabled)."""
        await super().async_added_to_hass()
        _LOGGER.debug("%s removed from HA", self.name)
        self.sensor_instance.set_enabled(False)
