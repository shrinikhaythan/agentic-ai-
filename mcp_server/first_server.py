from mcp.server.fastmcp import FastMCP
mcp=FastMCP("insurance server")
@mcp.tool()
def get_policy_details(policy_id:str)->str :
    ''' get insurance policy type by policy id'''
    db={
        "P1001":"health insurance"
    }
    return db.get(policy_id,"policy not found")

if __name__=="__main__ ":
    mcp.run()


    '''
    commanf to execute is
    npx @modelcontextprotocol/inspector python (your file name )
    '''


