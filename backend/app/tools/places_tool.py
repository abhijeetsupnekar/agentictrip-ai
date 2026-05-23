import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

gmaps = None

if GOOGLE_API_KEY:
    gmaps = googlemaps.Client(
        key=GOOGLE_API_KEY
    )
else:
    print(
        "WARNING: GOOGLE_API_KEY not found"
    )


def search_places(query: str):
    try:

        result = gmaps.places(
            query=query
        )

        return result.get(
            "results",
            []
        )

    except Exception as e:

        print(
            "Search error:",
            e
        )

        return []


def get_hotels(location: str):

    places = search_places(
        f"best hotels in {location}"
    )

    hotels=[]

    for place in places[:5]:

        hotels.append({

            "name":
            place.get(
                "name",
                "Unknown Hotel"
            ),

            "rating":
            place.get(
                "rating",
                "N/A"
            ),

            "address":
            place.get(
                "formatted_address",
                "Address unavailable"
            )

        })

    return hotels


def get_nightlife(location:str):

    places = search_places(
        f"nightlife bars clubs in {location}"
    )

    nightlife=[]

    for place in places[:5]:

        nightlife.append({

            "name":
            place.get(
                "name",
                "Unknown Place"
            ),

            "rating":
            place.get(
                "rating",
                "N/A"
            ),

            "address":
            place.get(
                "formatted_address",
                "Address unavailable"
            )

        })

    return nightlife


def get_restaurants(location:str):

    places = search_places(
        f"best restaurants in {location}"
    )

    restaurants=[]

    for place in places[:5]:

        restaurants.append({

            "name":
            place.get(
                "name",
                "Unknown Restaurant"
            ),

            "rating":
            place.get(
                "rating",
                "N/A"
            ),

            "address":
            place.get(
                "formatted_address",
                "Address unavailable"
            )

        })

    return restaurants