"""Diagnostics support for imou_life."""
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import ImouDataUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: ImouDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    to_redact = {"app_id", "app_secret", "access_token", "device_id", "entry_id"}
    return {
        "entry": async_redact_data(entry.as_dict(), to_redact),
        "device_info": async_redact_data(
            coordinator.device.get_diagnostics(), to_redact
        ),
    }
