
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_DIR = Path("data")
VECTOR_DIR = "vector_store"

def load_documents(data_dir=DATA_DIR):
    documents = []

    for path in Path(data_dir).rglob("*"):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            loader = PyPDFLoader(str(path))
        elif suffix in {".txt", ".md"}:
            loader = TextLoader(
                str(path),
                encoding="utf-8",
            )
        else:
            continue

        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata.update({
                "source": str(path),
                "file_name": path.name,
                "source_type": suffix.lstrip("."),
            })

        documents.extend(loaded_docs)

    if not documents:
        raise ValueError("No supported documents found.")

    return documents


def create_vector_store():
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(
        chunks,
        embeddings,
    )

    vector_db.save_local(VECTOR_DIR)
    
if __name__ == "__main__":
    create_vector_store()