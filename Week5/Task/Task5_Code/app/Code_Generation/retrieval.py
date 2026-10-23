from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    collection_name="programming_knowledge",
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)

def retrieve_documents(query):
    query = query.strip()

    if not query:
        return []

    search_results = vectordb.similarity_search(query=query, k=4)
    return search_results

def format_documents(documents):
    if not documents:
        return "No relevant documents were retrieved."

    formatted_context = []

    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Unknown")

        formatted_context.append(
            f"[Document {i}]\n"
            f"Source: {source}\n"
            f"Content:\n{doc.page_content}"
        )

    return "\n\n".join(formatted_context)
