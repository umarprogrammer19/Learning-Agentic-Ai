from agents import Agent, RunContextWrapper, Runner
from dataclasses import dataclass
from config import model


@dataclass
class UserContext:
    name: str
    uid: int


def dynamic_instructions(
    wrapper: RunContextWrapper[UserContext], agent: Agent[UserContext]
):
    return f"The user's name is {wrapper.context.name}. Help them with their questions."


agent = Agent(
    name="Triage agent",
    instructions=dynamic_instructions,
    model=model,
)

user_info = UserContext(name="Umar Farooq", uid=812739816234)

result = Runner.run_sync(
    agent,
    input="What is my name?",
    context=user_info,
)

print(result.final_output)
