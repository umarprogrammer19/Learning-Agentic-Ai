from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    InputGuardrailTripwireTriggered,
)
from main import config, model
import asyncio


class CodeAssignmentOutput(BaseModel):
    is_coding: bool
    reasoning: str


code_guardrail_agent = Agent(
    name="Code Assignment Detector",
    instructions="""
    You are a specialized agent that detects if users are asking for help with coding assignments.
    
    Analyze the input to determine if it's asking for direct solutions to coding problems that appear to be assignments.
    
    Consider these as code assignments:
    - Explicit requests to write code for specific problems with assignment-like framing
    - Questions that include requirements lists or specifications that sound like coursework
    - Requests that use phrases like "implement a function that..." or similar academic language
    
    Don't consider these as code assignments:
    - General questions about programming concepts
    - Requests for explanations of coding principles
    - Questions about debugging existing code
    - Professional development questions
    
    Provide clear reasoning for your decision.
    """,
    output_type=CodeAssignmentOutput,
    model=model,
)


async def main():
    result = await Runner.run(
        code_guardrail_agent,
        "What is the difference between mitosis and meosis?",
        run_config=config,
    )
    print(result.final_output)


asyncio.run(main())

# If i ask the coding question this returns these output
# Write a program using Python OOP for a basic Learning Management System. This is my assignment.

# Output Of Coding Question
# is_coding=True reasoning="The prompt explicitly states that it is a code assignment and asks for a program to be written using Python's object-oriented programming (OOP) principles for a Learning Management System (LMS)."

# if i ask non-conding question
# What is the difference between mitosis and meosis?

# output of non-conding question
# is_coding=False reasoning='The user is asking a general science question about the difference between mitosis and meiosis, which are biological processes. This is not related to computer programming or coding assignments.'

# See There is is is_coding value is changing according to the prompt

# Now make main agent for answering conding questions


@input_guardrail
async def coding_guardrails(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(code_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_coding,
    )


agent = Agent(
    name="Code agent",
    instructions="You are a coding agent. You help students with their coding questions.",
    input_guardrails=[coding_guardrails],
    model=model,
)


# if i ask non-coding question like What is the difference between mitosis and meosis? so the is_conding is False and not opearator do this True If true, an InputGuardrailTripwireTriggered exception is raised, so you can appropriately respond to the user or handle the exception. This will print Sorry i cant answer this question
async def run():
    try:
        result = await Runner.run(
            agent,
            "What is the difference between mitosis and meosis?",
            run_config=config,
        )
        print(f"Response: {result.final_output}...")
    except InputGuardrailTripwireTriggered:
        print("Sorry i cant answer this question")


asyncio.run(run())
