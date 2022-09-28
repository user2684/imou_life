"""
Custom integration to integrate Imou Life with Home Assistant.

For more details about this integration, please refer to
https://github.com/user2684/imou_life
"""
import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from imouapi.device import ImouDevice

from .const import CONF_APP_ID
from .const import CONF_APP_SECRET
from .const import CONF_DEVICE_ID
from .const import CONF_DEVICE_NAME
from .const import DEFAULT_SCAN_INTERVAL
from .const import DOMAIN
from .const import OPTION_API_TIMEOUT
from .const import OPTION_API_URL
from .const import OPTION_SCAN_INTERVAL
from .const import PLATFORMS
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
    name = entry.data.get(CONF_DEVICE_NAME)
    app_id = entry.data.get(CONF_APP_ID)
    app_secret = entry.data.get(CONF_APP_SECRET)
    device_id = entry.data.get(CONF_DEVICE_ID)
    _LOGGER.info("Setting up device %s (%s)", name, device_id)
    _LOGGER.debug("Loading entry %s", entry.entry_id)

    # create an imou device instance
    base_url = entry.options.get(OPTION_API_URL, None)
    timeout = entry.options.get(OPTION_API_TIMEOUT, None)
    device = ImouDevice(app_id, app_secret, device_id, session, base_url, timeout)
    device.enable_sensors(False)
    if name is not None:
        device.set_name(name)

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
