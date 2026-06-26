#bank loan 
import autogen
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



# 2. Define the AI Agents
risk_analyst = autogen.ConversableAgent(
    name="RiskAnalyst",
    system_message=(
        "You are a strict bank Risk Analyst. "
        "Review the customer's loan application, calculate their debt-to-income ratio roughly, "
        "and assess the risk as HIGH, MEDIUM, or LOW. Keep your analysis under 3 sentences."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

compliance_officer = autogen.ConversableAgent(
    name="ComplianceOfficer",
    system_message=(
        "You are a Bank Compliance Officer. "
        "Review the loan purpose. State whether it meets standard legal banking regulations "
        "and flag any suspicious activity. End your message by asking the BankManager for their final decision."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)


bank_manager = autogen.ConversableAgent(
    name="BankManager",
    system_message="You are the final human decision maker. You will read the AI reports and decide to APPROVE or REJECT.",
    llm_config=False, 
    human_input_mode="ALWAYS", 
)

customer = autogen.ConversableAgent(
    name="Customer",
    system_message="You are a customer applying for a loan. You just provide your initial details.",
    llm_config=False,
    human_input_mode="NEVER"
)


groupchat = autogen.GroupChat(
    agents=[customer, risk_analyst, compliance_officer, bank_manager],
    messages=[],
    max_round=6, 
    speaker_selection_method="auto"
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


customer_application = """
LOAN APPLICATION 
Name: Sarah Connor
Amount Requested: $120,000
Monthly Income: $8,500
Purpose: Purchasing heavy machinery for a robotics startup.
"""



customer.initiate_chat(
    manager,
    message=f"Hello, I am applying for a loan. Here are my details: {customer_application}"
)