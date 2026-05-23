import os
import requests
from dotenv import load_dotenv
from app.utils.query_parser import extract_flight_details
import re


def duration_to_minutes(duration):

    if not duration:
        return 999999

    days = 0
    hours = 0
    minutes = 0

    day_match = re.search(r"(\d+)D", duration)

    hour_match = re.search(r"(\d+)H", duration)

    minute_match = re.search(r"(\d+)M", duration)

    if day_match:
        days = int(day_match.group(1))

    if hour_match:
        hours = int(hour_match.group(1))

    if minute_match:
        minutes = int(minute_match.group(1))

    total_minutes = days * 24 * 60 + hours * 60 + minutes

    return total_minutes


load_dotenv()

DUFFEL_API_TOKEN = os.getenv("DUFFEL_API_TOKEN")

DUFFEL_API_URL = "https://api.duffel.com"

HEADERS = {
    "Authorization": f"Bearer {DUFFEL_API_TOKEN}",
    "Duffel-Version": "v2",
    "Content-Type": "application/json",
}


def get_flights(query: str):

    details = extract_flight_details(query)

    query = query.lower()

    sort_cheapest = "cheapest" in query

    sort_fastest = "fastest" in query

    direct_only = "direct" in query or "nonstop" in query

    origin = details["origin"]

    passengers = details["passengers"]

    cabin_class = details["cabin_class"]

    trip_type = details["trip_type"]

    return_date = details["return_date"]

    destination_code = details["destination"]

    departure_date = details["departure_date"]

    url = f"{DUFFEL_API_URL}" "/air/offer_requests"

    payload = {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination_code,
                    "departure_date": departure_date,
                }
            ],
            "passengers": [{"type": "adult"} for _ in range(passengers)],
            "cabin_class": cabin_class,
            "currency": "INR",
        }
    }

    # ROUND TRIP SUPPORT

    if trip_type == "round_trip" and return_date:

        payload["data"]["slices"].append(
            {
                "origin": destination_code,
                "destination": origin,
                "departure_date": return_date,
            }
        )

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 201:

        return {"error": response.json()}

    result = response.json()

    offers = result.get("data", {}).get("offers", [])

    formatted_flights = []

    for offer in offers[:5]:

        slices = offer.get("slices", [])

        if not slices:
            continue

        # OUTBOUND SLICE

        outbound_slice = slices[0]

        # RETURN SLICE

        return_slice = None

        if len(slices) > 1:

            return_slice = slices[1]

        # OUTBOUND SEGMENTS

        outbound_segments = outbound_slice.get("segments", [])

        if not outbound_segments:
            continue

        # BUILD OUTBOUND ROUTE

        outbound_route = []

        for seg in outbound_segments:

            outbound_route.append(seg["origin"]["iata_code"])

        outbound_route.append(outbound_segments[-1]["destination"]["iata_code"])

        outbound_route = " → ".join(outbound_route)

        # BUILD RETURN ROUTE

        return_route = None

        if return_slice:

            return_segments = return_slice.get("segments", [])

            route = []

            for seg in return_segments:

                route.append(seg["origin"]["iata_code"])

            route.append(return_segments[-1]["destination"]["iata_code"])

            return_route = " → ".join(route)

        # DURATION

        duration = outbound_slice.get("duration", "N/A")

        # STOPS

        stops = len(outbound_segments) - 1

        # PRIMARY SEGMENTS

        first_segment = outbound_segments[0]

        last_segment = outbound_segments[-1]

        formatted_flights.append(
            {
                "airline": offer["owner"]["name"],
                "origin": first_segment["origin"]["iata_code"],
                "destination": last_segment["destination"]["iata_code"],
                "outbound_route": outbound_route,
                "return_route": return_route,
                "departure": first_segment["departing_at"],
                "arrival": last_segment["arriving_at"],
                "duration": duration,
                "stops": stops,
                "cabin_class": cabin_class,
                "passengers": passengers,
                "price": offer["total_amount"],
                "currency": offer["total_currency"],
            }
        )

    # DIRECT FLIGHT FILTER

    if direct_only:

        formatted_flights = [
            flight for flight in formatted_flights if flight["stops"] == 0
        ]

    # SORT CHEAPEST

    if sort_cheapest:

        formatted_flights = sorted(formatted_flights, key=lambda x: float(x["price"]))

    # SORT FASTEST

    if sort_fastest:

        formatted_flights = sorted(
            formatted_flights, key=lambda x: duration_to_minutes(x["duration"])
        )

    return formatted_flights
