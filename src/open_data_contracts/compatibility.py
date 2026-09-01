"""Backward compatibility checks for contract evolution."""

from dataclasses import dataclass

from .models import DataContract


@dataclass(frozen=True)
class CompatibilityIssue:
    message: str
    field: str | None = None


def check_compatibility(previous: DataContract, current: DataContract) -> list[CompatibilityIssue]:
    """Report changes that break consumers of *previous*."""
    issues: list[CompatibilityIssue] = []
    old_fields = {field.name: field for field in previous.schema_}
    new_fields = {field.name: field for field in current.schema_}
    for name, old_field in old_fields.items():
        new_field = new_fields.get(name)
        if new_field is None:
            issues.append(CompatibilityIssue("field was removed", name))
        elif new_field.type != old_field.type:
            issues.append(CompatibilityIssue(f"type changed from {old_field.type} to {new_field.type}", name))
        elif old_field.nullable and not new_field.nullable:
            issues.append(CompatibilityIssue("field became required", name))
    return issues