//! Data-contract validation with allocation-conscious, streaming-friendly APIs.

use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Contract {
    pub required_fields: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ValidationIssue {
    pub row: usize,
    pub field: String,
    pub message: &'static str,
}

pub fn validate_records<'a>(contract: &Contract, records: impl IntoIterator<Item = &'a Value>) -> Vec<ValidationIssue> {
    let mut issues = Vec::new();
    for (row, record) in records.into_iter().enumerate() {
        let object = match record.as_object() {
            Some(object) => object,
            None => {
                issues.push(ValidationIssue { row, field: String::new(), message: "record must be an object" });
                continue;
            }
        };
        for field in &contract.required_fields {
            if object.get(field).is_none_or(Value::is_null) {
                issues.push(ValidationIssue { row, field: field.clone(), message: "required field is missing" });
            }
        }
    }
    issues
}

pub fn validate_json(contract_json: &str, records_json: &str) -> Result<String, serde_json::Error> {
    let contract: Contract = serde_json::from_str(contract_json)?;
    let records: Vec<Value> = serde_json::from_str(records_json)?;
    serde_json::to_string(&validate_records(&contract, &records))
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn reports_missing_required_fields() {
        let contract = Contract { required_fields: vec!["id".into()] };
        assert_eq!(validate_records(&contract, &[json!({})]).len(), 1);
    }
}