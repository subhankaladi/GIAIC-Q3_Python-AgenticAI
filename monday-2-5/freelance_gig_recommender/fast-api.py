import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from abc import ABC, abstractmethod
import uuid
from typing import List, Dict
from functools import lru_cache

app = FastAPI()

# Pydantic Models
class UserInput(BaseModel):
    name: str
    skills: List[str]
    min_budget: int
    preferred_category: str

class FeedbackInput(BaseModel):
    user_id: str
    gig_id: int
    rating: int

class SavedGigInput(BaseModel):
    user_id: str
    gig_id: int

class GigRecommendation(BaseModel):
    gig_id: int
    title: str
    budget: int
    category: str
    platform: str
    similarity: float
    generated_summary: str
    generated_pitch: str
    application_template: str

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[GigRecommendation]
    skill_tips: str

# Abstract Base Class for Data Processing (Abstraction)
class DataProcessor(ABC):
    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def analyze_trends(self):
        pass

# Abstract Base Class for Recommendation Engine (Abstraction)
class RecommendationEngine(ABC):
    @abstractmethod
    def recommend(self, user, gigs_df, feedback_df):
        pass

# User Profile Class (Encapsulation)
class UserProfile:
    def __init__(self, name: str, skills: List[str], min_budget: int, preferred_category: str):
        self.__name = name
        self.__skills = skills
        self.__min_budget = min_budget
        self.__preferred_category = preferred_category
        self.__id = str(uuid.uuid4())

        # Save to SQLite
        with sqlite3.connect("gigs.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    skills TEXT,
                    min_budget INTEGER,
                    preferred_category TEXT
                )
            """)
            cursor.execute(
                "INSERT OR REPLACE INTO users (id, name, skills, min_budget, preferred_category) VALUES (?, ?, ?, ?, ?)",
                (self.__id, name, ",".join(skills), min_budget, preferred_category)
            )
            conn.commit()

    def get_skills(self):
        return self.__skills

    def get_min_budget(self):
        return self.__min_budget

    def get_preferred_category(self):
        return self.__preferred_category

    def get_id(self):
        return self.__id

    def get_user_info(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "skills": self.__skills,
            "min_budget": self.__min_budget,
            "category": self.__preferred_category
        }

# Gig Data Processor Class (Inheritance)
class GigDataProcessor(DataProcessor):
    def __init__(self):
        self.gigs_df = self.__load_mock_data()

    def __load_mock_data(self):
        data = {
            "gig_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "title": [
                "React Developer for Web App",
                "AI Engineer for Generative Model",
                "Python Developer for Data Pipeline",
                "Content Writer for Tech Blog",
                "Data Scientist for ML Model",
                "Agentic AI Specialist for Automation",
                "Full-Stack Developer for E-commerce",
                "Frontend Developer for SaaS Platform",
                "Backend Developer for API Integration",
                "Mobile App Developer for Fintech"
            ],
            "skills": [
                "React, JavaScript, Tailwind CSS",
                "Python, Generative AI, TensorFlow",
                "Python, Pandas, SQL",
                "SEO, Creative Writing",
                "Python, Scikit-learn, Data Science",
                "Python, Agentic AI, Reasoning",
                "React, Python, FastAPI",
                "React, TypeScript, Next.js",
                "Python, FastAPI, PostgreSQL",
                "Flutter, Dart, Firebase"
            ],
            "budget": [600, 1200, 500, 200, 800, 1500, 1000, 700, 900, 1100],
            "category": [
                "Web Development", "AI Development", "Data Science",
                "Content Writing", "Data Science", "AI Development",
                "Web Development", "Web Development", "Backend Development",
                "Mobile Development"
            ],
            "platform": ["Upwork", "Freelancer", "Upwork", "Fiverr", "Freelancer", "Upwork", "Fiverr", "Upwork", "Freelancer", "Fiverr"]
        }
        df = pd.DataFrame(data)

        # Save to SQLite
        with sqlite3.connect("gigs.db") as conn:
            df.to_sql("gigs", conn, if_exists="replace", index=False)
        return df

    @lru_cache(maxsize=1)
    def process_data(self):
        self.gigs_df["skills"] = self.gigs_df["skills"].str.lower()
        self.gigs_df["title"] = self.gigs_df["title"].str.lower()
        return self.gigs_df

    def analyze_trends(self):
        skill_counts = self.gigs_df["skills"].str.split(", ").explode().value_counts().to_dict()
        budget_avg = self.gigs_df.groupby("category")["budget"].mean().to_dict()
        platform_counts = self.gigs_df["platform"].value_counts().to_dict()
        skill_gap = self.__analyze_skill_gap()
        success_rates = self.__analyze_success_rates()
        return {
            "skills": skill_counts,
            "budget": budget_avg,
            "platform": platform_counts,
            "skill_gap": skill_gap,
            "success_rates": success_rates
        }

    def __analyze_skill_gap(self):
        all_skills = self.gigs_df["skills"].str.split(", ").explode().unique()
        trending_skills = ["react", "generative ai", "agentic ai", "python", "typescript", "flutter"]
        return {skill: 1.0 if skill in trending_skills else 0.5 for skill in all_skills}

    def __analyze_success_rates(self):
        # Mock success rates based on budget and platform
        return self.gigs_df.groupby("platform")["budget"].mean().to_dict()

# Mock Generative AI Class (Simulates LLM)
class GenerativeAI:
    def generate_summary(self, gig):
        title = gig["title"]
        skills = gig["skills"]
        return f"This gig '{title}' requires skills like {skills}. It's a prime opportunity to showcase your expertise!"

    def generate_pitch(self, gig):
        title = gig["title"]
        return f"Apply for '{title}' to leverage your skills in a high-impact project with great earning potential!"

    def generate_application_template(self, gig):
        title = gig["title"]
        return f"Dear Client,\nI'm excited to apply for your '{title}' project. With my expertise in {gig['skills']}, I can deliver high-quality results. Let's discuss how I can contribute to your success!\nBest,\n[Your Name]"

    def generate_skill_tips(self, user_skills, missing_skills):
        if not missing_skills:
            return "Your skills are top-tier! Explore advanced projects to maintain your edge."
        resources = {
            "generative ai": "Enroll in Hugging Face's Transformers course: https://huggingface.co/learn",
            "agentic ai": "Learn LangChain for agentic systems: https://python.langchain.com/docs",
            "react": "Master React via freeCodeCamp: https://www.freecodecamp.org/learn",
            "typescript": "Study TypeScript handbook: https://www.typescriptlang.org/docs",
            "python": "Deepen Python skills with Automate the Boring Stuff: https://automatetheboringstuff.com",
            "flutter": "Explore Flutter with Google's official docs: https://flutter.dev/learn"
        }
        tips = [f"- {skill}: {resources.get(skill.lower(), 'Explore Udemy or Coursera courses.')}" for skill in missing_skills]
        return f"To unlock high-paying gigs, consider learning:\n" + "\n".join(tips)

# Feedback Manager Class (Encapsulation)
class FeedbackManager:
    def __init__(self):
        self.__conn = sqlite3.connect("gigs.db")
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                user_id TEXT,
                gig_id INTEGER,
                rating INTEGER,
                PRIMARY KEY (user_id, gig_id)
            )
        """)
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_gigs (
                user_id TEXT,
                gig_id INTEGER,
                PRIMARY KEY (user_id, gig_id)
            )
        """)
        self.__conn.commit()

    def save_feedback(self, user_id: str, gig_id: int, rating: int):
        self.__cursor.execute(
            "INSERT OR REPLACE INTO feedback (user_id, gig_id, rating) VALUES (?, ?, ?)",
            (user_id, gig_id, rating)
        )
        self.__conn.commit()

    def save_gig(self, user_id: str, gig_id: int):
        self.__cursor.execute(
            "INSERT OR REPLACE INTO saved_gigs (user_id, gig_id) VALUES (?, ?)",
            (user_id, gig_id)
        )
        self.__conn.commit()

    def get_saved_gigs(self, user_id: str):
        return pd.read_sql_query("SELECT gig_id FROM saved_gigs WHERE user_id = ?", self.__conn, params=(user_id,))

    def get_feedback(self):
        return pd.read_sql_query("SELECT * FROM feedback", self.__conn)

    def __del__(self):
        self.__conn.close()

# Agentic Recommendation Engine (Polymorphism)
class AgenticRecommendationEngine(RecommendationEngine):
    def __init__(self):
        self.generative_ai = GenerativeAI()
        self.feedback_manager = FeedbackManager()

    def recommend(self, user, gigs_df, feedback_df):
        # Cosine similarity for skill matching
        user_skills = ", ".join(user.get_skills()).lower()
        all_skills = gigs_df["skills"].tolist() + [user_skills]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_skills)
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        # Filter gigs
        filtered_gigs = gigs_df[
            (gigs_df["budget"] >= user.get_min_budget()) &
            (gigs_df["category"] == user.get_preferred_category())
        ].copy()

        # Agentic reasoning: Adaptive weighting
        trending_skills = ["react", "generative ai", "agentic ai", "python", "typescript", "flutter"]
        filtered_gigs["trending_score"] = filtered_gigs["skills"].apply(
            lambda x: sum(1 for skill in trending_skills if skill in x.lower())
        )
        filtered_gigs["similarity"] = cosine_sim[0][:len(filtered_gigs)]

        # Incorporate community feedback trends
        feedback_trend = feedback_df.groupby("gig_id")["rating"].mean().reset_index()
        filtered_gigs = filtered_gigs.merge(
            feedback_trend[["gig_id", "rating"]], on="gig_id", how="left"
        )
        filtered_gigs["rating"] = filtered_gigs["rating"].fillna(3)  # Default rating
        feedback_weight = 0.3 if feedback_df.shape[0] > 10 else 0.2  # Adaptive feedback weight
        filtered_gigs["final_score"] = (
            (0.5 - feedback_weight / 2) * filtered_gigs["similarity"] +
            (0.3 - feedback_weight / 2) * filtered_gigs["trending_score"] +
            feedback_weight * (filtered_gigs["rating"] / 5)
        )

        # Generate summaries, pitches, and application templates
        filtered_gigs["generated_summary"] = filtered_gigs.apply(
            lambda row: self.generative_ai.generate_summary(row), axis=1
        )
        filtered_gigs["generated_pitch"] = filtered_gigs.apply(
            lambda row: self.generative_ai.generate_pitch(row), axis=1
        )
        filtered_gigs["application_template"] = filtered_gigs.apply(
            lambda row: self.generative_ai.generate_application_template(row), axis=1
        )

        # Agentic feedback: Suggest missing skills
        gig_skills = filtered_gigs["skills"].str.split(", ").explode().unique()
        missing_skills = [s for s in gig_skills if s not in user_skills.lower()]
        skill_tips = self.generative_ai.generate_skill_tips(user.get_skills(), missing_skills)

        return filtered_gigs.sort_values(by="final_score", ascending=False), skill_tips

# API Endpoints
@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(user_input: UserInput):
    user = UserProfile(
        user_input.name,
        user_input.skills,
        user_input.min_budget,
        user_input.preferred_category
    )
    processor = GigDataProcessor()
    recommender = AgenticRecommendationEngine()
    gigs_df = processor.process_data()
    feedback_df = recommender.feedback_manager.get_feedback()
    recommendations, skill_tips = recommender.recommend(user, gigs_df, feedback_df)

    if recommendations.empty:
        raise HTTPException(status_code=404, detail="No gigs match your criteria")

    return {
        "user_id": user.get_id(),
        "recommendations": recommendations.to_dict(orient="records"),
        "skill_tips": skill_tips
    }

@app.get("/trends")
async def get_trends():
    processor = GigDataProcessor()
    return processor.analyze_trends()

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackInput):
    if not 1 <= feedback.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    feedback_manager = FeedbackManager()
    feedback_manager.save_feedback(feedback.user_id, feedback.gig_id, feedback.rating)
    return {"message": "Feedback submitted successfully"}

@app.post("/save_gig")
async def save_gig(saved_gig: SavedGigInput):
    feedback_manager = FeedbackManager()
    feedback_manager.save_gig(saved_gig.user_id, saved_gig.gig_id)
    return {"message": "Gig saved successfully"}

@app.get("/saved_gigs/{user_id}")
async def get_saved_gigs(user_id: str):
    feedback_manager = FeedbackManager()
    saved_gigs = feedback_manager.get_saved_gigs(user_id)
    processor = GigDataProcessor()
    gigs_df = processor.process_data()
    saved_gigs_data = gigs_df[gigs_df["gig_id"].isin(saved_gigs["gig_id"])].to_dict(orient="records")
    return {"saved_gigs": saved_gigs_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)