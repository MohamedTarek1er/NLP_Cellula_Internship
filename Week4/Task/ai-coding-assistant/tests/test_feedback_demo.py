
from app.feedback import save_user_solution
from app.Code_Generation.retrieval import retrieve_documents


def main():
    result = save_user_solution(
        solution=(
            "def factorial(n):\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be non-negative')\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)"
        ),
        topic="recursive_factorial",
        language="python",
        user_id="demo_user",
    )

    print(result["message"])

    documents = retrieve_documents(
        "How can I implement factorial using recursion?",
        top_k=4,
    )

    for document in documents:
        print("\nSource:", document.metadata.get("source"))
        print("Topic:", document.metadata.get("topic"))
        print(document.page_content)


if __name__ == "__main__":
    main()
