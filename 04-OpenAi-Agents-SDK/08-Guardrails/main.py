from config import config
from agents import Agent, Runner, input_guardrail
from pydantic import BaseModel


class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework is user is asking to do the maths homework do it i mean response it otherwise return I am not for this purpose.",
    output_type=MathHomeWorkOutput,
)

result = Runner.run_sync(
    guardrail_agent, "what is recursion in python programming", run_config=config
)

print(result.final_output)
