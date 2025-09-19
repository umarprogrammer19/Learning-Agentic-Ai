from agents import Agent, Runner, function_tool, ModelSettings
from config import model
import asyncio


@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of a rectangle."""
    area = length * width
    return f"Area = {length} × {width} = {area} square units"


async def main():
    """Learn Model Settings with simple examples."""
    # 🎯 Example 1: Temperature (Creativity Control)
    print("❄️🔥 Temperature Settings")
    print("-" * 30)

    agent_cold = Agent(
        name="Cold Agent",
        instructions="You are a helpful assistant.",
        model_settings=ModelSettings(temperature=0.1),
        model=model,
    )

    agent_hot = Agent(
        name="Hot Agent",
        instructions="You are a helpful assistant.",
        model_settings=ModelSettings(temperature=1.9),
        model=model,
    )

    question = "Tell me about AI in 2 sentences"

    # 📝 Note: Gemini temperature range extends to 2.0
    # Notice: Cold = focused, Hot = creative

    print("Cold Agent (Temperature = 0.1):")
    result_cold = await Runner.run(agent_cold, question)
    print(result_cold.final_output)

    print("\nHot Agent (Temperature = 1.9):")
    result_hot = await Runner.run(agent_hot, question)
    print(result_hot.final_output)

    # 🎯 Example 2: Tool Choice
    print("\n🔧 Tool Choice Settings")
    print("-" * 30)

    agent_auto = Agent(
        name="Auto",
        tools=[calculate_area],
        model_settings=ModelSettings(tool_choice="auto"),
        model=model,
    )

    agent_required = Agent(
        name="Required",
        tools=[calculate_area],
        model_settings=ModelSettings(tool_choice="required"),
        model=model,
    )

    agent_none = Agent(
        name="None",
        tools=[calculate_area],
        model_settings=ModelSettings(tool_choice="none"),
        model=model,
    )

    question = "What's the area of a 5x3 rectangle?"

    # 💡 Notice: Auto = decides, Required = must use tool

    print("Auto Tool Choice:")
    result_auto = await Runner.run(agent_auto, question)
    print(result_auto.final_output)

    print("\nRequired Tool Choice:")
    result_required = await Runner.run(agent_required, question)
    print(result_required.final_output)

    print("\nNone Tool Choice:")
    result_none = await Runner.run(agent_none, question)
    print(result_none.final_output)


asyncio.run(main())
