import streamlit as st
import requests
import json

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="Kicky AI",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------
# Custom CSS
# ---------------------------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

h1 {
    color: white;
    text-align: center;
    font-size: 42px;
}

.stCaption {
    text-align: center;
    color: #cbd5e1;
}

.stChatMessage {
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Header
# ---------------------------------
st.title("⚡ Kicky AI")
st.caption("Smart AI Chatbot using Phi-3")

# ---------------------------------
# Session Chat History
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------
# Display Previous Messages
# ---------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------------------------
# Chat Input
# ---------------------------------
prompt = st.chat_input("Ask anything...")

# ---------------------------------
# When User Sends Message
# ---------------------------------
if prompt:

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # ---------------------------------
    # AI Response Streaming
    # ---------------------------------
    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        full_reply = ""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 150
                    }
                },
                stream=True,
                timeout=60
            )

            for line in response.iter_lines():

                if line:
                    chunk = json.loads(line.decode("utf-8"))

                    if "response" in chunk:
                        full_reply += chunk["response"]
                        message_placeholder.write(full_reply + "▌")

            message_placeholder.write(full_reply)

        except Exception:
            full_reply = "⚠️ Unable to connect to Ollama. Please run: ollama serve"
            message_placeholder.error(full_reply)

    # Save AI Reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })