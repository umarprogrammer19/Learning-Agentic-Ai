from agents import Agent, RunConfig, Runner
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import find_dotenv, get_key
import asyncio

# Import ResponseTextDeltaEvent to handle event streams
from openai.types.responses import ResponseTextDeltaEvent

# Load the GEMINI API key from the environment variables
api_key = get_key(find_dotenv(), "GEMINI_API_KEY")


# Define the main asynchronous function
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        # Use the LitellmModel (Gemini 2.0) as the model for the agent
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
    )

    # Setup the RunConfig to disable tracing, Disable tracing to prevent unnecessary logs or traces
    config = RunConfig(tracing_disabled=True)

    # Run the agent asynchronously with streamed response
    result = Runner.run_streamed(
        agent,
        "write an essay on cricket for 300 words",
        run_config=config,
    )

    # Process and print the streamed response events
    # The stream_events() method will yield events as the agent processes the response

    # Iterate over the events generated during the streaming process
    async for event in result.stream_events():
        # Check if the event contains raw response text
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            # Print the text chunk (delta) from the event as it is generated
            print(
                event.data.delta, end="", flush=True
            )  # Print the event data (essay text) without newline, flush output immediately


asyncio.run(main())
