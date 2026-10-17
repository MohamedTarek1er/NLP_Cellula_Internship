import sqlite3
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "conversation_memory.db"

def get_connection():
    """Create the data directory and return a SQLite connection."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_memory_db():
    """Create the conversation and preference tables if needed."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                intent TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_messages_conversation
            ON messages (user_id, conversation_id, id)
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, preference_key)
            )
            """
        )

def save_message(
    user_id: str,
    conversation_id: str,
    role: str,
    content: str,
    intent: str | None = None,
):
    initialize_memory_db()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO messages (
                user_id, conversation_id, role, content, intent
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id.strip(),
                conversation_id.strip(),
                role,
                content.strip(),
                intent,
            ),
        )

        return cursor.lastrowid

def get_recent_history(
    user_id: str,
    conversation_id: str,
    limit: int = 10,
) -> list[dict]:
    """Return the most recent messages in chronological order."""

    if limit < 1:
        raise ValueError("limit must be at least 1.")

    initialize_memory_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT role, content, intent, created_at
            FROM messages
            WHERE user_id = ? AND conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, conversation_id, limit),
        ).fetchall()

    return [dict(row) for row in reversed(rows)]

def save_preference(
    user_id: str,
    preference_key: str,
    preference_value: str,
):

    initialize_memory_db()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO preferences (
                user_id, preference_key, preference_value
            )
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, preference_key)
            DO UPDATE SET
                preference_value = excluded.preference_value,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                user_id.strip(),
                preference_key.strip().lower(),
                preference_value.strip(),
            ),
        )

def get_preferences(user_id: str) -> dict[str, str]:
    """Return all saved preferences belonging to one user."""

    initialize_memory_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT preference_key, preference_value
            FROM preferences
            WHERE user_id = ?
            ORDER BY preference_key
            """,
            (user_id,),
        ).fetchall()

    return {
        row["preference_key"]: row["preference_value"]
        for row in rows
    }

def build_memory_context(
    user_id: str,
    conversation_id: str,
    history_limit: int = 10,
) -> str:
    """Format stored preferences and recent turns for an LLM prompt."""

    preferences = get_preferences(user_id)
    history = get_recent_history(
        user_id=user_id,
        conversation_id=conversation_id,
        limit=history_limit,
    )

    sections = []

    if preferences:
        preference_lines = [
            f"- {key}: {value}"
            for key, value in preferences.items()
        ]

        sections.append(
            "Saved user preferences:\n"
            + "\n".join(preference_lines)
        )

    if history:
        history_lines = []

        for message in history:
            role = message["role"].upper()
            history_lines.append(
                f"{role}: {message['content']}"
            )

        sections.append(
            "Recent conversation history:\n"
            + "\n\n".join(history_lines)
        )

    if not sections:
        return "No previous conversation memory is available."

    return "\n\n".join(sections)

def extract_and_save_preferences(
    user_id: str,
    message: str,
) -> dict[str, str]:
    """
    Detect a small set of explicit preference statements.

    Examples:
    - I prefer Python.
    - I prefer Flask.
    - I prefer concise answers.
    """

    if not isinstance(message, str):
        return {}

    text = message.strip()
    if not text:
        return {}

    detected = {}

    language_match = re.search(
        r"\b(?:i prefer|use|always use|my preferred language is)"
        r"\s+(python|java|kotlin|javascript|typescript|c\+\+|c#)\b",
        text,
        re.IGNORECASE,
    )

    if language_match:
        detected["programming_language"] = (
            language_match.group(1).lower()
        )

    framework_match = re.search(
        r"\b(?:i prefer|use|always use|my preferred framework is)"
        r"\s+(flask|django|fastapi|streamlit|react|angular|"
        r"spring boot|tensorflow|pytorch)\b",
        text,
        re.IGNORECASE,
    )

    if framework_match:
        detected["framework"] = framework_match.group(1).lower()

    if re.search(
        r"\b(?:i prefer|keep|make)\s+"
        r"(?:your answers |the answers )?"
        r"(?:concise|brief|short)\b",
        text,
        re.IGNORECASE,
    ):
        detected["response_style"] = "concise"

    if re.search(
        r"\b(?:i prefer|give me|provide)\s+"
        r"(?:detailed|in-depth|step-by-step)\s+"
        r"(?:answers|explanations|guidance|instructions)?",
        text,
        re.IGNORECASE,
    ):
        detected["response_style"] = "detailed"

    for key, value in detected.items():
        save_preference(user_id, key, value)

    return detected

if __name__ == "__main__":
    initialize_memory_db()
    print(f"Conversation memory initialized at: {DATABASE_PATH}")
