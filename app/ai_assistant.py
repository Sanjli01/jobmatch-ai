
import os
import time
import json

from dotenv import load_dotenv
from google import genai

from career_tools import (
    get_job_recommendations,
    get_skill_gap_report
)

from app.job_matcher import extract_skills


# -----------------------------------
# 1. Gemini Configuration
# -----------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash"


# -----------------------------------
# 2. Local Job Explanation Fallback
# -----------------------------------

def local_job_explanation(
    resume_text,
    job_description,
    matching_skills,
    missing_skills
):
    """
    Generate a job-match explanation locally
    without using Gemini.
    """

    matching = (
        ", ".join(matching_skills)
        if matching_skills
        else "None identified"
    )

    missing = (
        ", ".join(missing_skills)
        if missing_skills
        else "None identified"
    )

    if matching_skills:
        relevance = (
            "Your profile aligns with this role because "
            f"you have the following relevant skills: {matching}."
        )
    else:
        relevance = (
            "Your profile has limited detected skill overlap "
            "with this role. Review the job requirements carefully."
        )

    if missing_skills:
        improvement = (
            f"Skills to improve: {missing}. "
            "Focus on learning these technologies through "
            "practical projects."
        )
    else:
        improvement = (
            "No missing skills were identified by the current "
            "skill-matching dictionary."
        )

    return f"""
### Job Match Analysis

**Why this job is relevant**

{relevance}

**Your matching skills**

{matching}

**Skills to improve**

{improvement}

**Learning Recommendations**

1. Strengthen your practical knowledge of the skills required for this role.
2. Build a project demonstrating the relevant technologies and concepts.

*This explanation was generated using local Python analysis
because the Gemini service was unavailable. It is based on
detected skills, not a complete evaluation of your experience.*
"""


# -----------------------------------
# 3. Gemini Job Match Explanation
# -----------------------------------

def generate_job_explanation(
    resume_text,
    job_description,
    matching_skills,
    missing_skills
):
    """
    Generate a personalized job-match explanation.
    Uses local fallback if Gemini is unavailable.
    """

    prompt = f"""
    You are an AI career assistant.

    Analyze the candidate's profile against the job description.

    Candidate Skills:
    {resume_text}

    Job Description:
    {job_description}

    Matching Skills:
    {matching_skills}

    Missing Skills:
    {missing_skills}

    Provide:
    1. Why this job is relevant.
    2. How matching skills support the role.
    3. Which missing skills should be improved.
    4. Two practical learning recommendations.

    Keep the response concise and professional.
    Do not invent candidate experience.
    """

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response.text:
                return response.text

            return local_job_explanation(
                resume_text,
                job_description,
                matching_skills,
                missing_skills
            )

        except Exception as error:

            error_message = str(error)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:
                    time.sleep(2 ** (attempt + 1))
                    continue

                return (
                    "Gemini is currently experiencing high demand.\n\n"
                    "Using local job-match analysis instead:\n\n"
                    + local_job_explanation(
                        resume_text,
                        job_description,
                        matching_skills,
                        missing_skills
                    )
                )

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                return (
                    "Gemini quota is currently unavailable.\n\n"
                    "Using local job-match analysis instead:\n\n"
                    + local_job_explanation(
                        resume_text,
                        job_description,
                        matching_skills,
                        missing_skills
                    )
                )

            print("GEMINI EXPLANATION ERROR:", repr(error))

            return (
                "Unable to generate AI explanation.\n\n"
                "Using local job-match analysis instead:\n\n"
                + local_job_explanation(
                    resume_text,
                    job_description,
                    matching_skills,
                    missing_skills
                )
            )

    return local_job_explanation(
        resume_text,
        job_description,
        matching_skills,
        missing_skills
    )


# -----------------------------------
# 4. Local Career Assistant Fallback
# -----------------------------------

