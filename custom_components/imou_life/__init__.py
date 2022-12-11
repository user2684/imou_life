"""
Custom integration to integrate Imou Life with Home Assistant.

For more details about this integration, please refer to
https://github.com/user2684/imou_life
"""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from imouapi.api import ImouAPIClient
from imouapi.device import ImouDevice
from imouapi.exceptions import ImouException

from .const import (
    CONF_API_URL,
    CONF_APP_ID,
    CONF_APP_SECRET,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    DEFAULT_API_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    OPTION_API_TIMEOUT,
    OPTION_API_URL,
    OPTION_CAMERA_WAIT_BEFORE_DOWNLOAD,
    OPTION_SCAN_INTERVAL,
    OPTION_WAIT_AFTER_WAKE_UP,
    PLATFORMS,
)
from .coordinator import ImouDataUpdateCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
    session = async_get_clientsession(hass)

    # retrieve the configuration entry parameters
    _LOGGER.debug("Loading entry %s", entry.entry_id)
    name = entry.data.get(CONF_DEVICE_NAME)
    api_url = entry.data.get(CONF_API_URL)
    app_id = entry.data.get(CONF_APP_ID)
    app_secret = entry.data.get(CONF_APP_SECRET)
    device_id = entry.data.get(CONF_DEVICE_ID)
    _LOGGER.debug("Setting up device %s (%s)", name, device_id)

    # create an imou api client instance
    api_client = ImouAPIClient(app_id, app_secret, session)
    _LOGGER.debug("Setting API base url to %s", api_url)
    api_client.set_base_url(api_url)
    timeout = entry.options.get(OPTION_API_TIMEOUT, None)
    if isinstance(timeout, str):
        timeout = None if timeout == "" else int(timeout)
    if timeout is not None:
        _LOGGER.debug("Setting API timeout to %d", timeout)
        api_client.set_timeout(timeout)

    # create an imou device instance
    device = ImouDevice(api_client, device_id)
    if name is not None:
        device.set_name(name)
    camera_wait_before_download = entry.options.get(
        OPTION_CAMERA_WAIT_BEFORE_DOWNLOAD, None
    )
    if camera_wait_before_download is not None:
        _LOGGER.debug(
            "Setting camera wait before download to %f", camera_wait_before_download
        )
        device.set_camera_wait_before_download(camera_wait_before_download)
    wait_after_wakeup = entry.options.get(OPTION_WAIT_AFTER_WAKE_UP, None)
    if wait_after_wakeup is not None:
        _LOGGER.debug("Setting wait after wakeup to %f", wait_after_wakeup)
        device.set_wait_after_wakeup(wait_after_wakeup)

    # initialize the device so to discover all the sensors
    try:
        await device.async_initialize()
    except ImouException as exception:
        _LOGGER.error(exception.to_string())
        raise ImouException() from exception
    # at this time, all sensors must be disabled (will be enabled individually by async_added_to_hass())
    for sensor_instance in device.get_all_sensors():
        sensor_instance.set_enabled(False)

    # create a coordinator
    coordinator = ImouDataUpdateCoordinator(
        hass, device, entry.options.get(OPTION_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    )
    # fetch the data
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    # store the coordinator so to be accessible by each platform
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # for each enabled platform, forward the configuration entry for its setup
    for platform in PLATFORMS:
        coordinator.platforms.append(platform)
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    _LOGGER.debug("Unloading entry %s", entry.entry_id)
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_migrate_entry(hass, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)
    data = {**config_entry.data}
    options = {**config_entry.options}
    unique_id = data[CONF_DEVICE_ID]

    if config_entry.version == 1:
        # add the api url. If in option, use it, otherwise use the default one
        option_api_url = config_entry.options.get(OPTION_API_URL, None)
        api_url = DEFAULT_API_URL if option_api_url is None else option_api_url
        data[CONF_API_URL] = api_url
        config_entry.version = 2

    if config_entry.version == 2:
        # if api_url is empty, copy over the one in options
        if data[CONF_API_URL] == "":
            data[CONF_API_URL] = DEFAULT_API_URL
        if OPTION_API_URL in options:
            del options[OPTION_API_URL]
        config_entry.version = 3

    # update the config entry
    hass.config_entries.async_update_entry(
        config_entry, data=data, options=options, unique_id=unique_id
    )
    _LOGGER.info("Migration to version %s successful", config_entry.version)
    return True
