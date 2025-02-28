import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Streamlit Config
st.set_page_config(page_title="Kaladi AI Chatbot", page_icon="🤖", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    body {background-color: #0d1117; color: #ffffff;}
    .stApp {background-color: #0d1117;}
    .stTextInput>div>div>input {
        background-color: #161b22;
        color: white;
        border-radius: 10px;
        border: 1px solid #30363d;
        padding: 10px;
    }
    .user-message {background-color: #238636; padding: 10px; border-radius: 10px; color: white;}
    .bot-message {background-color: #161b22; padding: 10px; border-radius: 10px; color: white;}
    .stButton>button {background-color: #238636; color: white; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# Chat Title
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🤖 Kaladi AI Chatbot</h1>", unsafe_allow_html=True)
st.write("<h3 style='color: white;'>💬 Ask me anything!</h3>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# User Input
user_input = st.text_input("Type your message...", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)

    # Predefined responses
    lower_input = user_input.lower()
    predefined_responses = {
        "who created you": "I was created by Subhan Kaladi! 🚀",
        "who is subhan kaladi": "Subhan Kaladi is an expert in AI and Python development. 🧠💡"
    }
    
    bot_reply = predefined_responses.get(lower_input, None)
    
    if not bot_reply:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        bot_reply = response.text

    st.markdown(f"<div class='bot-message'>{bot_reply}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
