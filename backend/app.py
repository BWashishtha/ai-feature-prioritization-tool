from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
CORS(app, origins="*", supports_credentials=True, methods=["GET", "POST", "OPTIONS"])
# Read OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/api/prioritize', methods=['POST'])
def prioritize_features():
    data = request.json
    features = data.get('features', [])

    if not features:
        return jsonify({'error': 'No features provided'}), 400

    prompt = generate_prompt(features)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000/",   #we'll connect frontend on 3000
        "X-Title": "AI Feature Prioritization Tool"
    }

    body = {
        "model": "openai/gpt-3.5-turbo",  # You can also try anthropic/claude-3-haiku
        "messages": [
            {"role": "system", "content": "You are a senior Product Manager."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response_data = response.json()
        ai_output = response_data['choices'][0]['message']['content']
        return jsonify({'result': ai_output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_prompt(features):
    feature_list = "\n".join(f"- {f}" for f in features)
    prompt = (
        f"Given the following user feature requests:\n{feature_list}\n\n"
        "Please categorize each feature into:\n"
        "- High Impact / Low Effort\n"
        "- High Impact / High Effort\n"
        "- Low Impact / Low Effort\n"
        "- Low Impact / High Effort\n\n"
        "Summarize each item in 1–2 sentences."
    )
    return prompt

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
