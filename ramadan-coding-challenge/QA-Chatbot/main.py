import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash"
)

@cl.on_chat_start
async def handle_chat_start():
    await cl.Message(content="How can i help you").send()

@cl.on_message
async def handle_message(message: cl.Message):
    prompt = message.content

    response = model.generate_content(prompt)

    response_text = response.text if hasattr(response, "text") else ""

    await cl.Message(content=response_text).send()