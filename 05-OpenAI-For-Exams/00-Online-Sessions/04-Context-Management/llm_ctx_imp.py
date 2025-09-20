from agents import Agent, Runner
from config import model

agent = Agent(
    name="Context Agent",
    instructions=("You are helpful Assistant"),
    model=model,
)

result = Runner.run_sync(agent, "Wish a birthday to my friend Ammar")

print(result.final_output)
