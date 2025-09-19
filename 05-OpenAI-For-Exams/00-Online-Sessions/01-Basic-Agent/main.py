from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    enable_verbose_stdout_logging,
)
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()
enable_verbose_stdout_logging()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
#! 1) TypeError: Agent.__init__() missing 1 required positional argument: 'name' it means name is required on Agent Class
#! 2) OpenAI Agents SDK Uses By Default Model gpt-4.1
#! 3) OpenAI Agents SDK Uses "Responses API"
#! 4) OPENAI_API_KEY is not set, skipping trace export
#! 5) enable_verbose_stdout_logging() Show Workflow On Terminal

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

agent = Agent(name="Assistant", model=model)

result = Runner.run_sync(agent, "What is the capital of Pakistan?")

print(result.final_output)
