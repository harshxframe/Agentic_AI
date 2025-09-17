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
            "content":"You are an intelligent AI assistant."
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

