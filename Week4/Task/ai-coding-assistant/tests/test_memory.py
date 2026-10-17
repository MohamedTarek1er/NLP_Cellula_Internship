
import app.memory as memory


def setup_test_database(monkeypatch, tmp_path):
    monkeypatch.setattr(memory, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        memory,
        "DATABASE_PATH",
        tmp_path / "test_memory.db",
    )
    memory.initialize_memory_db()


def test_messages_persist(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    memory.save_message(
        user_id="user_1",
        conversation_id="chat_1",
        role="user",
        content="Write a Python function.",
        intent="GENERATE",
    )

    memory.save_message(
        user_id="user_1",
        conversation_id="chat_1",
        role="assistant",
        content="Here is a function.",
        intent="GENERATE",
    )

    history = memory.get_recent_history(
        user_id="user_1",
        conversation_id="chat_1",
    )

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_preferences_are_saved_and_updated(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    memory.save_preference(
        "user_1", "programming_language", "python"
    )
    memory.save_preference(
        "user_1", "programming_language", "kotlin"
    )

    preferences = memory.get_preferences("user_1")

    assert preferences["programming_language"] == "kotlin"
    assert len(preferences) == 1


def test_preference_extraction(monkeypatch, tmp_path):
    setup_test_database(monkeypatch, tmp_path)

    detected = memory.extract_and_save_preferences(
        user_id="user_1",
        message=(
            "I prefer Python and Flask. "
            "Give me detailed explanations."
        ),
    )

    assert detected["programming_language"] == "python"
    assert detected["framework"] == "flask"
    assert detected["response_style"] == "detailed"

    saved = memory.get_preferences("user_1")
    assert saved["programming_language"] == "python"
    assert saved["framework"] == "flask"


def test_memory_context_contains_history_and_preferences(
    monkeypatch, tmp_path
):
    setup_test_database(monkeypatch, tmp_path)

    memory.save_preference(
        "user_1", "programming_language", "python"
    )
    memory.save_message(
        "user_1",
        "chat_1",
        "user",
        "Explain recursion.",
    )

    context = memory.build_memory_context(
        "user_1",
        "chat_1",
    )

    assert "python" in context
    assert "Explain recursion." in context
