
from collections import Counter

from langchain_chroma import Chroma

from ai.rag.config import VECTOR_DB_PATH, COLLECTION_NAME
from ai.rag.embeddings import get_embeddings
from ai.rag.query_router import expand_query


def get_vector_store():
    """Load the existing Chroma vector database."""

    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vector_store


def get_retriever():
    """Return the standard retriever."""

    vector_store = get_vector_store()

    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )


def retrieve_documents(question):
    """
    Retrieve relevant documents using query expansion,
    scheme filtering, and source-diverse ranking.
    """

    vector_store = get_vector_store()

    routing_result = expand_query(question)

    expanded_queries = list(
        routing_result.get("expanded_queries", [])
    )

    detected_schemes = routing_result.get(
        "detected_schemes", []
    )

    women_related = routing_result.get(
        "women_related", False
    )

    all_results = []

    # --------------------------------------------------
    # 1. Women's entrepreneurship retrieval
    # --------------------------------------------------

    if women_related:

        targeted_searches = [
            (
                "PMEGP",
                "PMEGP women entrepreneurs special category subsidy "
                "lower beneficiary contribution",
                {"scheme": "pmegp"}
            ),
            (
                "MUDRA",
                "MUDRA loans women entrepreneurs loan accounts "
                "business financial assistance",
                {"scheme": "mudra"}
            ),
            (
                "DAY-NRLM",
                "DAY NRLM rural women self help groups "
                "livelihood enterprise financial inclusion",
                {"scheme": "day_nrlm"}
            ),
            (
                "PMFME",
                "PMFME women self help groups food processing "
                "micro enterprises subsidy support",
                {"scheme": "pmfme"}
            ),
            (
                "UMED",
                "UMED Maharashtra State Rural Livelihoods Mission "
                "annual action plan women SHG entrepreneurs "
                "Lakhpati Didi",
                {"scheme": "maharashtra_schemes"}
            )
        ]

        for name, query, metadata_filter in targeted_searches:

            results = vector_store.similarity_search_with_score(
                query,
                k=4,
                filter=metadata_filter
            )

            all_results.extend(results)

        # Additional unfiltered search for women's PMEGP evidence
        # in the MSME Annual Report.
        general_women_queries = [
            "women entrepreneurs PMEGP higher subsidy "
            "lower own contribution MSME Annual Report",

            "PMEGP number of women entrepreneur projects "
            "assisted government annual report"
        ]

        for query in general_women_queries:

            results = vector_store.similarity_search_with_score(
                query,
                k=3
            )

            all_results.extend(results)

    # --------------------------------------------------
    # 2. Scheme-specific retrieval
    # --------------------------------------------------

    elif detected_schemes:

        if "pm_vishwakarma" in detected_schemes:

            expanded_queries.extend([
                "PM Vishwakarma scheme objective traditional artisans craftspeople",
                "PM Vishwakarma support for traditional workers and artisans",
                "PM Vishwakarma 18 traditional trades skill training toolkit incentive",
                "PM Vishwakarma scheme benefits collateral free credit assistance"
            ])

        for scheme in detected_schemes:

            for query in expanded_queries:

                results = vector_store.similarity_search_with_score(
                    query,
                    k=5,
                    filter={"scheme": scheme}
                )

                all_results.extend(results)

    # --------------------------------------------------
    # 3. General retrieval
    # --------------------------------------------------

    else:

        for query in expanded_queries:

            results = vector_store.similarity_search_with_score(
                query,
                k=5
            )

            all_results.extend(results)

    # Lower distance means a better match.
    all_results.sort(key=lambda item: item[1])

    # --------------------------------------------------
    # 4. Remove duplicates and balance source documents
    # --------------------------------------------------

    unique_documents = []
    seen = set()
    source_counts = Counter()

    max_per_source = 2
    max_documents = 8

    for document, score in all_results:

        metadata = document.metadata

        source = metadata.get("source", "unknown")

        document_id = (
            source,
            metadata.get("page", ""),
            metadata.get("category", ""),
            metadata.get("topic", ""),
            metadata.get("scheme", ""),
            document.page_content
        )

        if document_id in seen:
            continue

        seen.add(document_id)

        # Limit repeated chunks from the same PDF.
        if source_counts[source] >= max_per_source:
            continue

        unique_documents.append(document)
        source_counts[source] += 1

        if len(unique_documents) >= max_documents:
            break

    return unique_documents
