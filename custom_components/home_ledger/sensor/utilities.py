"""Utility ledger sensor descriptions for home_ledger."""

from typing import Any

from custom_components.home_ledger.sensor.entity import HomeLedgerSensorEntityDescription
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import CURRENCY_EURO, UnitOfEnergy, UnitOfVolume
from homeassistant.helpers.typing import StateType

UTILITY_TYPES = ("electricity", "gas", "water", "other")


def _sum_values(data: Any, keys: tuple[str, ...]) -> StateType:
    total: float = 0
    for key in keys:
        value = getattr(data, key, None)
        if value is None:
            return None
        total += value
    return total


def _get_attr(data: Any, key: str) -> StateType:
    return getattr(data, key, None)


def _monthly_costs_attr(data: Any, utility_type: str) -> dict[str, float] | None:
    """Return monthly costs as extra attributes."""
    attr_name = f"{utility_type}_monthly_costs"
    return getattr(data, attr_name, None)


def _monthly_consumption_attr(data: Any, utility_type: str) -> dict[str, float] | None:
    """Return monthly consumption as extra attributes."""
    attr_name = f"{utility_type}_monthly_consumption"
    return getattr(data, attr_name, None)


COST_DESCRIPTIONS: tuple[HomeLedgerSensorEntityDescription, ...] = (
    *(
        HomeLedgerSensorEntityDescription(
            key=f"total_{utility_type}_cost",
            translation_key=f"total_{utility_type}_cost",
            device_class=SensorDeviceClass.MONETARY,
            native_unit_of_measurement=CURRENCY_EURO,
            state_class=SensorStateClass.TOTAL,
            suggested_display_precision=2,
            value_fn=lambda data, key=f"total_{utility_type}_cost": _get_attr(data, key),
            extra_attributes_fn=lambda data, ut=utility_type: _monthly_costs_attr(data, ut),
        )
        for utility_type in UTILITY_TYPES
    ),
    HomeLedgerSensorEntityDescription(
        key="total_utility_cost",
        translation_key="total_utility_cost",
        device_class=SensorDeviceClass.MONETARY,
        native_unit_of_measurement=CURRENCY_EURO,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        value_fn=lambda data: _sum_values(
            data,
            ("total_electricity_cost", "total_gas_cost", "total_water_cost", "total_other_cost"),
        ),
    ),
)

CONSUMPTION_DESCRIPTIONS: tuple[HomeLedgerSensorEntityDescription, ...] = (
    HomeLedgerSensorEntityDescription(
        key="total_electricity_consumption",
        translation_key="total_electricity_consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        value_fn=lambda data: _get_attr(data, "total_electricity_consumption"),
        extra_attributes_fn=lambda data: _monthly_consumption_attr(data, "electricity"),
    ),
    *(
        HomeLedgerSensorEntityDescription(
            key=f"total_{utility_type}_consumption",
            translation_key=f"total_{utility_type}_consumption",
            device_class=SensorDeviceClass.VOLUME,
            native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
            state_class=SensorStateClass.TOTAL,
            suggested_display_precision=2,
            value_fn=lambda data, key=f"total_{utility_type}_consumption": _get_attr(data, key),
            extra_attributes_fn=lambda data, ut=utility_type: _monthly_consumption_attr(data, ut),
        )
        for utility_type in ("gas", "water")
    ),
)

AVERAGE_COST_DESCRIPTIONS: tuple[HomeLedgerSensorEntityDescription, ...] = tuple(
    HomeLedgerSensorEntityDescription(
        key=f"{utility_type}_average_monthly_cost",
        translation_key=f"{utility_type}_average_monthly_cost",
        device_class=SensorDeviceClass.MONETARY,
        native_unit_of_measurement=CURRENCY_EURO,
        suggested_display_precision=2,
        value_fn=lambda data, key=f"{utility_type}_average_monthly_cost": _get_attr(data, key),
    )
    for utility_type in UTILITY_TYPES
)

AVERAGE_CONSUMPTION_DESCRIPTIONS: tuple[HomeLedgerSensorEntityDescription, ...] = (
    HomeLedgerSensorEntityDescription(
        key="electricity_average_monthly_consumption",
        translation_key="electricity_average_monthly_consumption",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=2,
        value_fn=lambda data: _get_attr(data, "electricity_average_monthly_consumption"),
    ),
    *(
        HomeLedgerSensorEntityDescription(
            key=f"{utility_type}_average_monthly_consumption",
            translation_key=f"{utility_type}_average_monthly_consumption",
            device_class=SensorDeviceClass.VOLUME,
            native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
            suggested_display_precision=2,
            value_fn=lambda data, key=f"{utility_type}_average_monthly_consumption": _get_attr(data, key),
        )
        for utility_type in ("gas", "water")
    ),
)

COST_PER_UNIT_DESCRIPTIONS: tuple[HomeLedgerSensorEntityDescription, ...] = (
    HomeLedgerSensorEntityDescription(
        key="electricity_cost_per_unit",
        translation_key="electricity_cost_per_unit",
        native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}",
        suggested_display_precision=2,
        value_fn=lambda data: _get_attr(data, "electricity_cost_per_unit"),
    ),
    *(
        HomeLedgerSensorEntityDescription(
            key=f"{utility_type}_cost_per_unit",
            translation_key=f"{utility_type}_cost_per_unit",
            native_unit_of_measurement=f"{CURRENCY_EURO}/{UnitOfVolume.CUBIC_METERS}",
            suggested_display_precision=2,
            value_fn=lambda data, key=f"{utility_type}_cost_per_unit": _get_attr(data, key),
        )
        for utility_type in ("gas", "water")
    ),
)

ENTITY_DESCRIPTIONS = (
    *COST_DESCRIPTIONS,
    *CONSUMPTION_DESCRIPTIONS,
    *AVERAGE_COST_DESCRIPTIONS,
    *AVERAGE_CONSUMPTION_DESCRIPTIONS,
    *COST_PER_UNIT_DESCRIPTIONS,
)
