import re

from app.Intent_Classifier.classifier import Intent, classify_intent
from app.Code_Generation.User_Feedback.memory import (
    extract_and_save_preferences,
    get_recent_history,
    save_message,
    build_memory_context,
)
from app.Code_Generation.User_Feedback.feedback import save_user_solution
from app.Code_Explanation.explain import explain_code
from app.Code_Generation.generation import generate_code

def detect_programming_language(solution: str) -> str:
    """Identify a likely programming language from a submitted solution."""
    if re.search(
        r"\b(def|elif|None|print|import|self)\b",
        solution,
    ):
        return "python"

    if re.search(
        r"\b(fun|val|var|when|println)\b",
        solution,
    ):
        return "kotlin"

    if re.search(
        r"\b(function|const|let|console\.log)\b",
        solution,
    ):
        return "javascript"

    if re.search(
        r"\b(public\s+static\s+void\s+main|System\.out)\b",
        solution,
    ):
        return "java"

    if re.search(
        r"#include\s*<|std::",
        solution,
    ):
        return "cpp"

    if re.search(
        r"\b(using\s+System|namespace\s+\w+)\b",
        solution,
    ):
        return "csharp"

    return "unknown"


def looks_like_programming_solution(text: str) -> bool:
    """Accept recognizable code rather than arbitrary follow-up messages."""
    if not isinstance(text, str) or not text.strip():
        return False

    if "```" in text:
        return True

    code_patterns = [
        r"^\s*def\s+\w+\s*\(",
        r"^\s*class\s+\w+",
        r"^\s*function\s+\w+",
        r"^\s*fun\s+\w+",
        r"^\s*import\s+\w+",
        r"^\s*#include\s*<",
        r"^\s*(const|let|var)\s+\w+",
        r"^\s*public\s+static\s+void\s+main",
    ]

    return any(
        re.search(pattern, text, re.MULTILINE)
        for pattern in code_patterns
    )

def route_query(
    query: str,
    user_id: str = "default",
    conversation_id: str = "default",
) -> dict:
    """Classify, process, and remember one user interaction."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("The user query must not be empty.")

    query = query.strip()

    # Step 1: Load recent history to determine whether feedback was requested.
    recent = get_recent_history(
        user_id=user_id,
        conversation_id=conversation_id,
        limit=10,
    )

    previous_assistant = next(
        (
            item
            for item in reversed(recent)
            if item["role"] == "assistant"
        ),
        None,
    )

    previous_user = next(
        (
            item
            for item in reversed(recent)
            if item["role"] == "user"
        ),
        None,
    )

    feedback_was_requested = (
        previous_assistant is not None
        and (
            "provide a correct solution"
            in previous_assistant["content"].lower()
            or "provide a solution or a reference"
            in previous_assistant["content"].lower()
        )
    )

    # Step 2: Handle a user-provided programming solution.
    if feedback_was_requested and looks_like_programming_solution(query):
        topic = (
            previous_user["content"][:200]
            if previous_user
            else "user_submitted_solution"
        )

        result = save_user_solution(
            solution=query,
            topic=topic,
            language=detect_programming_language(query),
            user_id=user_id,
        )

        answer = (
            "Thank you! Your submitted solution has been added "
            "to the programming knowledge base. Future retrieval "
            "requests can search for it."
        )

        save_message(
            user_id=user_id,
            conversation_id=conversation_id,
            role="user",
            content=query,
            intent="FEEDBACK",
        )

        save_message(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            intent="FEEDBACK",
        )

        return {
            "intent": "FEEDBACK",
            "answer": answer,
            "conversation_id": conversation_id,
            "solution_id": result["solution_id"],
        }

    # Step 3: Detect and save explicit preferences from the current query.
    extract_and_save_preferences(
        user_id=user_id,
        message=query,
    )

    # Step 4: Build memory before saving the current user message.
    # This gives the LLM previous history plus newly detected preferences.
    memory_context = build_memory_context(
        user_id=user_id,
        conversation_id=conversation_id,
        history_limit=10,
    )

    # Step 5: Save the incoming user message.
    save_message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=query,
    )

    # Step 6: Classify and process the request.
    intent = classify_intent(query)

    if intent == Intent.EXPLAIN:
        answer = explain_code(
            query,
            memory_context=memory_context,
        )

    elif intent == Intent.GENERATE:
        answer = generate_code(
            query,
            user_id=user_id,
            conversation_id=conversation_id,
            memory_context=memory_context,
        )

    else:
        raise ValueError(f"Unsupported intent: {intent}")

    # Step 7: Save the completed assistant response.
    save_message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=answer,
        intent=intent.value,
    )

    return {
        "intent": intent.value,
        "answer": answer,
        "conversation_id": conversation_id,
    }
