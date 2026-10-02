"""Base entity class for home_ledger."""

from typing import TYPE_CHECKING

from custom_components.home_ledger.const import DOMAIN
from custom_components.home_ledger.coordinator import HomeLedgerDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class HomeLedgerEntity(CoordinatorEntity[HomeLedgerDataUpdateCoordinator]):
    """Base entity providing device info, unique ID and attribution."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HomeLedgerDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={
                (DOMAIN, coordinator.config_entry.entry_id),
            },
            name="Home Ledger",
            manufacturer="Home Ledger",
            model="Home Ledger",
        )


def localize_currency_unit(unit: str | None, currency: str | None) -> str | None:
    """Replace the hard-coded euro sign with Home Assistant's configured currency.

    Sensor descriptions are module-level constants written in EUR; the real
    currency is only known at runtime, from hass.config.currency.
    """
    from homeassistant.const import CURRENCY_EURO  # noqa: PLC0415

    if unit and currency and CURRENCY_EURO in unit:
        return unit.replace(CURRENCY_EURO, currency)
    return unit
