import streamlit as st
from mistralai import Mistral

# ------------------------------
# Page Title
# ------------------------------
st.title("📌 Free Mistral API Chatbot")

# ------------------------------
# Load API Key from secrets
# ------------------------------
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL"]["api_key"]
except Exception:
    st.error("❗ Add your Mistral API key in .streamlit/secrets.toml")
    st.stop()

if not MISTRAL_API_KEY:
    st.error("❗ API key is missing in secrets.toml")
    st.stop()

# ------------------------------
# Initialize Mistral Client
# ------------------------------
client = Mistral(api_key=MISTRAL_API_KEY)

# ------------------------------
# Initialize Chat History
# ------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------
# Function to Get Mistral Response
# ------------------------------
def get_mistral_response(user_message):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages
    )

    return response.choices[0].message.content

# ------------------------------
# User Input Box
# ------------------------------
user_input = st.text_input("Enter your message:")

# ------------------------------
# When User Sends Message
# ------------------------------
if user_input:
    # Add user message to history
    st.session_state.history.append({
        "role": "user",
        "content": user_input
    })

    # Get AI response
    with st.spinner("🤖 Thinking..."):
        reply_text = get_mistral_response(user_input)

    # Add AI reply to history
    st.session_state.history.append({
        "role": "assistant",
        "content": reply_text
    })

# ------------------------------
# Display Chat History
# ------------------------------
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**AI:** {chat['content']}")

