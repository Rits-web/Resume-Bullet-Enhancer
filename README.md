# ResumeAI — Resume Analyzer

A simple Streamlit prototype that compares resume text with a job description without requiring an AI API key.

## Features
- Upload a text-based PDF resume or paste resume text
- Compare resume and job description using TF-IDF cosine similarity
- Detect skills from a small editable dictionary
- Show potential missing keywords and resume section checklist
- Download a plain-text analysis report

## Setup
Requires Python 3.10 or newer.

### Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## How to demonstrate
1. Paste a sample resume into the resume box.
2. Paste a job description into the other box.
3. Click **Analyze Resume**.
4. Show the similarity estimate, skills, checklist, and improvement tips.
5. Download the report.

## Important limitations
This is an explainable, rule-based NLP prototype, not a large language model. The similarity score is not a hiring probability. The skill list is limited and may miss synonyms. Do not invent skills or metrics to improve a resume. Do not use the score to make hiring decisions.
