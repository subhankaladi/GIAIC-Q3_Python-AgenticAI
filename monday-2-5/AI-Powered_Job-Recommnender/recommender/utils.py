import pandas as pd
from typing import List, Dict
from .models import UserProfile

class DataLoader:
    """Utility class for loading data"""
    
    @staticmethod
    def load_user_profiles(filepath: str) -> List[UserProfile]:
        """Load user profiles from CSV"""
        df = pd.read_csv(filepath)
        users = []
        
        for _, row in df.iterrows():
            user = UserProfile(
                user_id=str(row.get("user_id", "")),
                name=row.get("name", ""),
                skills=DataLoader._parse_skills(row.get("skills", "")),
                experience_years=int(row.get("experience_years", 0)),
                education=row.get("education", ""),
                preferred_job_titles=DataLoader._parse_list(row.get("preferred_job_titles", "")),
                preferred_locations=DataLoader._parse_list(row.get("preferred_locations", "")),
                experience_details=row.get("experience_details", "")
            )
            users.append(user)
        
        return users
    
    @staticmethod
    def _parse_skills(skills_str: str) -> List[str]:
        """Parse skills string into list of skills"""
        if pd.isna(skills_str):
            return []
        return [skill.strip().lower() for skill in skills_str.split(",")]
    
    @staticmethod
    def _parse_list(list_str: str) -> List[str]:
        """Parse comma-separated string into list"""
        if pd.isna(list_str):
            return []
        return [item.strip() for item in list_str.split(",")]