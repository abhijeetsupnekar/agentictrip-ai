from openai import OpenAI
from langsmith import traceable

from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


@traceable
def generate_trip_plan(prompt):

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": ("You are an expert AI travel planner."),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        stream=True,
    )

    final_response = ""

    for chunk in stream:

        if chunk.choices[0].delta.content:

            content = chunk.choices[0].delta.content

            print(content, end="", flush=True)

            final_response += content

    print()

    return final_response
