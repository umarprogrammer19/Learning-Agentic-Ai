from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpfull Assistant",
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is the capital of Pakistan",
)

print(result.final_output)
