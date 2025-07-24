from agents import Agent, Runner, RunConfig
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import get_key, find_dotenv

api_key = get_key(find_dotenv(), "GEMINI_API_KEY")

agent = Agent(
    name="Basic Agent",
    instructions="you are a helpfull assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)

config = RunConfig(tracing_disabled=True)

result = Runner.run_sync(agent, "What is a capital of japan", run_config=config)
print(result.final_output)
