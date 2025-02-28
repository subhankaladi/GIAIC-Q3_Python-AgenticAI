# import streamlit as st
# from nltk.chat.util import Chat, reflections

# # Streamlit App Title
# st.title("🤖 AI Chatbot")
# st.write("Ask me anything! I am a simple rule-based AI bot. 💬")

# # Define Pairs of Pattern & Response (Rule-Based)
# pairs = [
#     (r"hi|hello|hey", ["Hello! 👋", "Hey there! How can I help you?"]),
#     (r"how are you?", ["I'm just a bot, but I'm doing great! 😃"]),
#     (r"what is your name?", ["I am an AI Chatbot 🤖"]),
#     (r"who created you?", ["I was created by **Kaladi Developer**🔥"]),
#     (r"what can you do?", ["I can answer your questions and have basic conversations. Try asking me something! 💡"]),
#     (r"bye|goodbye", ["Goodbye! Have a great day! 👋"]),
#     (r"(.*)", ["Sorry, I didn't understand that. Can you try again? 🤔"])
# ]

# # Initialize Chatbot
# chatbot = Chat(pairs, reflections)

# # Chat Interface
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display Chat History
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# # User Input
# user_input = st.chat_input("Type your message...")

# if user_input:
#     # Append User Message
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Get Bot Response
#     response = chatbot.respond(user_input)

#     # Append Bot Response
#     st.session_state.messages.append({"role": "assistant", "content": response})

#     # Display Bot Message
#     st.chat_message("assistant").write(response)




# import google.generativeai as genai
# import streamlit as st

# # Set up Gemini AI API Key
# genai.configure(api_key="AIzaSyARsTdlBsMGRHWfprBvJB5ebgBP0EpIB8c")  # Replace with your actual API key

# # Streamlit App Title
# st.title("🤖 AI Chatbot using Google Gemini API")
# st.write("Ask me anything, and I'll try my best to answer! 💬")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history (Show both User & Bot Messages)
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# # User input
# user_input = st.chat_input("Type your message...")

# if user_input:
#     # **Display User Message**
#     with st.chat_message("user"):
#         st.write(user_input)

#     # Append user message to session
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Get response from Gemini AI
#     model = genai.GenerativeModel("gemini-1.5-flash")  # Use "gemini-1.5-pro" if needed
#     response = model.generate_content(user_input)

#     bot_reply = response.text  # Extract response text

#     # **Display Bot Message**
#     with st.chat_message("assistant"):
#         st.write(bot_reply)

#     # Append bot response to session
#     st.session_state.messages.append({"role": "assistant", "content": bot_reply})




import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv


# # Set up Gemini AI API Key
# genai.configure(api_key="AIzaSyARsTdlBsMGRHWfprBvJB5ebgBP0EpIB8c")  # Replace with your actual API key

load_dotenv()  # Load .env file
API_KEY = os.getenv("GEMINI_API_KEY")  # Fetch API key

genai.configure(api_key=API_KEY)

# Custom Streamlit Page Configuration
st.set_page_config(page_title="Kaladi AI Chatbot", page_icon="🤖", layout="wide")

# **Custom Styling for UI**
custom_css = """
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
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .user-message {
        background-color: #238636;
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: left;
        font-weight: bold;
    }
    .bot-message {
        background-color: #161b22;
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: left;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 10px;
        padding: 8px 12px;
        border: none;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# **Streamlit App Title**
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🤖 Kaladi AI Chatbot</h1>", unsafe_allow_html=True)
st.write("<h3 style='color: white;'>💬 Ask me anything, and I'll try my best to answer!</h3>", unsafe_allow_html=True)

# **Initialize chat history**
if "messages" not in st.session_state:
    st.session_state.messages = []

# **Display chat history (User & Bot messages)**
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# **User input**
user_input = st.text_input("Type your message...", key="user_input")

if user_input:
    # **Display User Message**
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # **Custom Responses**
    lower_input = user_input.lower()

    if any(phrase in lower_input for phrase in [
        "tumhen kisne banaya hai", "who created you", "who developed you","who is developed you", "who develop you","who is develop you","tumhen kisne banaya ha","kisne banaya hai tumhen","kisne banaya ha tumhen","kisne banaya hai tumhe","kisne banaya ha tumhe"
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
        # Get response from Gemini AI
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        bot_reply = response.text  # Extract response text

    # **Display Bot Message**
    st.markdown(f"<div class='bot-message'>{bot_reply}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
