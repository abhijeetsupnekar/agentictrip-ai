from app.agents.confirmation_agent import confirm_booking
from app.agents.booking_agent import handle_flight_booking, confirm_booking

from app.agents.hotel_agent import hotel_agent

from app.agents.restaurant_agent import restaurant_agent

from app.agents.weather_agent import weather_agent

from app.agents.planner_agent import planner_agent

from app.agents.flight_agent import handle_flight_query
from app.agents.nightlife_agent import nightlife_agent
from app.memory.session_memory import get_session


def orchestrator(session_id, intent, destination, user_message, history):
    session = get_session(session_id)
    if intent == "hotels":

        return hotel_agent(destination)

    elif intent == "restaurants":

        return restaurant_agent(destination)

    elif intent == "weather":

        return weather_agent(destination)
    elif intent == "flight":
        session["booking_stage"] = "flight_search"
        return handle_flight_query(user_message, session)

    elif intent == "nightlife":

        return nightlife_agent(destination)
    elif intent == "confirm_booking":

        session["booking_stage"] = "confirmation"
        return confirm_booking(session)
    # DEFAULT → TRIP PLANNER
    return planner_agent(user_message, history)
