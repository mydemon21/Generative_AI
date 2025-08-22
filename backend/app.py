from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# A simple list of tech skills to look for.
# A real AI would have a much more sophisticated understanding.
KNOWN_SKILLS = [
    "Python", "JavaScript", "React", "Node.js", "Flask", "Java", "C++", "C#",
    "Ruby", "Go", "TypeScript", "HTML", "CSS", "SQL", "NoSQL", "MongoDB",
    "PostgreSQL", "Git", "Docker", "Kubernetes", "AWS", "Azure", "GCP"
]

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    data = request.get_json()
    user_description = data.get('description', '')

    # Simulate AI processing by extracting skills and using the description as a summary.

    # Extract skills
    found_skills = []
    for skill in KNOWN_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', user_description, re.IGNORECASE):
            found_skills.append(skill)

    # Create the resume structure
    resume = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "summary": user_description,  # Use the user's text as the summary
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "dates": "2020 - Present",
                "description": "Developed and maintained web applications using modern technologies."
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "university": "State University",
                "dates": "2016 - 2020"
            }
        ],
        "skills": found_skills
    }

    return jsonify(resume)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
