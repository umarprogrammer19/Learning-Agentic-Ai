from agents import Agent, Runner, RunConfig, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Define a run configuration (disables tracing for debugging purposes)
config = RunConfig(tracing_disabled=True)


# Define a Pydantic model to structure the extracted calendar event data
class CalendarEvent(BaseModel):
    name: str  # Event title or name
    date: str  # Event date in YYYY-MM-DD format
    participants: List[str]  # List of people involved
    location: Optional[str] = None  # Optional location
    description: Optional[str] = None  # Optional event description


# Define a basic agent that extracts calendar events from text
calendar_extractor = Agent(
    name="Calendar Event Extractor",
    instructions="""
    You are a specialized assistant that extracts calendar events from text.
    Extract all details about events including:
    - Event name
    - Date (in YYYY-MM-DD format)
    - List of participants
    - Location (if mentioned)
    - Description (if available)

    If multiple events are mentioned, focus on the most prominent one.
    If a detail is not provided in the text, omit that field from your response.
    """,
    output_type=CalendarEvent,  # Expected output is a CalendarEvent object
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)


# Define a tool to validate and standardize date formats
@function_tool
def validate_date(date_str: str) -> str:
    """Validate and format a date string to YYYY-MM-DD format."""
    try:
        # List of accepted date formats
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y"]
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        # If no format matches, return the original string
        return date_str
    except Exception:
        return date_str


# Define an advanced agent that also uses the validate_date tool
advanced_calendar_extractor = Agent(
    name="Advanced Calendar Event Extractor",
    instructions="""
    You are a specialized assistant that extracts calendar events from text.
    Extract all details about events including:
    - Event name
    - Date (in YYYY-MM-DD format, use the validate_date tool to ensure correct formatting)
    - List of participants
    - Location (if mentioned)
    - Description (if available)

    If multiple events are mentioned, focus on the most prominent one.
    If a detail is not provided in the text, omit that field from your response.
    """,
    output_type=CalendarEvent,
    tools=[validate_date],  # Register the date validation tool for use within the agent
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=api_key),
)


# Async function to run and test both agents
async def main():
    # Example input text for the basic calendar extractor
    simple_text = "Let's have a team meeting on 2023-05-15 with Ali, Ammar, and Rabail."

    # More complex input with two events, used to test the advanced extractor
    complex_text = """
    Hi team,

    I'm scheduling our quarterly planning session for May 20, 2023 at the main conference room.
    All department heads (Ali, Ammar, Subhan and Rabail.) should attend. We'll be discussing
    our Q3 objectives and reviewing Q2 performance. Please bring your department reports.

    Also, don't forget about the company picnic on 06/15/2023!
    """

    # Run the basic agent on simple text
    print("\n--- Basic Calendar Extractor Example ---")
    result = await Runner.run(calendar_extractor, simple_text, run_config=config)
    print("Extracted Event:", result.final_output)
    print(f"Event Type: {type(result.final_output)}")

    # Run the advanced agent on the more complex text
    print("\n--- Advanced Calendar Extractor Example ---")
    result = await Runner.run(
        advanced_calendar_extractor, complex_text, run_config=config
    )
    print("Extracted Event:", result.final_output)

    # Access and display the structured event details
    event = result.final_output
    print(f"\nEvent Name: {event.name}")
    print(f"Date: {event.date}")
    print(f"Participants: {', '.join(event.participants)}")
    if event.location:
        print(f"Location: {event.location}")
    if event.description:
        print(f"Description: {event.description}")


# Run the async main function
asyncio.run(main())
