import pickle
from flask import Flask, request, jsonify, render_template

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path="/static",
    template_folder="frontend",
)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


store = load_pickle("store.pkl")
persona = load_pickle("persona.pkl")


def format_persona_answer(query):
    lower = query.lower()
    if any(keyword in lower for keyword in ["habit", "habits", "sleep", "eat", "food", "drink", "routine", "daily"]):
        habits = persona.get("habits", [])
        if habits:
            return "I found these habits in the conversation: " + ", ".join(habits)
        return "I didn't find any clear habits in the conversation."

    if any(keyword in lower for keyword in ["personality", "traits", "trait", "tone", "style", "emoji", "funny", "friendly", "polite"]):
        traits = persona.get("personality_traits", [])
        style = persona.get("communication_style", {})
        parts = []
        if traits:
            parts.append("Personality traits: " + ", ".join(traits))
        if style:
            style_info = [f"{key.replace('_', ' ')}={value}" for key, value in style.items()]
            parts.append("Communication style: " + ", ".join(style_info))
        if parts:
            return "\n".join(parts)
        return "I couldn't identify any strong personality signals from the conversation."

    if any(keyword in lower for keyword in ["who are you", "what are you", "about you", "you are", "yourself"]):
        return persona.get("summary", "I am a chatbot built from the conversation data.")

    return persona.get("summary", "I am a chatbot built from the conversation data.")


def format_search_answer(results):
    if not results:
        return "I couldn't find anything directly matching your question. Try another phrasing."
    if len(results) == 1:
        return f"I found one relevant passage:\n- {results[0]}"
    return "I found these relevant passages:\n" + "\n".join(f"- {item}" for item in results)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Please enter a question."}), 400

    persona_keywords = [
        "habit", "habits", "personality", "traits", "style", "tone", "emoji", "funny",
        "about you", "who are you", "what are you", "yourself", "you are",
    ]
    if any(keyword in query.lower() for keyword in persona_keywords):
        answer = format_persona_answer(query)
        return jsonify({"answer": answer, "source": "persona"})

    results = store.search(query)
    answer = format_search_answer(results)
    return jsonify({"answer": answer, "source": "search", "results": results})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

