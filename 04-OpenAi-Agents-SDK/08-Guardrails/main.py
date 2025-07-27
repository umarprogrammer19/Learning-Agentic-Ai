from config import config
from agents import (
    Agent,
    Runner,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    GuardrailFunctionOutput,
)
from pydantic import BaseModel


class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


math_guardrail_agent = Agent(
    name="Math Homework Detector",
    instructions="""
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
)


# @input_guardrail
# async def math_guardrail(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardailFunctionOutput:

result = Runner.run_sync(
    math_guardrail_agent,
    "Find the value of x if 3x + 4 = 9 and x - y = 5 (This is my Math Homework)",
    run_config=config,
)

print(result.final_output)
# If i ask about non math related questions i get these

# input
# what is recursion in python programming

# output
# is_math_homework=False reasoning='The user is asking a general question about a programming concept (recursion) in Python, not for help with a specific math problem or equation.'

# and if i ask this

# input
# Find the value of x if 3x + 4 = 9 and x - y = 5 (This is my Math Homework)

# Output
# is_math_homework=True reasoning='The user explicitly asks to solve for x in a set of equations and indicates that this is a math homework assignment.'
