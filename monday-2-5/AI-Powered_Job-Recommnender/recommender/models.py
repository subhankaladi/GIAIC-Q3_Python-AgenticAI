from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class JobPosting:
    """Class representing a job posting"""
    id: str
    title: str
    company: str
    location: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    education_level: str
    posted_date: str
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "experience_level": self.experience_level,
            "education_level": self.education_level,
            "posted_date": self.posted_date
        }

@dataclass
class UserProfile:
    """Class representing a user profile"""
    user_id: str
    name: str
    skills: List[str]
    experience_years: int
    education: str
    preferred_job_titles: List[str]
    preferred_locations: List[str]
    experience_details: str
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "skills": self.skills,
            "experience_years": self.experience_years,
            "education": self.education,
            "preferred_job_titles": self.preferred_job_titles,
            "preferred_locations": self.preferred_locations,
            "experience_details": self.experience_details
        }

class JobDataset:
    """Class for managing job postings data"""
    def __init__(self):
        self.jobs: List[JobPosting] = []
    
    def add_job(self, job: JobPosting):
        self.jobs.append(job)
    
    def get_job_by_id(self, job_id: str) -> Optional[JobPosting]:
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None
    
    def get_all_jobs(self) -> List[JobPosting]:
        return self.jobs
    
    def filter_jobs(self, filter_func) -> List[JobPosting]:
        return [job for job in self.jobs if filter_func(job)]