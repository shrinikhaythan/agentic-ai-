from langchain_core.prompts import ChatPromptTemplate 
prompt=ChatPromptTemplate.from_messages([("system", "You are a helpful assistant. on {domain}"), ("user", " explain the {input}")])
formatted_prompt=prompt.format_messages(domain="AI", input="LangChain")
print(formatted_prompt)
