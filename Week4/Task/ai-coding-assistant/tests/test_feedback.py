
from unittest.mock import patch

import pytest

from app.feedback import save_user_solution


def test_save_user_solution():
    with patch("app.feedback.get_vector_store") as mock_get_store:
        result = save_user_solution(
            solution="def add(a, b):\n    return a + b",
            topic="addition_function",
            language="python",
            user_id="test_user",
        )

    assert result["success"] is True
    assert result["topic"] == "addition_function"
    assert result["language"] == "python"

    store = mock_get_store.return_value
    store.add_documents.assert_called_once()

    call_kwargs = store.add_documents.call_args.kwargs
    document = call_kwargs["documents"][0]

    assert "return a + b" in document.page_content
    assert document.metadata["source"] == "user_feedback"
    assert document.metadata["content_type"] == "human_feedback_solution"


def test_save_user_solution_rejects_empty_solution():
    with pytest.raises(ValueError):
        save_user_solution(
            solution="   ",
            topic="addition",
        )


def test_save_user_solution_rejects_empty_topic():
    with pytest.raises(ValueError):
        save_user_solution(
            solution="print('Hello')",
            topic="   ",
        )
