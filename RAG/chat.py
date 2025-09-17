import time

from langchain_community.embeddings import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

timeFrame1 = time.perf_counter()
print("Program execution begin...")

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url=os.environ.get("DEEPSEEK_API_BASE"))

print("Model initializing...")
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
print("Model initialization done.")


print("DB operations begin...")
vectorDB = QdrantVectorStore.from_existing_collection(
    embedding=embeddings_model,
    url="http://localhost:6333/",
    collection_name="indianConstitution",
)
print("DB operations done.")

#Take the user inpout
print("User input required.")
userQuery = str(input("Ask something: "))

print("getting relevant documents...")
#Return you relevant chunks
search_result = vectorDB.similarity_search(query = userQuery)

content = "\n\n\n".join([f"Page Content: {result.page_content}\nPageNumber:{result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_result])
print("Documents retrieved...")

SYSTEM_PROMPT = f""""
You are a helpful AI assistant who answers user query based on the available context
retrieved from a PDF file along with page_contents and page number.

You should only ans user based on the following context and navigate the user
to open the right page number to know more.

Context: 
{content}

"""
print("Calling to AI API....")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": userQuery},
    ],
    stream=False
)
print("Waiting for the response by AI......")
print("AI response:",response.choices[0].message.content)
print("Execution completed.")
timeFrame2 = time.perf_counter()
print(f"Program execution ended... and taken {timeFrame2-timeFrame1}")

