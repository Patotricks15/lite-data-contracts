//! Lite Data Contracts - Rust Pipeline Example.
//!
//! Direct Rust core usage for verifying LLM structured JSON output.

use lite_data_contracts::{validate_records, Contract};
use serde_json::json;

fn main() {
    println!("=== Lite Data Contracts - Rust Example ===");

    let contract = Contract {
        required_fields: vec!["user_id".to_string(), "action".to_string()],
    };

    // Simulated LLM tool output
    let valid_tool_call = json!({
        "user_id": "usr_42",
        "action": "revoke_access"
    });

    let invalid_tool_call = json!({
        "user_id": "usr_42"
    });

    println!("\n[1] Validating LLM structured output 1...");
    let issues = validate_records(&contract, &[valid_tool_call]);
    if issues.is_empty() {
        println!(" -> Valid! Executing action in backend.");
    }

    println!("\n[2] Validating LLM structured output 2...");
    let issues2 = validate_records(&contract, &[invalid_tool_call]);
    if !issues2.is_empty() {
        println!(" -> Rejected: Found {} issue(s): {:?}", issues2.len(), issues2);
    }
}
