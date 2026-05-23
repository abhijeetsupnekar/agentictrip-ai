import os
import requests
from dotenv import load_dotenv

load_dotenv()
print("FLIGHT SERVICE FILE LOADED")

DUFFEL_API_TOKEN = os.getenv("DUFFEL_API_TOKEN")
DUFFEL_API_URL = os.getenv("DUFFEL_API_URL")

HEADERS = {
    "Authorization": f"Bearer {DUFFEL_API_TOKEN}",
    "Duffel-Version": "v2",
    "Content-Type": "application/json",
}


def search_flights(
    origin,
    destination,
    departure_date,
    adults=1,
    cabin_class="economy",
    return_date=None,
):

    url = f"{DUFFEL_API_URL}/air/offer_requests"

    payload = {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                }
            ],
            "passengers": [{"type": "adult"} for _ in range(adults)],
            "cabin_class": "economy",
        }
    }
    if return_date:

        payload["data"]["slices"].append(
            {
                "origin": destination,
                "destination": origin,
                "departure_date": return_date,
            }
        )

    print("SEARCHING FLIGHTS:")
    print("Origin:", origin)
    print("Destination:", destination)
    print("Departure:", departure_date)

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 201:
        return {"error": response.json()}

    result = response.json()

    offers = result.get("data", {}).get("offers", [])

    formatted_offers = []

    for offer in offers[:5]:
        if not offer.get("slices"):
            continue

        owner = offer.get("owner", {}).get("name")

        total_amount = offer.get("total_amount")

        slices = offer.get("slices", [])
        return_route = None
        return_departure = None
        return_arrival = None

        if slices:

            segments = slices[0].get("segments", [])

            if segments:

                route_points = []

                for seg in segments:

                    origin_code = seg["origin"]["iata_code"]

                    destination_code = seg["destination"]["iata_code"]

                    if not route_points:
                        route_points.append(origin_code)

                    route_points.append(destination_code)

                outbound_route = " → ".join(route_points)

                first_segment = segments[0]

                last_segment = segments[-1]

                # RETURN FLIGHT

                # RETURN FLIGHT

                if len(slices) > 1:

                    return_segments = slices[1].get("segments", [])

                    if return_segments:

                        return_points = []

                        for seg in return_segments:

                            origin_code = seg["origin"]["iata_code"]

                            destination_code = seg["destination"]["iata_code"]

                            if not return_points:
                                return_points.append(origin_code)

                            return_points.append(destination_code)

                        return_route = " → ".join(return_points)

                        return_departure = return_segments[0]["departing_at"]

                        return_arrival = return_segments[-1]["arriving_at"]

                        if (
                            not outbound_route
                            or not first_segment.get("departing_at")
                            or not last_segment.get("arriving_at")
                        ):

                            continue

                formatted_offers.append(
                    {
                        "type": "flights",
                        "airline": owner or "Unknown Airline",
                        "outbound_route": outbound_route or "N/A",
                        "return_route": return_route,
                        "return_departure": return_departure,
                        "return_arrival": return_arrival,
                        "departure": first_segment.get("departing_at"),
                        "arrival": last_segment.get("arriving_at"),
                        "duration": slices[0].get("duration") or "PT0H0M",
                        "stops": max(len(segments) - 1, 0),
                        "price": total_amount or "0",
                        "currency": offer.get("total_currency") or "GBP",
                        "cabin_class": cabin_class or "economy",
                        "passengers": adults or 1,
                    }
                )

    print(formatted_offers)

    return formatted_offers
