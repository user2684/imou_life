"""Test imou_life config flow."""
from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.imou_life.const import (
    CONF_API_URL,
    CONF_APP_ID,
    CONF_APP_SECRET,
    CONF_DEVICE_ID,
    DOMAIN,
    OPTION_API_TIMEOUT,
    OPTION_CALLBACK_URL,
    OPTION_SCAN_INTERVAL,
)

from .const import (
    CONF_DISCOVERED_DEVICE,
    MOCK_CONFIG_ENTRY,
    MOCK_CREATE_ENTRY_FROM_DISCOVER,
    MOCK_CREATE_ENTRY_FROM_MANUAL,
    MOCK_LOGIN_WITH_DISCOVER,
    MOCK_LOGIN_WITHOUT_DISCOVER,
)


# This fixture bypasses the actual setup of the integration
@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch(
        "custom_components.imou_life.async_setup",
        return_value=True,
    ), patch(
        "custom_components.imou_life.async_setup_entry",
        return_value=True,
    ):
        yield


@pytest.mark.asyncio
async def test_discover_ok(hass, api_ok):
    """Test discover flow: ok."""
    # Initialize a config flow as the user is clicking on add new integration
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    # Check that the config flow shows the login form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "login"
    # simulate the user entering app id, app secret and discover checked
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_LOGIN_WITH_DISCOVER
    )
    # ensure a new form is requested
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    # get the next step in the flow
    next(
        flow
        for flow in hass.config_entries.flow.async_progress()
        if flow["flow_id"] == result["flow_id"]
    )
    # ensure it is the discover step
    assert result["step_id"] == "discover"
    # submit the discover form
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CREATE_ENTRY_FROM_DISCOVER
    )
    # check that the config flow is complete and a new entry is created
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["data"][CONF_API_URL] == MOCK_LOGIN_WITH_DISCOVER[CONF_API_URL]
    assert result["data"][CONF_APP_ID] == MOCK_LOGIN_WITH_DISCOVER[CONF_APP_ID]
    assert result["data"][CONF_APP_SECRET] == MOCK_LOGIN_WITH_DISCOVER[CONF_APP_SECRET]
    assert (
        result["data"][CONF_DEVICE_ID]
        == MOCK_CREATE_ENTRY_FROM_DISCOVER[CONF_DISCOVERED_DEVICE]
    )
    assert result["result"]


@pytest.mark.asyncio
async def test_login_error(hass, api_invalid_app_id):
    """Test config flow: invalid app id."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_LOGIN_WITH_DISCOVER
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "invalid_configuration"}


@pytest.mark.asyncio
async def test_manual_ok(hass, api_ok):
    """Test manual flow: ok."""
    # Initialize a config flow as the user is clicking on add new integration
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    # Check that the config flow shows the login form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "login"
    # simulate the user entering app id, app secret and discover checked
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_LOGIN_WITHOUT_DISCOVER
    )
    # ensure a new form is requested
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    # get the next step in the flow
    next(
        flow
        for flow in hass.config_entries.flow.async_progress()
        if flow["flow_id"] == result["flow_id"]
    )
    # ensure it is the discover step
    assert result["step_id"] == "manual"
    # submit the discover form
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CREATE_ENTRY_FROM_MANUAL
    )
    # check that the config flow is complete and a new entry is created
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["data"][CONF_API_URL] == MOCK_LOGIN_WITHOUT_DISCOVER[CONF_API_URL]
    assert result["data"][CONF_APP_ID] == MOCK_LOGIN_WITHOUT_DISCOVER[CONF_APP_ID]
    assert (
        result["data"][CONF_APP_SECRET] == MOCK_LOGIN_WITHOUT_DISCOVER[CONF_APP_SECRET]
    )
    assert (
        result["data"][CONF_DEVICE_ID] == MOCK_CREATE_ENTRY_FROM_MANUAL[CONF_DEVICE_ID]
    )
    assert result["result"]


@pytest.mark.asyncio
async def test_options_flow(hass):
    """Test an options flow."""
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG_ENTRY, entry_id="test")
    entry.add_to_hass(hass)
    # Initialize an options flow
    await hass.config_entries.async_setup(entry.entry_id)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    # Verify that the first options step is a user form
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "init"
    # Enter some fake data into the form
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            OPTION_SCAN_INTERVAL: 30,
            OPTION_API_TIMEOUT: "20",
            OPTION_CALLBACK_URL: "url",
        },
    )
    # Verify that the flow finishes
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    # Verify that the options were updated
    assert entry.options[OPTION_SCAN_INTERVAL] == 30
    assert entry.options[OPTION_API_TIMEOUT] == "20"
    assert entry.options[OPTION_CALLBACK_URL] == "url"
