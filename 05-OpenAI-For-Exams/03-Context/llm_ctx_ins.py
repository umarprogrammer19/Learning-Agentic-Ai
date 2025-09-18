from agents import Agent, Runner
from config import model

agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful Assistant"
        "Extra Information"
        "The Weather of karachi is 30 Degree"
        ),
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is a Weather of Karachi?",
)

print(result.final_output)
