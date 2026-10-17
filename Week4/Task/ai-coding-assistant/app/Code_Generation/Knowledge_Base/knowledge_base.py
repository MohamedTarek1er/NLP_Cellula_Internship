from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"

COLLECTION_NAME = "programming_knowledge"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

def get_vector_store() -> Chroma:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )

def load_knowledge_documents() -> list[Document]:

    paths = sorted(KNOWLEDGE_DIR.rglob("*.md"))
    documents = []

    for path in paths:
        content = path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        source = path.relative_to(PROJECT_ROOT).as_posix()
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": source,
                    "topic": path.stem,
                    "file_type": path.suffix.lstrip("."),
                },
            )
        )

    return documents

def split_documents(
    documents: list[Document],
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    return chunks
