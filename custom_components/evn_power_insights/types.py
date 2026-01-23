from array import ArrayType
from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy

from .const import ID_ENERGY_TOTAL


@dataclass
class Entity:
    """Describe the sensor entities."""

    id: str
    friendly_name: str
    entity_class: str
    unit: str
    icon: str
    state_class: SensorStateClass or None


@dataclass
class Area:
    """Describe the supported areas."""

    name: str
    key: str | None = None
    location: str | None = None
    evn_login_url: str | None = None
    evn_data_url: str | None = None
    evn_payment_url: str | None = None
    evn_loadshedding_url: str | None = None
    supported: bool = True
    date_needed: bool = True
    pattern: ArrayType | None = None


@dataclass
class EVN_NAME:
    """Describe the EVN names."""

    HANOI = "EVNHANOI"
    HCMC = "EVNHCMC"
    NPC = "EVNNPC"
    CPC = "EVNCPC"
    SPC = "EVNSPC"


@dataclass
class EVNRequiredKeysMixin:
    """Mixin for required keys."""

    value_fn: Callable[[Any], float]


@dataclass
class EVNSensorEntityDescription(SensorEntityDescription, EVNRequiredKeysMixin):
    """Describes EVN sensor entity."""

    dynamic_name: None | bool = False
    dynamic_icon: None | bool = False


VIETNAM_EVN_AREA = [
    Area(
        name=EVN_NAME.HANOI,
        location="Thủ đô Hà Nội",
        evn_login_url="https://apicskh.evnhanoi.com.vn/connect/token",
        evn_data_url="https://evnhanoi.vn/api/TraCuu/LayChiSoDoXa",
        evn_payment_url="https://evnhanoi.vn/api/TraCuu/GetListThongTinNoKhachHang",
        pattern=["PD"],
    ),
    Area(
        name=EVN_NAME.HCMC,
        location="Thành phố Hồ Chí Minh",
        evn_login_url="https://cskh.evnhcmc.vn/Dangnhap/checkLG",
        evn_data_url="https://cskh.evnhcmc.vn/Tracuu/ajax_dienNangTieuThuTheoNgay",
        evn_payment_url="https://cskh.evnhcmc.vn/Tracuu/kiemTraNo",
        pattern=["PE"],
    ),
    Area(
        name=EVN_NAME.NPC,
        location="Khu vực miền Bắc",
        evn_login_url="https://billnpccc.enterhub.asia/login",
        evn_data_url="https://billnpccc.enterhub.asia/dailyconsump",
        evn_payment_url="https://billnpccc.enterhub.asia/mobileapi/home/",
        pattern=["PA", "PH", "PM", "PN"],
    ),
    Area(
        name=EVN_NAME.CPC,
        location="Khu vực miền Trung",
        evn_login_url="https://cskh-api.cpc.vn/connect/token",
        evn_data_url="https://cskh-api.cpc.vn/api/cskh/power-consumption-alerts/by-customer-code/",
        evn_payment_url="https://appcskh.cpc.vn:4433/api/v4/customer/home/",
        date_needed=False,
        pattern=["PQ", "PC", "PP"],
    ),
    Area(
        name=EVN_NAME.SPC,
        location="Khu vực miền Nam",
        evn_login_url="https://api.cskh.evnspc.vn/api/user/authenticate",
        evn_data_url="https://api.cskh.evnspc.vn/api/NghiepVu/LayThongTinSanLuongTheoNgay_v1",
        evn_payment_url="https://api.cskh.evnspc.vn/api/NghiepVu/TraCuuNoHoaDon",
        evn_loadshedding_url="https://api.cskh.evnspc.vn/api/NghiepVu/TraCuuLichNgungGiamCungCapDien",
        pattern=["PB", "PK"],
    ),
]

EVN_SENSORS: tuple[EVNSensorEntityDescription, ...] = (
    EVNSensorEntityDescription(
        key=ID_ENERGY_TOTAL,
        name="Tổng điện năng",
        icon="mdi:transmission-tower",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        value_fn=lambda data: data[ID_ENERGY_TOTAL],
    ),
)
