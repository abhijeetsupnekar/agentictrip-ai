from app.tools.weather_tool import get_weather


def weather_agent(destination: str):

    weather = get_weather(destination)

    return {
        "type": "weather",
        "destination": destination,
        "weather": weather
    }