from agents import Agent, Runner
from pydantic import BaseModel
from config import model
import asyncio


class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    resoning: str


math_guardrail_agent = Agent(
    name="Math Agent",
    instructions="You are a assistant for giving an answer of a math homework or you are here to verify a user input for the input is math related or not..",
    output_type=MathHomeWorkOutput,
    model=model,
)


async def main():
    result = await Runner.run(
        math_guardrail_agent,
        # "What is the value of x in 3x2 + 8x - 9 = 19",
        "What is javascript?",
    )

    print(result.final_output)


asyncio.run(main())
