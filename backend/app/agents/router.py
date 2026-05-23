from app.memory.session_memory import (
    get_session,
    update_session,
    clear_session,
)


def detect_intent(query: str):

    query = query.lower().strip()

    print("QUERY:", query)

    # CONFIRM BOOKING
    if query in ["yes", "confirm", "proceed", "okay", "ok"]:

        return "confirm_booking"

    # BOOK SPECIFIC OPTION
    if "book option" in query:

        print("INTENT: book_flight_option")

        return "book_flight_option"

    # HOTELS
    elif "hotel" in query or "hotels" in query or "stay" in query:

        print("INTENT: hotels")

        return "hotels"

    # RESTAURANTS
    elif (
        "restaurant" in query
        or "restaurants" in query
        or "food" in query
        or "eat" in query
    ):

        print("INTENT: restaurants")

        return "restaurants"

    # NIGHTLIFE
    elif (
        "nightlife" in query
        or "club" in query
        or "clubs" in query
        or "party" in query
        or "bar" in query
    ):

        print("INTENT: nightlife")

        return "nightlife"
    # WEATHER
    elif "weather" in query or "temperature" in query or "climate" in query:

        print("INTENT: weather")

        return "weather"

    # BOOK FLIGHT
    elif "book" in query or "reserve" in query:

        print("INTENT: book_flight")

        return "book_flight"

    # FLIGHTS
    elif "flight" in query or "flights" in query or "ticket" in query:

        print("INTENT: flight")

        return "flight"

    # DEFAULT = TRIP PLANNING
    print("INTENT: trip_planning")

    return "trip_planning"
