from agents import Agent, Runner, function_tool
from config import model, WEATHER_API_KEY
import requests


@function_tool
def fetch_weather(city: str) -> str:
    """This function fetches the current weather for a given city. It uses the WeatherAPI to get real-time weather data."""

    result = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    )

    if result.status_code == 200:
        data = result.json()
        return f"The weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."
