import json
import re

from app.services.azure_openai import generate_ai_response

from app.tools.places_tool import get_hotels, get_restaurants, get_nightlife

from app.tools.weather_tool import get_weather


def planner_agent(user_message, history):

    ai_response = generate_ai_response(user_message, history)

    try:

        cleaned_response = re.sub(r"[\x00-\x1F]+", "", ai_response)

        cleaned_response = (
            cleaned_response.replace("```json", "").replace("```", "").strip()
        )

        parsed_response = json.loads(cleaned_response)
        # HANDLE trip wrapper

        if "trip" in parsed_response:

            parsed_response = parsed_response["trip"]
    except json.JSONDecodeError as e:

        print("PLANNER JSON ERROR:", str(e))

        print("RAW AI RESPONSE:", ai_response)

        return {"type": "error", "message": "Planner returned invalid JSON"}

    destination = parsed_response.get("destination")

    days = parsed_response.get("days")

    if not days:

        days = parsed_response.get("itinerary", [])

    # ENRICH TRIP
    if destination:

        hotels = get_hotels(destination)

        restaurants = get_restaurants(destination)

        nightlife = get_nightlife(destination)

        weather = get_weather(destination)

        parsed_response["hotels"] = hotels[:3]

        parsed_response["restaurants"] = restaurants[:3]

        parsed_response["nightlife"] = nightlife[:3]

        parsed_response["weather"] = weather

    parsed_response["days"] = days

    parsed_response["itinerary"] = days
    parsed_response["type"] = "trip_plan"

    # FLATTEN trip object if present

    if "trip" in parsed_response:

        trip_data = parsed_response["trip"]

        trip_data["type"] = "trip_plan"

        return trip_data

    return parsed_response
