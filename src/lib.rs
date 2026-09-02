//! Data-contract validation with allocation-conscious, streaming-friendly APIs.

use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct SchemaField {
    pub name: String,
    #[serde(rename = "type")]
    pub field_type: Option<String>,
    #[serde(default)]
    pub nullable: bool,
    #[serde(default)]
    pub primary_key: bool,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct Contract {
    #[serde(default)]
    pub dataset: String,
    #[serde(default)]
    pub version: Option<u32>,
    #[serde(default)]
    pub required_fields: Vec<String>,
    #[serde(default)]
    pub schema: Vec<SchemaField>,
}

impl Contract {
    /// Loads and validates a contract directly from a YAML or JSON file.
    pub fn from_file(path: impl AsRef<Path>) -> Result<Self, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path.as_ref())?;
        let mut contract: Contract = serde_yaml::from_str(&content)?;
        
        // Populate required_fields from schema non-nullable fields if empty
        if contract.required_fields.is_empty() && !contract.schema.is_empty() {
            contract.required_fields = contract
                .schema
                .iter()
                .filter(|f| !f.nullable)
                .map(|f| f.name.clone())
                .collect();
        }
        Ok(contract)
    }

    /// Validates an array of JSON records against this contract.
    pub fn validate_records<'a>(&self, records: impl IntoIterator<Item = &'a Value>) -> Vec<ValidationIssue> {
        validate_records(self, records)
    }

    /// Validates a raw JSON string of records.
    pub fn validate_json(&self, records_json: &str) -> Result<Vec<ValidationIssue>, serde_json::Error> {
        let records: Vec<Value> = serde_json::from_str(records_json)?;
        Ok(self.validate_records(&records))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
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
        let contract = Contract {
            dataset: "orders".into(),
            version: Some(1),
            required_fields: vec!["id".into()],
            schema: vec![],
        };
        assert_eq!(validate_records(&contract, &[json!({})]).len(), 1);
    }

    #[test]
    fn loads_from_yaml_file() {
        let contract = Contract::from_file("examples/orders-v1.yaml").unwrap();
        assert_eq!(contract.dataset, "analytics.orders");
        assert!(contract.required_fields.contains(&"order_id".to_string()));
        assert!(contract.required_fields.contains(&"customer_email".to_string()));
    }
}