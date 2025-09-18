from agents import Agent, Runner, function_tool
from config import model


@function_tool
def get_data(a: int, b: int) -> str:
    print(f"Data Tool Called with number {a ,b}")
    return a + b


@function_tool
def get_data(dish: str, ai_response: str) -> str:
    print(f"Data Tool Called with dish {dish}")
    return f"The Recipe of dish {dish} is {ai_response}"


agent = Agent(
    name="Weather Or Dish Assistant",
    instructions="You are a helpful Agent, You need to answer the user questions.",
    tools=[get_data],
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="what is the recipe of biryani?"
    # input="Tell me 9 + 9",
)

print(result.final_output)
