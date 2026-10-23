from router import route_query
def main():
    print("Intelligent AI Coding Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a programming question.\n")
            continue
            
        result = route_query(query)
        # print(result)

if __name__ == "__main__":
    main()
