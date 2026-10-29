
from flask import Flask, render_template, request, Response
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import os
import re
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS = [
    "Python", "Java", "C++", "C", "SQL", "HTML", "CSS",
    "JavaScript", "Flask", "Django", "Machine Learning",
    "Deep Learning", "Data Science", "Data Analysis",
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
    "PyTorch", "Excel", "Power BI", "Tableau", "Git",
    "GitHub", "Communication", "Problem Solving",
    "Data Structures", "DBMS", "Artificial Intelligence"
]


def find_skills(text):
    found = []
    text = text.lower()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return found


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen_resume():
    if "resume" not in request.files:
        return "Please upload a PDF resume."

    file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return "Please select a PDF resume."

    if not job_description:
        return "Please enter a job description."

    filename = secure_filename(file.filename)

    if not filename:
        return "Invalid filename."

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        reader = PdfReader(file_path)
        resume_text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
    except Exception:
        return "Unable to read this PDF. Please try another file."

    if not resume_text.strip():
        return "No readable text found in this PDF."

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        score = cosine_similarity(
            vectors[0:1], vectors[1:2]
        )[0][0]
        match_percentage = round(score * 100, 2)
    except ValueError:
        match_percentage = 0.0

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    matched_skills = [
        skill for skill in job_skills if skill in resume_skills
    ]
    missing_skills = [
        skill for skill in job_skills if skill not in resume_skills
    ]

    return render_template(
        "result.html",
        filename=filename,
        resume_text=resume_text,
        match_percentage=match_percentage,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


@app.route("/download-report", methods=["POST"])
def download_report():
    filename = request.form.get("filename", "Resume")
    match_percentage = request.form.get("match_percentage", "0")
    matched_skills = request.form.getlist("matched_skills")
    missing_skills = request.form.getlist("missing_skills")

    report = f"""AI RESUME SCREENING REPORT

Resume: {filename}
Text Similarity Score: {match_percentage}%

Matched Skills:
{chr(10).join(matched_skills) if matched_skills else "None found"}

Missing Skills:
{chr(10).join(missing_skills) if missing_skills else "None found"}

Note:
This report uses text similarity and basic keyword matching.
It is not a hiring decision or a guarantee of suitability.
"""

    response = Response(
        report,
        mimetype="text/plain; charset=utf-8"
    )
    response.headers["Content-Disposition"] = (
        'attachment; filename="screening_report.txt"'
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
