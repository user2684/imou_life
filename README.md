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
- Sensors, binary sensors, select, buttons to control key features of each device
- Support for push notifications
- PTZ controls

## Installation

### [HACS](https://hacs.xyz/) (recommended)

After installing and configuring HACS, go to "Integrations", "Explore & Download Repositories", search for "Imou Life" and download the integration.

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

To interact with the Imou API, valid `App Id` and `App Secret` are **required**.

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
  - Enable/disable push notifications
- Sensors:
  - Storage Used on SD card
  - Callback URL used for push notifications
- Binary Sensors:
  - Online
  - Motion alarm
- Select:
  - Night Vision Mode
- Buttons:
  - Restart device
  - Refresh all data
  - Refresh motion alarm sensor

If you need to add another device, repeat the process above.

### Advanced Options

The following options can be customized through the UI by clicking on the "Configure" link:

- Polling interval - how often to refresh the data (in seconds, default 15 minutes)
- API Base URL - th url of the Imou Life API (default https://openapi.easy4ip.com/openapi)
- API Timeout - API call timeout in seconds (default 10 seconds)
- Callback URL - when push notifications are enabled, full url to use as a callback for push notifications

### Motion Detection

When adding a new device, a `Motion Alarm` binary sensor is created (provided your device supports motion detection). You can use it for building your automations, when its state changes, like any other motion sensors you are already familiar with.
There are multiple options available to keep the motion alarm sensor regularly updated, described below. All the options will update the same "Motion Alarm" sensor, just the frequency changes depending on the option. Option 1 and 2 does not require Home Assistant to be exposed over the Internet, Option 3 does but ensure realtime updates of the sensor.

#### Option 1

If you do nothing, by default the sensor will be updated every 15 minutes, like any other sensor of the device. If a motion is detected, the sensor triggers and it will get back to a "Clear" state at the next update cycle (e.g. after other 15 minutes)

#### Option 2

If you want to increase the frequency, you can force an update of the "Motion Alarm" sensor state manually or automatically, through the "Refresh Alarm" button which is created in the same device.
For example, you can create an automation like the below which press every 30 seconds the "Refresh Alarm" button for you, causing an update of the "Motion Alarm" sensor state (replace `button.webcam_refreshalarm` with the name of your entity):

```
alias: Imou - Refresh Alarm
description: ""
trigger:
  - platform: time_pattern
    seconds: "30"
condition: []
action:
  - service: button.press
    data: {}
    target:
      entity_id: <button.webcam_refreshalarm>
mode: single
```

Please note, the underlying Imou API is limited to 20000 calls per day.

#### Option 3

If you want relatime updates of the "Motion Alarm" sensor, you need to enable push notifications. In this scenario, upon an event occurs (e.g. alarm, device offline, etc.) a realtime notification is sent by the Imou API directly to your Home Assistance instance so you can immediately react upon it.
Since this is happening via a direct HTTP call to your instance, your Home Assistance must be [exposed to the Internet](https://www.home-assistant.io/docs/configuration/remote/) as a requirement.
Please note, push notification is a global configuration, not per device, meaning once enabled on one device it applies to ALL devices registered in your Imou account.

**Requirements**

- Home Assistant exposed to the Internet
- Home Assistant behind a reverse proxy, due to malformed requests sent by the Imou API (see below for details and examples)

**Configuration**

- Ensure Home Assistant is exposed over the Internet, is behind a reverse proxy, and you have implemented the [security checklists](https://www.home-assistant.io/docs/configuration/securing/)
- In Home Assistant, add at least a device through the Imou Life integration
- Go to "Settings", "Devices & Services", select your Imou Life integration and click on "Configure"
- In "Callback URL" add the external URL of your Home Assistant instance, followed by `/api/webhook/`, followed by a random string difficult to guess such as `imou_life_callback_123jkls` and save. For example `https://yourhomeassistant.duckdns.org/api/webhook/imou_life_callback_123jkls`. This will be name of the webhook which will be called when an event occurs.
- Visit the Device page, you should see a "Push Notifications" switch
- Enable the switch. Please remember **this is a global configuration, you just need to do it once** and in a SINGLE device only
- Go to "Settings", "Automation & Scenes" and click on "Create Automation" and select "Start with an empty automation"
- Click the three dots in the top-right of the screen, select "Edit in YAML", copy, paste the following and replace `<your_string_difficult_to_guess>` with yours (e.g. `imou_life_callback_123jkls`) and save it:

```
alias: Imou Push Notifications
description: "Handle Imou push notifications by requesting to update the Motion Alarm sensor of the involved device (v1)"
trigger:
  - platform: webhook
    webhook_id: <your_string_difficult_to_guess>
condition:
  - condition: template
    value_template: |
      {% for entity_name in integration_entities("imou_life") %}
        {%- if entity_name is match('.+_refreshalarm$') and is_device_attr(entity_name, "hw_version", trigger.json.did) %}
          true
        {%-endif%}
        {% else %}
          false
      {%- endfor %}
action:
  - service: button.press
    data: {}
    target:
      entity_id: |
        {% for entity_name in integration_entities("imou_life") %}
          {%- if entity_name is match('.+_refreshalarm$') and is_device_attr(entity_name, "hw_version", trigger.json.did) %}
            {{entity_name}}
          {%-endif%}
        {%- endfor %}
    enabled: true
mode: queued
max: 10
```

When using this option, please note the following:

- The API for enabling/disabling push notification is currently limited to 10 times per day by Imou so do not perform too many consecutive changes. Keep also in mind that if you change the URL, sometimes it may take up to 5 minutes for a change to apply on Imou side
- In Home Assistant you cannot have more than one webhook trigger with the same ID so customize the example above if you need to add any custom logic
- Unfortunately HTTP requests sent by the Imou API server to Home Assistant are somehow malformed, causing HA to reject the request (404 error, without any evidence in the logs). A reverse proxy like NGINX in front of Home Assistant without any special configuration takes care of cleaning out the request, hence this is a requirement.

**Reverse Proxy Configuration**

If running Home Assistant in Supervised mode, you can install and configure the "Nginx Proxy Manager Add-on" which has been tested and works fine.
Please note "NGINX Home Assistant SSL proxy Addon" instead is not able to handle the malformed requests sent by Imou.

If you are instead using a custom nginx proxy, the following is a sample configuration `nginx.conf` file you can use. Please note before using it:

- Replace `<home_assistant_ip>` with the IP address of your Home Assistance instance
- If using SSL:
  - Uncomment the commented lines
  - Place your certificate, private key and dhparms files in a directory accessible by nginx (`/ssl` in the example below)
  - If you don't have a dhparms file, generate one by running `openssl dhparam -dsaparam -out dhparams.pem 4096 > /dev/null`
- If serving multiple domains, customize the `server_name` directive. In this case, ensure there is no other server block with a catchall `server_name _` directive otherwise the malformed requests sent by Imou will be routed somewhere else
- If you need to debug the incoming requests, change `access_log /dev/stdout info` into `access_log /dev/stdout debug` and you will see the content of any POST requests

```
user  nginx;
worker_processes  auto;

error_log  stderr;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server_tokens off;
    server_names_hash_bucket_size 64;
    log_format  info  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    log_format debug '[$time_local] "$request" "$status" "$request_body"';

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    server {
        server_name _;
        ssl_session_timeout 1d;
        ssl_session_cache shared:MozSSL:10m;
        ssl_session_tickets off;
        #ssl_certificate /ssl/fullchain.pem;
        #ssl_certificate_key /ssl/privkey.pem;
        #ssl_dhparam /ssl/dhparams.pem;

        #listen 443 ssl http2;
        listen 80;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        proxy_buffering off;

        location /{
            access_log /dev/stdout info;
            proxy_pass http://<home_assistant_ip>:8123/;
            proxy_set_header Host $host;
            proxy_redirect http:// https://;
            proxy_http_version 1.1;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }

    }

}
```

### PTZ Controls

The integration exposes two services for interacting with the PTZ capabilities of the device:

- `imou_life.ptz_location`: if the device supports PTZ, you will be able to move it to a specified location by providing horizontal (between -1 and 1), vertical (between -1 and 1) and zoom (between 0 and 1)
- `imou_life.ptz_move` If the device supports PTZ, you will be able to move it around by providing an operation (one of "UP", "DOWN", "LEFT", "RIGHT", "UPPER_LEFT", "BOTTOM_LEFT", "UPPER_RIGHT", "BOTTOM_RIGHT", "ZOOM_IN", "ZOOM_OUT", "STOP") and a duration for the operation (in milliseconds)

Those services can be invoked on the camera entity.
To test this capability, in Home Assistant go to "Developer Tools", click on "Services", select one of the services above, select the target entity, provide the required information and click on "Call Service". If something will go wrong, have a look at the logs.

Presets are instead not apparently supported by the Imou APIs but could be implemented by combining HA scripts and calls to the `imou_life.ptz_location` service.

## Limitations / Known Issues

- The Imou API does not provide a stream of configuration events, for this reason the component periodically polls the devices, meaning if you change anything from the Imou Life App, it could take a few minutes to be updated in HA. Use the "Refresh Data" button to refresh data for all the devices' sensors
- For every new device to be added, AppId and AppSecret are requested
- Advanced options can be changed only after having added the device
- Due to malformed requests sent by the Imou API server, in order for push notifications to work, Home Assistant must be behind a reverse proxy

## Troubleshooting

If anything fails, you should find the error message and the full stack trace on your Home Assistant logs. This can be helpful for either troubleshoot the issue or reporting it.

### Device Diagnostics

Diagnostics information is provided by visiting the device page in Home Assistant and clicking on "Download Diagnostics".

### Debugging

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

Bugs and feature requests can be reported through [Github Issues](https://github.com/user2684/imou_life/issues).
When reporting bugs, ensure to include also diagnostics and debug logs. Please review those logs to redact any potential sensitive information before submitting the request.

## Roadmap

A high level roadmap of this integration can be found [here](https://github.com/users/user2684/projects/1)
