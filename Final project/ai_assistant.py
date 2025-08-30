# AI Assistant (CLI) — Major Project
# Run with: python ai_assistant.py
import wikipedia
import textwrap
from datetime import datetime

# ---------- tiny helpers ----------

def line():
    print("-" * 60)

def wrap(txt):
    return "\n".join(textwrap.wrap(txt, width=70))

def get_yes_no(prompt="Was this helpful? (yes/no): "):
    ans = input(prompt).strip().lower()
    return "yes" if ans.startswith("y") else "no"

def log_feedback(task_name, prompt_used, response_text, helpful):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now()}] TASK={task_name} | HELPFUL={helpful}\n"
            f"PROMPT: {prompt_used}\n"
            f"RESPONSE: {response_text}\n"
            f"{'-'*60}\n"
        )

# ---------- PROMPT TEMPLATES (3 per function) ----------

PROMPTS = {
    "qa": {
        "1": "Answer briefly: {question}",
        "2": "Answer clearly in 2-3 sentences: {question}",
        "3": "You are a knowledgeable tutor. Provide a concise, factual answer with 1 example if relevant: {question}"
    },
    "summarize": {
        "1": "Summarize in one line: {text}",
        "2": "Summarize in 3 bullet points: {text}",
        "3": "Summarize clearly with: (a) main idea, (b) 2 key points, (c) one takeaway: {text}"
    },
    "creative": {
        "1": "Write a 5-6 sentence story about: {topic}",
        "2": "Write a short story (120-150 words) with a warm tone about: {topic}",
        "3": "Write a vivid, engaging story (~180 words) with a clear beginning, middle, and end. Theme: {topic}"
    },
    "advice": {
        "1": "Give 3 quick tips about: {topic}",
        "2": "Give practical advice in 4-5 bullet points about: {topic}",
        "3": "Give a short step-by-step plan (5-6 steps) for: {topic}"
    }
}

# ---------- SIMPLE OFFLINE ENGINES (no API needed) ----------



def engine_qa(prompt_text, user_question):
    try:
        # Use Wikipedia to fetch summary (first 2 sentences)
        summary = wikipedia.summary(user_question, sentences=2, auto_suggest=True, redirect=True)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your question is too broad. Did you mean: {e.options[:5]}?"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find an answer on Wikipedia."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def engine_summarize(prompt_text, long_text):
    # naive summary: pick 1–3 key-ish sentences by length/position
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
    # template-based tiny storyteller
    return wrap(
        f"{topic.title()} began as a small idea, then grew into an unexpected journey. "
        f"At first, everything seemed ordinary, but a tiny twist changed the path. "
        f"With patience and courage, the hero learned what mattered most. "
        f"In the quiet moments, new strength appeared. "
        f"By the end, {topic.lower()} felt less like a challenge and more like a lesson—and a new beginning."
    )

def engine_advice(prompt_text, topic):
    if "step-by-step" in prompt_text.lower():
        return wrap(
            f"1) Define the goal for {topic}.\n"
            f"2) Gather simple tools/resources.\n"
            f"3) Start small and track progress daily.\n"
            f"4) Ask for feedback and adjust.\n"
            f"5) Remove blockers and keep it simple.\n"
            f"6) Review weekly and celebrate tiny wins."
        )
    elif "bullet points" in prompt_text.lower():
        return wrap(
            f"- Keep it simple and specific.\n- Set a small daily target.\n- Use checklists.\n- Review weekly and tweak."
        )
    else:
        return wrap("• Start small • Stay consistent • Track progress")

# ---------- MAIN MENU & FLOW ----------

def choose_variant():
    print("Choose prompt style:")
    print("1) Short  2) Medium  3) Detailed")
    v = input("Your choice (1/2/3): ").strip()
    return v if v in {"1", "2", "3"} else "2"

def do_qa():
    line()
    question = input("Type your question: ")
    variant = choose_variant()
    prompt_used = PROMPTS["qa"][variant].format(question=question)
    response = engine_qa(prompt_used, question)
    print("\nAI says:\n" + wrap(response))
    helpful = get_yes_no()
    log_feedback("Q&A", prompt_used, response, helpful)

def do_summarize():
    line()
    print("Paste the text to summarize (finish with an empty line):")
    lines = []
    while True:
        l = input()
        if l.strip() == "":
            break
        lines.append(l)
    text = "\n".join(lines)
    variant = choose_variant()
    prompt_used = PROMPTS["summarize"][variant].format(text=text)
    response = engine_summarize(prompt_used, text)
    print("\nSummary:\n" + response)
    helpful = get_yes_no()
    log_feedback("Summarize", prompt_used, response, helpful)

def do_creative():
    line()
    topic = input("Story topic (e.g., a lost key in a new city): ")
    variant = choose_variant()
    prompt_used = PROMPTS["creative"][variant].format(topic=topic)
    response = engine_creative(prompt_used, topic)
    print("\nStory:\n" + response)
    helpful = get_yes_no()
    log_feedback("Creative", prompt_used, response, helpful)

