
import re
import json
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from app.embeddings import generate_embeddings


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
        "Supertest", "Pytest", "Docker", "AWS", "Linux"
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


def load_jobs():
    """
    Load sample job descriptions from the JSON file.
    """

    project_root = Path(__file__).resolve().parent.parent
    jobs_file = project_root / "data" / "sample_jobs.json"

    with open(jobs_file, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    return jobs


def match_jobs(resume_text, top_n=5):
    """
    Find and rank jobs based on semantic similarity.
    """

    if not resume_text.strip():
        return []

    jobs = load_jobs()

    # Extract job descriptions
    job_descriptions = [
        job["description"] for job in jobs
    ]

    # Generate embeddings
    resume_embedding = generate_embeddings([resume_text])
    job_embeddings = generate_embeddings(job_descriptions)

    # Calculate similarity scores
    similarity_scores = cosine_similarity(
        resume_embedding,
        job_embeddings
    )[0]

    # Attach scores to jobs
    recommendations = []

    for job, score in zip(jobs, similarity_scores):
        recommendations.append({
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "description": job["description"],
            "match_score": round(float(score) * 100, 2)
        })

    # Sort jobs by highest similarity
    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    return recommendations[:top_n]


def analyze_skill_gaps(resume_text, job_description):
    """
    Compare candidate skills with job requirements.
    """

    candidate_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    candidate_list = {
        skill.lower()
        for skills in candidate_skills.values()
        for skill in skills
    }

    required_list = {
        skill.lower(): skill
        for skills in required_skills.values()
        for skill in skills
    }

    matching_skills = [
        skill for skill in required_list.values()
        if skill.lower() in candidate_list
    ]

    missing_skills = [
        skill for skill in required_list.values()
        if skill.lower() not in candidate_list
    ]

    total_required = len(required_list)

    coverage = (
        len(matching_skills) / total_required * 100
        if total_required > 0 else 0.0
    )

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_coverage": round(coverage, 2)
    }


