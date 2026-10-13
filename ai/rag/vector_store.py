from langchain_chroma import Chroma

from ai.rag.config import VECTOR_DB_PATH, COLLECTION_NAME
from ai.rag.embeddings import get_embeddings


def create_vector_store(chunks):
    """
    Create a ChromaDB vector store from document chunks.
    """

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
        collection_name=COLLECTION_NAME
    )

    print("Vector database created successfully.")

    return vector_store