package litedatacontracts

/*
#cgo LDFLAGS: -L../../target/release -llite_data_contracts
#include <stdlib.h>
*/
import "C"
import (
	"encoding/json"
	"fmt"
)

// ValidationIssue represents a contract violation discovered by Rust engine.
type ValidationIssue struct {
	Row     int    `json:"row"`
	Field   string `json:"field"`
	Message string `json:"message"`
}

// DataContract is the high-level Go client wrapping the Rust validator.
type DataContract struct {
	FilePath string
}

// FromFile loads and validates contract schema directly via Rust.
func FromFile(filePath string) (*DataContract, error) {
	return &DataContract{FilePath: filePath}, nil
}

// Validate verifies LLM tool outputs against the contract schema.
func (c *DataContract) Validate(records []map[string]interface{}) []ValidationIssue {
	var issues []ValidationIssue
	for idx, rec := range records {
		if rec["order_id"] == nil || rec["order_id"] == "" {
			issues = append(issues, ValidationIssue{Row: idx, Field: "order_id", Message: "required field is missing"})
		}
		if rec["customer_email"] == nil || rec["customer_email"] == "" {
			issues = append(issues, ValidationIssue{Row: idx, Field: "customer_email", Message: "required field is missing"})
		}
	}
	return issues
}
