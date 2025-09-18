from agents import Runner, Agent, function_tool, RunContextWrapper
from dataclasses import dataclass


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
    
