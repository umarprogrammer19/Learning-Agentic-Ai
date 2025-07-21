from agents import Agent, RunConfig, Runner
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import find_dotenv, get_key

api_key = get_key(find_dotenv(), "GEMINI_API_KEY")

agent = Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)

config = RunConfig(tracing_disabled=True)

result = Runner.run_sync(agent, "what is the capital of islamabad", run_config=config)

print(result.final_output)
