
import streamlit as st
import io
import contextlib

from intent_classifier import intent_classification
from code_explanation import explain_code

from Code_Generation.retrieval import (
    retrieve_documents,
    format_documents,
)
from Code_Generation.relevance import evaluate_relevance
from Code_Generation.generation import generate_code
from Code_Generation.user_knowledge import save_user_knowledge


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CodePilot AI",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .stApp [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                ellipse at top left,
                rgba(79, 70, 229, 0.12),
                transparent 38%
            ),
            var(--background-color);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.18);
    }

    .hero {
        padding: 28px 30px;
        border: 1px solid rgba(128, 128, 128, 0.20);
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            rgba(79, 70, 229, 0.17),
            rgba(14, 165, 233, 0.07)
        );
        margin-bottom: 25px;
    }

    .hero-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #818cf8;
        margin-bottom: 10px;
    }

    .hero h1 {
        font-size: clamp(30px, 4vw, 43px);
        font-weight: 800;
        letter-spacing: -1.5px;
        margin: 0;
        padding: 0;
    }

    .hero p {
        font-size: 15px;
        line-height: 1.8;
        opacity: 0.78;
        max-width: 720px;
        margin-top: 12px;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        margin: 8px 0 5px 0;
    }

    .section-subtitle {
        opacity: 0.68;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .feature-card {
        padding: 19px;
        min-height: 140px;
        border: 1px solid rgba(128, 128, 128, 0.20);
        border-radius: 16px;
        background: rgba(128, 128, 128, 0.045);
    }

    .feature-icon {
        font-size: 25px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .feature-description {
        font-size: 13px;
        opacity: 0.7;
        line-height: 1.6;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid rgba(128, 128, 128, 0.12);
        border-radius: 15px;
        padding: 15px 18px;
        margin-bottom: 12px;
    }

    div[data-testid="stChatInput"] {
        border-radius: 16px;
    }

    .status-label {
        font-size: 12px;
        opacity: 0.65;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #818cf8;
    }

    hr {
        opacity: 0.15;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_knowledge" not in st.session_state:
    st.session_state.pending_knowledge = None

if "sandbox_code" not in st.session_state:
    st.session_state.sandbox_code = ""

if "execution_result" not in st.session_state:
    st.session_state.execution_result = None

if "last_intent" not in st.session_state:
    st.session_state.last_intent = None


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_python_code(text):
    """Extract Python code from a Markdown code block."""
    import re

    pattern = r"```(?:python|py)?\s*\n(.*?)```"
    matches = re.findall(pattern, text, flags=re.DOTALL | re.IGNORECASE)

    return matches[0].strip() if matches else ""


def reset_conversation():
    st.session_state.messages = []
    st.session_state.pending_knowledge = None
    st.session_state.last_intent = None


def show_knowledge_form():
    """Show the knowledge form only when retrieval is insufficient."""

    pending = st.session_state.pending_knowledge

    if not pending:
        return

    st.markdown("---")
    st.markdown("### 📚 Help improve the knowledge base")
    st.info(
        "The available programming knowledge was not sufficiently relevant "
        "to answer your request. You can provide a reference solution or "
        "relevant information to improve future answers."
    )

    with st.form("knowledge_feedback_form", clear_on_submit=True):
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Python file handling",
        )

        knowledge = st.text_area(
            "Your solution or reference",
            placeholder="Enter a correct explanation, example, or solution...",
            height=180,
        )

        submitted = st.form_submit_button(
            "Save to Knowledge Base",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not topic.strip() or not knowledge.strip():
                st.warning("Please enter both a topic and reference content.")

            else:
                try:
                    result = save_user_knowledge(
                        topic=topic.strip(),
                        content=knowledge.strip(),
                    )

                    if isinstance(result, dict):
                        if result.get("success", False):
                            st.success(
                                result.get(
                                    "message",
                                    "Knowledge saved successfully!",
                                )
                            )
                            st.session_state.pending_knowledge = None
                        else:
                            st.error(
                                result.get("message", "Failed to save knowledge.")
                            )

                    elif result is False:
                        st.error("Failed to save knowledge.")

                    else:
                        # Handles functions that save successfully but return None.
                        st.success("Knowledge submitted successfully!")
                        st.session_state.pending_knowledge = None

                except Exception as exc:
                    st.error(f"Could not save knowledge: {exc}")

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 💻 CodePilot AI")
    st.caption("Your intelligent coding workspace")

    st.markdown("---")

    page = st.radio(
        "WORKSPACE",
        ["AI Chat", "Python Sandbox"],
        label_visibility="visible",
    )

    st.markdown("---")

    st.markdown("#### ⚙️ Preferences")

    if st.button(
        "＋ New Conversation",
        use_container_width=True,
    ):
        reset_conversation()
        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div class="feature-description">
            <b>AI-powered development</b><br><br>
            Ask questions, understand code, generate solutions,
            and test Python in one workspace.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("CodePilot AI · Intelligent Coding Assistant")


# =========================================================
# AI CHAT PAGE
# =========================================================

if page == "AI Chat":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">INTELLIGENT DEVELOPMENT WORKSPACE</div>
            <h1>Build smarter with AI.</h1>
            <p>
                Explain unfamiliar code, generate programming solutions,
                and expand the knowledge base when additional references
                are needed.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Code Explanation</div>
                <div class="feature-description">
                    Understand code, logic, functions, and programming concepts.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Code Generation</div>
                <div class="feature-description">
                    Generate solutions using relevant retrieved programming knowledge.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧪</div>
                <div class="feature-title">Python Sandbox</div>
                <div class="feature-description">
                    Move Python code into a separate workspace to test it.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Coding Assistant</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">'
        'Describe what you want to understand or build.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("code"):
                if st.button(
                    "↗ Open code in Sandbox",
                    key=f"sandbox_{message['id']}",
                ):
                    st.session_state.sandbox_code = message["code"]
                    st.session_state["navigate_to_sandbox"] = True
                    st.rerun()

    # Process new requests
    prompt = st.chat_input(
        "Ask about code or describe a programming task..."
    )

    if prompt:
        st.session_state.messages.append(
            {
                "id": len(st.session_state.messages),
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request..."):
                try:
                    intent = intent_classification(prompt)
                    st.session_state.last_intent = intent

                    intent_text = str(intent).strip().upper()

                    if "EXPLAIN" in intent_text:
                        answer = explain_code(prompt)

                    else:
                        documents = retrieve_documents(prompt)

                        if not documents:
                            relevance_result = {
                                "relevant": False,
                                "reason": (
                                    "No relevant programming documents "
                                    "were retrieved."
                                ),
                            }
                        else:
                            formatted_documents = format_documents(documents)
                            relevance_result = evaluate_relevance(
                                prompt,
                                formatted_documents,
                            )

                        if isinstance(relevance_result, dict):
                            is_relevant = relevance_result.get(
                                "relevant",
                                False,
                            )
                            reason = relevance_result.get(
                                "reason",
                                "The retrieved context was insufficient.",
                            )
                        else:
                            is_relevant = bool(relevance_result)
                            reason = (
                                "The retrieved context was insufficient."
                            )

                        if not is_relevant:
                            answer = (
                                "I couldn't find sufficiently relevant "
                                "programming knowledge to generate a reliable "
                                "solution. You can provide a reference below."
                            )

                            st.session_state.pending_knowledge = {
                                "query": prompt,
                                "reason": reason,
                            }

                        else:
                            answer = generate_code(
                                prompt,
                                formatted_documents,
                            )

                    if not isinstance(answer, str):
                        answer = str(answer)

                    st.markdown(answer)

                    code = extract_python_code(answer)

                    if code:
                        st.session_state.sandbox_code = code
                        st.caption(
                            "Python code detected. It is ready in the "
                            "Python Sandbox when you want to test it."
                        )

                    st.session_state.messages.append(
                        {
                            "id": len(st.session_state.messages),
                            "role": "assistant",
                            "content": answer,
                            "code": code,
                        }
                    )

                except Exception as exc:
                    error_message = f"Something went wrong: {exc}"
                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "id": len(st.session_state.messages),
                            "role": "assistant",
                            "content": error_message,
                        }
                    )

    # Conditional knowledge form
    show_knowledge_form()


# =========================================================
# PYTHON SANDBOX PAGE
# =========================================================

elif page == "Python Sandbox":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">CODE EXECUTION WORKSPACE</div>
            <h1>Python Sandbox.</h1>
            <p>
                Test Python snippets in your existing isolated execution
                environment. Review the output and errors below.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🐍 Python Editor")

    code = st.text_area(
        "Python source code",
        value=st.session_state.sandbox_code,
        height=350,
        placeholder=(
            "print('Hello, CodePilot!')\n\n"
            "# Write your Python code here"
        ),
        label_visibility="collapsed",
        key="python_editor",
    )

    run_col, clear_col = st.columns([2, 1])

    with run_col:
        run_code = st.button(
            "▶ Run Python Code",
            type="primary",
            use_container_width=True,
        )

    with clear_col:
        clear_code = st.button(
            "Clear Editor",
            use_container_width=True,
        )

    if clear_code:
        st.session_state.sandbox_code = ""
        st.session_state.execution_result = None
        st.rerun()

    if run_code:
        if not code.strip():
            st.warning("Enter some Python code before running it.")
        else:
            with st.spinner("Executing Python code..."):
                output = io.StringIO()
                errors = io.StringIO()

                try:
                    with contextlib.redirect_stdout(output), \
                        contextlib.redirect_stderr(errors):
                        exec(
                            compile(code, "<user_code>", "exec"),
                            {},
                        )

                    st.session_state.execution_result = {
                        "success": True,
                        "stdout": output.getvalue(),
                        "stderr": errors.getvalue(),
                        "error": None,
                    }

                except Exception:
                    import traceback

                    st.session_state.execution_result = {
                        "success": False,
                        "stdout": output.getvalue(),
                        "stderr": errors.getvalue(),
                        "error": traceback.format_exc(),
                    }

    result = st.session_state.execution_result

    if result is not None:
        st.markdown("---")
        st.markdown("### 📟 Execution Results")

        if isinstance(result, dict):
            stdout = result.get(
                "stdout",
                result.get("output", ""),
            )
            stderr = result.get("stderr", "")
            error = result.get("error", "")
            exit_code = result.get(
                "exit_code",
                result.get("return_code"),
            )
            timed_out = result.get("timed_out", False)
            success = result.get("success", exit_code == 0)

            if timed_out:
                st.warning("Execution stopped because it timed out.")

            if success and not error and not stderr:
                st.success("Execution completed.")

            if stdout:
                st.markdown("**Standard Output**")
                st.code(str(stdout), language="text")

            if stderr:
                st.markdown("**Standard Error**")
                st.code(str(stderr), language="text")

            if error:
                st.error(str(error))

            if exit_code is not None:
                st.caption(f"Exit code: {exit_code}")

            if not stdout and not stderr and not error and not timed_out:
                st.info("Execution finished without producing output.")

        else:
            st.code(str(result), language="text")
