import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configs
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
DATA_DIR = Path("data")
VECTOR_STORE_DIR = Path("vector_store")

# 1. Load and Chunk Text
def load_documents():
    docs = []

    for file_name in ["bns_sections.json", "constitution_articles.json", "ipc_sections.json"]:
        file_path = DATA_DIR / file_name
        with open(file_path, "r", encoding="utf-8") as f:
            sections = json.load(f)

        for key, value in sections.items():
            content = f"{key}:\n{value}"
            docs.append(Document(page_content=content, metadata={"source": file_name}))

    return docs

# 2. Split Documents
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64
    )
    return splitter.split_documents(docs)

# 3. Embed and Store in Vector DB
def create_vector_store():
    if not VECTOR_STORE_DIR.exists():
        print("Creating vector store...")
        raw_docs = load_documents()
        chunks = split_documents(raw_docs)

        embedding_function = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
        Chroma.from_documents(
            chunks,
            embedding=embedding_function,
            persist_directory=str(VECTOR_STORE_DIR)
        )
    else:
        print("Vector store already exists.")

# 4. Retrieve Context for a Query
def retrieve_context(query: str) -> str:
    embedding_function = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma(persist_directory=str(VECTOR_STORE_DIR), embedding_function=embedding_function)

    docs = vectordb.similarity_search(query, k=4)
    return "\n\n".join([doc.page_content for doc in docs])
