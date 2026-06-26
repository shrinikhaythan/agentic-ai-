from autogen import ConversableAgent,GroupChat,GroupChatManager
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

budget_expert=ConversableAgent(
    name="budget expert ",
    system_message="""
you take care of the pricing whenever question about money is asked , depending on situation u need to decide whrther discount should be provided or not and how much discount should be provided """
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=4
)
group_chat=GroupChat(
    agents=[customer_agent,retail_agent,budget_expert],messages=[],max_round=6,speaker_selection_method="round_robin" # instead of rr it can also be auto 
)
#max round , total messages 6
manager=GroupChatManager(groupchat=group_chat,llm_config=llm_config)
#strt convo 
result=customer_agent.initiate_chat(manager,message="""
hii i want to buy some watch please show me good colection , my budget is 1000 rupees"""

)
#conversation history 
messages=group_chat.messages
for msg in messages :
    name=msg.get("name",msg.get("role","?"))
    content=msg.get("content"," ")
    print(name)
    print(content)



