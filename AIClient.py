import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def main(prompt):
   # noinspection PyTypeChecker
   response = client.chat.completions.create(
    model="gemini-2.5-flash",
    reasoning_effort="low",
    messages=[
        {
            "role": "system",
            "content":"You are Maths expert, Here to answer only answer only Maths related questions, When someone ask anything if it not related to maths say them no in human friendly way."
        },
        {
            "role": "user",
            "content": prompt
        }
     ]
   )

   print(response.choices[0].message.content)


while True:
    query = input("Enter a Prompt here: ")
    main(query)

