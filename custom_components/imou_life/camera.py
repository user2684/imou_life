"""Camera platform for Imou."""
from collections.abc import Callable
import logging

from homeassistant.components.camera import (
    ENTITY_ID_FORMAT,
    Camera,
    CameraEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from imouapi.const import PTZ_OPERATIONS
import voluptuous as vol

from .const import (
    ATTR_PTZ_DURATION,
    ATTR_PTZ_HORIZONTAL,
    ATTR_PTZ_OPERATION,
    ATTR_PTZ_VERTICAL,
    ATTR_PTZ_ZOOM,
    DOMAIN,
    ENABLED_CAMERAS,
    SERVIZE_PTZ_LOCATION,
    SERVIZE_PTZ_MOVE,
)
from .entity import ImouEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


# async def async_setup_entry(hass, entry, async_add_devices):
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: Callable
):
    """Configure platform."""
    platform = entity_platform.async_get_current_platform()

    # Create PTZ location service
    platform.async_register_entity_service(
        SERVIZE_PTZ_LOCATION,
        {
            vol.Required(ATTR_PTZ_HORIZONTAL, default=0): vol.Range(min=-1, max=1),
            vol.Required(ATTR_PTZ_VERTICAL, default=0): vol.Range(min=-1, max=1),
            vol.Required(ATTR_PTZ_ZOOM, default=0): vol.Range(min=0, max=1),
        },
        "async_service_ptz_location",
    )

    # Create PTZ move service
    platform.async_register_entity_service(
        SERVIZE_PTZ_MOVE,
        {
            vol.Required(ATTR_PTZ_OPERATION, default=0): vol.In(list(PTZ_OPERATIONS)),
            vol.Required(ATTR_PTZ_DURATION, default=1000): vol.Range(
                min=100, max=10000
            ),
        },
        "async_service_ptz_move",
    )

    coordinator = hass.data[DOMAIN][entry.entry_id]
    device = coordinator.device
    sensors = []
    for sensor_instance in device.get_sensors_by_platform("camera"):
        sensor = ImouCamera(coordinator, entry, sensor_instance, ENTITY_ID_FORMAT)
        sensors.append(sensor)
        coordinator.entities.append(sensor)
        _LOGGER.debug(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouCamera(ImouEntity, Camera):
    """imou camera class."""

    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(self, coordinator, config_entry, sensor_instance, entity_format):
        """Initialize."""
        Camera.__init__(self)
        ImouEntity.__init__(
            self, coordinator, config_entry, sensor_instance, entity_format
        )

    @property
    def entity_registry_enabled_default(self) -> bool:
        """If the entity is enabled by default."""
        return self.sensor_instance.get_name() in ENABLED_CAMERAS

    async def async_camera_image(self, width=None, height=None) -> bytes:
        """Return bytes of camera image."""
        _LOGGER.debug(
            "[%s] requested camera image",
            self.device.get_name(),
        )
        return await self.sensor_instance.async_get_image()

    async def stream_source(self) -> str:
        """Return the source of the stream."""
        _LOGGER.debug(
            "[%s] requested camera stream url",
            self.device.get_name(),
        )
        return await self.sensor_instance.async_get_stream_url()

    async def async_service_ptz_location(self, horizontal, vertical, zoom):
        """Perform PTZ location action."""
        _LOGGER.debug(
            "[%s] invoked PTZ location action horizontal:%f, vertical:%f, zoom:%f",
            self.device.get_name(),
            horizontal,
            vertical,
            zoom,
        )
        await self.sensor_instance.async_service_ptz_location(
            horizontal,
            vertical,
            zoom,
        )

    async def async_service_ptz_move(self, operation, duration):
        """Perform PTZ move action."""
        _LOGGER.debug(
            "[%s] invoked PTZ move action operation:%s, duration:%i",
            self.device.get_name(),
            operation,
            duration,
        )
        await self.sensor_instance.async_service_ptz_move(
            operation,
            duration,
        )