def local_career_fallback(question, resume_text):
    """
    Provides career assistance without Gemini.
    Uses local job matching and skill-gap analysis.
    """

    question_lower = question.lower()

    # Job recommendations
    if any(word in question_lower for word in [
        "job", "jobs", "suitable", "recommend", "career"
    ]):

        jobs = get_job_recommendations(resume_text)

        if not jobs:
            return "No suitable job recommendations were found."

        result = "Here are your top job recommendations:\n\n"

        for index, job in enumerate(jobs[:3], start=1):

            result += (
                f"{index}. {job['title']} - {job['company']}\n"
                f"   Match Score: {job['match_score']:.2f}%\n\n"
            )

        result += (
            "These recommendations are based on semantic similarity "
            "between your resume and the available sample job descriptions."
        )

        return result

    # Skill-gap analysis
    elif any(word in question_lower for word in [
        "skill", "missing", "gap", "improve", "learn"
    ]):

        jobs = get_job_recommendations(resume_text)

        if not jobs:
            return "No job information is available for skill-gap analysis."

        selected_job = jobs[0]

        for job in jobs:

            if job["title"].lower() in question_lower:
                selected_job = job
                break

        report = get_skill_gap_report(
            resume_text,
            selected_job["title"]
        )

        return (
            f"Skill Gap Report for {report['job_title']}\n\n"
            f"Matching Skills: "
            f"{', '.join(report['matching_skills']) or 'None'}\n\n"
            f"Missing Skills: "
            f"{', '.join(report['missing_skills']) or 'None'}\n\n"
            f"Skill Coverage: {report['skill_coverage']}%\n\n"
            "Focus on learning the missing skills to improve "
            "your alignment with this job."
        )

    # General fallback
    return (
        "The AI assistant is temporarily unavailable.\n\n"
        "You can still ask me about suitable jobs or missing skills. "
        "These features use local analysis and do not require Gemini."
    )


# -----------------------------------
# 5. Gemini Career Assistant
# -----------------------------------

def chat_with_career_assistant(
    question,
    resume_text,
    conversation_history=None
):
    """
    Conversational career assistant with automatic
    function calling and local fallback.
    """

    if conversation_history is None:
        conversation_history = []

    candidate_skills = extract_skills(resume_text)

    # Tool 1: Find relevant jobs
    def find_relevant_jobs() -> str:
        """Find and rank jobs relevant to the candidate's resume."""

        results = get_job_recommendations(resume_text)

        return json.dumps(results)

    # Tool 2: Analyze skill gaps
    def check_skill_gaps(job_title: str = "") -> str:
        """Identify matching and missing skills for a job."""

        results = get_skill_gap_report(
            resume_text,
            job_title if job_title else None
        )

        return json.dumps(results)

    # Conversation history
    history = ""

    for message in conversation_history[-8:]:

        history += (
            f"\n{message['role']}: {message['content']}"
        )

    prompt = f"""
    You are JobMatch AI, an intelligent career assistant.

    Candidate's detected skills:
    {json.dumps(candidate_skills)}

    Previous conversation:
    {history}

    Current question:
    {question}

    Instructions:
    1. Answer using the candidate's profile.
    2. Use find_relevant_jobs when asked about suitable jobs.
    3. Use check_skill_gaps when asked about missing skills.
    4. Use both tools when necessary.
    5. Never invent candidate experience.
    6. Give practical career advice.
    7. Keep responses clear and concise.
    """

    # Gemini request with retry handling
    for attempt in range(3):

        try:

            chat = client.chats.create(
                model=MODEL_NAME,
                config={
                    "tools": [
                        find_relevant_jobs,
                        check_skill_gaps
                    ]
                }
            )

            response = chat.send_message(prompt)

            return response.text or local_career_fallback(
                question,
                resume_text
            )

        except Exception as error:

            error_message = str(error)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 2:

                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Gemini unavailable. Retrying in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return (
                    "Gemini is currently experiencing high demand.\n\n"
                    "Using local career analysis instead:\n\n"
                    + local_career_fallback(question, resume_text)
                )

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                return (
                    "Gemini quota is currently unavailable.\n\n"
                    "Using local career analysis instead:\n\n"
                    + local_career_fallback(question, resume_text)
                )

            print("GEMINI CAREER ASSISTANT ERROR:", repr(error))

            return (
                "Unable to process your request using Gemini.\n\n"
                "Using local career analysis instead:\n\n"
                + local_career_fallback(question, resume_text)
            )

    return local_career_fallback(question, resume_text)
