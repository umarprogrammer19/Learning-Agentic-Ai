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

asyncio.run(main())