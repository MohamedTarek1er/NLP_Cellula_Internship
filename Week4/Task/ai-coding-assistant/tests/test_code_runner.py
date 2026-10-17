import subprocess
from unittest.mock import patch

import pytest

from app.Code_Execution.code_runner import execute_python_code

def test_successful_execution():
    completed = subprocess.CompletedProcess(
        args=["docker"],
        returncode=0,
        stdout="2\n",
        stderr="",
    )

    with patch(
        "app.Code_Execution.code_runner.subprocess.run",
        return_value=completed,
    ) as mock_run:
        result = execute_python_code("print(1 + 1)")

    assert result["success"] is True
    assert result["stdout"] == "2\n"
    assert result["stderr"] == ""
    assert result["exit_code"] == 0
    assert result["timed_out"] is False
    assert result["error"] is None

    # Verify that code is sent through stdin, not a shell command.
    kwargs = mock_run.call_args.kwargs
    assert kwargs["input"] == "print(1 + 1)"
    assert kwargs["capture_output"] is True
    assert kwargs["timeout"] == 10


def test_runtime_error():
    completed = subprocess.CompletedProcess(
        args=["docker"],
        returncode=1,
        stdout="",
        stderr="ValueError: test error",
    )

    with patch(
        "app.Code_Execution.code_runner.subprocess.run",
        return_value=completed,
    ):
        result = execute_python_code(
            'raise ValueError("test error")'
        )

    assert result["success"] is False
    assert result["exit_code"] == 1
    assert "ValueError" in result["stderr"]


def test_timeout():
    error = subprocess.TimeoutExpired(
        cmd=["docker"],
        timeout=2,
        output=b"partial output",
        stderr=b"",
    )

    with patch(
        "app.Code_Execution.code_runner.subprocess.run",
        side_effect=error,
    ):
        result = execute_python_code(
            "while True: pass",
            timeout_seconds=2,
        )

    assert result["success"] is False
    assert result["timed_out"] is True
    assert result["exit_code"] is None
    assert "timeout" in result["error"].lower()


def test_empty_source_is_rejected():
    with pytest.raises(ValueError):
        execute_python_code("   ")


def test_non_string_source_is_rejected():
    with pytest.raises(ValueError):
        execute_python_code(None)


def test_invalid_timeout_is_rejected():
    with pytest.raises(ValueError):
        execute_python_code(
            "print('hello')",
            timeout_seconds=0,
        )


def test_oversized_source_is_rejected():
    with pytest.raises(ValueError):
        execute_python_code(" " * 50_001)


def test_missing_docker():
    with patch(
        "app.Code_Execution.code_runner.subprocess.run",
        side_effect=FileNotFoundError,
    ):
        result = execute_python_code("print('hello')")

    assert result["success"] is False
    assert result["exit_code"] is None
    assert "Docker CLI" in result["error"]
