from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from config import model
from rich import print


async def main():

    agent = Agent(
        name="Stream Agent",
        instructions="You are a helpful Assistant",
        model=model,
    )

    result = Runner.run_streamed(agent, "write me an essay on cricket for 500 words")

    async for event in result.stream_events():

        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            print(event.data.delta, end="")


asyncio.run(main())
