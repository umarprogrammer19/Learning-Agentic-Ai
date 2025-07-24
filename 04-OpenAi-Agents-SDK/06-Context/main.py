from agents import Agent, Runner, RunConfig, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import get_key, find_dotenv
from dataclasses import dataclass
from typing import List
import asyncio


@dataclass
class Purchase:
    id: str
    name: str
    price: float
    date: str


@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> List[Purchase]:
        if self.uid == "user123":
            return [
                Purchase(id="p1", name="Basic Plan", price=9.99, date="2023-01-15"),
                Purchase(id="p2", name="Premium Add-on", price=4.99, date="2023-02-20"),
            ]
        return []


@function_tool
def get_user_info(context: UserContext) -> str:
    """Get basic information about the current user"""
    user_type = "pro" if context.is_pro_user else "Free"
    print(f"Context in get_user_info: {context}")
    return f"User ID: {context.uid}, Account Type: {user_type}"


@function_tool
async def get_purchase_history(context: UserContext) -> str:
    """Get the purchase history for the current user"""
    print(f"Context in get_purchase_history: {context}")
    purchases = await context.fetch_purchases()
    if not purchases:
        return "No purchase history found."
    result = "Purchase History:\n"
    for p in purchases:
        result += f"- {p.name}: ${p.price} on {p.date}\n"
    return result


@function_tool
async def get_personalized_greeting(context: UserContext) -> str:
    """Get a personalized greeting based on user status"""
    if context.is_pro_user:
        return "Welcome back to our premium service! We value your continued support."
    else:
        return "Welcome! Consider upgrading to our Pro plan for additional features."


api_key = get_key(find_dotenv(), "GEMINI_API_KEY")

user_context_agent = Agent[UserContext](
    name="User Context Agent",
    instructions="""
    You are a helpful assistant that provides personalized responses based on user context.
    Use the available tools to retrieve user information and provide tailored assistance.
    For pro users, offer more detailed information and premium suggestions.
    """,
    tools=[get_user_info, get_purchase_history, get_personalized_greeting],
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)


async def main():
    # Create sample users
    pro_user_context = UserContext(uid="user123", is_pro_user=True)
    free_user_context = UserContext(uid="user456", is_pro_user=False)
    config = RunConfig(tracing_disabled=True)

    # Example with pro user
    print("\n--- Pro User Example ---")
    result = await Runner.run(
        user_context_agent,
        "Tell me about myself and my purchases",
        context=pro_user_context,
        run_config=config,
    )
    print("Response for Pro User:", result.final_output)

    print("\n--- Free User Example ---")
    result = await Runner.run(
        user_context_agent,
        "Tell me about myself and my purchases",
        context=free_user_context,
        run_config=config,
    )
    print("Response for Free User:", result.final_output)


asyncio.run(main())
