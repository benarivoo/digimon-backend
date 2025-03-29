from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
from dotenv import load_dotenv
import os

# === Load env vars ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not set in .env")

client = OpenAI(api_key=api_key)

# === Flask Setup ===
app = Flask(__name__)
CORS(app)

# === Chat Endpoint ===
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")
    form = data.get("form", "Agumon")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a helpful Digimon companion named {form}."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run the app ===
if __name__ == "__main__":
    app.run(debug=True)
