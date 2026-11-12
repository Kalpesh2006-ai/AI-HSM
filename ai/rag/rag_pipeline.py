
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
9. Base the answer on the provided sources and pages.
10. Copy numerical values accurately from the context.
    Never add, remove, or change digits.
11. Preserve Indian numbering format and the units used
    in the source documents.
12. Clearly distinguish between "up to", "above", and
    a numerical range.
13. Do not invent extra digits when formatting amounts.
    For example, ten lakh and one rupee is ₹10,00,001,
    not ₹10,000,001.
14. If retrieved sources disagree or do not establish
    an exact amount, explain the uncertainty instead
    of guessing.
15. When answering about PMMY, use the retrieved context
    to identify the four loan categories and their amounts.
16. Present each loan category only once. Do not include
    alternative formats, duplicate amounts, or phrases
    such as "or above..." to restate the same amount.
17. Use clear, consistent Indian number formatting.
    For example: ₹50,000, ₹5 lakh, ₹10 lakh, and ₹20 lakh.
18. Do not change the meaning or boundaries of any loan
    category when simplifying its amount.
19. For Tarun Plus eligibility, state the special condition
    only when supported by the retrieved context.
20. Do not claim that a source supports a detail unless
    that detail appears in its provided content.


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
