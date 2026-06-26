import os
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel


os.environ['GROQ_API_KEY'] = ' '
llm = ChatGroq(model="qwen-2.5-32b", temperature=0)


class SupportState(TypedDict):
    query: str
    classify: Literal['billing', 'technical', 'general']
    messages: Annotated[list[BaseMessage], add_messages]

@tool
def get_invoice_amount(invoice_id: str) -> str:
    """Look up the total dollar amount due for a specific invoice ID."""
  
    mock_db = {"INV-123": "$150.00", "INV-999": "$2,500.00"}
    return f"The total amount for invoice {invoice_id} is {mock_db.get(invoice_id, 'not found')}."

@tool
def process_refund(invoice_id: str, reason: str) -> str:
    """Initiate a refund process for a given invoice ID and reason."""
    return f"Success: Refund request for {invoice_id} submitted. Reason: '{reason}'."


billing_tools = [get_invoice_amount, process_refund]
# Bind these tools to a specific LLM instance for the billing node
billing_llm = llm.bind_tools(billing_tools)




class ClassificationFormat(BaseModel):
    category: Literal['billing', 'technical', 'general']

def classify_node(state: SupportState) -> dict:
    prompt = f"Classify this customer query into billing, technical, or general:\n\n{state['query']}"
    structured_llm = llm.with_structured_output(ClassificationFormat)
    result = structured_llm.invoke(prompt)
    

    return {
        "classify": result.category,
        "messages": [("user", state['query'])]
    }


def billing_agent_node(state: SupportState) -> dict:

    response = billing_llm.invoke(state["messages"])
    return {"messages": [response]}


def technical_agent_node(state: SupportState) -> dict:
    prompt = "You are a technical support agent. Provide a short helpful response to: " + state['query']
    response = llm.invoke(prompt)
    return {"messages": [response]}

def general_agent_node(state: SupportState) -> dict:
    prompt = "You are a general customer service agent. Provide a short polite response to: " + state['query']
    response = llm.invoke(prompt)
    return {"messages": [response]}



def route_classification(state: SupportState) -> str:
    """Routes to the correct specialized agent node."""
    return state['classify']



workflow = StateGraph(SupportState)


workflow.add_node("classifier", classify_node)
workflow.add_node("billing_agent", billing_agent_node)
workflow.add_node("technical_agent", technical_agent_node)
workflow.add_node("general_agent", general_agent_node)


workflow.add_node("billing_tools", ToolNode(billing_tools))


workflow.set_entry_point("classifier")


workflow.add_conditional_edge(
    "classifier",
    route_classification,
    {
        "billing": "billing_agent",
        "technical": "technical_agent",
        "general": "general_agent"
    }
)


workflow.add_conditional_edge(
    "billing_agent",
    tools_condition,
    {
        "tools": "billing_tools",  # If LLM wants to call a tool, go here
        "__end__": END             # If LLM responds with plain text, stop
    }
)


workflow.add_edge("billing_tools", "billing_agent")


workflow.add_edge("technical_agent", END)
workflow.add_edge("general_agent", END)


graph = workflow.compile()


if __name__ == "__main__":
    
    response = graph.invoke({"query": "How much do I owe for invoice INV-123?"})
    print(response["messages"])

    """
    the format of messages is 
    state={
    ...,"messages":[SystemMessage(content=""),HumanMessage(content=""),AIMessage(content=""),ToolMessage(content="")]

    }
    to accesss :
    state["messages"][index].content 
    
    
    
    
    """