
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = "vector_store"

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        VECTOR_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_documents(question, vector_db, k=4):
    
    results = vector_db.similarity_search_with_score(
        question,
        k=k,
    )

    retrieved = []

    for document, score in results:
        retrieved.append({"content": document.page_content})

    return retrieved