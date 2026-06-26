from typing import TypedDict,Literal,Optional,Annotated ,List 
from langgraph.graph import StateGraph 
from langchain.tools import tool 
from langchain_groq import ChatGroq 
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage,AiMessage,ToolMessage 
from langgraph.graph.message import  add_messages 
from langgraph.prebuilt import ToolNode,tools_condition 
import os
os.environ['GROQ_API_KEY'] = ' '
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.7, max_tokens=2000)
class AgentState(TypedDict):
    
    messages: Annotated[List[BaseMessage],add_messages]

@tool 
def calculator_tool(expression:str)->str :
    """ calculates the numerical execution"""
    return str(eval(expression)) 
@tool 
def weather_api(city:str)->str :
    """ given the city name ,find the wather details from db , if not there , mention,not avaliable"""
    return "condition is sunny"
#llms can only handle string 

tools=[calculator_tool,weather_api]
llm_tool=llm.bind_tools(tools)
def node_agent(state:AgentState)->AgentState:
    """it answers the questions and calls tools based on users necessary """
  

    
    response=llm_tool.invoke(state["messages"])
    state["messages"].append(response) #not good practice , good practice is return {"messages":[response]),but for me its easy to understand 
    
    return state 

def end_node(state:AgentState)->AgentState:
    return state 

builder=StateGraph(AgentState)
builder.add_node("agent",node_agent)
builder.add_node("end",end_node)
builder.add_node("tool_node",ToolNode(tools))
builder.add_conditional_edge("agent",tools_condition,{
    "tools":"tool_node",
    "__end__":"end"
})
builder.add_adge("tool_node","agent")
builder.set_entry_point("agent")
builder.set_finish_point("end")
graph=builder.compile()
if __name__ =="__main__":
    response=graph.invoke(
        {
            "messages":[SystemMessage(content="you are chat bot which has weather and calculator tools, if required use it"),HumanMessage(content=f"tell me the weather in chennai ")]
        }
    )
    print(response["messages"][-1])



    
