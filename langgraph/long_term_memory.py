from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage
)

from langchain_groq import ChatGroq

import os


os.environ["GROQ_API_KEY"] = "API "

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chatbot_node(state: ChatState):

   
    messages = state["messages"]

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }


builder = StateGraph(ChatState)

builder.add_node(
    "chatbot",
    chatbot_node
)

builder.set_entry_point("chatbot")
builder.set_finish_point("chatbot")


memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)
config = {
    "configurable": {
        "thread_id": "SHRINI"
    }
}

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="My name is Shrinikhaythan"
            )
        ]
    },
    config=config
)

print(result["messages"][-1].content)


#2ND PROMPT 
result = graph.invoke(
    {
        "messages":[
            HumanMessage(
                content="What is my name?"
            )
        ]
    },
    config=config
)

print(result["messages"][-1].content)