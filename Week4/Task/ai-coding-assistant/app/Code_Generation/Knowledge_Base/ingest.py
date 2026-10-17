import hashlib

from app.Code_Generation.Knowledge_Base.knowledge_base import (
    get_vector_store,
    load_knowledge_documents,
    split_documents,
)

def make_chunk_id(source: str, content: str) -> str:
    raw = f"{source}\n{content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def ingest_knowledge_base() -> int:

    documents = load_knowledge_documents()
    chunks = split_documents(documents)
    vector_store = get_vector_store()

    ids = [
        make_chunk_id(
            str(chunk.metadata["source"]),
            chunk.page_content,
        )
        for chunk in chunks
    ]

    vector_store.add_documents(
        documents=chunks,
        ids=ids,
    )

    print(f"Loaded source documents: {len(documents)}")
    print(f"Processed chunks: {len(chunks)}")
    print("Knowledge base stored in Chroma.")

    return len(chunks)

if __name__ == "__main__":
    ingest_knowledge_base()
