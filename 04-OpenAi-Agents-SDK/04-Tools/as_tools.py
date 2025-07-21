from agents import Agent, Runner
from config import config

# Define the Spanish Agent
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
)

# Define the French Agent
french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
)

# Define the Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. Use the tools to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            "translate_to_spanish", "Translate the user's message to Spanish"
        ),
        french_agent.as_tool(
            "translate_to_french", "Translate the user's message to French"
        ),
    ],
)

# Print debug info before running the agent
print("Running orchestrator agent...")

# Execute the orchestrator agent synchronously
result = Runner.run_sync(
    orchestrator_agent,
    input="Translate 'Hello, how are you?' in Spanish.",
    run_config=config,
)

# Print the final output for debugging
print("Final Output:", result.final_output)