def do_advice():
    line()
    topic = input("Advice about what? ")
    variant = choose_variant()
    prompt_used = PROMPTS["advice"][variant].format(topic=topic)
    response = engine_advice(prompt_used, topic)
    print("\nAdvice:\n" + response)
    helpful = get_yes_no()
    log_feedback("Advice", prompt_used, response, helpful)
import wikipedia
import tkinter as tk
from tkinter import scrolledtext

# ------------------------
# Core Functions
# ------------------------
def answer_question():
    question = input_text.get("1.0", tk.END).strip()
    try:
        response = wikipedia.summary(question, sentences=get_length())
    except wikipedia.exceptions.DisambiguationError as e:
        response = f"Too broad. Did you mean: {e.options[:5]}?"
    except wikipedia.exceptions.PageError:
        response = "Sorry, I couldn't find an answer."
    except Exception as e:
        response = f"Error: {str(e)}"
    show_output(response)

def summarize_text():
    text = input_text.get("1.0", tk.END).strip()
    words = text.split()
    length = get_length()
    if len(words) > length * 10:
        summary = "Summary: " + " ".join(words[:length*10]) + "..."
    else:
        summary = "Summary: " + text
    show_output(summary)

def creative_writing():
    topic = input_text.get("1.0", tk.END).strip()
    length = get_length()
    story = f"Once upon a time, {topic}... This is a {['short','medium','long'][length-1]} creative story."
    show_output(story)

def give_advice():
    topic = input_text.get("1.0", tk.END).strip()
    length = get_length()
    tips = {
        1: "Keep it simple, stay consistent.",
        2: "Stay consistent, keep learning, and stay positive.",
        3: "Stay consistent, keep learning, network with others, and embrace challenges."
    }
    advice = f"Tips for {topic}: {tips[length]}"
    show_output(advice)

# ------------------------
# Helpers
# ------------------------
def show_output(response):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)

def get_length():
    return {"Short": 1, "Medium": 2, "Long": 3}[length_var.get()]

# ------------------------
# Tkinter GUI with Cool Theme
# ------------------------
window = tk.Tk()
window.title("✨ AI Assistant ✨")
window.geometry("750x550")
window.config(bg="#1e1e2e")  # Dark background (like VS Code)

# Title
title_label = tk.Label(window, text="🤖 AI Assistant", font=("Helvetica", 22, "bold"), bg="#1e1e2e", fg="#f6f8f8")
title_label.pack(pady=15)

# Input Box
tk.Label(window, text="Enter your text or question:", bg="#d1d1e7", fg="#1e1e2e", font=("Arial", 12)).pack(pady=5)
input_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=6, bg="#2d2d44", fg="white", insertbackground="white")
input_text.pack(pady=5)

# Response Length Options
tk.Label(window, text="Select Response Length:", bg="#1e1e2e", fg="white", font=("Arial", 12)).pack(pady=5)
length_var = tk.StringVar(value="Medium")
length_menu = tk.OptionMenu(window, length_var, "Short", "Medium", "Long")
length_menu.config(bg="#444466", fg="white", font=("Arial", 11), relief="flat")
length_menu.pack(pady=5)

# Buttons Frame
button_frame = tk.Frame(window, bg="#1e1e2e")
button_frame.pack(pady=15)

btn_style = {"width": 18, "height": 2, "font": ("Arial", 10, "bold"), "relief": "flat"}

tk.Button(button_frame, text="Answer Question", command=answer_question, bg="#00cc66", fg="white", **btn_style).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_frame, text="Summarize Text", command=summarize_text, bg="#0099cc", fg="white", **btn_style).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_frame, text="Creative Writing", command=creative_writing, bg="#ff9933", fg="black", **btn_style).grid(row=0, column=2, padx=10, pady=5)
tk.Button(button_frame, text="Give Advice", command=give_advice, bg="#cc3366", fg="white", **btn_style).grid(row=0, column=3, padx=10, pady=5)

# Output Box
tk.Label(window, text="Output:", bg="#1e1e2e", fg="white", font=("Arial", 12)).pack(pady=5)
output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=12, bg="#2d2d44", fg="white", insertbackground="white")
output_text.pack(pady=5)

# Run
window.mainloop()

def main():
    print("Welcome to your AI Assistant! ✨")
    while True:
        line()
        print("Pick a function:")
        print("1) Answer Questions")
        print("2) Summarize Text")
        print("3) Creative Writing")
        print("4) Advice/Tips")
        print("5) Exit")
        choice = input("Your choice: ").strip()
        if choice == "1":
            do_qa()
        elif choice == "2":
            do_summarize()
        elif choice == "3":
            do_creative()
        elif choice == "4":
            do_advice()
        elif choice == "5":
            print("Bye! 👋")
            break
        else:
            print("Please choose 1-5.")

if __name__ == "__main__":
    main()
