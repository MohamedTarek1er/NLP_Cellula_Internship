import hashlib
from datetime import datetime, timezone

from langchain_core.documents import Document
from app.Code_Generation.Knowledge_Base.knowledge_base import get_vector_store

def save_user_solution(
    solution: str,
    topic: str,
    language: str = "unknown",
    user_id: str = "default",
    source: str = "user_feedback",
) -> dict:

    solution = solution.strip()
    topic = topic.strip()
    language = language.strip().lower()
    user_id = user_id.strip()

    content_to_hash = (
        f"{user_id}\n{topic}\n{language}\n{solution}"
    )
    solution_id = hashlib.sha256(
        content_to_hash.encode("utf-8")
    ).hexdigest()

    document = Document(
        page_content=(
            f"Programming language: {language}\n"
            f"Topic: {topic}\n\n"
            f"User-provided solution:\n{solution}"
        ),
        metadata={
            "source": source,
            "topic": topic,
            "language": language,
            "user_id": user_id,
            "content_type": "human_feedback_solution",
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    vector_store = get_vector_store()
    vector_store.add_documents(
        documents=[document],
        ids=[solution_id],
    )

    return {
        "success": True,
        "solution_id": solution_id,
        "topic": topic,
        "language": language,
        "message": "The solution was stored in the knowledge base.",
    }
