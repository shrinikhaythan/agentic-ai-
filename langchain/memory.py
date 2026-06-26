#same as customtools.py
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True,k=5)
#it will keep only last 5 msges 
AgentType.CONVERSATIONAL_REACT_DESCRIPTION
memory=memory 
#full these 2 parameters in initialize agent 
memory.chat_memory.messages
