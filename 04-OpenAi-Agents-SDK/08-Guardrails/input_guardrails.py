from pydantic import BaseModel, Field
from typing import Optional
from agents import Agent


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool = Field(
        ..., description="Whether the query appears to be math homework"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't math homework"
    )


class CodeAssignmentOutput(BaseModel):
    is_code_assignment: bool = Field(
        ..., description="Whether the query appears to be a coding assignment"
    )
    reasoning: str = Field(
        ..., description="Explanation of why this is or isn't a coding assignment"
    )


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
    output_type=MathHomeworkOutput,
)

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
    output_type=EssayWritingOutput,
)

