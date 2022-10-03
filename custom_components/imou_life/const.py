"""Constants."""
# Internal constants
DOMAIN = "imou_life"
PLATFORMS = ["switch", "sensor", "binary_sensor"]

# Configuration definitions
CONF_DEVICE_NAME = "device_name"
CONF_APP_ID = "app_id"
CONF_APP_SECRET = "app_secret"
CONF_ENABLE_DISCOVER = "enable_discover"
CONF_DISCOVERED_DEVICE = "discovered_device"
CONF_DEVICE_ID = "device_id"
OPTION_SCAN_INTERVAL = "scan_interval"
OPTION_API_URL = "api_url"
OPTION_API_TIMEOUT = "api_timeout"

# Scan interval
DEFAULT_SCAN_INTERVAL = 15 * 60

# switches which are enabled by default
ENABLED_SWITCHES = [
    "motionDetect",
    "headerDetect",
    "abAlarmSound",
    "breathingLight",
    "closeCamera",
    "linkDevAlarm",
    "whiteLight",
    "smartTrack",
]

# icons of the sensors
SENSOR_ICONS = {
    "__default__": "mdi:bookmark",
    "online": "mdi:lan-connect",
    "lastAlarm": "mdi:timer",
    "motionDetect": "mdi:motion-sensor",
    "headerDetect": "mdi:human",
    "abAlarmSound": "mdi:account-voice",
    "breathingLight": "mdi:television-ambient-light",
    "closeCamera": "mdi:sleep",
    "linkDevAlarm": "mdi:bell",
    "whiteLight": "mdi:light-flood-down",
    "smartTrack": "mdi:radar",
}
