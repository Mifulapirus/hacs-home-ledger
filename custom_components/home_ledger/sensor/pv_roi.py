"""PV ROI sensors for home_ledger."""

from typing import Any

from custom_components.home_ledger.entity import HomeLedgerEntity
from custom_components.home_ledger.entity.base import localize_currency_unit
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import CURRENCY_EURO, EntityCategory


class PVROISensor(HomeLedgerEntity, SensorEntity):
    """Sensor that exposes PV ROI metrics from the coordinator."""

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit, in Home Assistant's configured currency."""
        hass = getattr(self, "hass", None)
        return localize_currency_unit(
            super().native_unit_of_measurement,
            hass.config.currency if hass is not None else None,
        )

    entity_description: PVROISensorEntityDescription

    @property
    def native_value(self) -> Any:
        """Return the native value of the sensor."""
        data = self.coordinator.config_entry.runtime_data.pv_roi
        if data is None:
            return None

        return getattr(data, self.entity_description.key)


class PVROISensorEntityDescription(SensorEntityDescription):
    """Description of a PV ROI sensor."""

    def __init__(
        self,
        key: str,
        translation_key: str,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        native_unit_of_measurement: str | None = None,
        entity_category: EntityCategory = EntityCategory.DIAGNOSTIC,
    ):
        """Initialize a PV ROI sensor description."""
        super().__init__(
            key=key,
            translation_key=translation_key,
            device_class=device_class,
            state_class=state_class,
            native_unit_of_measurement=native_unit_of_measurement,
            entity_category=entity_category,
        )


ENTITY_DESCRIPTIONS = (
    PVROISensorEntityDescription(
        key="total_savings",
        translation_key="pv_total_savings",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=CURRENCY_EURO,
    ),
    PVROISensorEntityDescription(
        key="roi_percentage",
        translation_key="pv_roi_percentage",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="%",
    ),
    PVROISensorEntityDescription(
        key="payback_years",
        translation_key="pv_payback_years",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="years",
    ),
    PVROISensorEntityDescription(
        key="break_even_date",
        translation_key="pv_break_even_date",
        device_class=SensorDeviceClass.DATE,
        state_class=None,
    ),
)
