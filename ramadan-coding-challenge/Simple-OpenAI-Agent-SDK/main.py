import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai")


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

agent = Agent(
    name="Greeting Agent",
    instructions="You are a greeting agent, Your task is to greet user with a friendly message, when someone says hi you've reply back with salam from subhan kaladi, if someone says bye say Allah faiz from Subhan, when someone asks other than says other greeting than say Subhan Kaladi is here just for greeting, nothing else sorrry",
    model=model
)
user_question = input("Enter Your Question")
result = Runner.run_sync(agent, user_question)


