# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EVN Power Insights is a Home Assistant custom integration (HACS-compatible) that polls Vietnamese electricity provider (EVN) cloud APIs and exposes energy consumption as HA sensors. It supports 5 regional EVN companies: EVNHANOI, EVNHCMC, EVNNPC, EVNCPC, and EVNSPC.

There is no build system, test runner, or linter configured in this repository. Development and validation are done by deploying to a live Home Assistant instance.

## Development Workflow

**Deploy to HA for testing:**
1. Copy `custom_components/evn_power_insights/` into the HA `config/custom_components/` directory.
2. Restart Home Assistant.
3. Configure via Settings → Devices & Services → Add Integration → "EVN Power Insights".

**Check logs during testing:**
- Settings → System → Logs (filter for `evn_power_insights`)
- All logger calls use `_LOGGER = logging.getLogger(__name__)` with `[EVN ID <customer_id>]` prefixes for traceability.

**Validate sensor state:**
- Developer Tools → States → search `sensor.<customer_id>_`

See `TEST_CHECKLIST.md` for a full manual QA checklist.

## Architecture

### File Responsibilities

| File | Role |
|---|---|
| `__init__.py` | Entry point: `async_setup_entry`, `async_unload_entry`, `async_reload_entry` |
| `config_flow.py` | UI config flow: 3 steps — `customer_id` → `evn_info` → `fulfill_data` |
| `evn_power_insights.py` | `EVNAPI` class + all API logic, data parsing helpers |
| `sensor.py` | `EVNDevice` (coordinator wrapper) and `EVNSensor` (HA entity) |
| `types.py` | Dataclasses: `Area`, `EVN_NAME`, `EVNSensorEntityDescription`, `VIETNAM_EVN_AREA` list, `EVN_SENSORS` tuple |
| `const.py` | All constants: sensor IDs (`ID_*`), config keys (`CONF_*`), status strings, electricity pricing tiers |
| `evn_branches.json` | JSON mapping of customer ID prefixes → branch names (read at runtime) |

### Data Flow

```
Config flow (customer_id prefix)
    → get_evn_info_sync() → matches Area from VIETNAM_EVN_AREA
    → EVNAPI.login() → area-specific login method
    → DataUpdateCoordinator (polls every 24 hours)
        → EVNDevice.update()
            → EVNAPI.request_update() → area-specific fetch method
            → formatted_result() → normalises raw API response into {ID: {"value": ..., "info": ...}} dict
            → _update_derived_energy() → computes delta + derived_total, writes external statistics
    → EVNSensor.native_value → reads from EVNDevice._data via value_fn lambda
```

### Customer ID → EVN Area Routing

The customer ID prefix (2 letters after `P`) determines which EVN company handles the account. Routing is defined in `types.py` (`VIETNAM_EVN_AREA`) and matched in `get_evn_info_sync()`:

| Pattern | Company | Notes |
|---|---|---|
| `PD` | EVNHANOI | Bearer token auth; retries with index `"1"` if `"001"` fails |
| `PE` | EVNHCMC | Cookie-based session; custom SSL context |
| `PA/PH/PM/PN` | EVNNPC | Basic auth header with hardcoded client credentials |
| `PQ/PC/PP` | EVNCPC | `date_needed=False`; no billing-start-date step in config flow |
| `PB/PK` | EVNSPC | Includes loadshedding endpoint; uses `fetch_with_retries()` |

### Sensor Data Structure

`EVNAPI.request_update()` returns raw dicts; `formatted_result()` in `evn_power_insights.py` converts them into the standard internal format consumed by sensors:

```python
{
  "status": "success",
  "econ_total_new": {"value": 12345.67, "info": <date>},
  "econ_daily_new": {"value": 12.5,    "info": "hôm nay"},
  "payment_needed":  {"value": "Chưa thanh toán", "info": "mdi:comment-alert-outline"},
  ...
}
```

`EVNSensor.native_value` calls `entity_description.value_fn(self._device._data)` (a lambda defined in `types.py`) to extract the `"value"` field. The optional `"info"` field drives dynamic names and icons when `dynamic_name=True` or `dynamic_icon=True`.

### Persistence and External Statistics

`EVNDevice` uses HA's `Store` helper to persist energy state across restarts (stored under `{DOMAIN}.{entry_id}.energy_state`). On each successful update, `_update_derived_energy()` accumulates a monotonically increasing `derived_total` and calls `_write_backdated_statistics()` which writes two `StatisticData` entries to HA's recorder:
- End of previous day (23:59:59) with `sum=econ_total_old`
- Start of measurement date (00:00) with `sum=econ_total_new`

This gives the Energy Dashboard a correct daily delta. The `statistic_id` format is `evn_power_insights:<customer_id_lower>_energy_backdate`.

## Key Conventions

**Version must be updated in two places** when bumping: `manifest.json` and `const.py` (`CONF_DEVICE_SW_VERSION`).

**Sensor IDs** (`ID_*` in `const.py`) are used as dict keys throughout the data pipeline. Adding a new sensor requires: a new `ID_*` constant, a new `EVNSensorEntityDescription` entry in `EVN_SENSORS` (types.py), and corresponding population in `formatted_result()`.

**Area config dict** is mutable — login methods store tokens/sessions directly into `self._evn_area` (e.g. `self._evn_area["access_token"] = ...`). This dict originates from `dataclasses.asdict(Area(...))` during config flow.

**Electricity cost calculation** (`calc_ecost()` in `evn_power_insights.py`) uses Vietnam's tiered pricing defined in `VIETNAM_ECOST_STAGES` (const.py) with VAT from `VIETNAM_ECOST_VAT`. Update these constants when EVN changes pricing.

**EVNCPC** does not use date-range queries; it fetches the current meter reading directly and does not populate `from_date`/`to_date` from the API — `formatted_result()` synthesises those from `datetime.now()`.
