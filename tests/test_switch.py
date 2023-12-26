"""Test imou_life switch."""
from unittest.mock import patch

from homeassistant.components.switch import SERVICE_TURN_OFF, SERVICE_TURN_ON
from homeassistant.const import ATTR_ENTITY_ID
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.imou_life.const import DOMAIN

from .const import MOCK_CONFIG_ENTRY


# This fixture bypasses the actual setup of the integration
@pytest.fixture(autouse=True)
def bypass_added_to_hass():
    """Prevent added to hass."""
    with patch(
        "custom_components.imou_life.entity.ImouEntity.async_added_to_hass",
        return_value=True,
    ), patch(
        "custom_components.imou_life.entity.ImouEntity.async_will_remove_from_hass",
        return_value=True,
    ):
        yield


@pytest.mark.asyncio
async def test_switch(hass, api_ok):
    """Test switch services."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG_ENTRY, entry_id="test"
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    # check if the turn_on function is called when turning on the switch
    with patch(
        "custom_components.imou_life.switch.ImouSwitch.entity_registry_enabled_default",
        return_value=True,
    ), patch(
        "custom_components.imou_life.entity.ImouEntity.available",
        return_value=True,
    ), patch(
        "imouapi.device_entity.ImouSwitch.async_turn_on"
    ) as turn_on_func:
        await hass.services.async_call(
            "switch",
            SERVICE_TURN_ON,
            service_data={ATTR_ENTITY_ID: "switch.device_name_motiondetect"},
            blocking=True,
        )
    assert turn_on_func.called
    # check if the turn_off function is called when turning off the switch
    with patch(
        "custom_components.imou_life.switch.ImouSwitch.entity_registry_enabled_default",
        return_value=True,
    ), patch(
        "custom_components.imou_life.entity.ImouEntity.available",
        return_value=True,
    ), patch(
        "imouapi.device_entity.ImouSwitch.async_turn_off"
    ) as turn_off_func:
        await hass.services.async_call(
            "switch",
            SERVICE_TURN_OFF,
            service_data={ATTR_ENTITY_ID: "switch.device_name_motiondetect"},
            blocking=True,
        )
    assert turn_off_func.called
