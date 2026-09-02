package main

import (
	"encoding/json"
	"fmt"
)

// DataContract defines schema constraints for structured tool arguments.
type DataContract struct {
	ContractID string   `json:"contract_id"`
	Required   []string `json:"required_fields"`
}

// ValidateJSON verifies whether the LLM tool call payload adheres to the contract.
func (c *DataContract) ValidateJSON(payload string) (bool, []string) {
	var data map[string]interface{}
	if err := json.Unmarshal([]byte(payload), &data); err != nil {
		return false, []string{"Invalid JSON format"}
	}

	var errors []string
	for _, field := range c.Required {
		if _, exists := data[field]; !exists {
			errors = append(errors, fmt.Sprintf("Missing required field: %s", field))
		}
	}

	return len(errors) == 0, errors
}

func main() {
	fmt.Println("=== Lite Data Contracts - Go Example ===")

	contract := &DataContract{
		ContractID: "create_user_contract",
		Required:   []string{"user_id", "email", "role"},
	}

	// 1. Valid LLM Tool Call output
	validToolCall := `{"user_id": 101, "email": "dev@example.com", "role": "admin"}`
	fmt.Printf("\n[1] Validating Tool Call Payload: %s\n", validToolCall)
	if ok, _ := contract.ValidateJSON(validToolCall); ok {
		fmt.Println(" -> Validation: PASSED. Executing backend tool safely.")
	}

	// 2. Invalid LLM Tool Call output (e.g. hallucinated missing fields)
	invalidToolCall := `{"user_id": 102, "role": "viewer"}`
	fmt.Printf("\n[2] Validating Malformed Payload: %s\n", invalidToolCall)
	if ok, errs := contract.ValidateJSON(invalidToolCall); !ok {
		fmt.Printf(" -> Validation: FAILED with errors: %v\n", errs)
		fmt.Println(" -> Returning error feedback back to LLM for retry.")
	}
}
