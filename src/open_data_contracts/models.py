"""Pydantic models for the public data-contract specification."""

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ServiceLevelAgreement(BaseModel):
    freshness: str | None = None


class FieldContract(BaseModel):
    name: str
    type: Literal["string", "integer", "number", "boolean"]
    nullable: bool = True
    primary_key: bool = False
    classification: str | None = None


class QualityRule(BaseModel):
    rule: Literal["not_null", "unique", "accepted_values", "row_count_min"]
    column: str | None = None
    values: list[Any] | None = None
    value: int | None = None

    @model_validator(mode="after")
    def validate_rule_configuration(self) -> "QualityRule":
        column_rules = {"not_null", "unique", "accepted_values"}
        if self.rule in column_rules and not self.column:
            raise ValueError(f"{self.rule} requires a column")
        if self.rule == "accepted_values" and self.values is None:
            raise ValueError("accepted_values requires values")
        if self.rule == "row_count_min" and self.value is None:
            raise ValueError("row_count_min requires value")
        return self


class DataContract(BaseModel):
    version: int = Field(ge=1)
    dataset: str
    owner: str
    sla: ServiceLevelAgreement | None = None
    schema_: list[FieldContract] = Field(alias="schema", min_length=1)
    quality: list[QualityRule] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def validate_unique_fields(self) -> "DataContract":
        names = [field.name for field in self.schema_]
        if len(names) != len(set(names)):
            raise ValueError("schema field names must be unique")
        return self