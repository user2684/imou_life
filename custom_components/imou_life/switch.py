"""Switch platform for Imou."""
from collections.abc import Callable
import logging

from homeassistant.components.switch import ENTITY_ID_FORMAT, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import network

from .const import (
    DOMAIN,
    ENABLED_SWITCHES,
    OPTION_CALLBACK_URL,
    OPTION_CALLBACK_WEBHOOK,
)
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
    for sensor_instance in coordinator.device.get_sensors_by_platform("switch"):
        sensor = ImouSwitch(coordinator, entry, sensor_instance, ENTITY_ID_FORMAT)
        sensors.append(sensor)
        _LOGGER.debug(
            "[%s] Adding %s", device.get_name(), sensor_instance.get_description()
        )
    async_add_devices(sensors)


class ImouSwitch(ImouEntity, SwitchEntity):
    """imou switch class."""

    @property
    def entity_registry_enabled_default(self) -> bool:
        """If the entity is enabled by default."""
        return self.sensor_instance.get_name() in ENABLED_SWITCHES

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.sensor_instance.is_on()

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        # pushNotifications switch
        if self.sensor_instance.get_name() == "pushNotifications":
            callback_url = None
            # if a callback url is provided as an option, use it as is
            if (
                OPTION_CALLBACK_URL in self.config_entry.options
                and self.config_entry.options[OPTION_CALLBACK_URL] != ""
            ):
                callback_url = self.config_entry.options[OPTION_CALLBACK_URL]
            # if a webhook id is provided in the options, build the url
            elif (
                OPTION_CALLBACK_WEBHOOK in self.config_entry.options
                and self.config_entry.options[OPTION_CALLBACK_WEBHOOK] != ""
            ):
                external_url = None
                # get Home Assistant external url
                try:
                    external_url = network.get_url(
                        self.hass,
                        allow_internal=False,
                        allow_ip=True,
                        require_ssl=False,
                    )
                except network.NoURLAvailableError as exception:
                    raise Exception("Unable to determine external url") from exception
                # build the callback url
                callback_url = f"{external_url}/api/webhook/{self.config_entry.options[OPTION_CALLBACK_WEBHOOK]}"
            if callback_url is None:
                raise Exception("No callback url or webhook id provided")
            _LOGGER.debug("Callback URL: %s", callback_url)
            await self.sensor_instance.async_turn_on(url=callback_url)
        # control all other switches
        else:
            await self.sensor_instance.async_turn_on()
        # save the new state to the state machine (otherwise will be reset by HA and set to the correct value only upon the next update)
        self.async_write_ha_state()
        _LOGGER.debug(
            "[%s] Turned %s ON",
            self.device.get_name(),
            self.sensor_instance.get_description(),
        )

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        # control the switch
        await self.sensor_instance.async_turn_off()
        # save the new state to the state machine (otherwise will be reset by HA and set to the correct value only upon the next update)
        self.async_write_ha_state()
        _LOGGER.debug(
            "[%s] Turned %s OFF",
            self.device.get_name(),
            self.sensor_instance.get_description(),
        )
