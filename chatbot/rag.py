import ollama
from .vector_store import search_chunks


LLM_MODEL = "llama3.2"


def ask_pdf(document_id, question):

    # Step 1: Retrieve relevant chunks
    results = search_chunks(
        document_id,
        question,
        top_k=4
    )

    if not results:
        return {
            "answer": "No relevant information found.",
            "sources": []
        }

    # Step 2: Prepare PDF context
    context = ""

    for result in results:
        context += (
            f"\nPage {result['page_number']}:\n"
            f"{result['content']}\n"
        )

    # Step 3: Create prompt
    prompt = f"""
You are a PDF document assistant.

Answer the question using ONLY the provided PDF context.

If the answer is not available in the context,
say that the information is not available in the document.

Mention the relevant page numbers in your answer.

PDF CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    # Step 4: Generate answer
    response = ollama.generate(
        model=LLM_MODEL,
        prompt=prompt
    )

    answer = response["response"]

    # Step 5: Return answer and sources
    sources = [
        {
            "page_number": result["page_number"],
            "content": result["content"]
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources
    }