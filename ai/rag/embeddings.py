from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """
    Create and return the embedding model
    used to convert text into vectors.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings