from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)
