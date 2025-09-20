from agents import Agent, Runner, function_tool
from config import model


@function_tool
def get_friends_data():
    """For Getting a friend data"""
    return {
        "name": "Muhammad Ammar",
        "age": "18",
    }


agent = Agent(
    name="Context Agent",
    instructions=(
        "You are helpful Assistant use get_friends_data for gettings my friend data"
    ),
    tools=[get_friends_data],
    model=model,
)

result = Runner.run_sync(agent, "Wish a birthday to my friend")

print(result.final_output)
