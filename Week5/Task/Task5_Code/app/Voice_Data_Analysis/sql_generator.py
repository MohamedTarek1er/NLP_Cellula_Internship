import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from schema import get_dataset_schema

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model=os.getenv("OPENROUTER_MODEL"),
    temperature=0
)

def generate_sql(question: str):
    question = question.strip()

    if not question:
        return {"error": "Please provide a question."}

    schema = get_dataset_schema()

    if "error" in schema:
        return schema

    schema_text = "\n".join(
        f"- {column['column_name']} "
        f"(type: {column['data_type']})"
        for column in schema["columns"]
    )

    system_prompt = """
    You are an expert SQLite SQL query generator.

    Your task is to convert the user's question into
    a valid SQLite SELECT query.

    Rules:
    1. Use only the table named dataset.
    2. Use only columns present in the supplied schema.
    3. Generate SQLite-compatible SQL.
    4. Return SQL only, without Markdown or explanations.
    5. Do not generate INSERT, UPDATE, DELETE, DROP,
       ALTER, CREATE, or other modifying statements.
    6. Do not invent column names.
    7. Understand questions asked in Arabic or English.
    8. Use LIMIT when the user asks for a limited number
       of results.
    """

    user_prompt = f"""
    Dataset table: dataset

    Available columns:
    {schema_text}

    User question:
    {question}

    Generate the SQL query:
    """

    response = llm.invoke([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    sql_query = response.content.strip()

    # Remove Markdown fences if the model returns them
    if sql_query.startswith("```"):
        lines = sql_query.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        sql_query = "\n".join(lines).strip()

        if sql_query.lower().startswith("sql"):
            sql_query = sql_query[3:].strip()

    return {
        "question": question,
        "sql_query": sql_query,
        "table_name": "dataset"
    }
