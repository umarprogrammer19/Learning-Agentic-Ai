from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
)
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client, model="gemini-2.0-flash"
)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)
