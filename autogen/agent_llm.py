from autogen import ConversableAgent 
GROQ_API_KEY="API KEY OF MY GROQ, REMOVED IT FOR GITHUB"
config=[{
    "model":"qwen/qwen3-32b",
    "base_url": "https://groq.com",
    "api_key": GROQ_API_KEY 
}] #CAN HV MANY LLMS HERE 
llm_config={
    "config_list": config,
    "temperature": 0
}
customer_agent=ConversableAgent(
    name="customer agent ",
    system_message="""
you are a college student in india , trying to buy a smaert watch, your budget is 1000
negotiate properly and buy a watch mentioning ur financial constraints and buy cheap , cost effective watch 
WHEN YOU ARE SATISFIED ,SAY 'PRUCHASE CONFIRMED' IN ITS OWN LINE 
""",  #the last line is for sys termination veryy imp 
    llm_config=llm_config,
    human_input="NEVER",
    max_consecutive_auto_reply=4 #reply only for 4 consecutive text , has per agent ,safeguard against looping 

)
retail_agent=ConversableAgent(
    name="reatail agent",
    system_message="""
you are an expert in watches in india , u have all knowledge about all watches under 1000
sonata etc, for every watch include model name ,brand , cost ,be concise -short , when customer says 'PURCHASR CONFIRMED',reply with the total bill and purchase summary
""",
llm_config=llm_config,
human_input_mode="NEVER",
max_consecutive_auto_reply=4
)
chat_result=customer_agent.initiate_chat(
    retail_agent,message="""
hii im a student wanting to buy watch for under 1000 rupees , please show me your collections""",max_turns=5

)
print("total message is ",len(chat_result.chat_history)) #it will b max 10
for i,msg in enumerate(chat_result.chat_history): #just for displaying 
    name=msg.get("name",msg.get("role","?"))
    content=msg.get("content"," ")


                                



