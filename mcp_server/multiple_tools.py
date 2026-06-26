from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("Insurance Server")
 
 
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """Get insurance policy details by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return f"Policy {policy_id}: {policies.get(policy_id, 'Not Found')}"
 
 
@mcp.tool()
def claim_status(claim_id: str) -> str:
    """Check the current status of an insurance claim."""
    claims = {
        "C1001": "Approved",
        "C1002": "Under Review",
        "C1003": "Rejected",
    }
    status = claims.get(claim_id, "Claim Not Found")
    return f"Claim {claim_id}: {status}"
 
 
@mcp.tool()
def premium_due(customer_id: str) -> str:
    """Get the premium amount due for a customer."""
    premiums = {
        "CUST001": 5000,
        "CUST002": 3200,
        "CUST003": 7800,
    }
    amount = premiums.get(customer_id)
    if amount is None:
        return f"No premium record found for {customer_id}"
    return f"Premium due for {customer_id}: Rs {amount:,}"
 

if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("\n3 Tools available:")
    print("  1. get_policy(policy_id)")
    print("  2. claim_status(claim_id)")
    print("  3. premium_due(customer_id)")
    print("\nWaiting for MCP client connections (Ctrl+C to stop)...\n")
    mcp.run()