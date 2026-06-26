#!/usr/bin/env python3
"""
ACIS GraphRAG — Interactive Chat Demo

Usage:
    python examples/chat_demo.py

Example queries:
    > What is BODY?
    > Which classes inherit ENTITY?
    > How does api_blend_edges_pos_rad work?
    > What is SPAposition?
"""
import sys
import os

# Add src/ to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.graphrag_service import answer_question


def main():
    print("=" * 60)
    print("        ACIS GraphRAG Code Assistant")
    print("=" * 60)
    print()
    print("Ask questions about the ACIS C++ codebase.")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            result = answer_question(query)

            # Print the beautifully formatted response
            formatted = result.get("formatted_answer")
            if formatted:
                print(f"\n{formatted}\n")
            else:
                print(f"\nAssistant: {result.get('answer', 'No answer')}\n")

            # Print timing
            r_time = result.get("retrieval_time", 0)
            g_time = result.get("generation_time", 0)
            t_time = result.get("total_time", 0)
            print(f"[Retrieval: {r_time*1000:.0f}ms | Generation: {g_time:.2f}s | Total: {t_time:.2f}s]")
            print()

        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
