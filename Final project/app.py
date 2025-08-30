from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)

# ---------------- ENGINES ---------------- #

def engine_qa(prompt_text, user_question):
    try:
        # Use Wikipedia to fetch summary
        summary = wikipedia.summary(user_question, sentences=2, auto_suggest=True, redirect=True)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your question is too broad. Did you mean: {e.options[:5]}?"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find an answer on Wikipedia."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def engine_summarize(prompt_text, long_text):
    sents = [s.strip() for s in long_text.replace("\n", " ").split(".") if s.strip()]
    if "one line" in prompt_text.lower():
        return (sents[0] if sents else "No text provided.") + "."
    elif "3 bullet points" in prompt_text.lower():
        picks = (sents[:3] or ["(no content)"])
        return "- " + "\n- ".join(picks)
    else:
        main = sents[0] if sents else "(no main idea)"
        keys = sents[1:3] if len(sents) > 1 else ["(no key points)"]
        takeaway = sents[-1] if sents else "(no takeaway)"
        return f"(a) Main idea: {main}.\n(b) Key points: " + "; ".join(keys) + f".\n(c) Takeaway: {takeaway}."

def engine_creative(prompt_text, topic):
    return (
        f"{topic.title()} began as a small idea, then grew into an unexpected journey. "
        f"At first, everything seemed ordinary, but a tiny twist changed the path. "
        f"With patience and courage, the hero learned what mattered most. "
        f"In the quiet moments, new strength appeared. "
        f"By the end, {topic.lower()} felt less like a challenge and more like a lesson—and a new beginning."
    )

def engine_advice(prompt_text, topic):
    if "step-by-step" in prompt_text.lower():
        return (
            f"1) Define the goal for {topic}.\n"
            f"2) Gather simple tools/resources.\n"
            f"3) Start small and track progress daily.\n"
            f"4) Ask for feedback and adjust.\n"
            f"5) Remove blockers and keep it simple.\n"
            f"6) Review weekly and celebrate tiny wins."
        )
    elif "bullet points" in prompt_text.lower():
        return (
            f"- Keep it simple and specific.\n"
            f"- Set a small daily target.\n"
            f"- Use checklists.\n"
            f"- Review weekly and tweak."
        )
    else:
        return "• Start small • Stay consistent • Track progress"

# ---------------- PROMPTS ---------------- #

PROMPTS = {
    "Q&A": {
        "Short": "Answer briefly: {question}",
        "Medium": "Answer clearly in 2–3 sentences: {question}",
        "Long": "You are a tutor. Give a concise factual answer with 1 example: {question}",
    },
    "Summarize": {
        "Short": "Summarize in one line: {text}",
        "Medium": "Summarize in 3 bullet points: {text}",
        "Long": "Give (a) main idea, (b) 2 key points, (c) one takeaway: {text}",
    },
    "Creative": {
        "Short": "5–6 sentence story about: {topic}",
        "Medium": "120–150 word story, warm tone, about: {topic}",
        "Long": "~180-word story with clear beginning, middle, end. Theme: {topic}",
    },
    "Advice": {
        "Short": "3 quick tips about: {topic}",
        "Medium": "4–5 practical bullet points about: {topic}",
        "Long": "5–6 step step-by-step plan for: {topic}",
    }
}

# ---------------- FLASK APP ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    feedback_message = ""

    if request.method == "POST":
        text = request.form["text"]
        task = request.form["task"]
        length = request.form["length"]  # "Short", "Medium", or "Long"

        # Get the correct prompt
        prompt_used = PROMPTS[task][length]

        try:
            if task == "Q&A":
                result = engine_qa(prompt_used, text)
            elif task == "Summarize":
                result = engine_summarize(prompt_used, text)
            elif task == "Creative":
                result = engine_creative(prompt_used, text)
            elif task == "Advice":
                result = engine_advice(prompt_used, text)
        except Exception as e:
            result = f"Error: {str(e)}"

        # Save feedback if given
        if "feedback" in request.form and request.form["feedback"].strip():
            feedback = request.form["feedback"]
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"Task: {task}, Length: {length}, Query: {text}, Feedback: {feedback}\n")
            feedback_message = "✅ Feedback saved. Thank you!"

    return render_template("index.html", result=result, feedback_message=feedback_message)

if __name__ == "__main__":
    app.run(debug=True)
