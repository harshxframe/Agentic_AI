from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

print("Program is now started....")
# Take the pdf
pdf_path = Path(__file__).parent / "test.pdf"

# load this file
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()   #give a page by page

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(docs)

# Ollama embeddings
# Make sure you have pulled: ollama pull nomic-embed-text
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

# Store embeddings in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings_model,
    url="http://localhost:6333/",
    collection_name="learning_rag",
)

print("Indexing of documents done.....!")
