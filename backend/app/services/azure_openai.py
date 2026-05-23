import os
import json

from dotenv import load_dotenv
from openai import AzureOpenAI

# from app.tools.places_tool import search_places

from app.tools.places_tool import (
    get_hotels,
    get_restaurants,
    get_nightlife
)

load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)

tools = [

    {
        "type": "function",

        "function": {

            "name": "get_hotels",

            "description":
            "Get hotel recommendations for a destination",

            "parameters": {

                "type": "object",

                "properties": {

                    "destination": {
                        "type": "string"
                    }

                },

                "required": ["destination"]

            }

        }

    },

    {
        "type": "function",

        "function": {

            "name": "get_restaurants",

            "description":
            "Get restaurant recommendations for a destination",

            "parameters": {

                "type": "object",

                "properties": {

                    "destination": {
                        "type": "string"
                    }

                },

                "required": ["destination"]

            }

        }

    },

    {
        "type": "function",

        "function": {

            "name": "get_nightlife",

            "description":
            "Get nightlife recommendations for a destination",

            "parameters": {

                "type": "object",

                "properties": {

                    "destination": {
                        "type": "string"
                    }

                },

                "required": ["destination"]

            }

        }

    }

]
def generate_ai_response(
    user_message: str,
    history=None
):

    if history is None:
        history=[]

    system_prompt = """
You are AgenticTrip AI.

You are an intelligent multi-agent travel planner.

RULES:

1. If user asks to MODIFY itinerary:
- preserve existing trip
- preserve unchanged days
- modify ONLY requested parts

2. Never regenerate complete itinerary unless user explicitly asks.

3. Preserve:
- budget
- duration
- destination
- structure

4. Always return FULL updated itinerary.

5. Output MUST be valid JSON only.

6. Never explain outside JSON.

7. If itinerary exists in history:
- use it as memory
- intelligently modify it

8. Add realistic:
- activities
- transport
- accommodations
- food
- costs

9. Maintain clean JSON schema.

10. Preserve hotels, restaurants, nightlife and weather data unless modification requires changing them.
"""

    messages=[

        {
            "role":"system",
            "content":system_prompt
        }

    ]


    for msg in history:

        content = msg.content

        if isinstance(
            content,
            dict
        ):
            content=json.dumps(
                content
            )

        messages.append({

            "role":
            msg.role,

            "content":
            content

        })



#     tool_context=""


#     # Nightlife tool

#     if "nightlife" in user_message.lower():

#         nightlife = search_places(
#             "Bali",
#             "night clubs"
#         )

#         tool_context += f"""

# Nightlife recommendations:

# {json.dumps(
# nightlife[:3],
# indent=2
# )}

# Choose one.
# Append only.

# """


#     # Hotel tool

#     if any(
#         x in user_message.lower()
#         for x in [
#             "hotel",
#             "stay",
#             "accommodation"
#         ]
#     ):

#         hotels = search_places(
#             "Bali",
#             "hotels"
#         )

#         tool_context += f"""

# Hotel recommendations:

# {json.dumps(
# hotels[:3],
# indent=2
# )}

# Choose one hotel.

# Example:

# Accommodation:

# Courtyard Bali Seminyak Resort (4.6⭐)

# Use actual hotel names.

# """



    messages.append({

    "role": "user",

    "content": user_message

})



    response = client.chat.completions.create(

        model=deployment,

        messages=messages,

        temperature=0.3,
        
        tools=tools,
        
        tool_choice="auto",

        max_tokens=1800,

        response_format={
            "type":"json_object"
        }

    )
    print("\n===== TOOL CALL DEBUG =====")

    print(response.choices[0].message)

    message = response.choices[0].message

    # TOOL CALL HANDLING
    if message.tool_calls:

        tool_call = message.tool_calls[0]

        function_name = (
            tool_call.function.name
        )

        arguments = json.loads(
            tool_call.function.arguments
        )

        # HOTEL TOOL
        if function_name == "get_hotels":

            results = get_hotels(
                arguments["destination"]
            )

            return json.dumps({

                "type": "hotels",

                "results": results

            })

        # RESTAURANTS TOOL
        elif function_name == "get_restaurants":

            results = get_restaurants(
                arguments["destination"]
            )

            return json.dumps({

                "type": "restaurants",

                "results": results

            })

        # NIGHTLIFE TOOL
        elif function_name == "get_nightlife":

            results = get_nightlife(
                arguments["destination"]
            )

            return json.dumps({

                "type": "nightlife",

                "results": results

            })

    # NORMAL RESPONSE
    return message.content