from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path


def load_uhc_policies(data_path: str = "./data/uhc_policies"):
    documents = []

    pdf_files = sorted(Path(data_path).glob("*.pdf"))
    total_pdfs = len(pdf_files)
    print(f"Found {total_pdfs} PDF files in '{data_path}'.")

    loaded_pdfs = 0

    for pdf in pdf_files:
        print(f"Loading PDF {loaded_pdfs + 1}/{total_pdfs}: {pdf.name}")
        loader = PyPDFLoader(str(pdf))
        docs = loader.load()

        for d in docs:
            d.metadata["source"] = pdf.name

        documents.extend(docs)
        loaded_pdfs += 1

    print(f"Loaded {loaded_pdfs} PDFs and {len(documents)} pages in total.")

    return documents


if __name__ == "__main__":
    docs = load_uhc_policies()
    if docs:
        print(docs[0].page_content[:500])