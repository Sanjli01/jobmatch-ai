
import streamlit as st
from resume_parser import extract_text_from_pdf
from job_matcher import extract_skills

st.set_page_config(
    page_title="JobMatch AI",
    page_icon="💼",
    layout="centered"
)

st.title("JobMatch AI")
st.subheader("AI-Powered Job Matching System")

st.write(
    "Upload your resume to analyze your profile "
    "and discover relevant job opportunities."
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        resume_text = extract_text_from_pdf(
            uploaded_file.getvalue()
        )

        st.success("Resume uploaded successfully!")

        st.subheader("Extracted Resume Content")
        st.text_area(
            "Resume Text",
            value=resume_text,
            height=250
        )

        # Extract technical skills
        extracted_skills = extract_skills(resume_text)

        st.subheader("Detected Skills")

        if extracted_skills:
            for category, skills in extracted_skills.items():
                st.markdown(f"**{category}**")
                st.write(" • ".join(skills))
        else:
            st.info("No predefined technical skills detected.")

    except ValueError as error:
        st.error(str(error))
