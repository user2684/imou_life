"""Test imou setup process."""
from homeassistant.exceptions import ConfigEntryNotReady
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.imou_life import (
    async_reload_entry,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.imou_life.const import DOMAIN
from custom_components.imou_life.coordinator import ImouDataUpdateCoordinator

from .const import MOCK_CONFIG_ENTRY


async def test_setup_unload_and_reload_entry(hass, api_ok):
    """Test entry setup and unload."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG_ENTRY, entry_id="test"
    )
    # test setup entry
    assert await async_setup_entry(hass, config_entry)
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(
        hass.data[DOMAIN][config_entry.entry_id], ImouDataUpdateCoordinator
    )

    # Reload the entry and assert that the data from above is still there
    assert await async_reload_entry(hass, config_entry) is None
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(
        hass.data[DOMAIN][config_entry.entry_id], ImouDataUpdateCoordinator
    )

    # Unload the entry and verify that the data has been removed
    assert await async_unload_entry(hass, config_entry)
    assert config_entry.entry_id not in hass.data[DOMAIN]


async def test_setup_entry_exception(hass, api_invalid_data):
    """Test ConfigEntryNotReady when API raises an exception during entry setup."""
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG_ENTRY, entry_id="test"
    )

    # In this case we are testing the condition where async_setup_entry raises ConfigEntryNotReady
    with pytest.raises(ConfigEntryNotReady):
        assert await async_setup_entry(hass, config_entry)
