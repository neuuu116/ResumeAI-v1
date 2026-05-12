from pydantic import BaseModel
from typing import List, Optional

# --- Profile Models ---

class Project(BaseModel):
    title: str = ""
    description: str = ""
    tech_stack: str = ""
    impact: str = ""

class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""
    grade: str = ""

class Experience(BaseModel):
    role: str = ""
    company: str = ""
    duration: str = ""
    description: str = ""

class Certification(BaseModel):
    name: str = ""
    issuer: str = ""
    year: str = ""

class UserProfile(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    skills: List[str] = []
    projects: List[Project] = []
    education: List[Education] = []
    experience: List[Experience] = []
    certifications: List[Certification] = []

# --- Generation Models ---

class GenerateRequest(BaseModel):
    job_description: str
    company_name: str = ""
    job_title: str = ""

class GenerateResponse(BaseModel):
    generated_resume: str
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    history_id: int

# --- History Models ---

class HistoryItem(BaseModel):
    id: int
    company_name: str
    job_title: str
    job_description: str
    generated_resume: str
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    created_at: str
