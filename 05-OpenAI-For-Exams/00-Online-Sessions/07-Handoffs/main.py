from agents import Agent, Runner
from config import model

# [User Input]
#      ↓
# [Triage Agent] → Decides topic (e.g., "math", "history", etc.)
#      ↓
# [History Tutor / Math Tutor] → Executes based on triage decision
#      ↓
# Final Output (sent to user)

# History Tutor: Handles history-related homework questions
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=model,
)

# Math Tutor: Handles math-related homework questions
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
    model=model,
)

# Triage Agent: Delegates to Math or History tutor automatically
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question.",
    handoffs=[history_tutor_agent, math_tutor_agent],
    model=model,
)

result = Runner.run_sync(
    triage_agent,
    "What is value of x in eq 3x2 + 6x + 10",
)

print("→", result.final_output)
