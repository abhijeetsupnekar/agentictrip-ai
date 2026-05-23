from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def handle_trip_planning(user_input):

    prompt = f"""
You are an expert AI travel planner.

Create a travel itinerary in STRICT JSON format.

Trip Request:
{user_input}

Return ONLY valid JSON.

Structure:

{{
  "destination": "string",

  "best_areas_to_stay": [
    "area 1",
    "area 2"
  ],

  "estimated_budget": {{
    "budget": "string",
    "mid_range": "string",
    "luxury": "string"
  }},

  "food_recommendations": [
    "food 1",
    "food 2"
  ],

  "days": [
    {{
      "day": 1,

      "title": "string",

      "morning": [
        "activity"
      ],

      "afternoon": [
        "activity"
      ],

      "evening": [
        "activity"
      ]
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI travel planner."},
            {"role": "user", "content": prompt},
        ],
    )

    import json

    itinerary = response.choices[0].message.content

    parsed = json.loads(itinerary)

    return {"type": "trip_plan", "data": parsed}
