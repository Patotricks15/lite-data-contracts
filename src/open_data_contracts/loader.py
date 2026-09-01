"""Contract file loading."""

from pathlib import Path

import yaml

from .models import DataContract


def load_contract(path: str | Path) -> DataContract:
    """Load and validate a YAML contract from *path*."""
    with Path(path).open(encoding="utf-8") as contract_file:
        content = yaml.safe_load(contract_file)
    if not isinstance(content, dict):
        raise ValueError("contract must contain a YAML mapping")
    return DataContract.model_validate(content)