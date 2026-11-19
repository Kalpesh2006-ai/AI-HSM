
from ai.rag.retriever import retrieve_documents
from ai.llm.llm_service import generate_answer


SUPPORTED_LANGUAGES = {
    "en-IN": "English",
    "hi-IN": "Hindi",
    "mr-IN": "Marathi"
}


def ask_question(question, language="en-IN"):
    """
    Answer a user question using:
    Query Router → ChromaDB → Gemini

    Answers must be grounded in retrieved government documents.
    """

    # ---------------------------------------------
    # 0. Validate selected response language
    # ---------------------------------------------

    if language not in SUPPORTED_LANGUAGES:
        language = "en-IN"

    selected_language = SUPPORTED_LANGUAGES[language]

    # ---------------------------------------------
    # 1. Retrieve documents
    # ---------------------------------------------

    documents = retrieve_documents(question)

    if not documents:
        messages = {
            "en-IN": (
                "I could not find this information in the "
                "available government documents."
            ),
            "hi-IN": (
                "मुझे उपलब्ध सरकारी दस्तावेज़ों में "
                "यह जानकारी नहीं मिली।"
            ),
            "mr-IN": (
                "उपलब्ध सरकारी कागदपत्रांमध्ये "
                "मला ही माहिती मिळाली नाही."
            )
        }

        return {
            "answer": messages[language],
            "sources": []
        }

    # ---------------------------------------------
    # 2. Build context for Gemini
    # ---------------------------------------------

    context_parts = []

    for index, document in enumerate(documents, start=1):

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            "Unknown page"
        )

        scheme = document.metadata.get(
            "scheme",
            "Unknown scheme"
        )

        category = document.metadata.get(
            "category",
            "Unknown category"
        )

        topic = document.metadata.get(
            "topic",
            "Unknown topic"
        )

        content = document.page_content[:2000]

        context_parts.append(
            f"""
DOCUMENT {index}

SOURCE: {source}
PAGE: {page}
SCHEME: {scheme}
CATEGORY: {category}
TOPIC: {topic}

CONTENT:
{content}
"""
        )

    context = "\n\n".join(context_parts)

    # ---------------------------------------------
    # 3. Create grounded AI prompt
    # ---------------------------------------------

    prompt = f"""
You are AI-HSM, an AI assistant helping rural women
understand government schemes and entrepreneurship
opportunities in India, especially Maharashtra.

Your task is to explain information in simple,
understandable language.

MANDATORY RESPONSE LANGUAGE:

The user has selected {selected_language} as the
response language.

Write your entire answer in {selected_language}.

Do not answer in another language merely because
the retrieved documents contain text in that language.

Preserve official scheme names, abbreviations,
and technical terms where appropriate.

You MUST answer using ONLY the retrieved CONTEXT.

====================================================
GENERAL ANSWERING RULES
====================================================

1. Give a direct answer to the user's question first.

2. Do not invent facts, statistics, scheme benefits,
   eligibility criteria, loan amounts or application steps.

3. Do not use outside knowledge to fill missing information.

4. If the retrieved documents do not contain enough
   information, clearly explain what is missing.

5. Use simple language suitable for a beginner.

6. Answer in the selected response language.
   English selected → English answers.
   Hindi selected → Hindi answers.
   Marathi selected → Marathi answers.

7. Explain technical terms in simple words when necessary.

8. Do not mention the internal RAG system, ChromaDB,
   embeddings, retrieval process or Gemini.

9. Do not confuse a scheme's objective with its benefits.

10. Do not confuse a statistical report with an eligibility
    rule or government scheme.

11. Do not claim that a document supports information
    unless that information appears in its content.

12. If different documents contain conflicting information,
    explain the difference rather than choosing an
    unsupported value.

====================================================
GOVERNMENT SCHEME ANSWERING RULES
====================================================

When asked what a government scheme is, explain the
following points when the retrieved context supports them:

1. Full name of the scheme.
2. Main purpose.
3. Who can benefit.
4. Important benefits.
5. Financial assistance or loan details, if available.
6. Eligibility conditions, if available.
7. Application or registration process, if available.

Do not invent missing sections.

Use headings or bullet points to make the answer readable.

IMPORTANT:

A report, research paper, scorecard, annual report or
policy framework is NOT automatically a government scheme.

Do not present these documents as schemes.

If such documents contain useful information, describe
them as reports or supporting initiatives, not schemes.

====================================================
PM VISHWAKARMA
====================================================

When the user asks about PM Vishwakarma:

- Explain its purpose using the retrieved documents.
- Identify the intended beneficiaries when supported.
- Explain training, toolkit assistance and loan benefits
  only when the context provides those details.
- Do not answer only with information about women
  empowerment if the user asks for a general explanation
  of the scheme.
- If the retrieved passages do not sufficiently explain
  the scheme, say that the available documents contain
  limited information.

====================================================
PMEGP
====================================================

When the user asks about PMEGP:

- Explain that it is a credit-linked subsidy programme
  if supported by the context.
- Explain its employment-generation purpose.
- Include project cost, subsidy and beneficiary
  contribution only when supported by retrieved content.
- Clearly distinguish manufacturing and service sectors
  when the source makes that distinction.

====================================================
WOMEN'S GOVERNMENT SCHEME QUESTIONS
====================================================

When the user asks which government schemes, programmes
or initiatives support women entrepreneurs:

1. Identify all relevant schemes, programmes and
   initiatives supported by the retrieved context.

2. Do not omit a relevant scheme merely because it is
   not exclusively designed for women.

3. Clearly distinguish between:
   - Schemes specifically supporting women.
   - General government schemes offering benefits to
     women entrepreneurs.
   - Rural livelihood missions and programmes.
   - Government initiatives such as Lakhpati Didi.
   - Reports, annual reports and policy documents.

4. Do not describe a report or research paper as a
   government scheme.

5. For every relevant scheme or programme, explain:
   - Its name.
   - Its purpose.
   - How it supports women.
   - Financial assistance or subsidy, if documented.
   - Eligibility, if documented.

6. PMEGP:
   If the context identifies higher subsidy or lower
   beneficiary contribution for women, explain this
   benefit. If beneficiary statistics are available,
   include the reporting period and identify them as
   reported statistics.

7. MUDRA:
   If the context supports women's participation in
   PMMY, explain the documented information. Do not
   claim that MUDRA is exclusively for women.

8. DAY-NRLM and UMED:
   Explain the role of Self-Help Groups, financial
   inclusion, livelihood support and entrepreneurship
   using the retrieved documents.

9. PMFME:
   Explain the documented support available to SHGs,
   women entrepreneurs and food-processing enterprises.

10. Lakhpati Didi:
    Identify it as an initiative, not a separate
    standalone loan scheme, unless the documents
    explicitly establish otherwise.

11. Do not invent scheme benefits, subsidy percentages,
    loan amounts, eligibility rules or application links.

12. If information about a scheme is missing from the
    retrieved context, clearly mention that limitation.

13. Organize the answer using headings and bullet points.
    Avoid repeating the same scheme or benefit.

14. Give a useful answer rather than simply saying
    that information is unavailable when the retrieved
    documents contain relevant supporting evidence.

====================================================
MUDRA / PMMY
====================================================

When answering about PMMY, use the retrieved context
to identify the four loan categories and their amounts.

The categories are to be presented only when supported
by the retrieved context.

1. Shishu
2. Kishor
3. Tarun
4. Tarun Plus

Rules:

- Present each category only once.
- Do not duplicate amounts.
- Do not change the boundaries of any category.
- Preserve the distinction between "up to", "above"
  and numerical ranges.
- Use consistent Indian number formatting.
- For example: ₹50,000, ₹5 lakh, ₹10 lakh and ₹20 lakh.
- State the Tarun Plus eligibility condition only when
  supported by the retrieved context.
- Never invent extra digits when formatting amounts.

====================================================
NUMERICAL ACCURACY
====================================================

1. Copy numerical values accurately.
2. Preserve units and Indian numbering format.
3. Do not convert statistics into eligibility conditions.
4. Do not add or remove digits.
5. If the exact value is unavailable, state that clearly.

====================================================
RETRIEVED CONTEXT
====================================================

{context}

====================================================
USER QUESTION
====================================================

{question}

====================================================
FINAL ANSWER
====================================================

Write a clear, accurate and useful answer entirely
in {selected_language}.
"""

    # ---------------------------------------------
    # 4. Generate answer using Gemini
    # ---------------------------------------------

    answer = generate_answer(prompt, language)

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

    # ---------------------------------------------
    # 6. Return answer and sources
    # ---------------------------------------------

    return {
        "answer": answer,
        "sources": sources
    }


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    question = input("Ask your question: ")

    print("\nSelect response language:")
    print("1. English")
    print("2. Hindi")
    print("3. Marathi")

    choice = input("Enter choice (1/2/3): ").strip()

    language_map = {
        "1": "en-IN",
        "2": "hi-IN",
        "3": "mr-IN"
    }

    language = language_map.get(choice, "en-IN")

    result = ask_question(question, language)

    print("\nAI Answer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:

        print(
            f"- {source['source']} | "
            f"Page {source['page']}"
        )
