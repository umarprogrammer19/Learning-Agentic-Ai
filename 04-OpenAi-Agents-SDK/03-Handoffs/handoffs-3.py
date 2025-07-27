from agents import Agent, Runner, function_tool
from main import config


@function_tool
def (origin: str, destination: str, date: str) -> str:
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

@function_tool
def check_refund_eligibility(booking_reference: str) -> str:
    """Check if a flight booking is eligible for a refund"""
    # This is a mock implementation
    refund_policies = {
        "ABC123": {"eligible": True, "refund_amount": "$250", "reason": "Cancellation within 24 hours"},
        "DEF456": {"eligible": False, "reason": "Non-refundable fare"},
        "GHI789": {"eligible": True, "refund_amount": "$150", "reason": "Partial refund due to fare rules"}
    }
    
    if booking_reference in refund_policies:
        policy = refund_policies[booking_reference]
        if policy["eligible"]:
            return f"Booking {booking_reference} is eligible for a refund of ${policy['refund_amount']}. The reason for the refund is: {policy['reason']}"
        else:
            return f"Booking {booking_reference} is not eligible for a refund. The reason is: {policy['reason']}"
    else:
        return f"Booking {booking_reference} is not found in our records."    
     


