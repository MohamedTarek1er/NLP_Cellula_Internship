from intent_classifier import intent_classification
from code_explanation import explain_code
from Code_Generation.retrieval import retrieve_documents, format_documents
from Code_Generation.relevance import evaluate_relevance
from Code_Generation.generation import generate_code
from Code_Generation.user_knowledge import save_user_knowledge

def route_query(query):

    intent_result = intent_classification(query)
    print(intent_result)

    if intent_result.lower() == "explain":
        code_explained = explain_code(query)
        print(code_explained)
        return

    elif intent_result.lower() == "generate":

        retrieved_documents = retrieve_documents(query)
        formatted_documents = format_documents(retrieved_documents)

        relevance_result = evaluate_relevance(query, formatted_documents)
        print(relevance_result)

        if relevance_result["relevant"]:
            generated_code = generate_code(query, formatted_documents)
            print(generated_code)
            return

        else:
            print("I couldn't find sufficient relevant knowledge.")
            print("Please provide an explanation, example, or reference solution.")

            user_data = input("Enter your knowledge: ")
            save_user_knowledge(topic=query, content=user_data)
    else:
        print("Invalid intent. Please try again.")
