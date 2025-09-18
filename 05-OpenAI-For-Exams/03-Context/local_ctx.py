from agents import Runner, Agent, function_tool, RunContextWrapper
from dataclasses import dataclass
import asyncio
from config import model


@dataclass
class UserInfo:
    name: str
    uid: int


@function_tool
async def fetch_user_age(ctx: RunContextWrapper[UserInfo]) -> str:
    """Fetch the age of user. Call this function to get the user's age information"""
    return f"the user {ctx.context.name} is 17 years old"


async def main():
    user_info = UserInfo("Umar Farooq", 281479824)

    agent = Agent(
        name="Assistant",
        tools=[fetch_user_age],
        model=model,
    )

    result = await Runner.run(
        starting_agent=agent,
        input="What is a age of user",
        context=user_info,
    )

    print(result.final_output)


asyncio.run(main())
