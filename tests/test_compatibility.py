from open_data_contracts.compatibility import check_compatibility
from open_data_contracts.models import DataContract


def test_detects_removed_fields_and_type_changes() -> None:
    previous = DataContract.model_validate(
        {"version": 1, "dataset": "orders", "owner": "team", "schema": [{"name": "id", "type": "integer"}, {"name": "code", "type": "string"}]}
    )
    current = DataContract.model_validate(
        {"version": 2, "dataset": "orders", "owner": "team", "schema": [{"name": "id", "type": "string"}]}
    )

    issues = check_compatibility(previous, current)

    assert [issue.field for issue in issues] == ["id", "code"]