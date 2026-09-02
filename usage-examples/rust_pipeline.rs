//! Lite Data Contracts - Rust Pipeline Example.
//!
//! Demonstrates loading contracts from YAML (examples/orders-v1.yaml) and validating records.

use lite_data_contracts::Contract;
use serde_json::json;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    println!("=== Lite Data Contracts - Rust Example ===");

    // 1. Rust carrega e valida o arquivo de contrato YAML
    let contract_path = "examples/orders-v1.yaml";
    println!("\n[1] Carregando contrato de '{}'...", contract_path);
    let contract = Contract::from_file(contract_path)?;

    println!(
        " -> Contrato '{}' carregado. Campos obrigatórios: {:?}",
        contract.dataset, contract.required_fields
    );

    // 2. Simulando saída estruturada de Tool Call de um LLM
    println!("\n[2] Validando saída estruturada de Tool Call do LLM...");
    let valid_tool_call = json!({
        "order_id": "ORD-9821",
        "customer_email": "alice@example.com",
        "legacy_code": 104
    });

    let issues = contract.validate_records(&[valid_tool_call]);
    if issues.is_empty() {
        println!(" -> Validação: APROVADO (Zero violações)");
    }

    // 3. Simulando saída corrompida / com alucinação de campo ausente
    let malformed_tool_call = json!({
        "order_id": "ORD-9822"
        // customer_email ausente
    });

    let issues = contract.validate_records(&[malformed_tool_call]);
    println!(" -> Validação de payload inválido: {} problemas detectados: {:?}", issues.len(), issues);

    Ok(())
}
