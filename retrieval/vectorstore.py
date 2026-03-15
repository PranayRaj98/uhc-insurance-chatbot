import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

device = "cpu"

VECTOR_DB_PATH = "vectorstore"

# Global variables
embeddings = None
vector_store = None
retriever = None


def initialize_vector_store():
    global embeddings, vector_store, retriever

    if retriever is None:

        print("Loading embedding model...")

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True}
        )

        print("Loading FAISS index...")

        vector_store = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 6,
                "fetch_k": 20
            }
        )

        print("Retriever ready.")

    return retriever


def retrieve_documents(query):

    retriever = initialize_vector_store()

    query = f"Represent this sentence for searching relevant passage: {query}"

    docs = retriever.invoke(query)

    return docs


if __name__ == "__main__":

    docs = retrieve_documents("When is bariatric surgery covered?")

    for d in docs:
        print("\n---")
        print(d.page_content[:400])
        print(d.metadata)