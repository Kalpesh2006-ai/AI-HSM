from langchain_chroma import Chroma

from ai.rag.config import VECTOR_DB_PATH, COLLECTION_NAME
from ai.rag.embeddings import get_embeddings
from ai.rag.query_router import expand_query


def get_vector_store():
    """
    Load the existing Chroma vector database.
    """

    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vector_store


def get_retriever():
    """
    Return the standard retriever.
    """

    vector_store = get_vector_store()

    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )


def retrieve_documents(question):
    """
    Retrieve relevant documents using the query router.

    Current government-scheme routing remains supported.

    The retrieval system is now designed around the
    broader metadata structure:

        category
        topic
        scheme

    This allows future knowledge categories such as:

        entrepreneurship
        digital_skills
        digital_marketing
        financial_literacy
        business_compliance
        maharashtra
    """

    vector_store = get_vector_store()

    routing_result = expand_query(question)

    expanded_queries = routing_result[
        "expanded_queries"
    ]

    detected_schemes = routing_result.get(
        "detected_schemes",
        []
    )

    detected_scheme = (
        detected_schemes[0]
        if detected_schemes
        else None
    )

    all_results = []

    for query in expanded_queries:

        # ---------------------------------------------
        # GOVERNMENT SCHEME FILTER
        # ---------------------------------------------

        if detected_scheme:

            results = (
                vector_store
                .similarity_search_with_score(
                    query,
                    k=4,
                    filter={
                        "scheme": detected_scheme
                    }
                )
            )

        # ---------------------------------------------
        # GENERAL KNOWLEDGE RETRIEVAL
        # ---------------------------------------------

        else:

            results = (
                vector_store
                .similarity_search_with_score(
                    query,
                    k=4
                )
            )

        all_results.extend(results)

    # ---------------------------------------------
    # GLOBAL RELEVANCE SORTING
    # ---------------------------------------------

    all_results.sort(
        key=lambda item: item[1]
    )

    # ---------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------

    unique_documents = []

    seen = set()

    for document, score in all_results:

        source = document.metadata.get(
            "source",
            ""
        )

        page = document.metadata.get(
            "page",
            ""
        )

        category = document.metadata.get(
            "category",
            ""
        )

        topic = document.metadata.get(
            "topic",
            ""
        )

        scheme = document.metadata.get(
            "scheme",
            ""
        )

        content = document.page_content

        document_id = (
            source,
            page,
            category,
            topic,
            scheme,
            content
        )

        if document_id not in seen:

            seen.add(document_id)

            unique_documents.append(
                document
            )

    # ---------------------------------------------
    # RETURN TOP RESULTS
    # ---------------------------------------------

    top_documents = unique_documents[:5]

    return top_documents