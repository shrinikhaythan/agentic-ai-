from typing import TypedDict,Literal 
from pydantic import BaseModel,Field
from langgraph.graph import StateGraph 
from langchain_groq import ChatGroq 
import os
os.environ['GROQ_API_KEY'] = ''
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.7, max_tokens=2000)
class SupportState(TypedDict):
    query: str
    classify:Literal['billing','technical','general']
    answer:str

#classification node 
class format(BaseModel):
    response : Literal['billing','technical','general']
def classify(state :SupportState)->SupportState:
    """
    classify the given customer query to billing or technical or general"""
    prompt=f"""
you are customer query classification system , read the customer query carefully and classify it as either 
general , billing or technical ,reply only with the exact word, do not any other character 
user query :
{state['query']}


"""
    structured_llm=llm.with_structured_output(format)
    reply=structured_llm.invoke(prompt)
    state['classify']=reply.response
    return state

def billing_agent(state: SupportState)->SupportState:
    state["answer"]="""
the billing is 5000 """
    return state 

def technical_agent(state:SupportState)->SupportState :
    state["answer"]="this is the technical"
    return state 

def general_agent(state:SupportState)->SupportState :
    state["answer"]="this is the general"
    return state

#routing function the routes the state to the desired output , need to return the output based on it
def route(state: SupportState)->SupportState :
    """ based on the input in classify ,it routes the input in that direction"""
    a= state['classify']
    return a 
graph =StateGraph(SupportState)
graph.add_node("classify",classify)
graph.add_node("billing",billing_agent)
graph.add_node("technical",technical_agent)
graph.add_node("general",general_agent)
graph.add_conditional_edge("classify",route,{
    "billing":"billing",
    "technical":"technical",
    "general":"general"
})
graph.set_entry_point("classify")
graph.set_finish_point("billing")
graph.set_finish_point("technical")
graph.set_finish_point("general")
GRAPH=graph.compile()
if __name__=="__main__":
    GRAPH.invoke({
        "query":"i want technical"
    })


        
    #bad practice , each finish point over writes other , so better hv a another node end and connecit to end 
    



