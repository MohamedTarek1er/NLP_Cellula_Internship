import subprocess

DOCKER_IMAGE = "python:3.10-slim"

DEFAULT_TIMEOUT = 10
MAX_TIMEOUT = 30
MAX_CODE_LENGTH = 50_000
MAX_OUTPUT_LENGTH = 20_000

def _decode_output(value) -> str:
    """Convert subprocess output into a string safely."""
    if value is None:
        return ""

    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")

    return str(value)

def execute_python_code(
    source_code: str,
    timeout_seconds: int = DEFAULT_TIMEOUT,
) -> dict:

    if not isinstance(source_code, str):
        raise ValueError("Source code must be a string.")

    if not source_code.strip():
        raise ValueError("Source code must not be empty.")

    if len(source_code) > MAX_CODE_LENGTH:
        raise ValueError(
            f"Source code exceeds {MAX_CODE_LENGTH} characters."
        )

    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not 0 < timeout_seconds <= MAX_TIMEOUT
    ):
        raise ValueError(
            f"Timeout must be greater than 0 and "
            f"at most {MAX_TIMEOUT} seconds."
        )

    command = [
        "docker",
        "run",
        "--rm",
        "--interactive",
        "--network", "none",
        "--memory", "128m",
        "--memory-swap", "128m",
        "--cpus", "0.5",
        "--pids-limit", "64",
        "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=16m",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges:true",
        "--user", "65534:65534",
        "--workdir", "/tmp",
        DOCKER_IMAGE,
        "python", "-I", "-S", "-B", "-",
    ]

    try:
        result = subprocess.run(
            command,
            input=source_code,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )

    except subprocess.TimeoutExpired as exc:
        stdout = _decode_output(exc.stdout)
        stderr = _decode_output(exc.stderr)

        return {
            "success": False,
            "stdout": stdout[:MAX_OUTPUT_LENGTH],
            "stderr": stderr[:MAX_OUTPUT_LENGTH],
            "exit_code": None,
            "timed_out": True,
            "error": (
                f"Execution exceeded the "
                f"{timeout_seconds}-second timeout."
            ),
        }

    except FileNotFoundError:
        return {
            "success": False,
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "timed_out": False,
            "error": (
                "Docker CLI was not found. Install Docker Desktop, "
                "start it, and verify that 'docker info' works."
            ),
        }

    stdout = result.stdout[:MAX_OUTPUT_LENGTH]
    stderr = result.stderr[:MAX_OUTPUT_LENGTH]

    docker_error = result.returncode in (125, 126, 127)

    return {
        "success": result.returncode == 0,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": result.returncode,
        "timed_out": False,
        "error": (
            "Docker could not start the execution environment."
            if docker_error
            else None
        ),
    }
