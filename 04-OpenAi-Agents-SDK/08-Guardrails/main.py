from config import config
from agents import Agent, Runner, input_guardrail
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

result = Runner.run_sync(
    guardrail_agent, "what is recursion in python programming", run_config=config
)

print(result.final_output)
