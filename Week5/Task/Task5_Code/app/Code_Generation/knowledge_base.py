from pathlib import Path
from hashlib import sha256

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

knowledge_dir = Path(r"C:\Users\moham\Downloads\NLP_Cellula\Task4_Try\knowledge")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    collection_name="programming_knowledge",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

for file_path in knowledge_dir.rglob("*.md"):
    loader = UnstructuredMarkdownLoader(str(file_path))
    documents = loader.load()

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["source"] = str(file_path)

    ids = [
        sha256((chunk.metadata["source"]+ "\n"+ 
                chunk.page_content).encode("utf-8")).hexdigest()
        for chunk in chunks
    ]

    if chunks:
        vectordb.add_documents(
            documents=chunks,
            ids=ids
        )

print("Markdown ingestion completed.")