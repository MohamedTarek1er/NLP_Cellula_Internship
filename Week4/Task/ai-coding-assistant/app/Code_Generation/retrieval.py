from langchain_core.documents import Document
from app.Code_Generation.Knowledge_Base.knowledge_base import get_vector_store

def retrieve_documents(
    query: str,
    top_k: int = 4,
) -> list[Document]:

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query=query.strip(),
        k=top_k,
    )

    return results
