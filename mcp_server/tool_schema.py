
 
import json
 

claim_status_tool = {
    "name": "claim_status",
    "description": "Get insurance claim status",
    "parameters": {
        "claim_id": {
            "type": "string",
            "description": "Claim Identifier"
        }
    }
}
 
print("=" * 60)
print("SCHEMA: claim_status_tool")

print(json.dumps(claim_status_tool, indent=2))
 
 
 
policy_lookup_tool = {
    "name": "get_policy",
    "description": "Retrieve policy details by policy ID",
    "parameters": {
        "policy_id": {
            "type": "string",
            "description": "Unique policy identifier, e.g. P1001"
        }
    }
}
 
premium_calculator_tool = {
    "name": "calculate_premium",
    "description": "Calculate insurance premium based on customer age and policy type",
    "parameters": {
        "age": {
            "type": "integer",
            "description": "Customer age in years"
        },
        "policy_type": {
            "type": "string",
            "description": "Type of policy: Health, Car, or Life"
        }
    }
}
 
print("\n" + "=" * 60)
print("SCHEMA: get_policy")
print("=" * 60)
print(json.dumps(policy_lookup_tool, indent=2))
 
print("\n" + "=" * 60)
print("SCHEMA: calculate_premium (multiple parameters)")
print("=" * 60)
print(json.dumps(premium_calculator_tool, indent=2))
 
 
def validate_tool_schema(schema: dict) -> bool:
    """Check that a tool schema has the minimum required structure."""
    required_top_level = ["name", "description", "parameters"]
 
    for field in required_top_level:
        if field not in schema:
            print(f"  INVALID: missing top-level field '{field}'")
            return False
 
    for param_name, param_def in schema["parameters"].items():
        if "type" not in param_def:
            print(f"  INVALID: parameter '{param_name}' missing 'type'")
            return False
 
    print(f"  VALID: '{schema['name']}' schema is well-formed")
    return True
 
 
print("\n" + "=" * 60)
print("VALIDATING ALL 3 SCHEMAS")
print("=" * 60)
validate_tool_schema(claim_status_tool)
validate_tool_schema(policy_lookup_tool)
validate_tool_schema(premium_calculator_tool)

broken_schema = {"name": "broken_tool", "parameters": {}}
print("\nTesting an intentionally broken schema (missing 'description'):")
validate_tool_schema(broken_schema)
 
 
 