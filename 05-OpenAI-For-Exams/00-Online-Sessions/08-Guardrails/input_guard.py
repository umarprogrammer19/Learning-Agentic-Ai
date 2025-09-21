from agents import (
    Agent,
    Runner,
    input_guardrail,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
)
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


@input_guardrail
async def math_guardrails(
    ctx: RunContextWrapper[MathHomeWorkOutput],
    agent: Agent,
    input: str,
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        math_guardrail_agent,
        input,
        context=ctx.context,
    )

    print(result.final_output.is_math_homework)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(
    name="Final Agent",
    instructions="You are a helpful assistant.",
    input_guardrails=[math_guardrails],
    model=model,
)


async def main():
    try:
        result = await Runner.run(
            agent,
            "What is the value of x in 3x2 + 8x - 9 = 19",
            # "What is javascript?",
        )
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Aukat me reh kar sawal kar........")


asyncio.run(main())
