import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from models.embeddings import load_embeddings
from config.config import CHUNK_SIZE, CHUNK_OVERLAP

VECTOR_DB_DIR = "vector_db"


# -------------------------
# CREATE VECTOR STORE
# -------------------------

def create_vector_store(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = splitter.split_documents(documents)

    embeddings = load_embeddings()

    vectordb = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    return vectordb


# -------------------------
# LOAD VECTOR STORE
# -------------------------

def load_vector_store():

    embeddings = load_embeddings()

    # If vector DB does not exist → build it
    if not os.path.exists(VECTOR_DB_DIR):

        from utils.document_loader import load_documents

        print("Building knowledge base...")

        docs = load_documents("knowledge_base")

        vectordb = create_vector_store(docs)

        return vectordb

    vectordb = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )

    return vectordb