from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import sys

# Ensure project root in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from retrieval.vectorstore import get_retriever

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Lazy-loaded retriever
retriever = None


def load_retriever():
    global retriever
    if retriever is None:
        retriever = get_retriever()
    return retriever


def format_context(docs, max_chars=12000):
    context = ""
    citations = []

    for d in docs:
        source = d.metadata.get("source", "Unknown")
        page = d.metadata.get("page", "")

        chunk_text = f"\nPolicy: {source}\nPage: {page}\n{d.page_content}\n\n"

        if len(context) + len(chunk_text) > max_chars:
            break

        context += f"\nPolicy: {source}\nPage: {page}\n"
        context += d.page_content
        context += "\n\n"

        citations.append((source, page))

    return context, citations


def ask_question(question):

    retriever = load_retriever()

    docs = retriever.get_relevant_documents(question)

    context, citations = format_context(docs)

    prompt = f"""
You are assisting doctors and hospital staff in understanding UnitedHealthCare (UHC) insurance policies.

Answer the question using only the policy context below.

If the answer is not found in the context, say:
"The information is not available in the provided UHC policy documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)
    answer = response.content

    if "not available in the provided uhc policy documents" in answer.lower():
        return answer

    unique_citations = list(set(citations))

    citation_text = "\n\nSources:\n"

    for source, page in unique_citations:
        citation_text += f"Policy: {source} ---> Page: {page+1}\n"

    answer = answer + citation_text

    return answer