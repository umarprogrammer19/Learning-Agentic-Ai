from agents import Agent, Runner, function_tool
from main import config


@function_tool
def get_available_flights(origin: str, destination: str, date: str) -> str:
    """Get available flights between two cities on a specific date"""
    # This is a mock implementation
    flights = [
        {"flight": "AA123", "departure": "08:00", "arrival": "10:30", "price": "$299"},
        {"flight": "DL456", "departure": "12:15", "arrival": "14:45", "price": "$329"},
        {"flight": "UA789", "departure": "16:30", "arrival": "19:00", "price": "$279"},
    ]
    result = f"Available flight from {origin} to {distination} on {date}:\n"

    for flight in flights:
        result += f"{flight["flight"]} - {flight['departure']} to {flight['arrival']} - ${flight['price']}\n"

    return result


