# EVN Power Insights for Home Assistant

English | [Tiếng Việt](README.md)

This integration fetches EVN electricity consumption data per region and exposes it in Home Assistant via sensors. It supports UI setup and automatically detects the EVN company based on the customer ID.

## Features
- Track multiple customer IDs on one HA instance.
- Automatic EVN branch detection.
- Energy-compliant sensor (total energy) for Energy Dashboard.
- Supports all EVN regions (subject to EVN data availability).

## Requirements
- Home Assistant 2022.7.0 or newer.
- Smart meter with daily remote readings.
- Valid EVN account (username/password).

## Installation
### HACS (recommended)
1. HACS → Integrations → Explore & download repositories.
2. Search `EVN Power Insights` → Download.
3. Restart Home Assistant.

### Manual
1. Copy `custom_components/evn_power_insights` into your HA `custom_components` directory.
2. Restart Home Assistant.

## Setup
1. Settings → Devices & Services → Add Integration → `EVN Power Insights`.
2. Enter `Customer ID` (starts with `P`, 11–13 chars).
3. Confirm detected EVN branch.
4. Enter `Username`, `Password`, and `Billing start date`.

## Sensors and Energy Dashboard
The only sensor kept for Energy Dashboard:
- `Total energy` (Energy compliant)

Add to Energy Dashboard:
1. Settings → Energy → Add consumption.
2. Choose `Total energy` (kWh) entity.

## Limitations
- Data updates are periodic, not real-time.

## Support
Please open an issue or follow guidance in `SECURITY.md`.

## References
- https://github.com/trvqhuy/nestup_evn/tree/main
