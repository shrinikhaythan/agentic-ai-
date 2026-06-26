
from langchain_groq import ChatGroq 
import os 
os.environ['GROQ_API_KEY'] = ''
llm=ChatGroq(model="qwen/qwen3-32b", temperature=0.7, max_tokens=2000)
response=llm.invoke("Hello, how are you?")
print(response.content)


