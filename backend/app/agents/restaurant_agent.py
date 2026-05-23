from app.tools.places_tool import get_restaurants


def restaurant_agent(destination: str):

    restaurants = get_restaurants(
        destination
    )

    return {
        "type": "restaurants",
        "results": restaurants
    }