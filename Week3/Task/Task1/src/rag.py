
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from retrieval import load_vector_store, retrieve_documents

load_dotenv()

llm = ChatOpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    model=os.environ["OPENROUTER_MODEL"],
    temperature=0.7,
)

PROMPT = PromptTemplate.from_template("""
You are a personal professional knowledge assistant.
Answer the question using only the retrieved context below.

Rules:
- Do not invent personal facts, skills, dates, or achievements.

Retrieved context:
{context}

Question:
{question}
""")

def answer_question(question, vector_db, k=4):
    documents = retrieve_documents(
        question,
        vector_db,
        k=k,
    )

    if not documents:
        return "I couldn't find enough information in the knowledge base to answer."

    context = "\n\n".join(
        item["content"] for item in documents
    )

    prompt = PROMPT.format(
        context=context,
        question=question,
    )
    
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    vector_db = load_vector_store()
    
    question = input("\nAsk a question: ")

    result = answer_question(question, vector_db)
    print(result)