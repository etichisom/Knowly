from app.llm.client import client
from app.services.chat_service import ChatService


def get_chat_service():
    return ChatService(llm=client)