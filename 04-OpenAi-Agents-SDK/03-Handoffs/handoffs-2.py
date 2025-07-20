from agents import Agent, Runner
from main import config

# Basic Example
nextjs_agent = Agent(
    name="NextJs Agent",
    handoff_description="Specialist agent for Nextjs questions",
    instructions="Answer questions related to the Nextjs",
)

python_agent = Agent(
    name="Python Agent",
    handoff_description="Specialist agent for Python questions",
    instructions="Answer questions related to the Python",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question.",
    handoffs=[nextjs_agent, python_agent],
)

result = Runner.run_sync(
    triage_agent, "What is decorator in python OOPS", run_config=config
)

print(result.final_output)
