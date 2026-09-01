"""Record validation against a data contract."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .models import DataContract


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    row: int | None = None
    column: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    issues: list[ValidationIssue]

    @property
    def valid(self) -> bool:
        return not self.issues


TYPE_CHECKS: dict[str, type[Any] | tuple[type[Any], ...]] = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}


def validate_records(
    records: Sequence[Mapping[str, Any]], contract: DataContract
) -> ValidationResult:
    """Validate row-oriented records and return all detected contract violations."""
    issues: list[ValidationIssue] = []
    fields = {field.name: field for field in contract.schema_}

    for row_index, record in enumerate(records):
        for name, field in fields.items():
            value = record.get(name)
            if value is None:
                if not field.nullable:
                    issues.append(ValidationIssue("not_null", f"{name} cannot be null", row_index, name))
                continue
            if isinstance(value, bool) and field.type in {"integer", "number"}:
                is_correct_type = False
            else:
                is_correct_type = isinstance(value, TYPE_CHECKS[field.type])
            if not is_correct_type:
                issues.append(ValidationIssue("type", f"{name} must be {field.type}", row_index, name))

    for field in fields.values():
        if field.primary_key:
            _validate_unique(records, field.name, issues)

    for rule in contract.quality:
        if rule.rule == "not_null":
            _validate_not_null(records, rule.column, issues)
        elif rule.rule == "unique":
            _validate_unique(records, rule.column, issues)
        elif rule.rule == "accepted_values":
            _validate_accepted_values(records, rule.column, rule.values, issues)
        elif rule.rule == "row_count_min" and len(records) < rule.value:
            issues.append(ValidationIssue("row_count_min", f"expected at least {rule.value} records"))

    return ValidationResult(issues)


def _validate_not_null(records: Sequence[Mapping[str, Any]], column: str | None, issues: list[ValidationIssue]) -> None:
    for row_index, record in enumerate(records):
        if record.get(column) is None:
            issues.append(ValidationIssue("not_null", f"{column} cannot be null", row_index, column))


def _validate_unique(records: Sequence[Mapping[str, Any]], column: str | None, issues: list[ValidationIssue]) -> None:
    seen: set[Any] = set()
    for row_index, record in enumerate(records):
        value = record.get(column)
        if value is not None and value in seen:
            issues.append(ValidationIssue("unique", f"{column} must be unique", row_index, column))
        seen.add(value)


def _validate_accepted_values(records: Sequence[Mapping[str, Any]], column: str | None, values: list[Any] | None, issues: list[ValidationIssue]) -> None:
    accepted = set(values or [])
    for row_index, record in enumerate(records):
        value = record.get(column)
        if value is not None and value not in accepted:
            issues.append(ValidationIssue("accepted_values", f"{column} has an unsupported value", row_index, column))