"""Setup and manage HomeAssistant Entities."""

import logging
from datetime import datetime, time
import re
from typing import Any
import os
import json

from homeassistant.components.sensor import (
    DOMAIN as ENTITY_DOMAIN,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.components.recorder.statistics import (
    StatisticData,
    StatisticMetaData,
    async_add_external_statistics,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util
from homeassistant.const import UnitOfEnergy

from . import evn_power_insights
from .const import (
    CONF_AREA,
    CONF_CUSTOMER_ID,
    CONF_DEVICE_MANUFACTURER,
    CONF_DEVICE_MODEL,
    CONF_DEVICE_NAME,
    CONF_DEVICE_SW_VERSION,
    CONF_ERR_INVALID_AUTH,
    CONF_ERR_UNKNOWN,
    CONF_MONTHLY_START,
    CONF_PASSWORD,
    CONF_SUCCESS,
    CONF_USERNAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    ID_ECON_TOTAL_NEW,
    ID_ENERGY_DELTA,
    ID_ENERGY_TOTAL,
    ID_ENERGY_TOTAL_DERIVED,
    ID_TO_DATE,
)
from .types import EVN_SENSORS, EVNSensorEntityDescription

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Setup the sensor platform."""

    entry_config = hass.data[DOMAIN][entry.entry_id]

    evn_api = evn_power_insights.EVNAPI(hass, True)
    evn_device = EVNDevice(entry.entry_id, entry_config, evn_api)

    await evn_device.async_create_coordinator(hass)

    entities = []
    entities.extend(
        [EVNSensor(evn_device, description, hass) for description in EVN_SENSORS]
    )

    async_add_entities(entities)


class EVNDevice:
    """EVN Device Instance"""

    def __init__(self, entry_id, dataset, api: evn_power_insights.EVNAPI) -> None:
        """Construct Device wrapper."""
        self._entry_id = entry_id
        self._name = f"{CONF_DEVICE_NAME}: {dataset[CONF_CUSTOMER_ID]}"
        self._coordinator: DataUpdateCoordinator = None
        self.hass = api.hass
        self._username = dataset.get(CONF_USERNAME)
        self._password = dataset.get(CONF_PASSWORD)
        self._area_name = dataset.get(CONF_AREA)
        self._customer_id = dataset.get(CONF_CUSTOMER_ID)
        self._monthly_start = dataset.get(CONF_MONTHLY_START)
        self._api = api
        self._data = {}
        self._branches_data = None  # Will store the branch data
        self._energy_state = None
        self._store = Store(
            self.hass, STORAGE_VERSION, f"{DOMAIN}.{self._entry_id}.energy_state"
        )

    async def async_load_branches(self):
        """Load EVN branches data asynchronously"""
        try:
            file_path = os.path.join(
                os.path.dirname(evn_power_insights.__file__), "evn_branches.json"
            )
            self._branches_data = await self.hass.async_add_executor_job(
                evn_power_insights.read_evn_branches_file, file_path
            )
        except Exception as ex:
            _LOGGER.error("Error loading branches data: %s", str(ex))

    async def async_load_energy_state(self):
        """Load persisted energy state."""
        if self._energy_state is not None:
            return

        stored = await self._store.async_load()
        self._energy_state = stored or {
            "last_total": None,
            "derived_total": 0.0,
            "last_stat_date": None,
        }

    async def async_save_energy_state(self):
        """Persist energy state."""
        if self._energy_state is None:
            return
        await self._store.async_save(self._energy_state)

    async def _update_derived_energy(self):
        """Update derived energy values from the cumulative meter reading."""
        current_total = None
        if ID_ENERGY_TOTAL in self._data:
            current_total = self._data.get(ID_ENERGY_TOTAL, {}).get("value")

        if current_total is None:
            return

        await self.async_load_energy_state()

        last_total = self._energy_state.get("last_total")
        derived_total = float(self._energy_state.get("derived_total", 0.0))

        delta = 0.0
        if isinstance(last_total, (int, float)):
            delta = current_total - last_total
            if delta < 0:
                delta = 0.0
        else:
            daily_new = self._data.get("econ_daily_new", {}).get("value")
            if isinstance(daily_new, (int, float)):
                delta = max(daily_new, 0.0)

        derived_total += delta

        self._energy_state.update(
            {
                "last_total": current_total,
                "derived_total": derived_total,
                "last_update": datetime.utcnow().isoformat(),
            }
        )
        await self.async_save_energy_state()

        self._data[ID_ENERGY_DELTA] = {"value": round(delta, 2)}
        self._data[ID_ENERGY_TOTAL_DERIVED] = {"value": round(derived_total, 2)}
        await self._write_backdated_statistics()

    async def _write_backdated_statistics(self):
        """Write backdated statistics based on meter time."""
        to_date_str = self._data.get(ID_TO_DATE, {}).get("value")
        if not to_date_str:
            return

        try:
            measurement_date = datetime.strptime(to_date_str, "%d/%m/%Y").date()
        except ValueError:
            return

        await self.async_load_energy_state()
        last_stat_date = self._energy_state.get("last_stat_date")
        if last_stat_date == measurement_date.isoformat():
            return

        # Dùng chỉ số công tơ thực từ API
        econ_total_new = self._data.get(ID_ECON_TOTAL_NEW, {}).get("value")
        if econ_total_new is None:
            return
        
        tz = (
            dt_util.get_time_zone(self.hass.config.time_zone)
            if self.hass.config.time_zone
            else dt_util.UTC
        )
        start = dt_util.as_utc(
            datetime.combine(measurement_date, time.min).replace(tzinfo=tz)
        )

        raw_stat_id = f"{DOMAIN}_{self._customer_id}_{ID_ENERGY_TOTAL_DERIVED}".lower()
        statistic_id = re.sub(r"[^a-z0-9_]", "_", raw_stat_id)
        if not statistic_id[0].isalpha():
            statistic_id = f"evn_{statistic_id}"
        metadata = StatisticMetaData(
            has_mean=False,
            has_sum=True,
            name=f"{self._name} EVN Energy (theo thoi diem do)",
            source=DOMAIN,
            statistic_id=statistic_id,
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        )
        data = StatisticData(start=start, sum=econ_total_new)
        try:
            await async_add_external_statistics(self.hass, metadata, [data])
        except Exception as err:
            _LOGGER.warning("Failed to write backdated statistics: %s", err)
            return

        self._energy_state["last_stat_date"] = measurement_date.isoformat()
        await self.async_save_energy_state()

    async def update(self) -> dict[str, Any]:
        """Update device data from EVN Endpoints."""

        self._data = await self._api.request_update(
            self._area_name, self._username, self._password, self._customer_id, self._monthly_start
        )

        status = self._data.get("status")

        if status != CONF_SUCCESS:

            if status == CONF_ERR_INVALID_AUTH:
                _LOGGER.info(
                    "[EVN ID %s] Expired session, try reauthenticating.",
                    self._customer_id,
                )

                login_state = await self._api.login(
                    self._area_name, self._username, self._password, self._customer_id
                )

                if login_state == CONF_SUCCESS:
                    self._data = await self._api.request_update(
                        self._area_name,
                        self._username,
                        self._password,
                        self._customer_id,
                        self._monthly_start,
                    )
                    status = self._data.get("status")

        if status == CONF_SUCCESS:
            _LOGGER.info(
                "[EVN ID %s] Successfully fetched new data from EVN Server.",
                self._customer_id,
            )
            await self._update_derived_energy()

        else:
            _LOGGER.warning(
                "[EVN ID %s] Could not fetch new data - %s",
                self._customer_id,
                self._data.get("data"),
            )

        return self._data

    async def _async_update(self):
        """Fetch the latest data from EVN."""
        await self.update()

    async def async_create_coordinator(self, hass: HomeAssistant) -> None:
        """Create the coordinator for this specific device."""
        if self._coordinator:
            return

        await self.async_load_branches()
        await self.async_load_energy_state()

        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{self._customer_id}",
            update_method=self._async_update,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        await coordinator.async_config_entry_first_refresh()
        self._coordinator = coordinator

    @property
    def info(self) -> DeviceInfo:
        """Return device description for device registry."""
        evn_area = evn_power_insights.get_evn_info_sync(
            self._customer_id, self._branches_data
        )
        hw_version = f"by {self._area_name['name']}"

        if (evn_area["status"] == CONF_SUCCESS) and (
            evn_area["evn_branch"] != "Unknown"
        ):
            hw_version = f"by {evn_area['evn_branch']}"

        return DeviceInfo(
            name=self._name,
            identifiers={(DOMAIN, self._customer_id)},
            manufacturer=CONF_DEVICE_MANUFACTURER,
            sw_version=CONF_DEVICE_SW_VERSION,
            hw_version=hw_version,
            model=CONF_DEVICE_MODEL,
        )

    @property
    def coordinator(self) -> DataUpdateCoordinator or None:
        """Return coordinator associated."""
        return self._coordinator

    @property
    def branch_info(self):
        """Get branch info synchronously."""
        if self._branches_data is None:
            return {"status": CONF_ERR_UNKNOWN}
        return evn_power_insights.get_evn_info_sync(
            self._customer_id, self._branches_data
        )


class EVNSensor(CoordinatorEntity, SensorEntity):
    """EVN Sensor Instance."""

    def __init__(
        self, device: EVNDevice, description: EVNSensorEntityDescription, hass
    ):
        """Construct EVN sensor wrapper."""
        super().__init__(device.coordinator)

        self._device = device
        self._attr_name = f"{device._name} {description.name}"
        self._unique_id = str(f"{device._customer_id}_{description.key}").lower()
        self._default_name = description.name

        self.entity_id = (
            f"{ENTITY_DOMAIN}.{device._customer_id}_{description.key}".lower()
        )
        self.entity_description = description

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def native_value(self):
        """Return the state of the sensor."""
        data = self.entity_description.value_fn(self._device._data)

        if self.entity_description.dynamic_name:
            self._attr_name = f"{self._default_name} {data.get('info')}"

        if self.entity_description.dynamic_icon:
            self._attr_icon = data.get("info")

        return data.get("value")

    @property
    def device_info(self):
        """Return a device description for device registry."""
        hw_version = f"by {self._device._area_name['name']}"

        evn_area = self._device.branch_info
        if (evn_area["status"] == CONF_SUCCESS) and (
            evn_area["evn_branch"] != "Unknown"
        ):
            hw_version = f"by {evn_area['evn_branch']}"

        return DeviceInfo(
            name=self._device._name,
            identifiers={(DOMAIN, self._device._customer_id)},
            manufacturer=CONF_DEVICE_MANUFACTURER,
            sw_version=CONF_DEVICE_SW_VERSION,
            hw_version=hw_version,
            model=CONF_DEVICE_MODEL,
        )

    @property
    def available(self) -> bool:
        """Return the availability of the sensor."""
        return (
            self._device._data["status"] == CONF_SUCCESS
            and self.native_value is not None
        )

    @property
    def last_reset(self):
        if self.entity_description.state_class == SensorStateClass.TOTAL:
            data = self.entity_description.value_fn(self._device._data)

            return data.get("info")

        return None
