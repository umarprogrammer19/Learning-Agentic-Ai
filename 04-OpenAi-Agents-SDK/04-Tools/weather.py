from agents import Agent, Runner, function_tool, RunConfig
from agents.extensions.models.litellm_model import LitellmModel
import requests

from dotenv import find_dotenv, get_key

GEMINI_API_KEY = get_key(find_dotenv(), "GEMINI_API_KEY")


# Define the Weather Fetching Function using function_tool decorator
@function_tool
def getWeather(city: str) -> str:
    """
    This function fetches the current weather for a given city.
    It uses the WeatherAPI to get real-time weather data.
    """
    # Send a GET request to the WeatherAPI to retrieve current weather data
    result = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
    )

    # Check if the API request was successful
    if result.status_code == 200:
        data = result.json()
        return f"The weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."


# Define the Agent that uses the weather tool
agent: Agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful assistant.",
    model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=GEMINI_API_KEY),
    tools=[getWeather],
)


# Define the function to run the agent with a given message
def run(message: str) -> str:
    """
    This function takes a message, runs the agent with that message, and returns the output.
    It adds a "?" to the input to format it as a question for the agent to process.
    """
    # For disable tracing because we dont have an open ai key
    config = RunConfig(tracing_disabled=True)
    # Debugging: Print the message being sent to the agent
    print("Run message", message)
    result = Runner.run_sync(agent, f"{message}?", run_config=config)
    return result.final_output


prompt = input("Enter Prompt: ").strip()
print(run(prompt))
