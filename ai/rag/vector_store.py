
from langchain_chroma import Chroma

from ai.rag.config import VECTOR_DB_PATH, COLLECTION_NAME
from ai.rag.embeddings import get_embeddings


def create_vector_store(chunks):
    """
    Rebuild the configured Chroma collection from document chunks.
    Existing data in this collection is replaced.
    Other collections are preserved.
    """

    embeddings = get_embeddings()

    # Connect to the existing database and remove only
    # the collection being rebuilt, if it exists.
    existing_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    try:
        existing_store.delete_collection()
        print(f"Removed existing collection: {COLLECTION_NAME}")
    except Exception as error:
        print(f"Could not delete existing collection: {error}")
        raise

    # Create a fresh collection using the new document chunks.
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
        collection_name=COLLECTION_NAME,
    )

    print(f"Vector database rebuilt with {len(chunks)} chunks.")

    return vector_store
