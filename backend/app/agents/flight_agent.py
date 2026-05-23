import re
from datetime import datetime, timedelta

from app.services.flight_service import search_flights

from app.utils.airport_codes import AIRPORT_CODES

print("FLIGHT AGENT LOADED")


import re


def extract_cities(user_input):

    text = user_input.lower()

    # REMOVE DATES
    text = re.sub(
        r"\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)",
        "",
        text,
    )

    # REMOVE EXTRA WORDS
    remove_words = [
        "find",
        "show",
        "search",
        "get",
        "flight",
        "flights",
        "ticket",
        "tickets",
        "round",
        "trip",
        "return",
        "depart",
        "on",
    ]

    for word in remove_words:

        text = text.replace(word, "")

    text = re.sub(r"\s+", " ", text).strip()

    print("CLEANED TEXT:", text)

    # SUPPORT:
    # from pune to bali
    # to bali from pune

    match = re.search(r"from\s+(.*?)\s+to\s+(.*)", text)

    if match:

        origin_city = match.group(1).strip()

        destination_city = match.group(2).strip()

        return origin_city, destination_city

    match = re.search(r"to\s+(.*?)\s+from\s+(.*)", text)

    if match:

        destination_city = match.group(1).strip()

        origin_city = match.group(2).strip()

        return origin_city, destination_city

    return None, None


def extract_return_date(user_input):

    text = user_input.lower()

    match = re.search(r"return\s+(\d{1,2})\s+([a-zA-Z]+)", text)

    if match:

        day = match.group(1)

        month = match.group(2)

        year = datetime.now().year + 1

        try:

            date_obj = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")

            return date_obj.strftime("%Y-%m-%d")

        except:

            return None

    return None


def extract_passengers(user_input):

    text = user_input.lower()

    # LOOK FOR EXPLICIT PASSENGER WORDS ONLY

    patterns = [
        r"(\d+)\s+passenger",
        r"(\d+)\s+passengers",
        r"for\s+(\d+)",
        r"(\d+)\s+people",
        r"(\d+)\s+traveler",
        r"(\d+)\s+travelers",
        r"(\d+)\s+adult",
        r"(\d+)\s+adults",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            passengers = int(match.group(1))

            # DUFFEL LIMIT
            if passengers > 9:
                passengers = 9

            return passengers

    # DEFAULT
    return 1


def extract_cabin_class(user_input):

    text = user_input.lower()

    if "business" in text:
        return "business"

    if "first class" in text:
        return "first"

    if "premium economy" in text:
        return "premium_economy"

    return "economy"


def extract_departure_date(user_input):

    text = user_input.lower()

    today = datetime.now()

    if "tomorrow" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    match = re.search(r"(\d{1,2})\s+(may|june|july)", text)

    if match:

        day = int(match.group(1))
        month_name = match.group(2)

        months = {"may": 5, "june": 6, "july": 7}

        month = months[month_name]

        date_obj = datetime(2026, month, day)

        return date_obj.strftime("%Y-%m-%d")

    # DEFAULT → TOMORROW
    return (today + timedelta(days=1)).strftime("%Y-%m-%d")


def handle_flight_query(user_input, session):

    print("HANDLE FLIGHT QUERY CALLED")

    origin_city, destination_city = extract_cities(user_input)

    print("Origin City:", origin_city)
    print("Destination City:", destination_city)

    origin = AIRPORT_CODES.get(origin_city)

    destination = AIRPORT_CODES.get(destination_city)

    print("Origin Code:", origin)
    print("Destination Code:", destination)

    if not origin or not destination:

        return {"type": "error", "message": "Unsupported city."}

    departure_date = extract_departure_date(user_input)

    return_date = extract_return_date(user_input)

    print("Return Date:", return_date)

    passengers = extract_passengers(user_input)

    cabin_class = extract_cabin_class(user_input)

    print("Departure Date:", departure_date)
    print("Passengers:", passengers)
    print("Cabin:", cabin_class)

    flights = search_flights(
        origin, destination, departure_date, passengers, cabin_class, return_date
    )
    session["flight_options"] = flights
    print("FINAL FLIGHTS:", flights)

    # HANDLE API ERRORS
    if isinstance(flights, dict) and "error" in flights:

        return {"type": "error", "message": "Unable to fetch flights right now."}

    # ALWAYS RETURN ARRAY
    if not isinstance(flights, list):

        flights = []

    return {"type": "flights", "results": flights}
