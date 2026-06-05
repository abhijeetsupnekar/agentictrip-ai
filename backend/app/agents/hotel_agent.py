from app.tools.places_tool import get_hotels


def hotel_agent(destination: str):

    hotels = get_hotels(destination)

    return {
        "type": "hotels",
        "results": hotels
    }
def handle_hotel_query(user_input, session=None):

    return hotel_agent(user_input)