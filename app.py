"""
Main Streamlit application for the LLM chatbot.
Provides a modern chat interface with message history and streaming responses.
"""

import streamlit as st
from utils.llm import ChatbotManager

context = """
내 친구 보현이에게

보현아, 이제 곧 생일이다.
이 편지를 쓰기까지 참 여러 번 망설였어.
내가 무슨 말을 해야 할까, 또 네가 이 편지를 어떻게 받아들일까, 많이 고민했거든.

우리가 중학교 1학년 때 처음 만나서 벌써 20년 가까이 흘렀네.
그동안 자주 만나지는 못해도, 카톡으로 또 전화로 이런 저런 얘기를 나눌 수 있어 참 좋았어.

요즘 많은 고민이 있잖아?
세상살이, 말처럼 쉽지 않지.
하루하루 열심히 살아가는 너를 생각하면 내가 뭐라 쉽게 위로할 수도 없고,
그저 기도하고 있었어.

혹시 요즘은, 혼자 있는 시간이 길어질수록 문득 이런 생각이 들지는 않아?
“이게 다일까?”, “내 인생은 어디로 가고 있는 걸까?”

나도 그런 생각 많이 했거든.
겉으로 보기엔 괜찮아 보여도, 속은 공허하고, 의미 없이 하루를 흘려보내는 것 같을 때.
그럴 때마다 나는 내가 믿는 예수님을 떠올렸어.

사실 15년 전쯤, 내가 예수님 이야기를 꺼냈을 때
네가 단호하게 “다시는 이런 말 하지 마”라고 했던 거 기억해.
그땐 나도 젊고, 내가 전하고 싶은 말만 앞섰던 것 같아.
지금 생각하면 미안하고, 또 고맙기도 해.
그 후에도 널 친구로 마음에 두게 된 건 그만큼 네가 내게 소중한 사람이기 때문이야.

이번엔 무슨 말을 꼭 들려주고 싶다기보다,
그냥 내 이야기를 네게 들려주고 싶었어.

내가 만난 예수님은 사람을 바꾸려고만 하는 분이 아니라,
그냥 있는 그대로 받아주시고 함께 걸어가주시는 분이었어.
누구보다 나를 잘 아시고, 때로는 나보다 더 나를 이해해주시는 분이었지.

보현아,
너무 무거운 짐을 혼자 지고 있다면 잠깐은 내려놔도 괜찮다고,
그 짐을 함께 지고 싶어 하시는 분이 계시다는 걸
그냥 한 번… 기억해줬으면 좋겠어.

지금 이 편지가 또 부담스럽거나 불편하게 느껴진다면 미안해.
하지만 언젠가 네 마음에 “누군가 끝까지 나를 믿어주는 사람이 필요하다”는 생각이 들면
그때는 꼭 나에게 연락 줘.

나는 여전히 너의 친구고, 너를 위해 기도하고 있는 사람이야.

그리고 만약 지금은 나한테 직접 이런 이야기를 꺼내기 어려운 상황이라면,
편지 아래에 있는 작은 친구(챗봇)에게 먼저 말을 걸어봐도 좋아.
내가 쓴 이 편지의 내용을 바탕으로,
너의 궁금함에 조심스럽게, 따뜻하게 대답해줄 거야.

그럼 언제든, 내가 여기 있다는 것만 기억해줘.

너를 여전히 소중히 여기는 친구,
재환 드림
"""

# Constants
SYSTEM_PROMPT = f"""
You are an AI assistant modeled after a kind pastor. You are currently helping someone named Bohyun,
who recently shared the following message:

\"\"\"{context}\"\"\"

Please keep this in mind as you answer — she is on a spiritual journey and needs gentle guidance.
Please answer in Korean.
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
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling."""
    with st.chat_message(role):
        st.markdown(content)


def main():
    """Main application function."""
    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.title("💬 너를 위한, 작은 기독교 도우미")
        st.markdown("---")

        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
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

    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        # Get and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = st.session_state.chatbot.get_chat_response(prompt)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


if __name__ == "__main__":
    main()
