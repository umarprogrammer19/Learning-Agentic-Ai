import asyncio
from dataclasses import dataclass
from typing import Callable
from agents import Agent, Runner, function_tool, RunContextWrapper, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from config import model
from rich import print

@dataclass
class UserContext:
    username: str
    email: str | None = None


@function_tool()
async def search(ctx: RunContextWrapper[UserContext], query: str) -> str:
    import time

    time.sleep(30)
    return "No results found."


def special_prompt(
    special_context: RunContextWrapper[UserContext],
    agent: Agent[UserContext],
):
    # who is user?
    # which agent
    print(f"User: {special_context.context},\n Agent: {agent.name}\n")
    return f"You are a math expert. User: {special_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."


math_agent: Agent = Agent(
    name="Genius", instructions=special_prompt, model=model, tools=[search]
)


async def call_agent():
    user_context = UserContext(username="Umar Farooq")

    output = Runner.run_streamed(
        starting_agent=math_agent,
        input="search for the best math tutor in my area",
        context=user_context,
    )
    async for event in output.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            print(event.data)


asyncio.run(call_agent())
