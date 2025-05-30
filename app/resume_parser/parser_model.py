# app/resume_parser/parser_model.py
from app.resume_parser.ner_predict import predict_entities
import pdfplumber

def parse_resume_pdf(pdf_path: str) -> dict:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"

    info = predict_entities(text)
    return {
        "name": info.get("name", ""),
        "age": info.get("age", ""),
        "degree": info.get("education", ""),
        "job_target": info.get("match_position", ""),
        "skills": None,
        "phone": None,
        "email": None,
        "file_path": pdf_path,
        "parse_json": info,
        "status": "pending"
    }
