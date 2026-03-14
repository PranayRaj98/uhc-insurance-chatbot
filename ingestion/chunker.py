from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import pickle

try:
    from ingestion.loader import load_uhc_policies
except ImportError:
    from loader import load_uhc_policies


CHUNK_FILE = "storage/chunks.pkl"

def chunk_documents(documents):
    total_docs = len(documents)
    print(f"Preparing to chunk {total_docs} documents.")

    docs_by_source = {}
    current_section = "Unknown"
    for doc in documents:
        source = doc.metadata.get("source", "UNKNOWN_SOURCE")
        docs_by_source.setdefault(source, []).append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    all_chunks = []
    processed_docs = 0

    for source, docs_in_source in docs_by_source.items():
        processed_docs += 1
        # print(f"[CHUNKER] Processing document {processed_docs}/{len(docs_by_source)}: {source}")

        source_chunks = text_splitter.split_documents(docs_in_source)
        # print(f"[CHUNKER]   -> Created {len(source_chunks)} chunks from {source}")

        all_chunks.extend(source_chunks)

    print(f"Total chunks created from all documents: {len(all_chunks)}")

    return all_chunks


if __name__ == "__main__":
    docs = load_uhc_policies()

    chunks = chunk_documents(docs)
    
    os.makedirs("storage", exist_ok = True)
    
    with open(CHUNK_FILE, "wb") as f:
      pickle.dump(chunks, f)
      
    print("Chunks saved to pkl file")

    print("\nExample chunk: \n")
    print(chunks[0].page_content[:500])
    print("\nMetadata: ")
    print(chunks[0].metadata)