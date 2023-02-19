# Changelog

## [1.0.13] (2023-02-19)
### Added
- Added battery sensor for dormant devices
- Catalan translation
### Changed
- Added new conditions to the Imou Push Notifications automation template in the README file to prevent too many refresh
### Fixed
- Motion detection sensor now showing up for all devices

## [1.0.12] (2022-12-11)
### Fixed
- Dormant device logic

## [1.0.11] (2022-12-11)
### Added
- Support for dormant devices
- `status` sensor
- Options for customizing wait time for camera snapshot download and wait time after waking up dormant device
### Changed
- Device is now marked online if either online or dormant

## [1.0.10] (2022-12-04)
### Added
- Camera entity now supports snapshots and video streaming

## [1.0.9] (2022-11-26)
### Added
- PTZ Support, exposed as `imou_life.ptz_location` and `imou_life.ptz_move` services
- Camera entity, used for invoking the PTZ services

## [1.0.8] (2022-11-21)
### Fixed
- "Failed to setup" error after upgrading to v1.0.7 (#37)

## [1.0.7] (2022-11-20)
### Added
- Spanish and italian translations (#21)
- Reverse proxy sample configuration for custom configuration of push notifications (#29)
- Siren entity (#26)
### Changed
- API URL is now part of the configuration flow (#16)
- Bump imouapi version: 1.0.6 → 1.0.7
### Removed
- `siren` switch, now exposed as a siren entity
- API Base URL option, now part of the configuration flow
### Fixed
- Entities not correctly removed from HA

## [1.0.6] (2022-11-19)
### Added
- `motionAlarm` binary sensor which can be updated also via the `refreshAlarm` button
### Removed
- `lastAlarm` sensor. The same information has been moved into the `alarm_time` attribute inside the `motionAlarm` binary sensor, together with `alarm_type` and  `alarm_code`
### Changed
- Bump imouapi version: 1.0.5 → 1.0.6
- Updated README and link to the roadmap

## [1.0.5] (2022-11-13)
### Added
- Switch for turning the Siren on/off for those devices supporting it
- Buttons for restarting the device and manually refreshing device data in Home Assistant
- Sensor with the callback url set for push notifications
### Changed
- Bump imouapi version: 1.0.5 → 1.0.5
- Reviewed instructions for setting up push notifications
- Updated README with Roadmap
- Deprecated "Callback Webhook ID" option for push notifications, use "Callback URL" instead
- Reviewed switches' labels
### Fixed
- Storage left sensor without SD card now reporting Unknown

## [1.0.4] (2022-11-12)
### Added
- Brazilian Portuguese Translation
- HACS Default repository
### Changed
- Split Github action into test (on PR and push) and release (manual)

## [1.0.3] (2022-10-23)
### Added
- Support white light on motion switch through imouapi
- `linkagewhitelight` now among the switches enabled by default
- Support for SelectEntity and `nightVisionMode` select
- Support storage used through `storageUsed` sensor
- Support for push notifications through `pushNotifications` switch
- Options for configuring push notifications
### Changed
- Bump imouapi version: 1.0.2 → 1.0.4
- Redact device id and entry id from diagnostics

## [1.0.2] (2022-10-19)
### Changed
- Bump imouapi version: 1.0.1 → 1.0.2

## [1.0.1] (2022-10-16)
### Added
- Download diagnostics capability

## [1.0.0] (2022-10-15)
### Changed
- Bump imouapi version: 0.2.2 → 1.0.0
- Entity ID names are now based on the name of the sensor and not on the description

## [0.1.4] (2022-10-08)
### Added
- Test suite
### Changed
- Bump imouapi version: 0.2.1 → 0.2.2

## [0.1.3] (2022-10-04)
### Changed
- Bump imouapi version: 0.2.0 → 0.2.1

## [0.1.2] (2022-10-03)
### Added
- All the switches are now made available. Only a subset are then enabled in HA by default.
- Sensors' icons and default icon
### Changed
- Bump imouapi version: 0.1.5 → 0.2.0 and adapted the code accordingly
- Introduced `ImouEntity` class for all the sensors derived subclasses

## [0.1.1] (2022-09-29)
### Changed
- Bump imouapi version: 0.1.4 → 0.1.5
- Improved README

## [0.1.0] (2022-09-29)
### Added
- First release for beta testing
