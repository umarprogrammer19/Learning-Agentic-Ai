from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

config = RunConfig(tracing_disabled=True)
agent = Agent(
    name="Assistant",
    instructions="You are a powerful assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)

result = Runner.run_sync(
    agent,
    "Write a haiku about recursion in programming.",
    run_config=config,
)

print(result.final_output)
