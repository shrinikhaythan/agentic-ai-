#use a separate agent for runnig tool code 

import os
from typing import Annotated
from autogen import ConversableAgent, GroupChat, GroupChatManager, register_function


GROQ_API_KEY = "API KEY OF MY GROQ, REMOVED IT FOR GITHUB"

config = [{
    "model": "llama3-8b-8192",         
    "base_url": "https://groq.com",
    "api_key": GROQ_API_KEY 
}]

llm_config = {
    "config_list": config,
    "temperature": 0
}


def fetch_real_watch_discount(
    brand: Annotated[str, "The watch brand name mentioned by the retail agent"]
) -> str:
    """Calculates live student discounts for specific Indian watch brands."""
    brand_clean = brand.strip().lower()
    if "sonata" in brand_clean:
        return "SUCCESS: 15% student discount applied. Deducting 150 rupees from the final price."
    return f"SUCCESS: Checked backend database. No specific active student discount code available for {brand}."



customer_agent = ConversableAgent(
    name="customer_agent",
    system_message="""You are a college student in India, trying to buy a smart watch. Your maximum budget is 1000 INR. 
Negotiate properly and buy a watch mentioning your financial constraints. 
If the retail agent suggests a watch model, ALWAYS use the 'fetch_real_watch_discount' tool to check if you get a discount before agreeing to buy!
WHEN YOU ARE COMPLETELY SATISFIED AND THE RETAILER CONFIRMS THE PRICE, SAY 'PURCHASE CONFIRMED' IN ITS OWN LINE.""",
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5
)

retail_agent = ConversableAgent(
    name="retail_agent",
    system_message="""You are an expert store manager in watches in India. You have all knowledge about smart watches under 1000 INR (such as Sonata, etc.).
For every watch option you give, include model name, brand, and baseline cost. Be concise and short.
When the customer says 'PURCHASE CONFIRMED', reply with the total final bill and purchase summary.""",
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5
)

# tool exec agent ,only runs tools code , gemerally no need llm 
tool_executor_agent = ConversableAgent(
    name="tool_executor_agent",
    system_message="You are a silent tool execution engine. You do not talk, you only run code.",
    llm_config=False, 
    human_input_mode="NEVER"
)


register_function(
    fetch_real_watch_discount,
    caller=customer_agent,          
    executor=tool_executor_agent,   
    name="fetch_real_watch_discount",
    description="Checks the store server database if a watch brand qualifies for a student discount."
)


group_chat = GroupChat(
    agents=[customer_agent, retail_agent, tool_executor_agent],
    messages=[],
    max_round=12,
    
    speaker_selection_method="auto" 
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)



chat_result = customer_agent.initiate_chat(
    manager,
    message="Hii, I'm a college student wanting to buy a smartwatch for under 1000 rupees. Please show me your collections.",
    max_turns=6
)



for msg in chat_result.chat_history:
    sender = msg.get("name", msg.get("role", "?"))
    content = msg.get("content", "")
    
   