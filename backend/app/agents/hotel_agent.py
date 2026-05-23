from app.tools.places_tool import get_hotels


def hotel_agent(destination: str):

    hotels = get_hotels(destination)

    return {
        "type": "hotels",
        "results": hotels
    }