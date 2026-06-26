from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field # structure validation 
from langchain.tools import Tool # tool for agent to use  
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import ChatMessageHistory,inMemoryChatMessageHistory
from langchain_core.messages import SystemMessage, HumanMessage,AiMessage
import os
os.environ['GROQ_API_KEY'] = ''
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.7, max_tokens=2000)
chat_history = inMemoryChatMessageHistory()
embeddings = OllamaEmbeddings(model="text-embedding-3-small")
vectordb = FAISS.load_local("my_faiss_index", embeddings,allow_dangerous_deserialization=True)
retreiver = vectordb.as_retriever(search_kwargs={"k": 3})
@tool 
def experience_calculator(start_year: str)->str:
    '''check candidate experience'''
    return str(int(2024) - int(start_year)) 
@tool
def eligibility_checker(skills: str)->str:
    '''check candidate eligibility based on skills'''
    required_skills = {"python", "machine learning", "data analysis"}
    candidate_skills = dict.fromkeys(skills.lower().split(","))
    missing_skills = required_skills - set(candidate_skills.keys())
    if not missing_skills:
        return "Eligible"
    else:
        return f"Not Eligible. Missing skills: {', '.join(missing_skills)}"

@tool 
def company_policy_retriver(query: str)->str:
    '''retrive company policy based on query'''
    relevant_docs = retreiver.get_relevant_documents(query)
    context= "\n".join([doc.page_content for doc in relevant_docs])
    prompt=(
        SystemMessage(content="You are a helpful HR assistant. Use the following company policies to answer the question."),
        HumanMessage(content=f"Company Policies:\n{context}\n\nQuestion: {query}
        )
    )
    response = llm.invoke(prompt)
    return response.content

@tool 
def interview_questions(skills: str)->str:
    '''generate interview questions based on candidate skills'''
    prompt=(
        SystemMessage(content="You are a helpful HR assistant. Generate interview questions based on the candidate's skills."),
        HumanMessage(content=f"Candidate Skills: {skills}\n\nGenerate 5 interview questions.")
    )
    response = llm.invoke(prompt)
    return response.content

tools = [experience_calculator, eligibility_checker, company_policy_retriver, interview_questions]
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful HR assistant. Use the following tools to assist with HR tasks."),
    ("user", "Please assist with the following HR task: {input}")
    ("placeholder","{agent_scratchpad}")
])
class Candidate(BaseModel):
    name:str=Field(description="Candidate name")
    experience:int=Field(description="Candidate experience in years")
    skills: List[str]=Field(description="List of candidate skills")
structured_llm=llm.with_structured_output(Candidate)
agent=create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)
agent_executor=AgentExecutor(agent=agent, tools=tools, verbose=True)    
if(user_input.lower()=="resume"):
    user_input="Please review the candidate's resume and provide feedback."
    response=structured_llm.invoke(user_input)
"we are using nlp techniques to minimize llm calls and optimize the agent's performance by using structured output and tool calling capabilities."

