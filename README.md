# Open Data Contracts

A Python toolkit for defining versioned data contracts in YAML, validating records, and detecting breaking schema changes.

## Quick start

```bash
python -m pip install -e '.[dev]'
odc validate examples/orders.yaml examples/orders.json
odc diff examples/orders-v1.yaml examples/orders.yaml
```

## Contract format

```yaml
version: 1
dataset: analytics.orders
owner: commerce-data
sla:
  freshness: 2h
schema:
  - name: order_id
    type: string
    nullable: false
    primary_key: true
  - name: customer_email
    type: string
    nullable: false
    classification: pii.email
quality:
  - rule: unique
    column: order_id
```