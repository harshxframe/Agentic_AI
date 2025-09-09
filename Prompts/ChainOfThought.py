# Chian of thought prompting(CoT)

# Chian of thought is like make LLM to think before respond.


import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
Your work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to do done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly Follow the given JSON output
- Only run one step at a time.
- The sequence of steps is START (Where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).


Output JSON Format:
{
"step": "START" or "PLAN" or "OUTPUT",
"content": "string"
}

Example:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: {"step": "PLAN", "content": "Seems like user is interested in math problem"}
PLAN: {"step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method"}
PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here"}
PLAN: {"step": "PLAN", "content": "first we multiple 3 * 5 which is 15"}
PLAN: {"step": "PLAN", "content": "We must perform divide that is 2 + 15 / 10"
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"
PLAN: {"step": "PLAN", "content": "Now finally lets perform the add"
PLAN: {"step": "PLAN", "content": "Greate we have solved and finally left
with 3.5 as ans"
OUTPUT: {"step": "OUTPUT", "content": "3.5"
}



"""


def main(prompt):
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        reasoning_effort="low",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Hey write a code to add n numbers in js"},
            {"role": "assistant",
             "content": json.dumps({"step": "START", "content": "Hey write a code to add n numbers in js"})
             },
            {"role": "assistant",
             "content": json.dumps({
                 "step": "PLAN",
                 "content": "The user wants a JavaScript function to add 'n' numbers. I should define a function that can take multiple arguments and sum them up."
             })
             },
            {"role": "assistant",
             "content": json.dumps({
                 "step": "PLAN",
                 "content": "I will define a JavaScript function using the rest parameter (...numbers) to accept an arbitrary number of arguments. Then, I'll use the 'reduce' method on the 'numbers' array to sum all the elements. Finally, I will return the total sum and provide an example of how to use the function."
             })
             },
        ]
    )
    print(response.choices[0].message.content)


while True:
    print("____________________________")
    query = input("Enter a Prompt here: ")
    print("Processing.... User Prompt: ", query)
    main(query)
