from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import asyncio

# [User Input]
#      ↓
# [Triage Agent] → Decides topic (e.g. "finance")
#      ↓
# [FinanceAgent / CodeAgent / TravelAgent] → Returns answer
#      ↓
# Final Output (sent to user)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client, model="gemini-2.0-flash"
)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

# Agent A Financ eBot
finance_agent = Agent(
    name="FinanceBot", instructions="You only answer finance questions."
)

# Agent B: Code bot
code_agent = Agent(
    name="CodeBot", instructions="You only answer programming questions."
)

# Specialist Agent: History
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

# Specialist Agent: Math
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
)

# Triage Agent: Delegates to specialist agents based on question type
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question.",
    handoffs=[history_tutor_agent, math_tutor_agent],
)


# We can use handoffs like these also
def route_agent(query: str):
    if "invest" in query or "stock" in query:
        return Runner.run_sync(finance_agent, query, run_config=config).final_output
    return Runner.run_sync(code_agent, query, run_config=config).final_output


# Usage
print(route_agent("How to invest in crypto?"))
print(route_agent("How to reverse a string in Python?"))


async def main():
    result = await Runner.run(
        triage_agent, "What is the capital of France?", run_config=config
    )
    print("Final Output:", result.final_output)


# Start the async runner
asyncio.run(main())
