import os
import time

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url=os.environ.get("DEEPSEEK_API_BASE"))

def processQuery(userQuery):
    print("Execution begin..")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are AI assistant made by Harsh Verma!"},
            {"role": "user", "content": userQuery},
        ],
        stream=False,
    )
    return response.choices[0].message.content



