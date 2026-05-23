from app.tools.places_tool import get_nightlife


def nightlife_agent(destination: str):

    nightlife = get_nightlife(destination)

    return {"type": "nightlife", "results": nightlife}
