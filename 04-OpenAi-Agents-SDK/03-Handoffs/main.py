from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv  
import os

# [User Input]
#      ↓
# [Triage Agent] → Decides topic (e.g., "math", "history", etc.)
#      ↓
# [History Tutor / Math Tutor] → Executes based on triage decision
#      ↓
# Final Output (sent to user)

# Separately:
# [Manual Routing]
#      ↓
# [FinanceBot / CodeBot] → Decided via keyword rules

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Gemini API key from the environment
api_key = os.getenv("GEMINI_API_KEY")

# Configure AsyncOpenAI to work with Gemini API
# Treats Gemini like an OpenAI-compatible backend
external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini-compatible endpoint
)

# Define the model to use (Gemini 2.0 Flash)
model = OpenAIChatCompletionsModel(
    openai_client=external_client, model="gemini-2.0-flash"
)

# Create a run configuration object for consistent execution
# Includes the model and provider (client), and disables tracing
config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

# Define agents for manual routing (keyword-based logic)

# FinanceBot: Specializes in investment and financial queries
finance_agent = Agent(
    name="FinanceBot", instructions="You only answer finance questions."
)

# CodeBot: Specializes in programming and technical queries
code_agent = Agent(
    name="CodeBot", instructions="You only answer programming questions."
)

# Define agents for automatic handoff via triage agent

# History Tutor: Handles history-related homework questions
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",  # Helps triage agent understand routing
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

# Math Tutor: Handles math-related homework questions
math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
)

# Triage Agent: Delegates to Math or History tutor automatically
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question.",
    handoffs=[history_tutor_agent, math_tutor_agent],  # Handoff targets
)

# Manual Routing Logic
# Function that manually chooses FinanceBot or CodeBot based on keywords

# Explanation: This is a simple, rule-based routing approach.
# Instead of having a triage agent that decides dynamically, 
# we are using a Python function (`route_agent`) that applies keyword checks
# to decide which agent (FinanceBot or CodeBot) should handle the task.

# How it Works:
# 1. The `route_agent(query)` function accepts a user query (e.g., "How to invest in crypto?")
# 2. It checks for keywords like "invest" or "stock" in the input.
#    - If found, it routes the query to the `FinanceBot`
#    - Otherwise, it defaults to the `CodeBot`
# 3. The selected agent is run using `Runner.run_sync`, and the result is returned.

# Use Case:
# - This approach is ideal when the decision-making is simple and based on a few known rules.
# - It is **not dynamic or scalable** like the handoff system — but is fast and lightweight for binary choices.

def route_agent(query: str) -> str:
    """
    Custom routing logic for non-homework questions.
    If the query contains "invest" or "stock", use FinanceBot.
    Otherwise, use CodeBot.
    """
    if "invest" in query.lower() or "stock" in query.lower():
        return Runner.run_sync(finance_agent, query, run_config=config).final_output
    else:
        return Runner.run_sync(code_agent, query, run_config=config).final_output


# Execute and print manual routing examples
print("🔸 Manual Routing:")
print("→", route_agent("How to invest in crypto?"))  # Routed to FinanceBot
print("→", route_agent("How to reverse a string in Python?"))  # Routed to CodeBot

# Execute and print result from triage-based handoff
# TriageAgent will automatically forward the query to the appropriate sub-agent

# Explaination: Handoffs act like helpers for an agent.
# If you need to get two different tasks done (e.g., solving a math problem and learning about history), you wouldn’t expect a single agent to handle both.
# Instead, you’d use a main agent, often called a Triage Agent, whose job is to decide which task goes to which specialized agent.

# How it Works:
# 1. Triage Agent (Main coordinator)
# Accepts the user's input (question/task)

# Determines which domain it belongs to (e.g., Math or History)

# Delegates the task to the most appropriate agent

# 2. Specialist Agents (Helpers)
# These are individual agents responsible for specific domains:

# History Tutor → Handles historical questions

# Math Tutor → Handles mathematical problems

# 3. Handoffs
# When you define handoffs=[...] inside the triage agent, you're telling it:

# “These are the agents you can forward the task to.”

# The triage agent doesn’t do the work itself — it delegates it.
result = Runner.run_sync(
    triage_agent,
    "What is the capital of France?",  # Routed to History Tutor
    run_config=config,
)

# Print the final output
print("\n🔹 Auto-Handoff Routing:")
print("→", result.final_output)
