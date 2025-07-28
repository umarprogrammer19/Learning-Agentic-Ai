from config import config, model
from agents import (
    Agent,
    Runner,
    input_guardrail,  # Decorator function to apply guardrails (validation checks) on input
    RunContextWrapper,  # Context management for agent execution
    TResponseInputItem,  # Type for individual input items
    GuardrailFunctionOutput,  # Output format of the guardrail function
    InputGuardrailTripwireTriggered,  # Exception raised if guardrail is violated
)
from pydantic import BaseModel
import asyncio


class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


# Initialize the Math Homework detector agent
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
    output_type=MathHomeWorkOutput,  # The output type this agent should return
    model=model,
)


# Define a guardrail function to validate inputs
@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper,  # Context to provide additional information to the agent
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    # Run the math homework detection agent on the input
    result = await Runner.run(math_guardrail_agent, input, context=ctx.context)

    # Print whether the input is considered math homework or not
    print(result.final_output.is_math_homework)

    # Return the result, including whether the guardrail triggered (i.e., if it's math homework)
    return GuardrailFunctionOutput(
        output_info=result.final_output,  # The final output from the agent
        tripwire_triggered=not result.final_output.is_math_homework,  # Whether the guardrail has been triggered
    )


# Define a general math agent that uses the math_guardrail to check inputs
agent = Agent(
    name="Math agent",
    instructions="You are a math agent. You help students with their math questions.",
    input_guardrails=[
        math_guardrail
    ],  # Apply the guardrail to this agent to check if the input is math homework
    model=model,
)


# Main function to simulate the process of running the agent
async def main():
    try:
        # Example of an input asking for help with a math problem
        result = await Runner.run(
            agent,  # Running the agent
            "Hello, can you help me solve for x: 2x + 3 = 11?",  # Math problem input
            run_config=config,  # Configuration settings for running the agent
        )

        # If the guardrail doesn't trip (which is unexpected), print an error message
        print("Guardrail didn't trip - this is unexpected")
        print(f"Response: {result.final_output}...")

    except (
        InputGuardrailTripwireTriggered
    ):  # If the guardrail trips, i.e., math homework is detected
        print("Math homework guardrail tripped")


# Run the main function asynchronously
asyncio.run(main())


