
import re


# Technical skills grouped by category
SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "C++", "JavaScript", "SQL"
    ],
    "Backend Development": [
        "FastAPI", "Spring Boot", "Node.js",
        "Express.js", "REST APIs"
    ],
    "AI & Machine Learning": [
        "Machine Learning", "LLMs", "RAG",
        "FAISS", "Gemini API", "Sentence Transformers",
        "Embeddings"
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB",
        "H2"
    ],
    "Data Processing": [
        "Pandas", "NumPy", "ETL"
    ],
    "Tools & Testing": [
        "Git", "GitHub", "Postman", "Jest",
        "Supertest", "Pytest", "Docker"
    ]
}


def extract_skills(resume_text):
    """
    Extract technical skills from resume text.

    Args:
        resume_text: Text extracted from a candidate's resume.

    Returns:
        Dictionary containing detected skills by category.
    """

    if not isinstance(resume_text, str) or not resume_text.strip():
        return {}

    extracted_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        matched_skills = []

        for skill in skills:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

            if re.search(pattern, resume_text, re.IGNORECASE):
                matched_skills.append(skill)

        if matched_skills:
            extracted_skills[category] = matched_skills

    return extracted_skills
