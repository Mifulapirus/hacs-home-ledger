"""Data models for Home Ledger."""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from numbers import Real
from typing import Any, Self


class UtilityType(StrEnum):
    """Supported utility categories."""

    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    OTHER = "other"  # flat fees and charges with no metered consumption


UTILITY_UNITS: dict[UtilityType, str] = {
    UtilityType.ELECTRICITY: "kWh",
    UtilityType.GAS: "m\u00b3",
    UtilityType.WATER: "m\u00b3",
    UtilityType.OTHER: "",
}


@dataclass(frozen=True, kw_only=True)
class Bill:
    """A utility bill persisted in Home Assistant storage."""

    id: str
    start_date: date
    end_date: date
    total_cost: float
    consumption: float
    utility_type: UtilityType

    def __post_init__(self) -> None:
        """Validate and normalize bill fields."""
        bill_id = self._validate_id(self.id)
        start_date = self._validate_date(self.start_date, "start_date")
        end_date = self._validate_date(self.end_date, "end_date")

        if end_date <= start_date:
            raise ValueError("end_date must be after start_date")

        total_cost = self._validate_non_negative_number(self.total_cost, "total_cost")
        consumption = self._validate_non_negative_number(self.consumption, "consumption")
        utility_type = self._validate_utility_type(self.utility_type)

        object.__setattr__(self, "id", bill_id)
        object.__setattr__(self, "start_date", start_date)
        object.__setattr__(self, "end_date", end_date)
        object.__setattr__(self, "total_cost", total_cost)
        object.__setattr__(self, "consumption", consumption)
        object.__setattr__(self, "utility_type", utility_type)

    @property
    def unit_of_measurement(self) -> str:
        """Return the native consumption unit for the bill utility type."""
        return UTILITY_UNITS[self.utility_type]

    def as_storage_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation for Home Assistant storage."""
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "total_cost": self.total_cost,
            "consumption": self.consumption,
            "utility_type": self.utility_type.value,
        }

    @classmethod
    def from_storage_dict(cls, data: dict[str, Any]) -> Self:
        """Create a bill from Home Assistant storage data."""
        return cls(
            id=data["id"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            total_cost=data["total_cost"],
            consumption=data["consumption"],
            utility_type=data["utility_type"],
        )

    @staticmethod
    def _validate_id(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("id must be a non-empty string")
        return value

    @staticmethod
    def _validate_date(value: date | str, field_name: str) -> date:
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError as err:
                raise ValueError(f"{field_name} must be in ISO format (YYYY-MM-DD)") from err
        if not isinstance(value, date):
            raise TypeError(f"{field_name} must be a date object or ISO string")
        return value

    @staticmethod
    def _validate_non_negative_number(value: float, field_name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, Real) or value < 0:
            raise ValueError(f"{field_name} must be a non-negative number")
        return float(value)

    @staticmethod
    def _validate_utility_type(value: UtilityType | str) -> UtilityType:
        try:
            return UtilityType(value)
        except ValueError as err:
            supported = ", ".join(utility_type.value for utility_type in UtilityType)
            raise ValueError(f"utility_type must be one of: {supported}") from err


__all__ = ["UTILITY_UNITS", "Bill", "UtilityType"]
