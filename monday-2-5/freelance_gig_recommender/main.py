import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from tenacity import retry, stop_after_attempt, wait_fixed

# Streamlit App Configuration
st.set_page_config(page_title="Freelance Gig Recommender", layout="wide")

# Initialize Session State
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "skill_tips" not in st.session_state:
    st.session_state.skill_tips = ""
if "saved_profile" not in st.session_state:
    st.session_state.saved_profile = None
if "compare_gigs" not in st.session_state:
    st.session_state.compare_gigs = []
if "saved_gigs" not in st.session_state:
    st.session_state.saved_gigs = []

# Custom CSS for Styling
def apply_custom_css():
    st.markdown("""
        <style>
        .stSlider > div > div > div > div {
            background-color: #4CAF50;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        .stExpander {
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 16px;
            font-weight: bold;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)

# Retry decorator for API calls
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def make_api_request(method, url, **kwargs):
    response = method(url, **kwargs)
    response.raise_for_status()
    return response.json()

# Save Profile
def save_profile(name, skills, min_budget, category):
    st.session_state.saved_profile = {
        "name": name,
        "skills": skills,
        "min_budget": min_budget,
        "preferred_category": category
    }
    st.success("Profile saved successfully!")

# Load Profile
def load_profile():
    if st.session_state.saved_profile:
        return (
            st.session_state.saved_profile["name"],
            st.session_state.saved_profile["skills"],
            st.session_state.saved_profile["min_budget"],
            st.session_state.saved_profile["preferred_category"]
        )
    return "", [], 200, "Web Development"

# Main Dashboard
def render_dashboard():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Recommendations", "Saved Gigs", "Analytics", "Compare Gigs"])

    apply_custom_css()

    if page == "Dashboard":
        st.title("Freelance Gig Recommender System")
        st.markdown("Discover top freelance gigs tailored to your skills and preferences. Use the sidebar to navigate.")

        st.subheader("Overview")
        st.write("This AI-powered system recommends freelance gigs based on your skills, budget, and category preferences. "
                 "Save profiles, bookmark gigs, compare opportunities, and analyze market trends to boost your freelancing career.")

        st.subheader("Features")
        st.write("- **Personalized Recommendations**: Get gigs matched to your skills using Agentic AI.")
        st.write("- **Skill Gap Analysis**: Identify skills to learn for high-paying opportunities.")
        st.write("- **Saved Gigs**: Bookmark gigs for later review.")
        st.write("- **Compare Gigs**: View multiple gigs side-by-side.")
        st.write("- **Analytics**: Visualize market trends and success rates.")

        # Skill Match Scorecard
        if st.session_state.recommendations:
            st.subheader("Skill Match Scorecard")
            match_scores = [gig["similarity"] * 100 for gig in st.session_state.recommendations]
            avg_score = sum(match_scores) / len(match_scores) if match_scores else 0
            st.metric("Average Skill Match Score", f"{avg_score:.2f}%")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_score,
                title={"text": "Skill Match Score"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#4CAF50"}}
            ))
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Recommendations":
        st.title("Get Your Gig Recommendations")
        saved_name, saved_skills, saved_min_budget, saved_category = load_profile()

        with st.form("user_form"):
            st.subheader("Enter Your Details")
            name = st.text_input("Your Name", value=saved_name, placeholder="John Doe")
            skills = st.multiselect(
                "Select Your Skills",
                [
                    "React", "JavaScript", "Tailwind CSS", "Python", "Generative AI",
                    "Agentic AI", "Pandas", "SQL", "SEO", "Creative Writing",
                    "Scikit-learn", "Data Science", "FastAPI", "TypeScript", "Next.js",
                    "PostgreSQL", "Flutter", "Dart", "Firebase"
                ],
                default=saved_skills
            )
            min_budget = st.slider("Minimum Budget ($)", 100, 2000, saved_min_budget, step=50)
            category = st.selectbox(
                "Preferred Category",
                ["Web Development", "AI Development", "Data Science", "Content Writing", "Backend Development", "Mobile Development"],
                index=["Web Development", "AI Development", "Data Science", "Content Writing", "Backend Development", "Mobile Development"].index(saved_category)
            )
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Get Recommendations")
            with col2:
                save_profile_btn = st.form_submit_button("Save Profile")

        if save_profile_btn:
            save_profile(name, skills, min_budget, category)

        if submitted and name and skills:
            progress_bar = st.progress(0)
            try:
                progress_bar.progress(50)
                response_data = make_api_request(
                    requests.post,
                    "http://127.0.0.1:8000/recommend",
                    json={
                        "name": name,
                        "skills": skills,
                        "min_budget": min_budget,
                        "preferred_category": category
                    }
                )
                if not isinstance(response_data, dict):
                    st.error("Unexpected response format from server. Expected a dictionary.")
                    return
                st.session_state.user_id = response_data.get("user_id")
                st.session_state.recommendations = response_data.get("recommendations", [])
                st.session_state.skill_tips = response_data.get("skill_tips", "")
                progress_bar.progress(100)
            except requests.RequestException as e:
                st.error(f"Error fetching recommendations: {e}")
            finally:
                progress_bar.empty()

        if st.session_state.recommendations:
            st.subheader("Recommended Gigs")
            for gig in st.session_state.recommendations:
                with st.expander(f"{gig['title']} - ${gig['budget']}"):
                    st.write(f"**Category**: {gig['category']}")
                    st.write(f"**Platform**: {gig['platform']}")
                    st.write(f"**Match Score**: {(gig['similarity'] * 100):.2f}%")
                    st.write(f"**Summary**: {gig['generated_summary']}")
                    st.write(f"**Pitch**: {gig['generated_pitch']}")
                    st.write(f"**Application Template**:\n{gig['application_template']}")
                    feedback_rating = st.slider(
                        f"Rate this gig (Gig ID: {gig['gig_id']})", 1, 5, 3, key=f"feedback_{gig['gig_id']}"
                    )
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Submit Feedback", key=f"submit_{gig['gig_id']}"):
                            if st.session_state.user_id:
                                try:
                                    make_api_request(
                                        requests.post,
                                        "http://127.0.0.1:8000/feedback",
                                        json={
                                            "user_id": st.session_state.user_id,
                                            "gig_id": gig["gig_id"],
                                            "rating": feedback_rating
                                        }
                                    )
                                    st.success("Feedback submitted successfully!")
                                except requests.RequestException as e:
                                    st.error(f"Error submitting feedback: {e}")
                            else:
                                st.error("No user ID found. Please get recommendations first.")
                    with col2:
                        if st.button("Save Gig", key=f"save_{gig['gig_id']}"):
                            if st.session_state.user_id:
                                try:
                                    make_api_request(
                                        requests.post,
                                        "http://127.0.0.1:8000/save_gig",
                                        json={
                                            "user_id": st.session_state.user_id,
                                            "gig_id": gig["gig_id"]
                                        }
                                    )
                                    st.session_state.saved_gigs.append(gig)
                                    st.success(f"Saved '{gig['title']}'!")
                                except requests.RequestException as e:
                                    st.error(f"Error saving gig: {e}")
                            else:
                                st.error("No user ID found. Please get recommendations first.")
                    with col3:
                        if st.button("Add to Compare", key=f"compare_{gig['gig_id']}"):
                            if len(st.session_state.compare_gigs) < 3:
                                st.session_state.compare_gigs.append(gig)
                                st.success(f"Added '{gig['title']}' to comparison.")
                            else:
                                st.warning("Maximum 3 gigs can be compared.")

            # Download Report
            report_df = pd.DataFrame(st.session_state.recommendations)
            csv = report_df.to_csv(index=False)
            st.download_button(
                label="Download Recommendations as CSV",
                data=csv,
                file_name="gig_recommendations.csv",
                mime="text/csv"
            )

        if st.session_state.skill_tips:
            st.subheader("Skill Improvement Tips")
            st.info(st.session_state.skill_tips)

    elif page == "Saved Gigs":
        st.title("Saved Gigs")
        if st.session_state.user_id:
            try:
                saved_gigs_data = make_api_request(
                    requests.get,
                    f"http://127.0.0.1:8000/saved_gigs/{st.session_state.user_id}"
                )
                st.session_state.saved_gigs = saved_gigs_data.get("saved_gigs", [])
            except requests.RequestException as e:
                st.error(f"Error fetching saved gigs: {e}")

        if st.session_state.saved_gigs:
            st.subheader("Your Saved Gigs")
            for gig in st.session_state.saved_gigs:
                with st.expander(f"{gig['title']} - ${gig['budget']}"):
                    st.write(f"**Category**: {gig['category']}")
                    st.write(f"**Platform**: {gig['platform']}")
                    st.write(f"**Match Score**: {(gig['similarity'] * 100):.2f}%")
                    st.write(f"**Summary**: {gig['generated_summary']}")
                    st.write(f"**Pitch**: {gig['generated_pitch']}")
                    st.write(f"**Application Template**:\n{gig['application_template']}")
                    if st.button("Remove from Saved", key=f"remove_saved_{gig['gig_id']}"):
                        st.session_state.saved_gigs = [g for g in st.session_state.saved_gigs if g["gig_id"] != gig["gig_id"]]
                        st.experimental_rerun()
        else:
            st.info("No saved gigs yet. Save gigs from the Recommendations page.")

    elif page == "Analytics":
        st.title("Market Trends and Analytics")
        try:
            trends = make_api_request(requests.get, "http://127.0.0.1:8000/trends")
            if not isinstance(trends, dict):
                st.error("Unexpected trends data format.")
                return

            # Skill Demand
            st.markdown("### Most In-Demand Skills")
            skill_df = pd.DataFrame(trends["skills"].items(), columns=["Skill", "Count"])
            fig1 = px.bar(skill_df, x="Count", y="Skill", orientation="h", title="Skill Demand")
            st.plotly_chart(fig1, use_container_width=True)

            # Budget by Category
            st.markdown("### Average Budget by Category")
            budget_df = pd.DataFrame(trends["budget"].items(), columns=["Category", "Average Budget"])
            fig2 = px.pie(budget_df, names="Category", values="Average Budget", title="Budget Distribution")
            st.plotly_chart(fig2, use_container_width=True)

            # Platform Popularity
            st.markdown("### Platform Popularity")
            platform_df = pd.DataFrame(trends["platform"].items(), columns=["Platform", "Count"])
            fig3 = px.bar(platform_df, x="Platform", y="Count", title="Gigs by Platform")
            st.plotly_chart(fig3, use_container_width=True)

            # Skill Gap Analysis
            st.markdown("### Skill Gap Analysis")
            skill_gap_df = pd.DataFrame(trends["skill_gap"].items(), columns=["Skill", "Demand Score"])
            fig4 = px.bar(skill_gap_df, x="Demand Score", y="Skill", orientation="h", title="Your Skill Gap vs. Market Demand")
            st.plotly_chart(fig4, use_container_width=True)

            # Success Rates
            st.markdown("### Platform Success Rates (Avg Budget)")
            success_df = pd.DataFrame(trends["success_rates"].items(), columns=["Platform", "Avg Budget"])
            fig5 = px.bar(success_df, x="Platform", y="Avg Budget", title="Platform Success Rates")
            st.plotly_chart(fig5, use_container_width=True)

            # Feedback Distribution
            st.markdown("### Feedback Distribution")
            try:
                feedback_df = pd.read_sql_query("SELECT rating, COUNT(*) as count FROM feedback GROUP BY rating", sqlite3.connect("gigs.db"))
                fig6 = px.bar(feedback_df, x="rating", y="count", title="Community Feedback Distribution")
                st.plotly_chart(fig6, use_container_width=True)
            except Exception as e:
                st.warning("No feedback data available yet.")

            # Export Analytics
            analytics_df = pd.concat([
                skill_df.rename(columns={"Count": "Skill Demand"}),
                budget_df.rename(columns={"Average Budget": "Avg Budget"}),
                platform_df.rename(columns={"Count": "Platform Popularity"}),
                skill_gap_df.rename(columns={"Demand Score": "Skill Gap Score"}),
                success_df.rename(columns={"Avg Budget": "Success Rate"})
            ], axis=1)
            csv = analytics_df.to_csv(index=False)
            st.download_button(
                label="Download Analytics as CSV",
                data=csv,
                file_name="market_analytics.csv",
                mime="text/csv"
            )

        except requests.RequestException as e:
            st.error(f"Error fetching trends: {e}")

    elif page == "Compare Gigs":
        st.title("Compare Gigs")
        if not st.session_state.compare_gigs:
            st.info("No gigs selected for comparison. Add gigs from the Recommendations page.")
        else:
            st.subheader("Selected Gigs for Comparison")
            cols = st.columns(len(st.session_state.compare_gigs))
            for i, gig in enumerate(st.session_state.compare_gigs):
                with cols[i]:
                    st.markdown(f"**{gig['title']}**")
                    st.write(f"**Budget**: ${gig['budget']}")
                    st.write(f"**Category**: {gig['category']}")
                    st.write(f"**Platform**: {gig['platform']}")
                    st.write(f"**Match Score**: {(gig['similarity'] * 100):.2f}%")
                    st.write(f"**Summary**: {gig['generated_summary']}")
                    if st.button("Remove", key=f"remove_{gig['gig_id']}"):
                        st.session_state.compare_gigs.pop(i)
                        st.experimental_rerun()

# Run the App
if __name__ == "__main__":
    render_dashboard()