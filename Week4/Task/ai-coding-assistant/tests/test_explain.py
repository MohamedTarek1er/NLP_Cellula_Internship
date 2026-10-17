
from unittest.mock import Mock, patch

import pytest

from app.Code_Explanation.explain import explain_code


def test_explain_code_returns_response():
    mock_response = Mock()
    mock_response.content = "The loop iterates over the list."

    with patch(
        "app.explain.llm",
    ) as mock_llm:
        mock_llm.invoke.return_value = mock_response

        result = explain_code(
            "Explain this loop: for x in [1, 2]: print(x)"
        )

    assert result == "The loop iterates over the list."
    mock_llm.invoke.assert_called_once()


def test_explain_code_rejects_empty_query():
    with patch("app.explain.llm") as mock_llm:
        with pytest.raises(ValueError):
            explain_code("   ")

        mock_llm.invoke.assert_not_called()


def test_explain_code_rejects_empty_response():
    mock_response = Mock()
    mock_response.content = "   "

    with patch("app.explain.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response

        with pytest.raises(RuntimeError):
            explain_code("Explain a Python function.")


def test_explain_code_rejects_unexpected_response():
    mock_response = Mock()
    mock_response.content = ["unexpected", "response"]

    with patch("app.explain.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response

        with pytest.raises(RuntimeError):
            explain_code("Explain a Python function.")
