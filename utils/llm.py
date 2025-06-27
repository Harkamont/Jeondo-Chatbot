"""
LLM interaction utilities for the chatbot application using the google-generativeai library.
Handles chat model initialization and message processing.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 20000


# --- Compatibility Layer ---
# This layer mimics the structure of Langchain's message objects
# to ensure app.py's UI code doesn't break after the refactor.
class BaseMessage:
    """A base class for chat messages, used for UI compatibility."""

    def __init__(self, content, role):
        self.content = content
        self.role = role


class HumanMessage(BaseMessage):
    """Represents a message from the user."""

    def __init__(self, content):
        super().__init__(content, "user")


class AIMessage(BaseMessage):
    """Represents a message from the assistant."""

    def __init__(self, content):
        super().__init__(content, "assistant")  # Streamlit uses 'assistant'


# --- End Compatibility Layer ---


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

        genai.configure(api_key=self.api_key)

        self.model_name = model_name
        self.generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        self.system_instruction = None
        self.chat_model = None  # Model will be initialized on first message
        self.conversation_history = []  # Stores native google-genai history
        self.ui_history = []  # Stores compatibility messages for the UI

    def _initialize_model(self):
        """Initializes the model with the system instruction if provided."""
        self.chat_model = genai.GenerativeModel(
            self.model_name,
            generation_config=self.generation_config,
        )

    def add_system_message(self, message: str) -> None:
        """Sets the system message for the chat model."""
        self.system_instruction = message

    def add_user_message(self, message: str) -> None:
        """Adds a user message to the history for the UI."""
        # This method is now primarily for UI display consistency.
        self.ui_history.append(HumanMessage(content=message))

    def get_chat_response(self, user_message: str) -> str:
        """
        Gets a chat response from the Gemini model using the native library.
        Manages both the native conversation history and the UI-compatible history.
        """
        if not self.chat_model:
            self._initialize_model()

        # Prepare the initial history with system instruction if it exists
        initial_history = []
        if self.system_instruction:
            initial_history.append({'role': 'user', 'parts': [{'text': self.system_instruction}]})
            initial_history.append({'role': 'model', 'parts': [{'text': 'ok'}]}) # Model acknowledges system instruction

        # Combine initial history with existing conversation history
        combined_history = initial_history + self.conversation_history

        chat_session = self.chat_model.start_chat(history=combined_history)

        try:
            self.add_user_message(user_message)
            response = chat_session.send_message(user_message)
            ai_response_content = response.text

            self.conversation_history = chat_session.history
            self.ui_history.append(AIMessage(content=ai_response_content))

            return ai_response_content
        except Exception as e:
            error_msg = f"Error getting chat response: {str(e)}"
            print(error_msg)
            self.ui_history.append(AIMessage(content=error_msg))
            return error_msg

    def clear_history(self) -> None:
        """Clears both conversation histories."""
        self.conversation_history = []
        self.ui_history = []
        self.chat_model = None
