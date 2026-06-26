from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
os.environ['GROQ_API_KEY'] = '' 
llm=ChatGroq(model="qwen/qwen3-32b", temperature=0, max_tokens=2000)
#define output structure 
class OutputStructure(BaseModel):
    name: str = Field( description="The answer to the question")
    department: str = Field( description="The department of the employee")
    cgpa: float = Field( description="The CGPA of the employee")
    risk_score: str=Field(description="the risk score of student: low/medium/high")

#initialize json output parser
json_parser=JsonOutputParser(pydantic_object=OutputStructure)
#this helps to parse the output of the model and convert it into a structured format. It is used in the chain to ensure that the output of the model is in a readable format. based on the schema
profile_prompt_template=ChatPromptTemplate.from_messages([("system", "You are a helpful assistant. give the result in json based on {format_instructions}"), ("user", " give the profile of student based on the input {input}")]).partial(format_instructions=json_parser.get_format_instructions())
chain= profile_prompt_template | llm | json_parser
response=chain.invoke({"input": "Name: John Doe, Department is Computer Science, CGPA is 3.8, struggling"})

print(response)


#ADVANCED : USE with_structured_output(), will give the out as the object of input class 
