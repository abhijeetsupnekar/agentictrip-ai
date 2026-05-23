from typer import prompt
from langsmith import traceable
from app.graph.state import AgentState

from app.agents.router import detect_intent

from app.agents.flight_agent import handle_flight_query
from app.agents.hotel_agent import hotel_agent
from app.agents.booking_agent import handle_flight_booking

from app.agents.weather_agent import (
    weather_agent,
)
from app.agents.nightlife_agent import (
    nightlife_agent,
)

from app.services.llm_service import (
    generate_trip_plan,
)


# NIGHTLIFE NODE
@traceable
def nightlife_node(state: AgentState):

    print("NIGHTLIFE NODE CALLED")

    destination = "Delhi"

    nightlife = nightlife_agent(destination)

    return {
        "nightlife_info": nightlife,
        "messages": ["Nightlife recommendations generated"],
    }


# WEATHER NODE
@traceable
def weather_node(state: AgentState):

    print("WEATHER NODE CALLED")

    destination = "Delhi"

    weather = weather_agent(destination)

    return {
        "weather_info": weather,
        "messages": ["Weather information generated"],
    }


# HOTEL NODE
@traceable
def hotel_node(state: AgentState):

    print("HOTEL NODE CALLED")

    user_input = state["user_input"]

    result = hotel_agent(user_input)

    return {
        "recommended_hotels": result,
        "messages": ["Hotel recommendations generated"],
    }


@traceable
def booking_node(state: AgentState):

    print("BOOKING NODE CALLED")

    flights = state.get("flights", [])

    print("FLIGHTS IN BOOKING NODE:")
    print(flights)

    if not flights:

        return {"messages": ["No flights available for booking"]}

    selected_option = state.get("selected_option", 1)

    booking_result = handle_flight_booking(
        {"flight_options": flights},
        selected_option=selected_option,
    )

    return {
        "booking_details": booking_result,
        "messages": ["Booking summary generated"],
    }


# CONFIRMATION NODE
@traceable
def confirmation_node(state: AgentState):

    print("CONFIRMATION NODE CALLED")

    booking = state.get("booking_details")

    if not booking:

        return {"messages": ["No booking details found"]}

    return {
        "booking_status": "confirmed",
        "messages": ["Booking confirmed successfully"],
    }


# INTENT NODE
@traceable
def intent_node(state: AgentState):

    print("INTENT NODE CALLED")

    user_input = state["user_input"]

    intent = detect_intent(user_input)

    print("QUERY:", user_input)
    print("INTENT:", intent)

    # RESET STATE FOR NEW FLIGHT SEARCH
    if intent == "flight":

        state["flights"] = []

        state["booking_details"] = None

        state["booking_status"] = None

        state["selected_option"] = None

        state["trip_plan"] = None

        state["weather"] = None

        state["nightlife"] = None

        state["hotel_recommendations"] = None

        state["messages"] = []

        state["workflow_stage"] = None

    state["intent"] = intent

    state.setdefault("messages", [])

    state["messages"] = [f"Intent detected: {intent}"]

    return state


# FLIGHT SEARCH NODE
@traceable
def flight_search_node(state: AgentState):

    print("FLIGHT SEARCH NODE CALLED")

    user_input = state["user_input"]

    dummy_session = {}

    result = handle_flight_query(user_input, dummy_session)

    flights = result.get("results", [])

    print("FLIGHTS FOUND:")
    print(flights)

    return {
        "flights": flights,
        "workflow_stage": "waiting_for_selection",
        "messages": ["Flights fetched successfully"],
    }


# RESUME NODE
@traceable
def resume_booking_node(state: AgentState):

    print("RESUME BOOKING NODE CALLED")

    user_input = state["user_input"]

    option = 1

    if "2" in user_input:
        option = 2

    elif "3" in user_input:
        option = 3

    elif "4" in user_input:
        option = 4

    elif "5" in user_input:
        option = 5

    return {
        "selected_option": option,
        "workflow_stage": "booking",
        "messages": [f"User selected option {option}"],
    }


# HOTEL RECOMMENDATION NODE
@traceable
def hotel_recommendation_node(state: AgentState):

    print("HOTEL RECOMMENDATION NODE CALLED")

    destination = "Delhi"

    hotels = hotel_agent(destination)

    return {
        "recommended_hotels": hotels,
        "messages": ["Hotel recommendations generated"],
    }


# PLANNER NODE
@traceable
def planner_node(state: AgentState):

    print("PLANNER NODE CALLED")

    booking = state.get("booking_details", {})

    weather = state.get("weather_info", {})

    hotels = state.get("recommended_hotels", {})

    nightlife = state.get("nightlife_info", {})

    airline = booking.get("airline", "Unknown Airline")

    hotel_name = "Recommended Hotel"

    if hotels.get("results"):

        hotel_name = hotels["results"][0].get("name")

    weather_condition = weather.get(
        "weather",
        {},
    ).get(
        "condition",
        "Normal",
    )

    nightlife_place = "Popular Club"

    if nightlife.get("results"):

        nightlife_place = nightlife["results"][0].get("name")

    destination = state.get("destination")

    if not destination:

        user_input = state.get("user_input", "")

        words = user_input.split()

        destination = words[-1]

    prompt = f"""

Create a detailed 3-day travel itinerary.

Destination: {destination}

Flight Airline:
{airline}

Recommended Hotel:
{hotel_name}

Weather:
{weather_condition}

Nightlife Suggestion:
{nightlife_place}

Generate:
- day-wise itinerary
- food suggestions
- sightseeing
- nightlife
- travel tips
- weather-aware recommendations

"""

    plan = generate_trip_plan(prompt)

    return {"trip_plan": plan, "messages": ["Trip plan generated"]}
