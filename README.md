# Home Assistant custom component for controlling Imou devices

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
pip install imouapi
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

The following entities are created:

- Switches (only if supported by the remote device):
  - Motion detection
  - Head detection (Human detection)
  - Abnormal alarm sound
  - Breathing light (indicator light)
- Sensor:
  - Time of the last alarm
- Binary Sensor:
  - Online

If you need to add another device, repeat the process above.

## Advanced Options

The following options can be customized through the UI by clicking on the "Configure" link:

- Polling interval (seconds) - default 15 minutes
- API Base URL - default https://openapi.easy4ip.com/openapi
- API Timeout - default 10 seconds

## Limitations

- The Imou API does not provide a stream of configuration events, for this reason the component periodically polls the devices, meaning if you change anything from the Imou Life App, it could take a few minutes to be updated in HA

## Troubleshooting

If anything fails, you should find the error message and the full stack trace on your Home Assistant logs. This can be helpful for either troubleshoot the issue or reporting it.
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
