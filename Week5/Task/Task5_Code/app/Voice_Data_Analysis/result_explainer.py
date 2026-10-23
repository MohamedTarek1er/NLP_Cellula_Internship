import json
from sql_generator import llm

def explain_results(question: str, query_result: dict):
    if "error" in query_result:
        return {
            "error": query_result["error"]
        }

    result_summary = {
        "columns": query_result.get("columns", []),
        "rows": query_result.get("rows", [])[:50],
        "row_count": query_result.get("row_count", 0),
        "truncated": query_result.get("truncated", False)
    }

    system_prompt = """
    You are a data analysis assistant.

    Explain SQL query results clearly and accurately.

    Rules:
    1. Answer in the same language as the user's question.
       Support both Arabic and English.
    2. Use only the supplied question and query results.
    3. Do not invent values, statistics, or conclusions.
    4. Explain important numbers and patterns when possible.
    5. If the results are empty, clearly say that no rows
       matched the query.
    6. If only some rows are shown, mention that the
       displayed results may be incomplete.
    7. Keep the explanation clear and concise.
    """

    user_prompt = f"""
    User question:
    {question}

    SQL query results:
    {json.dumps(result_summary, ensure_ascii=False, default=str)}

    Explain these results to the user.
    """

    response = llm.invoke([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    return {
        "question": question,
        "explanation": response.content.strip(),
        "row_count": result_summary["row_count"],
        "results_preview": result_summary["rows"]
    }
