#simulate how mcp works internally 
def get_policy(policy_id):
    return f"Policy Details for {policy_id}"
 
def claim_status(claim_id):
    return f"Claim Status for {claim_id}"
 
def calculate_premium(age):
    if age < 30:
        return 5000
    elif age < 50:
        return 8000
    else:
        return 12000
 
 

tool_registry = {
    "get_policy": get_policy,
    "claim_status": claim_status,
    "calculate_premium": calculate_premium
}

 
print("Tools discovered from MCP Server:\n")
 
for tool_name in tool_registry:
    print("•", tool_name)
 

selected_tool = "claim_status"
 
print("\nClient selected tool:", selected_tool)
 
result = tool_registry[selected_tool]("C1001")
 
print("Tool Result:", result)
 

selected_tool = "calculate_premium"
 
print("\nClient selected tool:", selected_tool)
 
result = tool_registry[selected_tool](35)
 
print("Tool Result:", result)
 