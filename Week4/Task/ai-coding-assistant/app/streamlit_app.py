
import re
import uuid

import streamlit as st

from app.router import route_query
from app.Code_Generation.User_Feedback.memory import (
    get_recent_history,
    initialize_memory_db,
)
from app.Code_Execution.code_runner import execute_python_code


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="CodePilot | Intelligent Coding Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Theme
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #101729;
        border-right: 1px solid #273550;
    }

    .hero {
        padding: 25px 28px;
        margin-bottom: 22px;
        border-radius: 18px;
        border: 1px solid #293957;
        background: linear-gradient(120deg, #192744, #111827);
    }

    .hero h1 {
        color: #f8fafc;
        font-size: 2.1rem;
        margin: 0;
    }

    .hero p {
        color: #a8b8d0;
        margin: 8px 0 0 0;
    }

    .muted {
        color: #9caec8;
        font-size: 0.92rem;
    }

    div[data-testid="stMetric"] {
        background: #121b2e;
        border: 1px solid #293550;
        padding: 14px;
        border-radius: 12px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 10px;
        min-height: 40px;
        font-weight: 600;
    }

    div[data-testid="stTextArea"] textarea {
        background: #0e1628;
        color: #e5e7eb;
        border: 1px solid #34415c;
        border-radius: 10px;
        font-family: monospace;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid #26344d;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 12px;
    }

    hr {
        border-color: #273550;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Persistent session state
# =========================================================

if "user_id" not in st.session_state:
    st.session_state.user_id = "default"

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "sandbox_code" not in st.session_state:
    st.session_state.sandbox_code = (
        'print("Hello from CodePilot!")\n'
        "for number in range(1, 4):\n"
        "    print(number)\n"
    )

if "execution_result" not in st.session_state:
    st.session_state.execution_result = None

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "last_intent" not in st.session_state:
    st.session_state.last_intent = ""

if "last_request" not in st.session_state:
    st.session_state.last_request = ""


# =========================================================
# Helpers
# =========================================================

def extract_python_code(answer: str) -> str:
    """
    Extract Python code from the assistant's Markdown response.
    Prefer explicitly labelled Python fences.
    """
    if not isinstance(answer, str):
        return ""

    python_blocks = re.findall(
        r"```(?:python|py)\s*\n(.*?)```",
        answer,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if python_blocks:
        return python_blocks[0].strip()

    # Fall back to an unlabelled fenced code block.
    generic_blocks = re.findall(
        r"```\s*\n(.*?)```",
        answer,
        flags=re.DOTALL,
    )

    if generic_blocks:
        return generic_blocks[0].strip()

    return ""


def load_conversation():
    """Read persisted conversation history for this user and session."""
    return get_recent_history(
        user_id=st.session_state.user_id,
        conversation_id=st.session_state.conversation_id,
        limit=200,
    )


# Initialize the SQLite database.
initialize_memory_db()


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:
    st.markdown("## ⚡ CodePilot")
    st.caption("Intelligent AI Coding Assistant")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "AI Chat",
            "Python Sandbox",
            "Memory & Feedback",
            "About & Security",
        ],
    )

    st.divider()
    st.markdown("### Conversation")

    st.text_input(
        "User ID",
        key="user_id",
        help=(
            "Used to separate stored preferences and conversation "
            "history. Use a consistent ID to retrieve that user's memory."
        ),
    )

    st.code(
        st.session_state.conversation_id[:8],
        language="text",
    )

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.last_answer = ""
        st.session_state.last_intent = ""
        st.session_state.last_request = ""
        st.session_state.execution_result = None
        st.rerun()

    st.divider()
    st.caption("RAG · Memory · Feedback · Docker")


# =========================================================
# Header
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>CodePilot</h1>
        <p>
            Your coding workspace for programming explanations,
            retrieval-grounded generation, persistent memory,
            and isolated Python execution.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# AI Chat
# =========================================================

if page == "AI Chat":
    st.subheader("AI Coding Assistant")
    st.markdown(
        '<p class="muted">Ask a question, request code, or continue '
        'a previous conversation.</p>',
        unsafe_allow_html=True,
    )

    try:
        history = load_conversation()
    except Exception as exc:
        st.error(f"Could not load conversation history: {exc}")
        history = []

    # Render messages stored by route_query in SQLite.
    for message in history:
        role = message.get("role", "assistant")

        # Streamlit chat messages accept user and assistant roles.
        if role not in ("user", "assistant"):
            continue

        with st.chat_message(role):
            content = message.get("content", "")

            if role == "assistant" and message.get("intent"):
                st.caption(f"Intent: {message['intent']}")

            st.markdown(content)

    prompt = st.chat_input(
        "Ask about code, generate a solution, or submit feedback..."
    )

    if prompt:
        try:
            with st.spinner(
                "Classifying your request, retrieving context, and preparing a response..."
            ):
                result = route_query(
                    query=prompt,
                    user_id=st.session_state.user_id.strip() or "default",
                    conversation_id=st.session_state.conversation_id,
                )

            st.session_state.last_request = prompt
            st.session_state.last_answer = result.get("answer", "")
            st.session_state.last_intent = result.get("intent", "")

            # Display the new interaction immediately.
            st.rerun()

        except Exception as exc:
            st.error(f"Unable to process your request: {exc}")

    # Show actions for the latest generated solution.
    if st.session_state.last_intent == "GENERATE":
        code = extract_python_code(st.session_state.last_answer)

        if code:
            st.divider()
            st.markdown("#### Generated solution")

            if st.button(
                "Load latest Python code into Sandbox",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.sandbox_code = code
                st.session_state.execution_result = None
                st.success(
                    "Code loaded. Open Python Sandbox to review it."
                )

    if st.session_state.last_intent == "FEEDBACK":
        st.success(
            "Your submitted solution was accepted by the feedback workflow."
        )


# =========================================================
# Python Sandbox
# =========================================================

elif page == "Python Sandbox":
    st.subheader("Python Execution Sandbox")
    st.markdown(
        '<p class="muted">Review generated or manually entered code '
        'before executing it through Docker.</p>',
        unsafe_allow_html=True,
    )

    st.warning(
        "Docker restrictions reduce risk but do not guarantee complete "
        "isolation. Review code before running it."
    )

    with st.form("python_execution_form"):
        st.text_area(
            "Python code",
            key="sandbox_code",
            height=350,
        )

        timeout_seconds = st.slider(
            "Execution timeout (seconds)",
            min_value=1,
            max_value=30,
            value=10,
        )

        run_clicked = st.form_submit_button(
            "▶ Run Python",
            type="primary",
            use_container_width=True,
        )

    if run_clicked:
        try:
            with st.spinner("Running code in Docker..."):
                st.session_state.execution_result = (
                    execute_python_code(
                        source_code=st.session_state.sandbox_code,
                        timeout_seconds=timeout_seconds,
                    )
                )
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Execution request failed: {exc}")

    result = st.session_state.execution_result

    if result is not None:
        st.divider()
        st.subheader("Execution results")

        if result.get("success"):
            st.success("Execution completed successfully.")
        elif result.get("timed_out"):
            st.warning("Execution timed out.")
        else:
            st.error("Execution failed.")

        col1, col2, col3 = st.columns(3)

        with col1:
            exit_code = result.get("exit_code")
            st.metric(
                "Exit code",
                str(exit_code) if exit_code is not None else "N/A",
            )

        with col2:
            st.metric(
                "Timeout",
                "Yes" if result.get("timed_out") else "No",
            )

        with col3:
            st.metric(
                "Status",
                "Success" if result.get("success") else "Failed",
            )

        output_tab, error_tab, details_tab = st.tabs(
            ["Standard Output", "Error Output", "Execution Details"]
        )

        with output_tab:
            stdout = result.get("stdout", "")
            if stdout:
                st.code(stdout, language="text")
            else:
                st.caption("No standard output was produced.")

        with error_tab:
            stderr = result.get("stderr", "")
            error = result.get("error")

            if stderr:
                st.code(stderr, language="text")

            if error:
                st.error(error)

            if not stderr and not error:
                st.caption("No error output was produced.")

        with details_tab:
            st.json(result)


# =========================================================
# Memory & Feedback
# =========================================================

elif page == "Memory & Feedback":
    st.subheader("Conversation Memory & Learning")
    st.markdown(
        "This page shows saved conversation history and explains "
        "how the existing feedback workflow works."
    )

    st.info(
        "Your router detects feedback when the previous assistant "
        "message requests a correct solution or reliable reference. "
        "Submit the solution in the same conversation so the router "
        "can associate it with that request."
    )

    try:
        history = load_conversation()

        st.markdown("#### Recent conversation")

        if history:
            for message in history:
                with st.container(border=True):
                    st.caption(
                        f"{message.get('role', 'unknown').title()} · "
                        f"{message.get('created_at', '')}"
                    )
                    st.markdown(message.get("content", ""))

        else:
            st.caption("No messages have been saved in this conversation.")

    except Exception as exc:
        st.error(f"Could not retrieve memory: {exc}")

    st.divider()
    st.markdown("#### How feedback learning works")

    st.markdown(
        "1. The generation pipeline checks retrieved context relevance.\n"
        "2. If relevant knowledge is insufficient, the assistant asks "
        "for a solution or reliable reference.\n"
        "3. Submit a recognizable programming solution in this conversation.\n"
        "4. The router calls `save_user_solution()`.\n"
        "5. The solution is added to the vector store for future retrieval."
    )


# =========================================================
# About & Security
# =========================================================

else:
    st.subheader("System Overview")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### AI pipeline")
            st.markdown(
                "- Intent classification\n"
                "- Code explanation with memory\n"
                "- RAG-based code generation\n"
                "- Context relevance evaluation\n"
                "- Retrieved-source reporting\n"
                "- User-solution feedback"
            )

    with col2:
        with st.container(border=True):
            st.markdown("#### Persistence and execution")
            st.markdown(
                "- SQLite conversation history\n"
                "- Saved programming preferences\n"
                "- Vector-store knowledge retrieval\n"
                "- Docker-based Python execution\n"
                "- Output, errors, exit codes and timeouts"
            )

    st.divider()
    st.markdown("#### Docker execution restrictions")

    st.markdown(
        "- Network disabled inside the container.\n"
        "- Memory, CPU and process limits.\n"
        "- Read-only root filesystem.\n"
        "- Restricted temporary filesystem.\n"
        "- Dropped capabilities and non-root user.\n"
        "- Execution timeout and capped displayed output."
    )

    st.warning(
        "The current executor captures all subprocess output before "
        "truncating it. Incremental, bounded output capture is recommended "
        "before exposing the service to untrusted users."
    )

    st.caption(
        "The interface calls your existing application modules; "
        "it does not replace your retrieval, memory, or feedback logic."
    )
