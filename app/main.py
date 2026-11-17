
import streamlit as st
import hashlib

from app.resume_parser import extract_text_from_pdf
from app.job_matcher import (
    extract_skills,
    match_jobs,
    analyze_skill_gaps
)
from app.ai_assistant import (
    generate_job_explanation,
    chat_with_career_assistant
)


# -----------------------------------
# 1. Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="JobMatch AI",
    page_icon="💼",
    layout="centered"
)


# -----------------------------------
# 2. Application Header
# -----------------------------------

st.title("JobMatch AI")
st.subheader("AI-Powered Job Matching System")

st.write(
    "Upload your resume to analyze your profile "
    "and discover relevant job opportunities."
)


# -----------------------------------
# 3. Resume Upload
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)


if uploaded_file is not None:

    try:

        # -----------------------------------
        # 4. Resume Text Extraction
        # -----------------------------------

        resume_bytes = uploaded_file.getvalue()

        resume_text = extract_text_from_pdf(resume_bytes)

        st.success("Resume uploaded successfully!")

        st.subheader("Extracted Resume Content")

        st.text_area(
            "Resume Text",
            value=resume_text,
            height=250
        )

        # Reset chat when a different resume is uploaded
        resume_key = hashlib.sha256(resume_bytes).hexdigest()

        if st.session_state.get("resume_key") != resume_key:
            st.session_state.resume_key = resume_key
            st.session_state.chat_history = []

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []


        # -----------------------------------
        # 5. Skill Extraction
        # -----------------------------------

        extracted_skills = extract_skills(resume_text)

        st.subheader("Detected Skills")

        if extracted_skills:

            for category, skills in extracted_skills.items():
                st.markdown(f"**{category}**")
                st.write(" • ".join(skills))

        else:
            st.info("No predefined technical skills detected.")


        # -----------------------------------
        # 6. Semantic Job Matching
        # -----------------------------------

        st.divider()
        st.subheader("Recommended Jobs")

        with st.spinner("Finding relevant job opportunities..."):
            recommendations = match_jobs(resume_text)


        if recommendations:

            # -----------------------------------
            # 7. Display Job Recommendations
            # -----------------------------------

            for index, job in enumerate(recommendations, start=1):

                gap_analysis = analyze_skill_gaps(
                    resume_text,
                    job["description"]
                )

                with st.container(border=True):

                    st.markdown(f"### {index}. {job['title']}")

                    st.write(f"**Company:** {job['company']}")

                    st.progress(
                        max(
                            0.0,
                            min(1.0, job["match_score"] / 100)
                        )
                    )

                    st.write(
                        f"**Similarity Score:** "
                        f"{job['match_score']:.2f}%"
                    )

                    st.write(job["description"])


                    # -----------------------------------
                    # 8. Matching Skills
                    # -----------------------------------

                    st.markdown("**Matching Skills**")

                    if gap_analysis["matching_skills"]:
                        st.write(
                            " • ".join(gap_analysis["matching_skills"])
                        )
                    else:
                        st.info("No matching skills detected.")


                    # -----------------------------------
                    # 9. Missing Skills
                    # -----------------------------------

                    st.markdown("**Missing Skills**")

                    if gap_analysis["missing_skills"]:
                        st.warning(
                            " • ".join(gap_analysis["missing_skills"])
                        )
                    else:
                        st.success("No missing skills detected.")


                    # -----------------------------------
                    # 10. Skill Coverage
                    # -----------------------------------

                    st.write(
                        f"**Skill Coverage:** "
                        f"{gap_analysis['skill_coverage']}%"
                    )


                    # -----------------------------------
                    # 11. Gemini AI Explanation
                    # -----------------------------------

                    with st.expander("✨ AI Job Match Explanation"):

                        if st.button(
                            "Generate AI Explanation",
                            key=f"explain_{job['id']}"
                        ):

                            candidate_profile = ", ".join(
                                skill
                                for skills in extracted_skills.values()
                                for skill in skills
                            )

                            with st.spinner(
                                "Generating job match explanation..."
                            ):

                                explanation = generate_job_explanation(
                                    candidate_profile,
                                    job["description"],
                                    gap_analysis["matching_skills"],
                                    gap_analysis["missing_skills"]
                                )

                            st.markdown(explanation)


        else:
            st.info("No matching jobs found.")


        # -----------------------------------
        # 12. AI Career Assistant
        # -----------------------------------

        st.divider()

        st.header("💬 AI Career Assistant")

        st.write(
            "Ask questions about your job matches, "
            "missing skills, and career development."
        )

        # Display previous chat messages
        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        # Chat input
        user_question = st.chat_input(
            "Ask something about your career..."
        )

        if user_question:

            # Display user question
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            with st.chat_message("user"):
                st.markdown(user_question)


            # Generate assistant response
            with st.chat_message("assistant"):

                with st.spinner("Analyzing your career profile..."):

                    response = chat_with_career_assistant(
                        user_question,
                        resume_text,
                        st.session_state.chat_history[:-1]
                    )

                st.markdown(response)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })


    except Exception as error:

        st.error(f"Something went wrong: {error}")


else:

    st.info("Upload your PDF resume to get started.")
