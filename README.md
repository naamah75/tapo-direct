# Tapo Direct

Experimental Home Assistant custom integration for TP-Link Tapo bulbs that work with a direct **KLAP v2 / HTTP port 80** connection but cannot be configured through normal discovery.

The integration uses its own `tapo_direct` domain and never replaces Home Assistant’s built-in `tplink` integration.

## Supported features

- Direct host and TP-Link credential configuration
- Local polling through `python-kasa`
- On/off, brightness, HS color and color temperature
- Safe diagnostics with sensitive data redacted
- One automatic reconnect attempt after a transport failure

Initially developed and tested with a **Tapo L530** using KLAP v2 over HTTP port 80. Other models are not guaranteed to work.

## Installation with HACS

1. Open HACS → Integrations → Custom repositories.
2. Add `https://github.com/naamah75/tapo-direct` as category **Integration**.
3. Install **Tapo Direct**.
4. Restart Home Assistant when HACS requests it and the owner authorizes it.
5. Open Settings → Devices & services → Add integration → Tapo Direct.
6. Enter the bulb IP address and TP-Link/Tapo account credentials.

## Avoiding duplicate entities

Do not configure the same bulb simultaneously in both `tplink` and `tapo_direct`. The separate domain prevents overwriting Core, but duplicate entities could control the same physical device.

## Rollback

1. Remove the Tapo Direct config entry.
2. Uninstall Tapo Direct from HACS.
3. Restart Home Assistant only if requested and authorized.
4. Optionally remove the custom repository from HACS.

Removing this integration does not modify the built-in `tplink` integration.

## Security

Credentials remain in the Home Assistant config entry. Diagnostics redact host, username, password, device ID, MAC address, SSID and network identifiers.

## Disclaimer

This project is not affiliated with TP-Link or Home Assistant.
