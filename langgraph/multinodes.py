from typing import TypedDict 
from pydantic import BaseModel, Field 
from langgraph.graph import StateGraph 

#define state 
class StudentState(TypedDict):
    name: str=Field(description="Student's name")
    age: int=Field(description="Student's age")
    marks:float=Field(description="mark of student")
    student_id: int=Field(description="the id of student")
    message: str=Field(description="the final welcome msg")
def create_id(state: StudentState)->StudentState:
    '''
       node :generate a unique id of student 
    '''
    state["student_id"]=4
    return state 
def assign_department(state: StudentState)->StudentState:
    '''
      node : which assigns dept to student based on scored marks
      if marks>90 cse 

    '''
    if(state["marks"]>=90):
        state["department"]="cse"
    return state 
def welcome(state: StudentState)->StudentState:
    ''' node : prints the welcome msg '''
    state["message"]=f"welcome {state["name"]}"
    return state 
#build the graph 

builder= StateGraph(StudentState)
builder.add_node("create_id",create_id)
builder.add_node("assign_department",assign_department)
builder.add_node("msg",welcome)
#add edges - linear chain 
builder.add_edge("create_id","assign_department")
builder.add_edge("assign_department","msg")
builder.set_entry_point("create_id")
builder.set_finish_point("msg")
graph=builder.compile()
if __name__=="__main__":
    response=graph.invoke({"name":"shrini","marks":98})
    print(response["message"])

