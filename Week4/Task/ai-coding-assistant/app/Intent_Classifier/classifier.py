from enum import Enum
from pydantic import BaseModel, ValidationError
from app.llm import llm

class Intent(str, Enum):
    EXPLAIN = "EXPLAIN"
    GENERATE = "GENERATE"

class IntentResult(BaseModel):
    intent: Intent

def classify_intent(query: str) -> Intent:

    prompt = f"""
You are an intent classifier for an AI coding assistant.

Classify the user's request into exactly one category:

EXPLAIN:
- Explain existing code.
- Describe what a function or code snippet does.
- Debug existing code or explain a programming error.
- Explain code line by line.

GENERATE:
- Write new code.
- Implement a function, algorithm, or application.
- Create a model, API, or software feature.
- Modify existing code by implementing a requested feature.

If the request contains both existing code and a request to
explain it, choose EXPLAIN.
If the main request is to create or implement code, choose GENERATE.

Return exactly one label: EXPLAIN or GENERATE.
Do not include explanations, punctuation, or Markdown.

User request:
{query}
"""

    response = llm.invoke(prompt)
    raw_output = response.content

    label = raw_output.strip().upper()
    result = IntentResult(intent=label)

    return result.intent
