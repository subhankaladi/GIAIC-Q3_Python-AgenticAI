import os
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from typing import Optional, Dict
from agents.tool import function_tool

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")



provider = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai")


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)
@function_tool("get_waether")

def get_weather(location: str, unit: str = "C") -> str:
    """fetch the weather for a given location return the weather"""

    return f"The weather in {location} is 22 degree{unit}"

agent = Agent(
    name="Greeting Agent",
    instructions="You are a greeting agent,if somone asks about weather the use the get_weather too,to get the wather, Your task is to greet user with a friendly message, when someone says hi you've reply back with salam from subhan kaladi, if someone says bye say Allah faiz from Subhan, when someone asks other than says other greeting than say Subhan Kaladi is here just for greeting, nothing else sorrry",
    model=model,
    tools=get_weather
)
user_question = input("Enter Your Question")
result = Runner.run_sync(agent, user_question)



@cl.oauth_callback

def oauth_callback(
    provider_id: str,
    raw_user_data: dict[str, str],
    token: str,
    default_user: cl.User,
) -> Optional[cl.User]:
    """
    Handle the Oauth callback from GitHub
    Return the user object if authentication is successful, None otherwise.
    """

    print(f"Provider: {provider_id}")
    print(f"User Data: {raw_user_data}")

    return default_user

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello, how can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")  # Fix: correct spelling of "history"
    history.append({"role": "user", "content": message.content})

    formatted_history = []
    for msg in history:  # Fix: corrected history variable name
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    response = model.generate_content(formatted_history)

    response_text = response.text if hasattr(response, "text") else "Sorry, I couldn't understand that."  # Fix: check for response text

    history.append({"role": "assistant", "content": response_text})

    cl.user_session.set("history", history)

    await cl.Message(content=response_text).send()
