# AI Resume Screening System

## About the Project
AI Resume Screening System is a web application built using Python and Flask to compare a candidate's resume with a job description. It calculates text similarity and identifies matched and missing skills to support the initial resume screening process.

## Features
- Upload resumes in PDF format
- Enter a job description
- Calculate text similarity using TF-IDF and Cosine Similarity
- Identify matched and missing skills
- Display extracted resume text
- Download a screening report
- Responsive and user-friendly interface

## Technologies Used
- Python
- Flask
- HTML5
- CSS3
- Scikit-learn
- PyPDF

## How It Works
1. Upload a PDF resume.
2. Enter the job description.
3. The application extracts readable text from the PDF.
4. TF-IDF and Cosine Similarity calculate the text similarity score.
5. The system identifies matched and missing skills using keyword matching.
6. View the results and download the screening report.

## Installation and Setup

1. Clone the repository:

   `git clone https://github.com/vaishnavijoshi215/AI-Resume-Screening-System.git`

2. Open the project folder:

   `cd AI-Resume-Screening-System`

3. Create and activate a virtual environment:

   `python -m venv venv`

   Windows PowerShell:

   `.\venv\Scripts\Activate.ps1`

4. Install the required packages:

   `pip install Flask pypdf scikit-learn`

5. Run the application:

   `python app.py`

6. Open `http://127.0.0.1:5000` in your browser.

## Important Note
The similarity score measures text similarity; it is not a hiring probability or a final hiring decision. Skill identification is based on a predefined keyword list.

## Future Improvements
- Expand the skill database
- Improve resume parsing
- Add more detailed screening analytics
- Support additional resume formats
