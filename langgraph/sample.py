from typing import TypedDict #dict with specific types, langgraph uses this for the state
from langgraph.graph import StateGraph #manages state and transitions
class AgentState(TypedDict):
     #define the state structure for the agent
    '''state structure for the agent'''
    input: str  #input 
    greeting: str #output filled by node 

#define nodes - python function 
def generate_greeting(state: AgentState)->AgentState:  #always input and output of node should be the state 
    '''node: greeting generator 
    reads name from state and writes greeting back '''   #doc string is important for langgraph to understand the node's purpose
    name=state["input"]  #read input from state
    state["greeting"]=f"hello {name}, welcome to india !!"
    return state 
#build the graph 

builder=StateGraph(AgentState) #initialize graph with state structure
builder.add_node("greet",generate_greeting) #add node to graph with name and function
#set starting point of the graph
builder.set_entry_point("greet") #set entry point of the graph
#set the ending point 
builder.set_finish_point("greet") #set finish point of the graph
graph=builder.compile() #compile the graph, after compiling we cant change the graph structure
#run the graph 
if __name__=="__main__":
    result=graph.invoke({"input":"shrini"})
    print(result['greeting'])






   

