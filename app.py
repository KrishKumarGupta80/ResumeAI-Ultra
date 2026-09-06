from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)

SKILLS = {
    "python","java","c","c++","html","css","javascript",
    "flask","django","react","sql","mysql","mongodb",
    "machine learning","deep learning","ai","nlp",
    "git","github","docker","linux"
}

def extract_text(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            if p.extract_text():
                text += p.extract_text().lower()

    return text

def get_skills(text):
    return {s for s in SKILLS if s in text}

def calculate_score(resume, job):
    if not job:
        return 0

    match = resume & job
    return round((len(match) / len(job)) * 100, 2)

def insight(score):
    if score >= 80:
        return "Excellent match. Strong candidate for this role."

    elif score >= 50:
        return "Moderate match. Improve missing skills to increase chances."

    return "Low match. Resume needs optimization for this role."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]
    job = request.form["jobdesc"].lower()

    resume_text = extract_text(file)

    resume_skills = get_skills(resume_text)
    job_skills = get_skills(job)

    score = calculate_score(
        resume_skills,
        job_skills
    )

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    matched_count = len(matched)
    missing_count = len(missing)

    # Professional Analytics

    if score >= 80:
        verdict = "Strong Candidate"
        readiness = "Interview Ready"
        rank = "Top 10%"

    elif score >= 50:
        verdict = "Potential Candidate"
        readiness = "Almost Ready"
        rank = "Top 25%"

    else:
        verdict = "Needs Improvement"
        readiness = "Not Ready"
        rank = "Below Average"

    return render_template(
        "result.html",

        score=score,

        matched=matched,
        missing=missing,

        matched_count=matched_count,
        missing_count=missing_count,

        insight=insight(score),

        verdict=verdict,
        readiness=readiness,
        rank=rank
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,
            debug=True)