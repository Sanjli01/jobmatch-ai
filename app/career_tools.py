
from app.job_matcher import match_jobs, analyze_skill_gaps


def get_job_recommendations(resume_text):
    """
    Tool 1: Find the most relevant jobs for a candidate.
    """

    recommendations = match_jobs(resume_text)

    results = []

    for job in recommendations:

        results.append({
            "title": job["title"],
            "company": job["company"],
            "match_score": job["match_score"],
            "description": job["description"]
        })

    return results


def get_skill_gap_report(resume_text, job_title=None):
    """
    Tool 2: Identify matching and missing skills.
    """

    recommendations = match_jobs(resume_text)

    if not recommendations:
        return {"message": "No job recommendations found."}

    # Select a particular job if requested
    selected_job = None

    if job_title:

        for job in recommendations:

            if job_title.lower() in job["title"].lower():
                selected_job = job
                break

    # Otherwise select the highest-ranked job
    if selected_job is None:
        selected_job = recommendations[0]

    gap_analysis = analyze_skill_gaps(
        resume_text,
        selected_job["description"]
    )

    return {
        "job_title": selected_job["title"],
        "company": selected_job["company"],
        "matching_skills": gap_analysis["matching_skills"],
        "missing_skills": gap_analysis["missing_skills"],
        "skill_coverage": gap_analysis["skill_coverage"]
    }
