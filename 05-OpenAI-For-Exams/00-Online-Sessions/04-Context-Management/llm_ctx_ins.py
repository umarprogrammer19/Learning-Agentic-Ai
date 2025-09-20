from agents import Agent, Runner
from config import model

agent = Agent(
    name="Context Agent",
    instructions=(
        "You are helpful Assistant"
        "Extra Information:"
        "The Weather of karachi is 30 Degree"
    ),
    model=model,
)

result = Runner.run_sync(agent, "what is the weather of karachi")

print(result.final_output)
