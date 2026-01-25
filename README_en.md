# EVN Power Insights for Home Assistant

English | [Tiếng Việt](README.md)

This integration fetches EVN electricity consumption data per region and exposes it in Home Assistant via sensors. It supports UI setup and automatically detects the EVN company based on the customer ID.

## Features
- Track multiple customer IDs on one HA instance.
- Automatic EVN branch detection.
- Energy sensor based on meter timestamp for Energy Dashboard.
- Supports 5 EVN companies: EVNHANOI, EVNHCMC, EVNNPC, EVNCPC, EVNSPC.

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
2. Enter `Customer ID` (11–13 chars, usually starts with `P`).
3. Confirm detected EVN branch.
4. Enter `Username`, `Password`, and `Billing start date` (only required for some regions; e.g. EVNCPC does not need it).

## Sensors and Energy Dashboard
The only sensor kept for Energy Dashboard:
- `EVN Energy (theo thoi diem do)` (Energy compliant)

Add to Energy Dashboard:
1. Settings → Energy → Add consumption.
2. Choose `EVN Energy (theo thoi diem do)` (kWh) entity.

## Limitations
- Data updates are periodic (default 3 hours), not real-time.
- Energy date is recorded based on meter time when available.

## Support
Please open an issue or follow guidance in `SECURITY.md`.

## References
- https://github.com/trvqhuy/nestup_evn/tree/main
