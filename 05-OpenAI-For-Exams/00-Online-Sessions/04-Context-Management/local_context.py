from agents import Agent, Runner, function_tool, RunContextWrapper
from dataclasses import dataclass
from config import model
from rich import print
import asyncio

# Local context m secret information store hoti hai jo llm k pass nh jati


@dataclass
class UserInfo:
    name: str
    uid: int


@function_tool
def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Fetch the age of the user"""
    print("Fetch User Age Tool Called With Name", wrapper.context.name)
    return f"The User {wrapper.context.name} is 17 Years Old"


async def main():
    user_info = UserInfo("Umar Farooq", 943435)

    agent = Agent(
        name="User Assistant",
        tools=[fetch_user_age],
        model=model,
    )

    result = await Runner.run(
        agent,
        "what is a age of user",
        context=user_info,
    )

    print(result.final_output)


asyncio.run(main())
