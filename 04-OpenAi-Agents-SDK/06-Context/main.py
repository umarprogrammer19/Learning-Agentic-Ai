from agents import Agent, Runner, RunConfig
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import get_key, find_dotenv
from dataclasses import dataclass
from typing import List


@dataclass
class Purchase:
    id: str
    name: str
    price: float
    date: str


@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> List[Purchase]:
        if self.uid == "user123":
            return [
                Purchase(id="p1", name="Basic Plan", price=9.99, date="2023-01-15"),
                Purchase(id="p2", name="Premium Add-on", price=4.99, date="2023-02-20"),
            ]
        return []


api_key = get_key(find_dotenv(), "GEMINI_API_KEY")

agent = Agent(
    name="Basic Agent",
    instructions="you are a helpfull assistant",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)

config = RunConfig(tracing_disabled=True)

result = Runner.run_sync(agent, "What is a capital of japan", run_config=config)
print(result.final_output)
