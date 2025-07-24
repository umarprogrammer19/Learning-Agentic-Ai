from agents import Agent, Runner, RunConfig, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import get_key, find_dotenv
from dataclasses import dataclass
from typing import List


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
    return f"User ID: {context.uid}, Account Type: {user_type}"


@function_tool
async def get_purchase_history(context: UserContext) -> str:
    """Get the purchase history for the current user"""
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
)


config = RunConfig(tracing_disabled=True)

result = Runner.run_sync(user_context_agent, "What is a capital of japan", run_config=config)
print(result.final_output)
