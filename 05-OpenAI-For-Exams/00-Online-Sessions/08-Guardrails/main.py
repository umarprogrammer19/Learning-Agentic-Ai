from agents import (
    Agent,
    Runner,
    input_guardrail,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
)
import asyncio
from pydantic import BaseModel
from config import model


class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


math_guardrail_agent = Agent(
    name="Math Homework Detector",
    instructions="""  # Instructions to define how the agent should behave
    You are a specialized agent that detects if users are asking for help with math homework.
    
    Analyze the input to determine if it's asking for direct solutions to math problems that appear to be homework.
    
    Consider these as math homework:
    - Explicit requests to solve equations or math problems
    - Questions that ask for step-by-step solutions to math problems
    - Requests that use phrases like "solve for x" or similar academic language
    
    Don't consider these as math homework:
    - General questions about math concepts
    - Requests for explanations of mathematical principles
    - Questions about how to approach a type of problem (without asking for the specific solution)
    - Real-world math applications (like calculating a tip or mortgage payment)
    
    Provide clear reasoning for your decision.
    """,
    output_type=MathHomeWorkOutput,
    model=model,
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input,
) -> GuardrailFunctionOutput:
    result = await Runner.run(math_guardrail_agent, input, context=ctx.context)

    print(result.final_output.is_math_homework)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(
    name="Math agent",
    instructions="You are a math agent. You help students with their math questions.",
    input_guardrails=[math_guardrail],
    model=model,
)


async def main():
    try:
        result = await Runner.run(
            agent,
            "Hello, can you help me solve for x: 2x + 3 = 11?",
        )
        print(f"Response: {result.final_output}...")

    except InputGuardrailTripwireTriggered:
        print("I cant help you with math question")


asyncio.run(main())
