# chat_test.py

from graphrag_service import answer_question

print("ACIS GraphRAG Assistant")
print("Type 'exit' to quit\n")

while True:
    query = input("You: ")

    if query.lower() in ["exit", "quit"]:
        break

    try:
        result = answer_question(query)

        print("\nAssistant:")
        print(result["answer"])

        print("\nSources:")
        for s in result.get("sources", []):
            print(f"- {s.get('entity_type')} : {s.get('entity_name')}")

        print("\n" + "="*80 + "\n")

    except Exception as e:
        print("Error:", e)