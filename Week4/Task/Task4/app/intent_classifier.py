from llm_setup import llm

def intent_classification(message):
    system_message= f"""

role: You are an intent classifier for an AI coding assistant.
Classify the user's request into exactly one category:

explain:
- Explain existing code.
- Describe what a function or code snippet does.
- Debug existing code or explain a programming error.
- Explain code line by line.

generate:
- Write new code.
- Implement a function, algorithm, or application.
- Create a model, API, or software feature.
- Modify existing code by implementing a requested feature.

rules:
dont return any unrelated message just "generate" if the classification is generate message and "explain" 
if the message is explain some code 

Return exactly one label: explain or generate.
Do not include explanations, punctuation, or Markdown.

User request:
{message}
"""

    result= llm.invoke(system_message)

    cls_label = result.content
    cls_label = cls_label.strip().lower()

    return cls_label