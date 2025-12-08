import os
import markdown
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HUGGINGFACE_API_KEY")
)

def is_incomplete(text: str) -> bool:
    text = text.strip()

    if not text.endswith(('.', '!', '?')):
        return True

    last_line = text.split("\n")[-1].lower()
    if last_line.startswith(("##", "###", "1.", "2.", "3.", "4.", "5.", "-", "|")):
        return True

    if text.count("|") % 2 != 0:  # odd number of pipes → broken table
        return True

    if len(text.split()) > 900:  # approaching 1000
        return True

    return False

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Handle JSON request
        if request.is_json:
            data = request.get_json()
            prompt = data.get("prompt", "")
        else:
            # Fallback for standard form submit if needed (though UI uses JSON)
            prompt = request.form.get("prompt", "")

        if not prompt or len(prompt) < 20:
            return jsonify({"error": "Prompt must be at least 20 characters."}), 400

        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b:together",
                messages=[{"role": "user", "content": f"Write a detailed, engaging blog of ~1000 words on: {prompt}"}],
                max_tokens=1500
            )
            blog = completion.choices[0].message.content
            blog = re.sub(r"By .?\n+Published: .?\n+", "", blog)

            if is_incomplete(blog):
                continuation = client.chat.completions.create(
                    model="openai/gpt-oss-120b:together",
                    messages=[
                        {"role": "system", "content": "You are a blog continuation assistant."},
                        {"role": "user", "content": f"Continue this blog without repeating, and finish it properly:\n\n{blog}"}
                    ],
                    max_tokens=500
                )
                blog += "\n" + continuation.choices[0].message.content

            # Return raw markdown for client-side rendering
            return jsonify({"blog": blog})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)