#convert memory to json format 

msgs=memory.chat_memory.messages
report=[
    {
        "role": m.type,
        "content": m.content
    }
    for m in msgs
]
