from pydantic import BaseModel, Field
from typing import Optional, Union, List
from agents import (
    Agent,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    GuardrailFunctionOutput,
    Runner,
)
import asyncio
from config import config, model

# Math
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool = Field(
        ..., description="Whether the query appears to be math homework"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't math homework"
    )

# CodeAssignmentOutput class
class CodeAssignmentOutput(BaseModel):
    is_code_assignment: bool = Field(
        ..., description="Whether the query appears to be a coding assignment"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't a coding assignment"
    )

# for EssayWritingOutput
class EssayWritingOutput(BaseModel):
    is_essay_request: bool = Field(
        ..., description="Whether the query appears to be asking for an essay"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't an essay request"
    )
    subject: Optional[str] = Field(
        None, description="The subject of the essay if applicable"
    )

# Create specialized guardrail agents
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
    model=model,
    output_type=MathHomeworkOutput,
)

# code_guardrail_agent
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
    model=model,
    output_type=CodeAssignmentOutput,
)

essay_guardrail_agent = Agent(
    name="Essay Request Detector",
    instructions="""
    You are a specialized agent that detects if users are asking for help writing essays or papers.
    
    Analyze the input to determine if it's asking for direct writing of essays that appear to be academic assignments.
    
    Consider these as essay requests:
    - Explicit requests to write essays, papers, or reports on specific topics
    - Questions that include word counts, formatting requirements, or citation styles
    - Requests that use phrases like "write an essay about..." or similar academic language
    
    Don't consider these as essay requests:
    - Requests for outlines or brainstorming help
    - Questions about essay structure or writing techniques
    - Requests for feedback on existing writing
    - Professional writing assistance (like resume help)
    
    Provide clear reasoning for your decision and identify the subject if it's an essay request.
    """,
    model=model,
    output_type=EssayWritingOutput,
)


async def main():
    result = await Runner.run(
        math_guardrail_agent,
        "What is the difference between mitosis and meosis?",
        run_config=config,
    )
    print(result.final_output)
    result = await Runner.run(
        code_guardrail_agent,
        "What is the difference between mitosis and meosis?",
        run_config=config,
    )
    print(result.final_output)


# is_math_homework=False reasoning='The question is asking for a general comparison of two biological processes, not for help with a specific math problem. Therefore, it is not math homework.'
# is_code_assignment=False reasoning='The user is asking a general question about biology, not a coding assignment.'

asyncio.run(main())


@input_guardrail
async def math_homework_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str | list[TResponseInputItem]],
) -> GuardrailFunctionOutput:
    """Detect and block requests for math homework help."""
    result = await Runner.run(math_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
        message="I'm sorry, but I can't help with solving math homework problems directly. I'd be happy to explain math concepts or guide you through the problem-solving process instead.",
    )


@input_guardrail
async def code_assignment_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str, List[TResponseInputItem]],
) -> GuardrailFunctionOutput:
    """Detect and block requests for coding assignment solutions."""
    result = await Runner.run(code_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_code_assignment,
        message="I'm sorry, but I can't write code for assignments directly. I'd be happy to explain programming concepts, help debug issues, or guide you through the development process instead.",
    )


@input_guardrail
async def essay_writing_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str, List[TResponseInputItem]],
) -> GuardrailFunctionOutput:
    """Detect and block requests for writing essays."""
    result = await Runner.run(essay_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_essay_request,
        message="I'm sorry, but I can't write essays or papers for academic assignments. I'd be happy to help with brainstorming ideas, creating outlines, or providing feedback on your writing instead.",
    )
