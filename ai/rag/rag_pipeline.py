from ai.rag.retriever import retrieve_documents
from ai.llm.llm_service import generate_answer


def ask_question(question):
    """
    Answer a user question using:
    Query Router → ChromaDB → Gemini

    The answer is grounded only in the retrieved
    government documents.
    """

    # ---------------------------------------------
    # 1. Retrieve documents using Query Router
    # ---------------------------------------------

    documents = retrieve_documents(question)

    if not documents:
        return {
            "answer": (
                "I could not find this information in the "
                "available government documents."
            ),
            "sources": []
        }

    # ---------------------------------------------
    # 2. Build context for Gemini
    # ---------------------------------------------

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            "Unknown page"
        )

        # Limit text from each document
        # to control Gemini token usage.
        content = document.page_content[:1200]

        context_parts.append(
            f"""
SOURCE: {source}
PAGE: {page}

CONTENT:
{content}
"""
        )

    context = "\n\n".join(context_parts)

    # ---------------------------------------------
    # 3. Create grounded AI prompt
    # ---------------------------------------------

    prompt = f"""
You are an AI assistant helping rural women understand
government schemes and entrepreneurship.

Answer the user's question using ONLY the information
provided in the CONTEXT.

IMPORTANT RULES:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer cannot be found in the context, say:
   "I could not find this information in the available
   government documents."
4. Keep the answer simple and easy to understand.
5. Give a direct answer first.
6. Do not mention the internal RAG system.
7. If the context provides statistics, state them accurately.
8. Do not turn statistics into eligibility rules unless
   the documents explicitly state that rule.
9. If the documents provide a source/page, use that
   information as the basis of the answer.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    # ---------------------------------------------
    # 4. Generate grounded answer using Gemini
    # ---------------------------------------------

    answer = generate_answer(prompt)

    # ---------------------------------------------
    # 5. Collect unique source + page combinations
    # ---------------------------------------------

    sources = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            "Unknown page"
        )

        source_info = {
            "source": source,
            "page": page
        }

        if source_info not in sources:
            sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":

    question = input("Ask your question: ")

    result = ask_question(question)

    print("\nAI Answer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:

        print(
            f"- {source['source']} | "
            f"Page {source['page']}"
        )