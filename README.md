# JobMatch AI – AI-Powered Job Matching & Recommendation System

JobMatch AI is an AI-powered job recommendation system designed to help job seekers discover relevant opportunities based on their skills, qualifications, and experience.

The application analyzes candidate resumes and job descriptions using semantic search and embedding-based similarity to identify and rank relevant job opportunities. It also uses an LLM to generate personalized job-match explanations and identify missing skills.

## Problem Statement

Traditional job search platforms often rely heavily on keyword matching, which can overlook relevant opportunities when candidates and employers describe similar skills using different terminology.

JobMatch AI aims to address this limitation by understanding the semantic relationship between candidate profiles and job requirements, helping users discover more relevant job opportunities.

## Key Features

- **Resume Parsing:** Extract relevant information and skills from uploaded PDF resumes.
- **Skill Extraction:** Identify technical skills and qualifications from candidate profiles.
- **Semantic Job Search:** Find relevant job opportunities using text embeddings rather than relying only on exact keyword matches.
- **Job Recommendation:** Calculate similarity scores and rank job opportunities based on candidate profiles.
- **AI-Powered Explanations:** Generate explanations of why a job matches a candidate's profile.
- **Skill Gap Analysis:** Identify skills present in job descriptions but missing from candidate profiles.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Embeddings | Sentence Transformers |
| Similarity Calculation | Cosine Similarity |
| LLM Integration | Gemini API |
| Database | SQLite |
| Testing | Pytest |

## System Workflow

1. User uploads a resume in PDF format.
2. The application extracts text and identifies relevant skills.
3. Resume content and job descriptions are converted into numerical embeddings.
4. Semantic similarity is calculated between the candidate profile and available job descriptions.
5. Jobs are ranked according to their relevance.
6. The LLM generates personalized explanations and identifies potential skill gaps.
7. Recommended jobs are displayed through an interactive dashboard.

## Project Structure

```text
jobmatch-ai/
│
├── app/
│   ├── main.py
│   ├── resume_parser.py
│   ├── job_matcher.py
│   ├── embeddings.py
│   └── ai_assistant.py
│
├── data/
│   └── sample_jobs.json
│
├── tests/
│   └── test_job_matcher.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/jobmatch-ai.git
cd jobmatch-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit your actual API key to GitHub.

### 5. Run the application

Run commands will be added once the application entry points are implemented.

## Future Enhancements

- AI-powered conversational career assistant.
- Tool calling for job search and skill-gap analysis.
- Improved recommendation ranking and evaluation.
- Candidate preference-based job filtering.
- Expanded job datasets and recommendation testing.

## Project Status

Currently under development. Features and implementation details will be updated as development progresses.
