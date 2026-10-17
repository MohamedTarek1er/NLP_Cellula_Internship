from app.Code_Generation.retrieval import retrieve_documents

def main():
    query = "How do I write a Python function with parameters?"

    documents = retrieve_documents(query, top_k=4)

    if not documents:
        print("No documents were retrieved.")
        return

    for index, document in enumerate(documents, start=1):
        print(f"\n--- Result {index} ---")
        print("Source:", document.metadata.get("source", "Unknown"))
        print("Topic:", document.metadata.get("topic", "Unknown"))
        print("Content:")
        print(document.page_content)


if __name__ == "__main__":
    main()
