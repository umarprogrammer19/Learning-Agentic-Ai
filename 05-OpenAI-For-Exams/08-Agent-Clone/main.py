from agents import function_tool, Agent, ModelSettings, Runner
from config import model
from rich import print
import asyncio


@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of a rectangle."""
    area = length * width
    return f"Area = {length} × {width} = {area} square units"


@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny and 72°F"


async def main():
    """Learn Agent Cloning with simple examples."""
    print("🧬 Agent Cloning: Create Agent Variants")
    print("=" * 50)

    # 🎯 Example 1: Basic Cloning
    print("\n🎯 Example 1: Basic Cloning")
    print("-" * 40)

    # Base agent
    base_agent = Agent(
        name="Base Assistant",
        instructions="You are a helpful assistant.",
        model_settings=ModelSettings(temperature=0.7),
        model=model,
    )

    # Simple clone
    friendly_agent = base_agent.clone(
        name="Friendly Assistant",
        instructions="You are a very friendly and warm assistant.",
    )

    query = "Hello, how are you?"

    result_base = await Runner.run(base_agent, query)
    result_friendly = await Runner.run(friendly_agent, query)

    print("Base Agent:")
    print(result_base.final_output)
    print("\nFriendly Agent:")
    print(result_friendly.final_output)

    # 🎯 Example 2: Cloning with Different Settings
    print("\n🎯 Example 2: Cloning with Different Settings")
    print("-" * 40)

    # Clone with different temperature
    creative_agent = base_agent.clone(
        name="Creative Assistant",
        instructions="You are a creative writing assistant.",
        model_settings=ModelSettings(temperature=0.9),  # Higher creativity
    )

    precise_agent = base_agent.clone(
        name="PreciseAssistant",
        instructions="You are a precise, factual assistant.",
        model_settings=ModelSettings(temperature=0.1),  # Lower creativity
    )

    query = "Describe a sunset."

    result_creative = await Runner.run(creative_agent, query)
    result_precise = await Runner.run(precise_agent, query)

    print("Creative Agent:")
    print(result_creative.final_output)
    print("\nPrecise Agent:")
    print(result_precise.final_output)

    # 🎯 Example 3: Cloning with Different Tools
    print("\n🎯 Example 3: Cloning with Different Tools")
    print("-" * 40)

    # Base agent with one tool
    base_agent_with_tools = Agent(
        name="Base Assistant",
        tools=[calculate_area],
        instructions="You are a helpful assistant.",
        model=model,
    )

    # Clone with additional tool
    weather_agent = base_agent_with_tools.clone(
        name="Weather Assistant",
        tools=[calculate_area, get_weather],  # New tools list
        instructions="You are a weather and math assistant.",
    )

    # Clone with different tools
    math_agent = base_agent_with_tools.clone(
        name="Math Assistant",
        tools=[calculate_area],  # Same tools
        instructions="You are a math specialist.",
    )

    query = "What's the area of a 5x3 rectangle and the weather in Tokyo?"

    result_weather = await Runner.run(weather_agent, query)
    result_math = await Runner.run(math_agent, query)

    print("Weather Agent:")
    print(result_weather.final_output)
    print("\nMath Agent:")
    print(result_math.final_output)

    # 🎯 Example 4: Multiple Clones from One Base
    print("\n🎯 Example 4: Multiple Clones from One Base")
    print("-" * 40)

    # Create multiple specialized variants
    agents = {
        "Creative": base_agent.clone(
            name="Creative Writer",
            instructions="You are a creative writer. Use vivid language.",
            model_settings=ModelSettings(temperature=0.9),
        ),
        "Precise": base_agent.clone(
            name="Precise Assistant",
            instructions="You are a precise assistant. Be accurate and concise.",
            model_settings=ModelSettings(temperature=0.1),
        ),
        "Friendly": base_agent.clone(
            name="Friendly Assistant",
            instructions="You are a very friendly assistant. Be warm and encouraging.",
        ),
        "Professional": base_agent.clone(
            name="Professional Assistant",
            instructions="You are a professional assistant. Be formal and business-like.",
        ),
    }

    # Test all variants
    query = "Tell me about artificial intelligence."

    for name, agent in agents.items():
        result = Runner.run_sync(agent, query)
        print(f"\n{name} Agent:")
        print(result.final_output[:150] + "...")


asyncio.run(main())
