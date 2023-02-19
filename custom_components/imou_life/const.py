"""Constants."""
# Internal constants
DOMAIN = "imou_life"
PLATFORMS = ["switch", "sensor", "binary_sensor", "select", "button", "siren", "camera"]

# Configuration definitions
CONF_API_URL = "api_url"
CONF_DEVICE_NAME = "device_name"
CONF_APP_ID = "app_id"
CONF_APP_SECRET = "app_secret"
CONF_ENABLE_DISCOVER = "enable_discover"
CONF_DISCOVERED_DEVICE = "discovered_device"
CONF_DEVICE_ID = "device_id"

OPTION_SCAN_INTERVAL = "scan_interval"
OPTION_API_TIMEOUT = "api_timeout"
OPTION_CALLBACK_URL = "callback_url"
OPTION_API_URL = "api_url"
OPTION_CAMERA_WAIT_BEFORE_DOWNLOAD = "camera_wait_before_download"
OPTION_WAIT_AFTER_WAKE_UP = "wait_after_wakeup"

SERVIZE_PTZ_LOCATION = "ptz_location"
SERVIZE_PTZ_MOVE = "ptz_move"
ATTR_PTZ_HORIZONTAL = "horizontal"
ATTR_PTZ_VERTICAL = "vertical"
ATTR_PTZ_ZOOM = "zoom"
ATTR_PTZ_OPERATION = "operation"
ATTR_PTZ_DURATION = "duration"

# Defaults
DEFAULT_SCAN_INTERVAL = 15 * 60
DEFAULT_API_URL = "https://openapi.easy4ip.com/openapi"

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
    "linkagewhitelight",
    "pushNotifications",
]

# cameras which are enabled by default
ENABLED_CAMERAS = [
    "camera",
]

# icons of the sensors
SENSOR_ICONS = {
    "__default__": "mdi:bookmark",
    # sensors
    "lastAlarm": "mdi:timer",
    "storageUsed": "mdi:harddisk",
    "callbackUrl": "mdi:phone-incoming",
    "status": "mdi:lan-connect",
    "battery": "mdi:battery",
    # binary sensors
    "online": "mdi:check-circle",
    "motionAlarm": "mdi:motion-sensor",
    # select
    "nightVisionMode": "mdi:weather-night",
    # switches
    "motionDetect": "mdi:motion-sensor",
    "headerDetect": "mdi:human",
    "abAlarmSound": "mdi:account-voice",
    "breathingLight": "mdi:television-ambient-light",
    "closeCamera": "mdi:sleep",
    "linkDevAlarm": "mdi:bell",
    "whiteLight": "mdi:light-flood-down",
    "smartTrack": "mdi:radar",
    "linkagewhitelight": "mdi:light-flood-down",
    "pushNotifications": "mdi:webhook",
    # buttons
    "restartDevice": "mdi:restart",
    "refreshData": "mdi:refresh",
    "refreshAlarm": "mdi:refresh",
    # sirens
    "siren": "mdi:alarm-light",
    # cameras
    "camera": "mdi:video",
    "cameraSD": "mdi:video",
}
