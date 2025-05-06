class Config:
    """Configuration settings for the job recommendation system"""
    DATA_PATH = "data/"
    JOB_DATA_FILE = "sample_jobs.csv"
    USER_DATA_FILE = "sample_users.csv"
    
    # NLP settings
    STOPWORDS = ["a", "an", "the", "and", "or", "in", "on", "at"]
    SKILLS_KEYWORDS = [
        "python", "java", "sql", "machine learning", "data analysis",
        "tensorflow", "pytorch", "scikit-learn", "deep learning",
        "pandas", "numpy", "spark", "hadoop", "aws", "azure",
        "docker", "kubernetes", "flask", "django", "fastapi"
    ]
    
    # Recommendation weights
    SKILLS_WEIGHT = 0.5
    EXPERIENCE_WEIGHT = 0.3
    EDUCATION_WEIGHT = 0.2
    
    @classmethod
    def get_data_path(cls, filename):
        return f"{cls.DATA_PATH}{filename}"