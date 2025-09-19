from agents import Agent, Runner, function_tool
from config import model
from rich import print

# 1) function tool use to perform a agent action

@function_tool
def send_mail(email: str) -> str:
    print(f"Send Mail Tool Caled with email {email}")
    return f"Email Sent to {email} Successfully"


@function_tool
def calculation(a: int, b: int) -> int:
    print(f"calculation Tool Called with number {a,b}")
    return a + b


@function_tool
def calculation(a: int, b: int) -> int:
    print(f"calculation Tool Called with number {a,b}")
    return a - b


@function_tool
def calculation(a: int, b: int) -> int:
    print(f"calculation Tool Called with number {a,b}")
    return a * b


agent = Agent(
    name="Email Assistant",
    instructions="You are a helpful assistant developed for sending a mail, use send_mail to send the emails any emails do you want whether it is empty or not or with invitition or anything else.",
    model=model,
    tools=[send_mail],
)

result = Runner.run_sync(
    agent,
    "This is my friend's email uhhfj0345@gmail.com, I want to send the birthday party invitition scheduled at 21 Sep 5PM on My House could you send the email?",
)

calculation_agent = Agent(
    name="Add Assistant",
    instructions="You are a helpful assistant developed for calculation use calculation tool for calculation if needed other wise use llm for response.",
    model=model,
    tools=[calculation],
)

result_add = Runner.run_sync(
    calculation_agent,
    "9 - 10",
)

print("Final Result", result_add.final_output)
