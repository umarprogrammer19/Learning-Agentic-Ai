from agents import Agent, Runner
from config import model

agent = Agent(
    name="Assistant",
    instructions="You are a helpful Assistant",
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="wish a happy birthday to my friend Ammar",
)

print(result.final_output)
