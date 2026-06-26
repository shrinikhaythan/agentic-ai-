from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
#DtrOutputParser is used to parse the output of the model and convert it into a string format. It is used in the chain to ensure that the output of the model is in a readable format.
import os
from langchain_core.prompts import ChatPromptTemplate
os.environ['GROQ_API_KEY'] = ''
prompt_template=ChatPromptTemplate.from_messages([("system", "You are a helpful assistant. on {domain}"), ("user", " explain the {input}")])
formatted_prompt=prompt_template.format_messages(domain="AI", input="LangChain")
#invoke 
llm=ChatGroq(model="qwen/qwen3-32b", temperature=0, max_tokens=2000)
#invoke method 
chain= prompt_template | llm | StrOutputParser()
response=chain.invoke({"domain": "AI", "input": "LangChain"})
print(response)
print()
#stream method
response_stream=chain.stream({"domain": "AI", "input": "LangChain"})
for chunk in response_stream:
    print(chunk,end="",flush=True)
#batch method 
batch_inputs=[{"domain": "AI", "input": "LangChain"}, {"domain": "AI", "input": "Groq"}]
batch_responses=chain.batch(batch_inputs)
for response in batch_responses:
    print(response)
#batch is involved in parallel processing and is faster than invoke method when we have multiple inputs.




