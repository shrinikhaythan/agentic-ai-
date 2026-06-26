from autogen import ConversableAgent 
#create 2 agents with no llms 
#pyautogen version 0.3.2
teacher=ConversableAgent(
    name="TeacherAgent",
    llm_config=False,
    human_input_mode="NEVER"
)
student=ConversableAgent(
    name="student agent",
    llm_config=False,
    human_input_mode="NEVER"
)
print("\n teacher sends a question\n")
teacher.send(
    message="what is python",
    recipient=student,
    request_reply=False
)

print("\n student sends an. answer\n ")
student.send(message="python is language",recipient=teacher,request_reply=False)
# chat message: history: {partner_agent:[{"role":.., content: content},....]}, each inner dict both sent and received msges 
for msg in teacher.chat_messages.get(student,[]):
    print(f"{msg["role"]} and {msg["content"]}")

#for student agent , student is the assistant and other agents are users , similarly for all the agents 

