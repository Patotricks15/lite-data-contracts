"""Lite Data Contracts - Python LLM Tool Validation Example.

Validates structured LLM tool arguments against contracts before execution.
"""

import json

# In production with compiled PyO3 bindings: from lite_data_contracts import validate_json
# Here demonstrating the caller workflow logic:

def execute_tool_with_contract_check(tool_name: str, arguments_json: str):
    print(f"\n[1] LLM wants to execute tool: '{tool_name}' with args: {arguments_json}")
    
    # Contract schema definition
    order_contract = {
        "required_fields": ["customer_id", "amount", "currency"]
    }
    
    # Validate tool call payload
    args = json.loads(arguments_json)
    records = [args] if isinstance(args, dict) else args
    
    missing_fields = []
    for req in order_contract["required_fields"]:
        if req not in args or args[req] is None:
            missing_fields.append(req)
            
    if missing_fields:
        error_msg = f"Validation Failed: missing required fields {missing_fields}"
        print(f" -> [REJECTED TOOL CALL] {error_msg}")
        return {"status": "error", "message": error_msg}
    
    print(" -> [PASSED] Contract validation succeeded. Executing tool...")
    return {"status": "success", "order_id": "ord_98765"}


def main():
    print("=== Lite Data Contracts - Python Tool Call Example ===")
    
    # Valid LLM tool call
    valid_call = json.dumps({"customer_id": "cust_123", "amount": 150.0, "currency": "USD"})
    execute_tool_with_contract_check("create_order", valid_call)
    
    # Invalid LLM tool call (hallucinated / incomplete arguments)
    invalid_call = json.dumps({"customer_id": "cust_123", "amount": 150.0})
    execute_tool_with_contract_check("create_order", invalid_call)


if __name__ == "__main__":
    main()
