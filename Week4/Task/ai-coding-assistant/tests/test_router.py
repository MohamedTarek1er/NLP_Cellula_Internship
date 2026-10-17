import sys
from types import ModuleType
from unittest.mock import Mock, patch

import pytest

from app.Intent_Classifier.classifier import Intent
from app.router import route_query

def test_router_explain():
    mock_explain = Mock(
        return_value="This code prints the numbers."
    )

    fake_module = ModuleType("app.explain")
    fake_module.explain_code = mock_explain

    with patch(
        "app.router.classify_intent",
        return_value=Intent.EXPLAIN,
    ), patch.dict(
        sys.modules,
        {"app.explain": fake_module},
    ):
        result = route_query("Explain this code")

    assert result["intent"] == "EXPLAIN"
    assert result["answer"] == "This code prints the numbers."
    mock_explain.assert_called_once_with("Explain this code")


def test_router_generate():
    mock_generate = Mock(
        return_value="```python\nprint('Hello')\n```"
    )

    fake_module = ModuleType("app.generation")
    fake_module.generate_code = mock_generate

    with patch(
        "app.router.classify_intent",
        return_value=Intent.GENERATE,
    ), patch.dict(
        sys.modules,
        {"app.generation": fake_module},
    ):
        result = route_query("Write Python code")

    assert result["intent"] == "GENERATE"
    assert "print('Hello')" in result["answer"]
    mock_generate.assert_called_once_with("Write Python code")


def test_router_rejects_empty_query():
    with pytest.raises(ValueError):
        route_query("   ")
