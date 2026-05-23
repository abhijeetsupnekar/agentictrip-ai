import requests
import os

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)


def get_weather(city):

    try:

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

        params = {

            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"

        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        print(
            "WEATHER API RESPONSE:",
            data
        )

        # SAFE CHECK
        if "main" not in data:

            return {

                "error":
                data.get(
                    "message",
                    "Weather unavailable"
                )

            }

        return {

            "temperature":
            data["main"]["temp"],

            "condition":
            data["weather"][0]["main"],

            "humidity":
            data["main"]["humidity"]

        }

    except Exception as e:

        print(
            "Weather Error:",
            str(e)
        )

        return {

            "error":
            "Unable to fetch weather"

        }