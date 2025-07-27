from agents import Agent, Runner, function_tool
from main import config
import asyncio


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


@function_tool
def check_refund_eligibility(booking_reference: str) -> str:
    """Check if a flight booking is eligible for a refund"""
    # This is a mock implementation
    refund_policies = {
        "ABC123": {
            "eligible": True,
            "refund_amount": "$250",
            "reason": "Cancellation within 24 hours",
        },
        "DEF456": {"eligible": False, "reason": "Non-refundable fare"},
        "GHI789": {
            "eligible": True,
            "refund_amount": "$150",
            "reason": "Partial refund due to fare rules",
        },
    }

    if booking_reference in refund_policies:
        policy = refund_policies[booking_reference]
        if policy["eligible"]:
            return f"Booking {booking_reference} is eligible for a refund of ${policy['refund_amount']}. The reason for the refund is: {policy['reason']}"
        else:
            return f"Booking {booking_reference} is not eligible for a refund. The reason is: {policy['reason']}"
    else:
        return f"Booking {booking_reference} is not found in our records."


booking_agent = Agent(
    name="Booking Agent",
    instructions="""
    You are a specialized booking agent for a travel company.
    Help users book flights by collecting necessary information:
    - Origin city
    - Destination city
    - Travel date
    - Number of passengers
    - Class of service (economy, business, first class)
    - Budget (if applicable)
    """,
    tools=[get_available_flights],
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="""
    You are a specialized refund agent for a travel company.
    Help users with refund requests by:
    - Asking for their booking reference
    - Explaining refund policies
    - Checking eligibility using the check_refund_eligibility tool
    
    Be empathetic and clear about the refund process and timelines.
    """,
    tools=[check_refund_eligibility],
)


triage_agent = Agent(
    name="Travel Assistant",
    instructions="""
    You are a helpful travel assistant that can help with various travel-related questions.
    
    If the user asks about booking flights or needs help with a new reservation,
    hand off the conversation to the Booking Agent.
    
    If the user asks about refunds, cancellations, or reimbursements,
    hand off the conversation to the Refund Agent.
    
    For general travel questions, answer directly without handing off.
    Be friendly and helpful in all interactions.
    """,
    handoffs=[booking_agent, refund_agent],
)


async def main():
    # Example conversations
    booking_query = "I need to book a flight from New York to Los Angeles next week"
    refund_query = (
        "I need to cancel my flight and get a refund. My booking reference is ABC123"
    )
    general_query = "What's the weather like in Paris this time of year?"

    # Create a runner
    runner = Runner()

    # Simulate conversations with different queries
    print("\n--- Booking Query Example ---")
    response = await runner.run(triage_agent, booking_query, run_config=config)
    print(f"Initial Query: {booking_query}")
    print(f"Response: {response.final_output}")
    print(
        f"Handled by: {response.agent_name if hasattr(response, 'agent_name') else triage_agent.name}"
    )

    print("\n--- Refund Query Example ---")
    response = await runner.run(triage_agent, refund_query, run_config=config)
    print(f"Initial Query: {refund_query}")
    print(f"Response: {response.final_output}")
    print(
        f"Handled by: {response.agent_name if hasattr(response, 'agent_name') else triage_agent.name}"
    )

    print("\n--- General Query Example ---")
    response = await runner.run(triage_agent, general_query, run_config=config)
    print(f"Initial Query: {general_query}")
    print(f"Response: {response.final_output}")
    print(
        f"Handled by: {response.agent_name if hasattr(response, 'agent_name') else triage_agent.name}"
    )

    # Optional: Interactive mode
    print("\n--- Interactive Mode ---")
    print("Type 'exit' to quit")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break

        response = await runner.run(triage_agent, user_input, run_config=config)
        agent_name = (
            response.agent_name
            if hasattr(response, "agent_name")
            else triage_agent.name
        )
        print(f"\nAgent ({agent_name}): {response.final_output}")


asyncio.run(main())
