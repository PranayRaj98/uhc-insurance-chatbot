import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.tools import retriever
from langchain_openai import OpenAIEmbeddings
import pickle

from openai.types import vector_store
import torch
device = "cpu"



VECTOR_DB_PATH = "vectorstore"

def load_vector_store():
  embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-en-v1.5",
    model_kwargs = {"device": device},
    encode_kwargs = {"normalize_embeddings": True}
  )
  
  vector_store = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
  )
  
  return vector_store

def get_retriever():
  vector_store = load_vector_store()
  
  retriever = vector_store.as_retriever(
    search_type = "mmr",
    search_kwargs = {
      "k" : 6,
      "fetch_k": 20
    }
  )
  
  return retriever


def retrieve_documents(query):
  retriever = get_retriever()
  
  query = f"Represent this sentence for searching relevant passage: {query}"
  
  docs = retriever.invoke(query)
  
  return docs

if __name__ == "__main__":
  docs = retrieve_documents(
    "When is bariatric surgery covered?"
  )
  
  for d in docs:
    print("\n---")
    print(d.page_content[:400])
    print(d.metadata)