from hashlib import sha256
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    collection_name="programming_knowledge",
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def save_user_knowledge(topic, content):
    
    topic = topic.strip()
    content = content.strip()

    if not content:
        print("No data provided. Nothing was saved.")
        return        

    document = Document(
        page_content=content,
        metadata={
            "source": "user_feedback",
            "topic": topic or "general",
            "content_type": "user_provided_knowledge"
        }
    )

    chunks = splitter.split_documents([document])

    if not chunks:
        print("No Chunks were generated.")
        return

    base_id = sha256(
        (
            document.metadata["source"]
            + "\n"
            + document.metadata["topic"]
            + "\n"
            + document.page_content
        ).encode("utf-8")
    ).hexdigest()

    chunk_ids = [
        sha256(
            f"{base_id}:{i}:{chunk.page_content}".encode("utf-8")
        ).hexdigest()
        for i, chunk in enumerate(chunks)
    ]

    vectordb.add_documents(
        documents=chunks,
        ids=chunk_ids
    )

    print(f"Knowledge saved successfully!, chunks_saved: {len(chunks)}")
