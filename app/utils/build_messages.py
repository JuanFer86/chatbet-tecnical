from langchain_core.messages import HumanMessage, ToolMessage
import uuid


def build_messages_from_history(conversation):
    messages = []
    for msg in conversation:
        content = " ".join(msg["parts"])
        if msg["role"] == "user":
            messages.append(HumanMessage(content=content))
        elif msg["role"] == "model":
            messages.append(ToolMessage(tool_call_id=uuid.uuid4(), content=content))
    return messages
