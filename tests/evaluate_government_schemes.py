import json
from pathlib import Path

from ai.rag.rag_pipeline import ask_question
from ai.rag.config import QUESTIONS_PATH


def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_questions(limit=5):
    questions = load_questions()

    print(f"Total questions available: {len(questions)}")
    print(f"Testing first {limit} questions...\n")

    for item in questions[:limit]:

        question_id = item["id"]
        question = item["question"]
        expected_answer = item["answer"]

        print("=" * 70)
        print(f"Question ID: {question_id}")
        print(f"Question: {question}")

        result = ask_question(question)

        print("\nExpected Answer:")
        print(expected_answer)

        print("\nRAG Answer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print(
                f"- Page {source['page']}: "
                f"{source['source']}"
            )

        print()


if __name__ == "__main__":
    evaluate_questions(limit=5)