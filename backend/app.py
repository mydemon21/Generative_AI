import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# This is the prompt that will be sent to the Gemini API.
PROMPT_TEMPLATE = """
You are an expert resume-building assistant. A user will provide you with a description of their professional background.
Your task is to parse this description and generate a professional, well-structured resume in JSON format.

The user's description is:
---
{user_description}
---

Please generate a JSON object with the following structure:
{{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "123-456-7890",
  "summary": "A concise and professional summary of the user's background.",
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "dates": "Start Date - End Date",
      "description": "A detailed description of responsibilities and achievements."
    }}
  ],
  "education": [
    {{
      "degree": "Degree and Major",
      "university": "University Name",
      "dates": "Start Date - End Date"
    }}
  ],
  "skills": ["Skill 1", "Skill 2", "Skill 3"]
}}

- If the user does not provide enough information for a field, use your expertise to fill it with plausible information or leave it as a placeholder.
- The tone should be professional and polished.
- Ensure the output is a single, valid JSON object and nothing else.
"""

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    # Configure Gemini API at the time of the request
    try:
        api_key = os.environ["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    except KeyError:
        print("GEMINI_API_KEY not found in environment variables.")
        return jsonify({"error": "API key not configured on the server."}), 500

    data = request.get_json()
    user_description = data.get('description', '')

    if not user_description:
        return jsonify({"error": "Description is required."}), 400

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = PROMPT_TEMPLATE.format(user_description=user_description)
        response = model.generate_content(prompt)

        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")

        resume_json = json.loads(cleaned_response)
        return jsonify(resume_json)

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse the response from the AI model."}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred while communicating with the AI."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
