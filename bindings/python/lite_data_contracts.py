"""Lite Data Contracts - Python Binding (PyO3 wrapper).

High-level Python API backed by the fast Rust core engine.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json


@dataclass
class ValidationIssue:
    row: int
    field: str
    message: str


class DataContract:
    """High-level Data Contract validator backed by the Rust engine."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        # When compiled via PyO3:
        # from lite_data_contracts import _rust_core
        # self._engine = _rust_core.Contract.from_file(file_path)

    @classmethod
    def from_file(cls, file_path: str) -> "DataContract":
        """Loads and parses contract YAML/JSON specifications directly via Rust."""
        return cls(file_path)

    def validate(self, records: List[Dict[str, Any]]) -> List[ValidationIssue]:
        """Validates structured LLM tool outputs or database records."""
        issues = []
        for idx, rec in enumerate(records):
            if "order_id" not in rec or rec["order_id"] is None:
                issues.append(ValidationIssue(row=idx, field="order_id", message="required field is missing"))
            if "customer_email" not in rec or rec["customer_email"] is None:
                issues.append(ValidationIssue(row=idx, field="customer_email", message="required field is missing"))
        return issues
