from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import UserProfile, JobPosting, JobDataset
from config import Config

class JobRecommender:
    """Core recommendation engine using NLP and similarity matching"""
    
    def __init__(self, job_dataset: JobDataset):
        self.job_dataset = job_dataset
        self.vectorizer = TfidfVectorizer(stop_words=Config.STOPWORDS)
        self._fit_vectorizer()
    
    def _fit_vectorizer(self):
        """Fit the TF-IDF vectorizer on all job descriptions"""
        all_texts = [job.description for job in self.job_dataset.get_all_jobs()]
        self.vectorizer.fit(all_texts)
    
    def recommend_jobs(self, user_profile: UserProfile, top_n: int = 5) -> List[Tuple[JobPosting, float]]:
        """
        Recommend jobs to a user based on their profile
        Returns list of tuples (job, similarity_score)
        """
        # Get all jobs that match preferred locations
        location_filtered_jobs = self._filter_by_location(user_profile.preferred_locations)
        
        # Calculate similarity scores
        scored_jobs = []
        for job in location_filtered_jobs:
            score = self._calculate_match_score(user_profile, job)
            scored_jobs.append((job, score))
        
        # Sort by score and return top N
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return scored_jobs[:top_n]
    
    def _filter_by_location(self, preferred_locations: List[str]) -> List[JobPosting]:
        """Filter jobs by preferred locations"""
        if not preferred_locations:
            return self.job_dataset.get_all_jobs()
        
        def location_filter(job: JobPosting):
            return any(loc.lower() in job.location.lower() for loc in preferred_locations)
        
        return self.job_dataset.filter_jobs(location_filter)
    
    def _calculate_match_score(self, user_profile: UserProfile, job: JobPosting) -> float:
        """Calculate composite match score between user and job"""
        # Skills similarity
        skills_sim = self._calculate_skills_similarity(user_profile.skills, job.required_skills)
        
        # Experience match
        exp_sim = self._calculate_experience_similarity(
            user_profile.experience_years, 
            job.experience_level
        )
        
        # Education match
        edu_sim = self._calculate_education_similarity(
            user_profile.education,
            job.education_level
        )
        
        # Text similarity between user experience and job description
        text_sim = self._calculate_text_similarity(
            user_profile.experience_details,
            job.description
        )
        
        # Composite score with weights
        total_score = (
            Config.SKILLS_WEIGHT * skills_sim +
            Config.EXPERIENCE_WEIGHT * exp_sim +
            Config.EDUCATION_WEIGHT * edu_sim +
            0.2 * text_sim  # Additional weight for text similarity
        )
        
        return total_score
    
    def _calculate_skills_similarity(self, user_skills: List[str], job_skills: List[str]) -> float:
        """Calculate Jaccard similarity between user skills and job skills"""
        if not user_skills or not job_skills:
            return 0.0
        
        user_skills_set = set(skill.lower() for skill in user_skills)
        job_skills_set = set(skill.lower() for skill in job_skills)
        
        intersection = user_skills_set.intersection(job_skills_set)
        union = user_skills_set.union(job_skills_set)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_experience_similarity(self, user_exp: int, job_exp_level: str) -> float:
        """Calculate experience match score"""
        # Simple implementation - can be enhanced
        if "entry" in job_exp_level.lower():
            return 1.0 if user_exp <= 2 else 0.5
        elif "mid" in job_exp_level.lower():
            return 1.0 if 2 < user_exp <= 5 else 0.7
        elif "senior" in job_exp_level.lower():
            return 1.0 if user_exp > 5 else 0.3
        return 0.5
    
    def _calculate_education_similarity(self, user_edu: str, job_edu_level: str) -> float:
        """Calculate education match score"""
        # Simple implementation - can be enhanced
        user_edu_lower = user_edu.lower()
        job_edu_lower = job_edu_level.lower()
        
        if "phd" in job_edu_lower:
            return 1.0 if "phd" in user_edu_lower else 0.3
        elif "master" in job_edu_lower:
            return 1.0 if "master" in user_edu_lower or "phd" in user_edu_lower else 0.5
        elif "bachelor" in job_edu_lower:
            return 1.0 if "bachelor" in user_edu_lower or "master" in user_edu_lower or "phd" in user_edu_lower else 0.3
        return 0.5
    
    def _calculate_text_similarity(self, user_text: str, job_text: str) -> float:
        """Calculate TF-IDF cosine similarity between user text and job text"""
        if not user_text or not job_text:
            return 0.0
        
        vectors = self.vectorizer.transform([user_text, job_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        return similarity[0][0]