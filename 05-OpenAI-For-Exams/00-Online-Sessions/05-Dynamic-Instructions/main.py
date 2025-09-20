from agents import Agent, Runner, RunContextWrapper
from dataclasses import dataclass
from config import model


@dataclass
class UserContext:
    name: str
    uid: int


def dynamic_instructions(
    ctx: RunContextWrapper[UserContext], agent: Agent[UserContext]
):
    return f"the user's name is {ctx.context.name}. Help them with thier question"


agent = Agent(
    name="Triage Agent",
    instructions=dynamic_instructions,
    model=model,
)

user_info = UserContext(name="Samiya", uid=872871)

result = Runner.run_sync(
    agent,
    "Hey How are you?",
    context=user_info,
)

print(result.final_output)
