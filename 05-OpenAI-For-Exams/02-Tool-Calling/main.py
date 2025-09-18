from agents import Agent, Runner, function_tool
from config import model


@function_tool
def send_mail(email: str) -> str:
    print(f"Got Email: {email}")
    return "Email Send Successfully"


agent = Agent(
    name="Assistant",
    instructions="You are a Assistant to generate content and send mails to user",
    tools=[send_mail],
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="generate and send email to him for birthday party invite at my house on 5PM his email is umarofficial0121@gmail.com send normally this.",
)

print("Result: ",result.final_output)
