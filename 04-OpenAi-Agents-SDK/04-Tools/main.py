from agents import Runner, Agent, function_tool, FunctionTool
from config import config
import json

# You can use any Python function as a tool. The Agents SDK will setup the tool automatically:

# The name of the tool will be the name of the Python function (or you can provide a name)
# Tool description will be taken from the docstring of the function (or you can provide a description)
# The schema for the function inputs is automatically created from the function's arguments
# Descriptions for each input are taken from the docstring of the function, unless disabled


# Example: Define the Calculator Tool using @function_tool decorator
@function_tool
def calculator_tool(query: str) -> str:
    """
    This tool evaluates a math expression passed as a string query.
    The query is evaluated using the `eval()` function to calculate the result.
    """
    try:
        return str(eval(query))
    except Exception as e:
        return f"Error: {str(e)}"


# Create an agent that uses the calculator tool
agent = Agent(
    name="Calculator Agent",
    instructions="You are a math assistant. Use the calculator tool for all math.",
    tools=[calculator_tool],  # Assign the calculator_tool to the agent's list of tools
)

# Display the tool information (including parameter schema)
# Loop through each tool assigned to the agent
for tool in agent.tools:
    # Check if the tool is a function tool
    if isinstance(tool, FunctionTool):
        # Print the tool's name
        print(tool.name)
        # Print the tool's description
        print(tool.description)
        # Print the tool's JSON parameter schema in a readable format
        print(json.dumps(tool.params_json_schema, indent=2))
        # For line break
        print()

# Execute the agent synchronously
# We call the agent with a math query ("what is 2+5") and run it synchronously.
result = Runner.run_sync(
    agent,
    "what is 2+5",
    run_config=config,
)

print(result.final_output)
