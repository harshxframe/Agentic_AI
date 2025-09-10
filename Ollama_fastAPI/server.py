from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434/"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getResponse")
def sendResponse():
    return {"message": "Hey, I am AI I am here to help you?"}

@app.post("/chat")
def chat(message: str = Body(..., description="The message to be sent."), ):
    response = client.chat(model='gemma:2b',
                           messages=[
                               {"role": "user", "content": message}
                           ]
                           )
    return {"message": response.message.content}
