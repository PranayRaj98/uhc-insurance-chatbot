from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from tqdm import tqdm
import os
import time
import pickle



try:
    # When used as part of the `ingestion` package
    from ingestion.loader import load_uhc_policies
    from ingestion.chunker import chunk_documents
    from ingestion.chunker import CHUNK_FILE
except ImportError:
    # When running this file directly: `python ingestion/embedder.py`
    from loader import load_uhc_policies
    from chunker import chunk_documents
    from chunker import CHUNK_FILE

load_dotenv()


def create_vector_score():
    CHUNK_FILE = "storage/chunks.pkl"
    print("Loading chunks...")

    with open(CHUNK_FILE, "rb") as f:
      chunks = pickle.load(f)
      
    print(f"Loaded {len(chunks)} chunks")

    print(f"Total chunks to embed (approximate size of index): {len(chunks)}")
    print("Creating embeddings model on GPU")
    
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 128},
    )

    print("Building FAISS vector store")
    start = time.perf_counter()
    vector_store = FAISS.from_documents(
        chunks,
        embeddings,
    )
    elapsed = time.perf_counter() - start
    print(f"FAISS index built in {elapsed:.1f} seconds.")

    print("Saving vector database")
    vector_store.save_local("vectorstore")

    print("Vector store saved successfully")


if __name__ == "__main__":
    create_vector_score()