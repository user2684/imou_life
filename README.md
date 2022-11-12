# Home Assistant custom component for controlling Imou devices

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Donate](https://img.shields.io/badge/donate-BuyMeCoffee-yellow.svg)](https://www.buymeacoffee.com/user2684)

This Home Assistant component helps in interacting with devices registered with the Imou Life App and specifically enabling/disabling motion detection, siren, and other switches.

Despite Imou webcams video streams can be integrated in Home Assistant through Onvif, the only way to interact with the device as if using the Imou Life App is to leverage the Imou API,
that is what this component under the hood does.

Once an Imou device is added to Home Assistant, switches can be controlled through the frontend or convenientely used in your automations.

## Features

- Configuration through the UI
- Auto discover registered devices
- Auto discover device capabilities and supported switches
- Sensors, binary sensors and select to control key features of each device

## Installation

### [HACS](https://hacs.xyz/) (recommended)

Installation can be done through [HACS custom repository](https://hacs.xyz/docs/faq/custom_repositories).

### Manual installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `imou_life`.
4. Download _all_ the files from the `custom_components/imou_life/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant

This integration depends on the library `imouapi` for interacting with the end device. The library should be installed automatically by Home Assistante when initializing the integration.
If this is not happening, install it manually with:

```
pip3 install imouapi
```

## Requirements

To interact with Imou API, valid `App Id` and `App Secret` are **required**.

In order to get them:

- Register an account on Imou Life if not done already
- Register a developer account on [https://open.imoulife.com](https://open.imoulife.com)
- Open the Imou Console at [https://open.imoulife.com/consoleNew/myApp/appInfo](https://open.imoulife.com/consoleNew/myApp/appInfo)
  - Go to "My App", "App Information" and click on Edit
  - Fill in the required information and copy your AppId and AppSecret

## Configuration

The configuration of the component is done entirely through the UI.

1. In the Home Assistant UI to "Configuration" -> "Integrations" click "+" and search for "Imou Life"
1. Fill in `App Id` and `App Secret`
   1. If `Discover registered devices` is selected:
      - A list of all the devices associated with your account is presented
      - Select the device you want to add
      - Optionally provide a name (otherwise the same name used in Imou Life will be used)
   1. If `Discover registered devices` is NOT selected:
      - Provide the Device ID of the device you want to add
      - Optionally provide a name (otherwise the same name used in Imou Life will be used)

Once done, you should see the integration added to Home Assistant, a new device and a few entities associated with it.

The following entities are created (if supported by the device):

- Switches:
  - All of those supported by the remote device
  - Push notifications (see below)
- Sensor:
  - Time of the last alarm
  - Storage Used
- Binary Sensor:
  - Online
- Select:
  - Night Vision Mode

If you need to add another device, repeat the process above.

## Push Notifications

Upon an event occurs (e.g. alarm, device offline, etc.) a realtime notification can be sent by the Imou API directly to your Home Assistance instance so you can immediately react upon it.
Since this is happening via a direct HTTP call to your instance, your Home Assistance must be [exposed to the Internet](https://www.home-assistant.io/docs/configuration/remote/) as a requirement.
Please note, for Imou API, push notification is a global configuration, not per device, meaning once enabled on one device it applies to ALL devices registered in your Imou account.
To enable push notifications:

- Ensure Home Assistant is exposed over the Internet and you have implemented the [security checklists](https://www.home-assistant.io/docs/configuration/securing/)
- In Home Assistant, add at least a device through the Imou Life integration
- Go to "Settings", "Devices & Services", select your Imou Life integration and click on "Configure"
- In the "Callback Webhook ID" add in a random string difficult to guess such as `imou_life_callback_123jkls` and save. This will be name of the webhook which will be called when an event occurs.
- Visit the Device page, you should see a "Push Notifications" switch
- Enable the switch. Please remember this is a global configuration, you just need to do it once and on a SINGLE device only
- Go to "Settings", "Automation & Scenes" and click on "Create Auitomation". Select "Start with an empty automation"
- In Triggers, click on "Add Trigger" and select "Webhook". In Webhook ID write down the webhook ID previously configured (e.g. `imou_life_callback_123jkls`)
- Save the automation. The Imou API will call this webhook so triggering the automation upon each event
- Make the device firing an event and review in "Traces" if it has triggered and which data has been passed along in "Changed Variables"
- Refine your automation. you can then react based on the data passed along in `trigger.json`

Please note that:

- Imou API documentation details both [the type of the messages](https://open.imoulife.com/book/push/alarm.html) you can receive as well as their [formats](https://open.imoulife.com/book/push/event.html). However reviewing the automation traces could be a quicker and easier way to understand which information you are receiving
- If the integration struggles in identifying the external URL of your Home Assisstance instance or you want use a custom url, provide the full url to use in "Options", "Callback Full URL". When a callback full urls is set, any webhook ID is ignored
- The API for enabling/disabling push notification is currently limited to 10 times per day by Imou so do not perform too many consecutive changes
- In Home Assistant you cannot have more than one webhook trigger with the same ID

## Options

The following options can be customized through the UI by clicking on the "Configure" link:

- Polling interval - how often to refresh the data (in seconds, default 15 minutes)
- API Base URL - th url of the Imou Life API (default https://openapi.easy4ip.com/openapi)
- API Timeout - API call timeout in seconds (default 10 seconds)
- Callback Webhook ID - when push notifications are enabled, the webhook ID which will be used in automation
- Callback Full URL - when push notifications are enabled, full url to use as a callback. Takes precedence over any configured webhook ID

## Limitations / Known Issues

- The Imou API does not provide a stream of configuration events, for this reason the component periodically polls the devices, meaning if you change anything from the Imou Life App, it could take a few minutes to be updated in HA
- For every new device to be added, AppId and AppSecret are requested
- Advanced options can be changed only after having added the device
- Push notifications are not working, investigation is in progress

## Troubleshooting

If anything fails, you should find the error message and the full stack trace on your Home Assistant logs. This can be helpful for either troubleshoot the issue or reporting it.
Diagnostics information is as well provided by visiting the device page in Home Assistant and clicking on "Download Diagnostics".

To gain more insights on what the component is doing or why is failing, you can enable debug logging:

```
logger:
  default: info
  logs:
    custom_components.imou_life: debug
```

Since this integration depends on the library `imouapi` for interacting with the end device, you may want to enable debug level logging to the library itself:

```
logger:
  default: info
  logs:
    custom_components.imou_life: debug
    imouapi: debug
```

## Bugs or feature requests

Bugs and feature requests can be reported through Github Issues.
When reporting bugs, ensure to include also diagnostics and debug logs. Please review those logs to redact any potential sensitive information before submitting the request.
