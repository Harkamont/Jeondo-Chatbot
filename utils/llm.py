"""
LLM interaction utilities for the chatbot application using Langchain and Gemini.
Handles chat model initialization and message processing.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
)

# Load environment variables
load_dotenv()

# Constants
DEFAULT_MODEL = "gemini-2.5-flash-preview-05-20"
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 1024


class ChatbotManager:
    """Manages Gemini chat model interactions and conversation history."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        self.chat_model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=self.api_key,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        self.conversation_history: List[BaseMessage] = []

    def add_system_message(self, message: str) -> None:
        self.conversation_history.append(SystemMessage(content=message))

    def add_user_message(self, message: str) -> None:
        self.conversation_history.append(HumanMessage(content=message))

    def get_chat_response(self, user_message: str) -> str:
        try:
            self.add_user_message(user_message)
            response = self.chat_model(self.conversation_history)
            self.conversation_history.append(AIMessage(content=response.content))
            return response.content
        except Exception as e:
            error_msg = f"Error getting chat response: {str(e)}"
            print(error_msg)
            return error_msg

    def clear_history(self) -> None:
        self.conversation_history = []
