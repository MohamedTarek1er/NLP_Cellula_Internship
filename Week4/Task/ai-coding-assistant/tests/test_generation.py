
from unittest.mock import Mock, patch

import pytest
from langchain_core.documents import Document

from app.Code_Generation.generation import (
    INSUFFICIENT_CONTEXT_MESSAGE,
    generate_code,
)

@pytest.fixture
def sample_documents():
    return [
        Document(
            page_content=(
                "A recursive factorial function needs a base case. "
                "For n <= 1, return 1; otherwise return "
                "n * factorial(n - 1)."
            ),
            metadata={
                "source": "knowledge/python_functions.md",
                "topic": "python_functions",
            },
        )
    ]

def test_generate_code_skips_generation_without_documents():
    with patch(
        "app.generation.retrieve_documents",
        return_value=[],
    ), patch(
        "app.generation.evaluate_context_relevance"
    ) as mock_evaluator, patch(
        "app.generation.llm"
    ) as mock_llm:
        result = generate_code("Write a factorial function")

    assert INSUFFICIENT_CONTEXT_MESSAGE in result
    mock_evaluator.assert_not_called()
    mock_llm.invoke.assert_not_called()

def test_generate_code_skips_generation_when_irrelevant(
    sample_documents,
):
    with patch(
        "app.generation.retrieve_documents",
        return_value=sample_documents,
    ), patch(
        "app.generation.evaluate_context_relevance",
        return_value={
            "relevant": False,
            "reason": "The retrieved information is insufficient.",
        },
    ), patch(
        "app.generation.llm"
    ) as mock_llm:
        result = generate_code("Build a complex web application")

    assert INSUFFICIENT_CONTEXT_MESSAGE in result
    assert "insufficient" in result.lower()
    mock_llm.invoke.assert_not_called()


def test_generate_code_calls_llm_when_relevant(
    sample_documents,
):
    mock_response = Mock()
    mock_response.content = (
        "```python\n"
        "def factorial(n):\n"
        "    if n < 0:\n"
        "        raise ValueError('n must be non-negative')\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)\n"
        "```"
    )

    with patch(
        "app.generation.retrieve_documents",
        return_value=sample_documents,
    ), patch(
        "app.generation.evaluate_context_relevance",
        return_value={
            "relevant": True,
            "reason": "The context explains recursion and the base case.",
        },
    ), patch(
        "app.generation.llm"
    ) as mock_llm:
        mock_llm.invoke.return_value = mock_response
        result = generate_code("Write a factorial function")

    assert "def factorial(n)" in result
    assert "python_functions.md" in result
    mock_llm.invoke.assert_called_once()

def test_generate_code_rejects_empty_query():
    with pytest.raises(ValueError):
        generate_code("   ")
