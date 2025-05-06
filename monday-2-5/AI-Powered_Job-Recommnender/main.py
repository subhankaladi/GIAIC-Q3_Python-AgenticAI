import streamlit as st
import pandas as pd
import os
from PIL import Image
from recommender.job_scraper import JobScraper
from recommender.recommender import JobRecommender
from recommender.utils import DataLoader
from recommender.models import UserProfile
from config import Config
import pdfplumber  # For resume parsing
import tempfile

# Page configuration
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="💼",
    layout="wide"
)

def parse_resume(file_path):
    """Extract text from resume PDF and identify key sections"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    # Simple parsing logic - can be enhanced with NLP
    skills = []
    experience = 0
    education = ""
    experience_details = ""
    
    # Extract skills (simple keyword matching)
    for skill in Config.SKILLS_KEYWORDS:
        if skill.lower() in text.lower():
            skills.append(skill)
    
    # Extract experience (looking for years)
    import re
    exp_matches = re.findall(r'(\d+)\s*(years?|yrs?)', text, re.IGNORECASE)
    if exp_matches:
        experience = max(int(m[0]) for m in exp_matches)
    
    # Extract education
    edu_keywords = ["bachelor", "master", "phd", "university", "college"]
    for word in edu_keywords:
        if word in text.lower():
            education = word.capitalize()
            break
    
    return {
        "skills": skills,
        "experience_years": experience,
        "education": education if education else "Bachelor's Degree",
        "experience_details": text[:500]  # First 500 chars as experience
    }

def main():
    st.title("💼 AI-Powered Job Recommendation Engine")
    st.markdown("""
    This system analyzes your profile and matches you with the most relevant job opportunities 
    using advanced NLP techniques.
    """)
    
    # Initialize components
    job_scraper = JobScraper()
    job_scraper.load_from_csv(Config.get_data_path(Config.JOB_DATA_FILE))
    recommender = JobRecommender(job_scraper.get_dataset())
    
    # Input options
    input_option = st.radio(
        "Select input method:",
        ["Use sample test data", "Upload your profile (CSV)", "Upload your resume (PDF)"],
        horizontal=True
    )
    
    user_profile = None
    
    if input_option == "Use sample test data":
        st.subheader("Testing with Sample Data")
        sample_users = DataLoader.load_user_profiles(Config.get_data_path(Config.USER_DATA_FILE))
        selected_user = st.selectbox(
            "Select a sample user profile",
            options=[f"{user.name} ({user.education}, {user.experience_years} yrs exp)" 
                    for user in sample_users]
        )
        user_idx = [f"{user.name} ({user.education}, {user.experience_years} yrs exp)" 
                   for user in sample_users].index(selected_user)
        user_profile = sample_users[user_idx]
        
    elif input_option == "Upload your profile (CSV)":
        st.subheader("Upload Your Profile")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # Load user data
                users = DataLoader.load_user_profiles(tmp_path)
                if users:
                    user_profile = users[0]  # Take first user
                    st.success("Profile loaded successfully!")
                else:
                    st.error("No valid user data found in the CSV file.")
                
                # Clean up
                os.unlink(tmp_path)
            except Exception as e:
                st.error(f"Error processing CSV file: {str(e)}")
    
    elif input_option == "Upload your resume (PDF)":
        st.subheader("Upload Your Resume")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            try:
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # Parse resume
                resume_data = parse_resume(tmp_path)
                
                # Create user profile
                user_profile = UserProfile(
                    user_id="resume_user",
                    name=st.text_input("Your Name", value="Resume User"),
                    skills=resume_data["skills"],
                    experience_years=resume_data["experience_years"],
                    education=resume_data["education"],
                    preferred_job_titles=st.text_input(
                        "Preferred Job Titles (comma separated)",
                        value="data scientist, machine learning engineer"
                    ).split(","),
                    preferred_locations=st.text_input(
                        "Preferred Locations (comma separated)",
                        value="remote, new york"
                    ).split(","),
                    experience_details=resume_data["experience_details"]
                )
                
                # Clean up
                os.unlink(tmp_path)
                st.success("Resume parsed successfully!")
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
    
    # Display recommendations if profile exists
    if user_profile:
        st.divider()
        st.subheader(f"Profile Summary for {user_profile.name}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Skills:**")
            st.write(", ".join(user_profile.skills) if user_profile.skills else "None")
        with col2:
            st.markdown("**Experience:**")
            st.write(f"{user_profile.experience_years} years")
        with col3:
            st.markdown("**Education:**")
            st.write(user_profile.education)
        
        if st.button("Get Job Recommendations"):
            with st.spinner("Finding best matching jobs..."):
                recommended_jobs = recommender.recommend_jobs(user_profile, top_n=5)
                
                if not recommended_jobs:
                    st.warning("No matching jobs found. Try broadening your search criteria.")
                else:
                    st.subheader("Top Job Recommendations")
                    
                    for job, score in recommended_jobs:
                        with st.expander(f"{job.title} at {job.company} (Match: {score:.0%})"):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**Location:** {job.location}")
                                st.markdown(f"**Experience Level:** {job.experience_level}")
                                st.markdown(f"**Education Level:** {job.education_level}")
                                
                                st.markdown("**Required Skills:**")
                                st.write(", ".join(job.required_skills))
                                
                                st.markdown("**Job Description:**")
                                st.write(job.description[:500] + "...")
                            
                            with col2:
                                st.metric("Match Score", f"{score:.0%}")
                                
                                # Apply button with confirmation
                                if st.button("Apply", key=f"apply_{job.id}"):
                                    st.session_state[f'applied_{job.id}'] = True
                                
                                # Show success message if applied
                                if st.session_state.get(f'applied_{job.id}', False):
                                    st.success(f"✅ Application submitted for {job.title} at {job.company}!")
                                    st.balloons()
                                
                                st.markdown("**Shared Skills:**")
                                shared_skills = set(user_profile.skills).intersection(
                                    set(job.required_skills + job.preferred_skills))
                                st.write(", ".join(shared_skills) if shared_skills else "None")

if __name__ == "__main__":
    main()