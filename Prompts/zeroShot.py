# Zero shot prompting


# Giving a direct prompt to the model


import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "Answer only python related thing do not answer anything else, Your name is HarshGPT an developed by Harsh Verma in India, And you can also answer about your self."

def main(prompt):
   # noinspection PyTypeChecker
   response = client.chat.completions.create(
    model="gemini-2.5-flash",
    reasoning_effort="low",
    messages=[
        {
            "role": "system",
            "content":SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": prompt
        }
     ]
   )
   print(response.choices[0].message.content)

while True:
    print("____________________________")
    query = input("Enter a Prompt here: ")
    print("Processing.... User Prompt: ",query)
    main(query)


