
from pathlib import Path
import sys

from flask import Flask, jsonify, render_template, request

# Project root: parent of web_demo
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai.rag.rag_pipeline import ask_question

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if len(question) > 1000:
        return jsonify({"error": "Please keep your question under 1000 characters."}), 400

    try:
        result = ask_question(question)
        sources = [
            {
                "file": Path(item["source"]).name,
                "page": item["page"],
            }
            for item in result.get("sources", [])
        ]

        return jsonify({
            "answer": result.get("answer", "No answer was returned."),
            "sources": sources,
        })
    except Exception:
        app.logger.exception("Error while answering question")
        return jsonify({
            "error": "Something went wrong while generating the answer. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
