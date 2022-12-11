"""entity sensor platform for Imou."""
import logging

from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from imouapi.exceptions import ImouException

from .const import DOMAIN, SENSOR_ICONS

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ImouEntity(CoordinatorEntity):
    """imou entity class."""

    def __init__(self, coordinator, config_entry, sensor_instance, entity_format):
        """Initialize."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.device = coordinator.device
        self.sensor_instance = sensor_instance
        self.entity_id = async_generate_entity_id(
            entity_format,
            f"{self.device.get_name()}_{self.sensor_instance.get_name()}",
            hass=coordinator.hass,
        )
        self.entity_available = None

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
        """Entity available."""
        # if the availability of the sensor is set, return it
        if self.entity_available is not None:
            return self.entity_available
        # otherwise return the availability of the device
        return self.coordinator.device.get_status()

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device.get_name()} {self.sensor_instance.get_description()}"

    @property
    def icon(self):
        """Return the icon of this sensor."""
        if self.sensor_instance.get_name() in SENSOR_ICONS:
            return SENSOR_ICONS[self.sensor_instance.get_name()]
        return SENSOR_ICONS["__default__"]

    @property
    def extra_state_attributes(self):
        """State attributes."""
        return self.sensor_instance.get_attributes()

    async def async_added_to_hass(self):
        """Entity added to HA (at startup or when re-enabled)."""
        await super().async_added_to_hass()
        _LOGGER.debug("%s added to HA", self.name)
        self.sensor_instance.set_enabled(True)
        # request an update of this sensor
        try:
            await self.sensor_instance.async_update()
        except ImouException as exception:
            _LOGGER.error(exception.to_string())

    async def async_will_remove_from_hass(self):
        """Entity removed from HA (when disabled)."""
        await super().async_will_remove_from_hass()
        _LOGGER.debug("%s removed from HA", self.name)
        self.sensor_instance.set_enabled(False)
