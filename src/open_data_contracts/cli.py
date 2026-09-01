"""Command-line interface for data contract workflows."""

import json
from pathlib import Path

import typer

from .compatibility import check_compatibility
from .loader import load_contract
from .validation import validate_records

app = typer.Typer(no_args_is_help=True)


@app.command()
def validate(contract: Path, records: Path) -> None:
    """Validate JSON records against a YAML contract."""
    loaded_records = json.loads(records.read_text(encoding="utf-8"))
    result = validate_records(loaded_records, load_contract(contract))
    if result.valid:
        typer.echo("Contract validation passed.")
        return
    for issue in result.issues:
        location = f" row={issue.row}" if issue.row is not None else ""
        typer.echo(f"{issue.code}:{location} {issue.message}")
    raise typer.Exit(code=1)


@app.command()
def diff(previous: Path, current: Path) -> None:
    """Report breaking changes from a previous contract to a current contract."""
    issues = check_compatibility(load_contract(previous), load_contract(current))
    if not issues:
        typer.echo("Contracts are compatible.")
        return
    for issue in issues:
        typer.echo(f"{issue.field}: {issue.message}")
    raise typer.Exit(code=1)