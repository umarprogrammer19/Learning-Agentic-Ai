from agents import (
    Agent,
    Runner,
    StopAtTools,
    function_tool,
    ModelSettings,
    MaxTurnsExceeded,
)
from config import model


@function_tool
def addition(a: int, b: int) -> int:
    return a + b


@function_tool
def subtraction(a: int, b: int) -> int:
    return a - b


@function_tool
def multiply(a: int, b: int) -> int:
    return a * b


agent = Agent(
    name="Tool Use Agent",
    instructions="You are a assistant designed to give the answers to user questions use addition and subtraction and multiply tools for giving a response",
    tools=[addition, subtraction, multiply],
    model_settings=ModelSettings(tool_choice="none"),
    tool_use_behavior=StopAtTools(stop_at_tool_names=["addition","subtraction"]),
    model=model,
)

# use first tool answer as a final output without llm processing
try:
    result = Runner.run_sync(agent, "What is 7 + 7 and 9 - 10 and 9 * 7", max_turns=1)
    print(result.final_output)
except MaxTurnsExceeded:
    print("Max Turn Exceeded LLM Stop Working")
