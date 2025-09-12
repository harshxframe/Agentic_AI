#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.
#MALFUNCTION EXIST IN THIS PROGRAM.

######################################################################
######################################################################


import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

from pyasn1_modules.rfc3560 import pSpecifiedEmptyIdentifier

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def getWeather(city):
    apiRequest = requests.get(f"https://wttr.in/{city}?format=%C+%t")
    if apiRequest.status_code == 200:
        return f"Whether of the {city} is {apiRequest.text}"
    else:
        return "Something went wrong"

toolList = {"getWeather":getWeather}

def main(USER_PROMPT):
    try:
        SYSTEM_PROMPT = """
          You are an expert AI assistant and and your role to resolve user query using Chain of thoughts.
          Your work on START, PLAN, TOOL, OUTPUT, OBSERVE steps.
          You first need to PLAN what needs to be done. The Plan can be in multiple steps.
          Once you think enough PLAN has been done than you use TOOL and than OUTPUT step.
          Follow every step properly strictly never give response it another json key or like that.


          Rules:
          -Strictly follow the given JSON output.
          -Run one PLAN step at the time.
          -The sequence of steps is START (Where user give input), PLAN (Can be multiple times), TOOL(Run tool to get data), OBSERVE(Observe the fetched data) and finally OUTPUT (Which is going to display to user).

          Output JSON format follow it strictly:
          {
          "step": "START" or "PLAN" or "TOOL" or "OUTPUT" or "OBSERVE",
          "content": "string",
          "tool": "string",
          "input":"string"
          }

          Available Tools:
          -getWeather(city:str): Takes city name as an input string and return the weather info about

          Follow example.

          Examples 1: 
          START: What is the weather of Mumbai
          PLAN: {"step": "PLAN", "content": "Seems user asking the weather of Mumbai in India"}
          PLAN: {"step": "PLAN", "content": "Lets see if we have any available tools from the list of available tools"}
          PLAN: {"step": "PLAN", "content": "Great we gave getWeather tool available for this query"}
          PLAN: {"step": "PLAN", "content": "I need to call getWeather tool for Mumbai as input for city"}
          PLAN: {"step": "TOOL", "tool": "getWeather" "input": "Mumbai"}
          PLAN: {"step": "OBSERVE", "tool": "getWeather", "output": "The temp of Mumbai is cloudy with 20 C"}
          PLAN: {"step": "OUTPUT", "output": "The current weather info about Mumbai is 20 C with some cloudy"}

          Examples 2: 
          START: What is the weather of Kanpur
          PLAN: {"step": "PLAN", "content": "Seems user asking the weather of Kanpur in India"}
          PLAN: {"step": "PLAN", "content": "Lets see if we have any available tools from the list of available tools"}
          PLAN: {"step": "PLAN", "content": "Great we gave getWeather tool available for this query"}
          PLAN: {"step": "PLAN", "content": "I need to call getWeather tool for Kanpur as input for city"}
          PLAN: {"step": "TOOL", "tool": "getWeather", "input": "Kanpur"}
          PLAN: {"step": "OBSERVE", "tool": "getWeather", "content": "The temp of Kanpur is cloudy with 30 C"}
          PLAN: {"step": "OUTPUT", "output": "The current weather info about Kanpur is 30 C with some cloudy"}



          """

        messageHistory = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT
            },
        ]
        while True:

            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                reasoning_effort="low",
                response_format={"type": "json_object"},
                messages=messageHistory
            )

            raw = response.choices[0].message.content
            messageHistory.append({
                "role": "assistant",
                "content": json.dumps(raw)
            })
            parsedResult = json.loads(raw)
            if parsedResult.get("step") == "START":
                print("🤖 Thinking...")
                continue
            if parsedResult.get("step") == "PLAN":
                print("🚀 Planning...")
                continue
            if parsedResult.get("step") == "TOOL":
                print("⚙️ API data fetching...")
                if parsedResult.get("tool") == "getWeather":
                    observer = toolList["getWeather"](parsedResult["input"])
                    messageHistory.append({
                        "role": "assistant",
                        "content": json.dumps(
                            {
                                "step": "OBSERVE",
                                "tool": "getWeather",
                                "content": observer,

                            }
                        )
                    })
                continue
            if parsedResult.get("step") == "OUTPUT":
                print("🤖", parsedResult["output"])
                return None
            print("🤖", parsedResult["output"])
            break
    except Exception as e:
        print("<UNK>", e)


while True:
    prompt = str(input("Prompt: "))
    if prompt != "" and prompt != "None":
       main(prompt)


print("+++++++++++++++++++++++++++++++++Solid Example......")

promptExample =  """ 
You are an assistant that MUST follow this strict step protocol and output EXACTLY one valid JSON object, and nothing else (no explanation, no extra text, only the JSON).

Schema (required):
- START: {"step":"START","content":"<user message>"}
- PLAN:  {"step":"PLAN","content":"<one short planning sentence>"}
- TOOL:  {"step":"TOOL","tool":"<tool_name>","input":"<string>"}
- OBSERVE: {"step":"OBSERVE","tool":"<tool_name>","content":"<tool output or error>"}
- OUTPUT: {"step":"OUTPUT","content":"<final user-facing answer>"}

Rules:
1. Always return a single JSON object per assistant turn and nothing else.
2. Emit one PLAN object per assistant reply (you may send multiple PLAN replies across turns if needed).
3. When calling a tool emit a TOOL object. Do NOT call tools yourself; the system will execute the tool if you output TOOL.
4. After a TOOL is executed, the system will add an OBSERVE object containing tool results; then you should produce the OUTPUT object.
5. If the requested tool is not available, produce OBSERVE with content "Tool '<tool>' not found." then continue.
6. Use plain short sentences in PLAN and OUTPUT. No chain-of-thought text beyond the single JSON objects.
7. Examples (valid JSON only):

Example:
User: "What is the weather of Mumbai?"
Assistant -> START:
{"step":"START","content":"What is the weather of Mumbai?"}

Assistant -> PLAN:
{"step":"PLAN","content":"User asks for Mumbai weather; we have getWeather tool."}

Assistant -> TOOL:
{"step":"TOOL","tool":"getWeather","input":"Mumbai"}

(then system will run getWeather and add an OBSERVE)

Assistant -> OBSERVE:
{"step":"OBSERVE","tool":"getWeather","content":"Weather of Mumbai is: ☀️ 28°C"}

Assistant -> OUTPUT:
{"step":"OUTPUT","content":"Current weather in Mumbai: ☀️ 28°C"}

End of prompt.

"""

