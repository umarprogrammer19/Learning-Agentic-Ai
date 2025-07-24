from agents import Agent, Runner, RunConfig, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import get_key, find_dotenv
from dataclasses import dataclass
from typing import List
import asyncio


# Define the 'Purchase' class with the purchase details.
@dataclass
class Purchase:
    id: str
    name: str
    price: float
    date: str


# Define the 'UserContext' class with information about the user.
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> List[Purchase]:
        """Method to simulate fetching the purchase history based on the user's ID."""
        # print(f"Fetching purchases for UID: {self.uid}")

        if self.uid == "user123":  # If the user is a Pro user with uid "user123"
            # Simulate a list of purchases for a Pro user.
            return [
                Purchase(id="p1", name="Basic Plan", price=9.99, date="2023-01-15"),
                Purchase(id="p2", name="Premium Add-on", price=4.99, date="2023-02-20"),
            ]
        return []  # If no match, return an empty list.


# Define the function tool that fetches basic user info.
@function_tool
def get_user_info(context: UserContext) -> str:
    """This tool fetches basic information about the current user."""
    user_type = (
        "Pro" if context.is_pro_user else "Free"
    )  # Determine account type based on the user's pro status.
    return f"User ID: {context.uid}, Account Type: {user_type}"


# Define the function tool that fetches the purchase history.
@function_tool
async def get_purchase_history(context: UserContext) -> str:
    """This tool fetches the purchase history for the current user."""
    purchases = (
        await context.fetch_purchases()
    )  # Fetch the purchase history asynchronously.
    if not purchases:
        return "No purchase history found."  # If no purchases are found, return a default message.

    result = "Purchase History:\n"
    for p in purchases:  # Iterate through the list of purchases.
        result += f"- {p.name}: ${p.price} on {p.date}\n"  # Add each purchase's details to the result string.
    return result


# Define the function tool that generates a personalized greeting.
@function_tool
async def get_personalized_greeting(context: UserContext) -> str:
    """This tool generates a personalized greeting based on user status."""
    if context.is_pro_user:
        return "Welcome back to our premium service! We value your continued support."
    else:
        return "Welcome! Consider upgrading to our Pro plan for additional features."


# Load API keys using dotenv (to secure sensitive information like keys).
api_key = get_key(find_dotenv(), "GEMINI_API_KEY")

# Create the user context agent using the Litellm model.
user_context_agent = Agent[UserContext](
    name="User Context Agent",
    instructions=""" 
    You are a helpful assistant that provides personalized responses based on user context.
    You have already been given the user's context, including their account type (pro or free).
    Do not ask for confirmation about whether the user is a pro. Use the context directly to generate the response:
    - If the user is a pro, provide detailed purchase information and a personalized greeting.
    - If the user is a free user, provide basic information and suggest the pro plan.
    - Use the provided tools to fetch the user's information such as purchase history.
    - Do not send the user ID in the final response, use the data fetched by the tools instead.
    """,  # Instructions for the agent on how to handle requests based on user context.
    tools=[
        get_user_info,
        get_purchase_history,
        get_personalized_greeting,
    ],  # Tools the agent can use to answer questions.
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)


# Main function to execute the agent with different user contexts.
async def main():
    # Create sample users with distinct UIDs
    pro_user_context = UserContext(uid="user123", is_pro_user=True)  # Pro user context.
    free_user_context = UserContext(
        uid="user456", is_pro_user=False
    )  # Free user context.
    config = RunConfig(tracing_disabled=True)

    # Example with pro user
    print("\n--- Pro User Example ---")
    result = await Runner.run(
        user_context_agent,  # Run the user context agent.
        "Tell me about myself and my purchases",  # The query to be asked.
        context=pro_user_context,  # The context passed for the Pro user.
        run_config=config,  # The configuration passed for running.
    )
    print(
        "Response for Pro User:", result.final_output
    )  # Print the result for Pro user.

    # Example with free user
    print("\n--- Free User Example ---")
    result = await Runner.run(
        user_context_agent,  # Run the user context agent.
        "Tell me about myself and my purchases",  # The query to be asked.
        context=free_user_context,  # The context passed for the Free user.
        run_config=config,  # The configuration passed for running.
    )
    print(
        "Response for Free User:", result.final_output
    )  # Print the result for Free user.


asyncio.run(main())
