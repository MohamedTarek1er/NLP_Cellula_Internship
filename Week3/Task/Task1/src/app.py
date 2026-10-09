
import streamlit as st

from retrieval import load_vector_store
from rag import answer_question

st.set_page_config(
    page_title="Personal RAG Assistant",
    page_icon="🧠",
)

st.title("🧠 Personal Knowledge Assistant")
st.caption(
    "Ask questions about professional experience, "
    "projects, skills, and certifications."
)

@st.cache_resource
def get_vector_db():
    return load_vector_store()

vector_db = get_vector_db()

question = st.chat_input("Ask a question about the person...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            result = answer_question(question, vector_db)

        st.markdown(result)
