


import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# Streamlit Page Config
st.set_page_config(page_title="Kaladi AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for UI
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
    .user-message {background-color: #238636; padding: 10px; border-radius: 10px; color: white; font-weight: bold;}
    .bot-message {background-color: #161b22; padding: 10px; border-radius: 10px; color: white;}
    .stButton>button {background-color: #238636; color: white; border-radius: 10px; padding: 8px 12px; border: none;}
    </style>
""", unsafe_allow_html=True)

# Chatbot Header
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🤖 Kaladi AI Chatbot</h1>", unsafe_allow_html=True)
st.write("<h3 style='color: white;'>💬 Ask me anything!</h3>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# User input
user_input = st.text_input("Type your message...", key="user_input")

if user_input:
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Predefined responses
    lower_input = user_input.lower()

    if any(phrase in lower_input for phrase in [
        "tumhen kisne banaya hai", "who created you","tumhen banaya kisne ha", "tumhen banaya kisne hai","tumhe banaya kisne ha","tumhe banaya kisne hai","tumhen kisne train kya ha","tumhen kisne train kya hai","tumhen kisne train kiya ha","tumhen train kisne kya hai","tumhen train kisne kiya hai","tumhen train kisne kiya ha","tumhe train kisne kiya ha","tumhe train kisne kiya hai", "tumhen train kisne kya ha","tumhe train kisne kya ha","tumhe train kisne kya hai", "tumhen kisne train kiya hai","tumhe kisne train kiya ha","tumhen kisne train kiya hai","who train you","who is train you", "who developed you","who is developed you", "who develop you","who is develop you","tumhen kisne banaya ha","kisne banaya hai tumhen","kisne banaya ha tumhen","kisne banaya hai tumhe","kisne banaya ha tumhe"
    ]):
        bot_reply = "Mujhe Subhan Kaladi ne banaya hai! 🚀\nI was created by Subhan Kaladi! 🔥"

    elif any(phrase in lower_input for phrase in ["who is subhan kaladi", "subhan kaladi kon hai", "subhan kaladi kon ha", "kon hai subhan kaladi","kon ha subhan kaladi"]):
        bot_reply = (
            "Subhan Kaladi is an expert in Agentic AI and Python development. 🧠💡 "
            "He has deep knowledge of Next.js, React.js, and TypeScript. 🚀 "
            "With a strong focus on AI-driven solutions, he is passionate about "
            "building intelligent applications and automation systems. 🏆"
        )

    else:
        # Call Gemini API with timeout handling
        try:
            with st.spinner("Thinking..."):
                model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"temperature": 0.7, "max_output_tokens": 256})
                response = model.generate_content(user_input)
                bot_reply = response.text  
        except Exception as e:
            bot_reply = "⚠️ Sorry, I am facing an issue. Please try again later."

    st.markdown(f"<div class='bot-message'>{bot_reply}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
