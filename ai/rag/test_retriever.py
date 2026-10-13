from ai.rag.retriever import retrieve_documents


question = "Are women eligible for MUDRA loans?"

documents = retrieve_documents(question)

print("Documents retrieved:", len(documents))

for i, document in enumerate(documents, start=1):

    source = document.metadata.get("source", "Unknown")
    page = document.metadata.get("page", "Unknown")

    print("\n" + "=" * 80)
    print(f"DOCUMENT {i}")
    print(f"SOURCE: {source}")
    print(f"PAGE: {page}")
    print(f"CHARACTERS: {len(document.page_content)}")
    print("=" * 80)

    # Show the complete retrieved text
    print(document.page_content)