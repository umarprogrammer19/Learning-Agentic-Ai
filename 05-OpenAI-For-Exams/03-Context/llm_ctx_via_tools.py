from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from config import model

enable_verbose_stdout_logging()


@function_tool
def get_friends_data():
    """For Getting Friends Data"""
    return {
        "name": "Muhammad Ammar",
        "age": 18,
    }


# Update the instructions to clarify the agent's task
agent = Agent(
    name="Assistant",
    instructions=(
        "You are an Assistant. Use the 'get_friends_data' tool to retrieve the friend's data"
    ),
    tools=[get_friends_data],
    model=model,
)

# Run the agent and print results at each step
result = Runner.run_sync(
    starting_agent=agent,
    input="Make a Birthday Wish for my friend",
)

# Print the final output (birthday wish)
print("Final output:", result.final_output)
