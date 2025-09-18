from config import model
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging

enable_verbose_stdout_logging()


@function_tool
def add(a: int, b: int) -> int:
    print(f"Add Tool Called with numbers {a} and {b}")
    return a + b


@function_tool
def sub(a: int, b: int) -> int:
    print(f"Sub Tool Called with numbers {a} and {b}")
    return a - b


@function_tool
def mul(a: int, b: int) -> int:
    print(f"Mul Tool Called with numbers {a} and {b}")
    return a * b


@function_tool
def div(a: int, b: int) -> int:
    print(f"Div Tool Called with numbers {a} and {b}")
    return int(a / b)


agent = Agent(
    name="Calculation Agent",
    instructions="You are a Helpful Calculation Agent to perform users calculations.",
    tools=[add, sub, mul, div],
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="Tell me the answer of 1 add 5 , 7 subtracted by 4, 8 multiply by 8, 9 devide by 3",
)

print(result.final_output)
