from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import json
from openai import OpenAI
load_dotenv()

app = Flask(__name__)
CORS(app)
CORS(app, origins="*", supports_credentials=True, methods=["GET", "POST", "OPTIONS"])
# Read OpenRouter API key

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
@app.route('/api/prioritize', methods=['POST'])
def prioritize():
    data = request.get_json()
    features = data.get('features', [])

    prompt = f"""
You are an experienced product manager.

Given the following list of feature requests, estimate for each:
- Effort on a scale of 1 (very low) to 5 (very high)
- Impact on a scale of 1 (very low) to 5 (very high)

Output strictly in the following JSON format:
[
  {{ "feature": "Feature Name", "effort": number, "impact": number }},
  ...
]

Features:
{features}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        print("🔵 Raw AI response:", response)

        reply = response.choices[0].message.content
        parsed_reply = json.loads(reply)
        return jsonify(parsed_reply)

    except Exception as e:
        print("🔴 Exception:", str(e))
        return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500

#@app.route('/api/prioritize', methods=['POST'])
#@app.route('/api/prioritize', methods=['POST'])
# def prioritize():
#     data = request.get_json()
#     features = data.get('features', [])

#     prompt = f"""
# You are an experienced product manager.

# Given the following list of feature requests, estimate for each:
# - Effort on a scale of 1 (very low) to 5 (very high)
# - Impact on a scale of 1 (very low) to 5 (very high)

# Output strictly in the following JSON format:
# [
#   {{ "feature": "Feature Name", "effort": number, "impact": number }},
#   ...
# ]

# Features:
# {features}
# """

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # or your current OpenRouter model
#         messages=[
#             {"role": "system", "content": "You are a helpful product management assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     reply = response.choices[0].message.content

#     # Parse the AI's JSON output
#     try:
#         parsed_reply = json.loads(reply)
#         return jsonify(parsed_reply)
#     except Exception as e:
#         return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500

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
