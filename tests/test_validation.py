from open_data_contracts.loader import load_contract
from open_data_contracts.validation import validate_records


def test_validates_schema_primary_key_and_quality_rules(tmp_path) -> None:
    contract_path = tmp_path / "contract.yaml"
    contract_path.write_text(
        """
version: 1
dataset: analytics.orders
owner: commerce-data
schema:
  - name: id
    type: integer
    nullable: false
    primary_key: true
  - name: status
    type: string
    nullable: false
quality:
  - rule: accepted_values
    column: status
    values: [new, done]
""",
        encoding="utf-8",
    )

    result = validate_records(
        [{"id": 1, "status": "new"}, {"id": 1, "status": "invalid"}, {"id": None, "status": "done"}],
        load_contract(contract_path),
    )

    assert not result.valid
    assert [issue.code for issue in result.issues] == ["not_null", "not_null", "unique", "accepted_values"]