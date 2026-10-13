from ai.rag.document_loader import load_documents
from ai.rag.text_splitter import split_documents
from ai.rag.vector_store import create_vector_store


def build_rag_database():
    print("Loading documents...")

    documents = load_documents()

    if not documents:
        print("No documents found.")
        return None

    print("Splitting documents into chunks...")

    chunks = split_documents(documents)

    if not chunks:
        print("No chunks created.")
        return None

    print("Creating vector database...")

    vector_store = create_vector_store(chunks)

    print("RAG database built successfully!")

    return vector_store


if __name__ == "__main__":
    build_rag_database()