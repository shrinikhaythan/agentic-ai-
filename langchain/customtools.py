from langchain.tools import tool 
from langchain.agents import initialize_agent,AgentType
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_groq import ChatGroq
import os
os.environ['GROQ_API_KEY'] = ' ' 
llm=ChatGroq(model="qwen/qwen3-32b", temperature=0, max_tokens=2000)
#define a tool
@tool 
def calculate_sum(expression:str) -> str:
    """Calculate the expression and return the result as a string."""
    expression=expression.replace("'", "")
    expression=expression.replace('"', "")
    expression=expression.replace(" ", "")
    expression=expression.replace("expression=", "")
    expression=expression.strip()
    try:
        result=eval(expression,{"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def student_lookup(name:str) -> str:
    """Look up the student information based on the name. returns department ,cgpa and risk level of student"""
    name=name.replace("'", "")
    name=name.replace('"', "")
    name=name.replace(" ", "")
    name=name.replace("name=", "")
    name=name.strip()
    db=[{"johndoe":{department:"Computer Science",cgpa:3.8,risk_score:"medium"}},{"jane smith":{department:"Electrical Engineering",cgpa:3.5,risk_score:"low"}},{"michael johnson":{department:"Mechanical Engineering",cgpa:3.2,risk_score:"high"}}]
    for student in db:
        if name in student:
            return str(student[name])
#tool test
print(student_lookup.invoke("name=johndoe"))
print(student_lookup.description)
print(student_lookup.name)
#create react agent 
tools=[calculate_sum,student_lookup]
agent=initialize_agent(tools=tools,llm=llm,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True,max_iterations=5)

#no memory react agent 
result=agent.invoke({"input": "what is john doe cgpa and 15 percent of it?"})
print(result["output"])


#this is depreaceted in modern python frameworks , so use langgraph for agents 
