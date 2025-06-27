"""
Main Streamlit application for the LLM chatbot.
Provides a modern chat interface with message history and streaming responses.
"""

import streamlit as st
from utils.llm import ChatbotManager, BaseMessage, AIMessage

context = """
이 편지는 오랜 친구 보현에게 전하는 진심 어린 생일 축하와 위로의 메시지입니다. 재환은 보현이 인생의 무게를 홀로 감당하고 있을까 걱정하며, 예수님을 통해 자신이 받은 위로를 조심스럽게 나눕니다. 과거 종교 이야기에 거절당했던 경험을 기억하며 이번엔 강요 없이 그저 자신의 이야기를 들려주고, 언제든 도움이 필요할 때 연락하길 바란다는 따뜻한 마음을 전합니다.
"""

# Constants
SYSTEM_PROMPT = f"""
You are an AI assistant modeled after a kind pastor. You are currently helping someone named Bohyun,
who recently shared the following message:

\"\"\"{context}\"\"\"

Please keep this in mind as you answer — she is on a spiritual journey and needs gentle guidance.
Please answer in Korean And keep your responses concise and friendly with 존대말 (polite language).
"""
# Page configuration
st.set_page_config(
    page_title="너를 위한 작은 도우미",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown(
    """
<style>
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20px;
    }
    .chat-message .content {
        width: 100%;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables."""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatbotManager()
        st.session_state.chatbot.add_system_message(SYSTEM_PROMPT)
        # Add a welcome message to the chat history on first run
        welcome_message = AIMessage(
            content="안녕하세요! 저는 당신을 돕기 위해 여기에 있는 작은 기독교 도우미입니다. 무엇이든 물어보세요."
        )
        st.session_state.chatbot.ui_history.append(welcome_message)


def display_chat_message(message: BaseMessage):
    """Display a chat message with appropriate styling."""
    with st.chat_message(message.role):
        st.markdown(message.content)


def main():
    """Main application function."""
    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.title("💬 너를 위한, 작은 기독교 도우미")
        st.markdown("---")

        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chatbot.clear_history()
            st.session_state.chatbot.add_system_message(SYSTEM_PROMPT)
            st.rerun()

        st.markdown("---")
        st.markdown(
            """
            # 작은 기독교 도우미
            ### 이 챗봇은 당신을 위해 준비되었습니다.
            Google Gemini 2.5 Flash 모델이 미리 입력된 기독교 지식을 바탕으로 답변합니다.
            * 제작자: 김재환 (johnkimjaehwan@gmail.com)
        """
        )

    # Main chat interface
    st.title("기독교, 교회, 성경, 무엇이든 물어보세요.")

    # Display chat history from the chatbot's UI history
    for message in st.session_state.chatbot.ui_history:
        display_chat_message(message)

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to UI and get response
        display_chat_message(BaseMessage(prompt, "user"))

        # Get and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = st.session_state.chatbot.get_chat_response(prompt)
            message_placeholder.markdown(full_response)


if __name__ == "__main__":
    main()
