from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner
from agents.run import RunConfig
import asyncio

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client, model="gemini-2.0-flash"
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

agent = Agent(
    name="CodeQueen Assistant",
    instructions="You are a Helpful Assistant",
)


async def main():
    result = await Runner.run(
        agent, "Write a Haiku about Recursion in Programming", run_config=config
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
