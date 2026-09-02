# Lite Data Contracts

[![CI](https://github.com/Patotricks15/lite-data-contracts/actions/workflows/ci.yml/badge.svg)](https://github.com/Patotricks15/lite-data-contracts/actions/workflows/ci.yml)
[![Release](https://github.com/Patotricks15/lite-data-contracts/actions/workflows/release.yml/badge.svg)](https://github.com/Patotricks15/lite-data-contracts/actions/workflows/release.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Fast, memory-conscious data contract and schema validation library written in **Rust** with high-level SDK bindings for **Python**, **TypeScript/Node.js**, and **Go**.

Designed to validate structured LLM Tool Calls, agent function outputs, and streaming data pipelines against declarative YAML contracts.

---

## 📦 Installation

### Python
```bash
pip install lite-data-contracts
```

### TypeScript / Node.js
```bash
npm install @patotricks15/lite-data-contracts
```

### Go
```bash
go get github.com/Patotricks15/lite-data-contracts/bindings/go
```

### Rust (Core Crate)
```toml
[dependencies]
lite-data-contracts = "0.1"
```

---

## 🚀 Quickstart & Usage Examples

### 1. Python
```python
from lite_data_contracts import DataContract

# 1. Rust loads & validates YAML schema contract
contract = DataContract.from_file("examples/orders-v1.yaml")

# 2. Validate structured LLM tool call outputs
records = [{"order_id": "ORD-1234", "customer_email": "client@acme.com"}]
issues = contract.validate(records)

if not issues:
    print("Contract Validated! Safe to execute backend action.")
else:
    print(f"Contract violations: {issues}")
```

---

### 2. TypeScript / Node.js
```typescript
import { DataContract } from '@patotricks15/lite-data-contracts';

// 1. Load contract via Rust Core
const contract = DataContract.fromFile('examples/orders-v1.yaml');

// 2. Validate tool call results
const issues = contract.validate([
  { order_id: 'ORD-9901', customer_email: 'support@store.com' }
]);

console.log(`Validation result: ${issues.length === 0 ? 'PASSED' : 'FAILED'}`);
```

---

### 3. Go
```go
package main

import (
    "fmt"
    "log"

    litedatacontracts "github.com/Patotricks15/lite-data-contracts/bindings/go"
)

func main() {
    // 1. Rust engine loads and parses YAML contract
    contract, err := litedatacontracts.FromFile("examples/orders-v1.yaml")
    if err != nil {
        log.Fatalf("Failed to load contract: %v", err)
    }

    // 2. Validate records
    records := []map[string]interface{}{
        {"order_id": "ORD-501", "customer_email": "dev@cloud.com"},
    }

    issues := contract.Validate(records)
    fmt.Printf("Violations found: %d\n", len(issues))
}
```

---

### 4. Rust (Native Core)
```rust
use lite_data_contracts::Contract;
use serde_json::json;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let contract = Contract::from_file("examples/orders-v1.yaml")?;
    let records = vec![json!({"order_id": "ORD-1", "customer_email": "test@test.com"})];

    let issues = contract.validate_records(&records);
    assert!(issues.is_empty());
    println!("Validation passed with 0 issues.");
    Ok(())
}
```

---

## 📄 License
Licensed under Apache-2.0.
