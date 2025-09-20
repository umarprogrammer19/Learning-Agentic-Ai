from agents import (
    Agent,
    Runner,
    function_tool,
    ModelSettings,
)
from config import model
import asyncio
from rich import print

# tool_choice="auto" by default

@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of rectangle"""
    area = length * width
    return f"Area = {length} x {width} = {area} square units"


async def main():

    agent_cold = Agent(
        name="Cold Agent",
        instructions="You are a helpful Assistant",
        model_settings=ModelSettings(temperature=0.1),
        model=model,
    )

    agent_hot = Agent(
        name="Hot Agent",
        instructions="You are a helpful Assistant",
        model_settings=ModelSettings(temperature=1.9),
        model=model,
    )

    question = "Tell Me about AI in two sentance"

    result_cold = await Runner.run(agent_cold, question)
    result_hot = await Runner.run(agent_hot, question)
    # print("Cold:", result_cold.final_output)
    # print("\nHot:", result_hot.final_output)

    agent_required = Agent(
        name="Required Agent",
        instructions="You are a helpful Assistant",
        model_settings=ModelSettings(tool_choice="required"),
        tools=[calculate_area],
        model=model,
    )

    agent_none = Agent(
        name="None Agent",
        instructions="You are a helpful Assistant",
        model_settings=ModelSettings(tool_choice="auto"),
        tools=[calculate_area],
        model=model,
    )

    question = "what is the area of 5x3 rectangle"

    result_required = await Runner.run(agent_required, question)
    result_none = await Runner.run(agent_none, question)
    print("Required:", result_required.final_output)
    print("\nNone:", result_none.final_output)


asyncio.run(main())
