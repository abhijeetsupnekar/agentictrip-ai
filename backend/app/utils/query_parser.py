from datetime import datetime, timedelta
import dateparser

CITY_AIRPORT_MAP = {
    "pune": "PNQ",
    "mumbai": "BOM",
    "delhi": "DEL",
    "bangalore": "BLR",
    "dubai": "DXB",
    "hyderabad": "HYD",
    "goa": "GOI",
}


def extract_flight_details(query: str):

    query = query.lower()
    passengers = 1
    cabin_class = "economy"
    trip_type = "one_way"
    # PASSENGER EXTRACTION

    for i in range(1, 10):

        if (
            f"{i} passenger" in query
            or f"{i} passengers" in query
            or f"{i} people" in query
            or f"{i} tickets" in query
        ):

            passengers = i
            break

    origin = "BOM"
    destination = "DEL"
    # CABIN CLASS EXTRACTION

    if "business class" in query:

        cabin_class = "business"

    elif "first class" in query:

        cabin_class = "first"

    elif "premium economy" in query:

        cabin_class = "premium_economy"

    elif "economy" in query:

        cabin_class = "economy"

    # ROUND TRIP DETECTION

    if "round trip" in query or "return" in query:

        trip_type = "round_trip"

    # CITY EXTRACTION
    for city, code in CITY_AIRPORT_MAP.items():

        if f"from {city}" in query:
            origin = code

        if f"to {city}" in query:
            destination = code

    # DATE EXTRACTION
    date_keywords = [
        "today",
        "tomorrow",
        "next friday",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next saturday",
        "next sunday",
        "return monday",
        "return tuesday",
        "return wednesday",
        "return thursday",
        "return friday",
        "return saturday",
        "return sunday",
    ]

    detected_date_text = None

    for keyword in date_keywords:

        if keyword in query:
            detected_date_text = keyword
            break

    if detected_date_text:

        parsed_date = dateparser.parse(
            detected_date_text, settings={"PREFER_DATES_FROM": "future"}
        )

    else:

        parsed_date = None

    # FINAL DATE
    if parsed_date:

        departure_date = parsed_date.strftime("%Y-%m-%d")

    else:

        departure_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    return_date = None

    if trip_type == "round_trip":

        return_keywords = [
            "return monday",
            "return tuesday",
            "return wednesday",
            "return thursday",
            "return friday",
            "return saturday",
            "return sunday",
        ]

        for keyword in return_keywords:

            if keyword in query:

                parsed_return = dateparser.parse(
                    keyword.replace("return ", ""),
                    settings={"PREFER_DATES_FROM": "future"},
                )

                if parsed_return:

                    return_date = parsed_return.strftime("%Y-%m-%d")

                    break

    return {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "passengers": passengers,
        "cabin_class": cabin_class,
        "trip_type": trip_type,
        "return_date": return_date,
    }
