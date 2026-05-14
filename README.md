# BenQ Infrared (Home Assistant Custom Integration)

Home Assistant custom integration for controlling BenQ projectors through the `infrared` integration (tested for Power with a TK700, and using W1070 codes for other features).

## Features

- Config flow setup from the UI
- Media player entity for projector-style controls
- Button entities for direct IR actions
- Power On/Off buttons enabled by default; additional buttons are created disabled by default and can be enabled in the entity registry
- Uses `infrared-protocols` command definitions

## Installation with HACS

[![Open your Home Assistant instance and open this repository inside Home Assistant Community Store](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=johannrichard&repository=hacs-benq-infrared&category=integration)

## Manually install the Home Assistant integration in HACS

1. Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.
2. Open **HACS -> Integrations -> ... -> Custom repositories**.
3. Add `https://github.com/johannrichard/hacs-benq-infrared` as **Integration**.
4. Install and restart Home Assistant.

## Configuration

1. Go to **Settings -> Devices & Services -> Add Integration**.
2. Search for **BenQ Infrared**.
3. Select your existing `infrared` emitter entity.
4. Finish the config flow.

## Requirements

- Home Assistant with the built-in `infrared` integration configured
- A compatible IR blaster/emitter entity

## Development

The integration code is under:

- `custom_components/benq_infrared/`

## Support

- Issues: <https://github.com/johannrichard/hacs-benq-infrared/issues>
