import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_resume_with_ai(profile: dict, job_description: str, company_name: str, job_title: str) -> dict:
    """
    Core AI function:
    1. Analyzes JD against profile
    2. Picks ONLY relevant skills/projects
    3. Generates ATS-optimized resume
    4. Returns match score + missing skills + suggestions
    """

    profile_summary = f"""
CANDIDATE PROFILE:
Name: {profile.get('name', '')}
Email: {profile.get('email', '')}
Phone: {profile.get('phone', '')}
LinkedIn: {profile.get('linkedin', '')}
GitHub: {profile.get('github', '')}
Portfolio: {profile.get('portfolio', '')}

ALL SKILLS: {', '.join(profile.get('skills', []))}

ALL PROJECTS:
{json.dumps(profile.get('projects', []), indent=2)}

EDUCATION:
{json.dumps(profile.get('education', []), indent=2)}

WORK EXPERIENCE / INTERNSHIPS:
{json.dumps(profile.get('experience', []), indent=2)}

CERTIFICATIONS:
{json.dumps(profile.get('certifications', []), indent=2)}
"""

    prompt = f"""You are an expert ATS resume writer and career coach.

{profile_summary}

JOB DESCRIPTION:
Company: {company_name}
Role: {job_title}
{job_description}

YOUR TASK:
1. Analyze the job description carefully — extract key required skills, technologies, and responsibilities.
2. From the candidate's profile, SELECT ONLY the most relevant skills, projects, and experience for THIS specific job.
3. Do NOT include everything. Be selective. Quality over quantity.
4. If skills are limited, smartly highlight relevant projects, coursework, and certifications instead.
5. Generate a complete ATS-optimized resume tailored to this specific job.
6. Calculate a match score (0-100) based on how well the profile fits the JD.
7. List matched skills, missing skills, and specific learning suggestions.

RESUME FORMAT RULES:
- Use clean plain text format with clear sections
- Use standard section headers: SUMMARY, SKILLS, EXPERIENCE, PROJECTS, EDUCATION, CERTIFICATIONS
- Use bullet points starting with strong action verbs (Developed, Built, Implemented, Optimized, Led, Designed)
- Quantify achievements wherever possible (even if estimated)
- Incorporate keywords from the JD naturally
- Keep it to 1 page equivalent
- ATS-friendly: no tables, no columns, no special characters

Return ONLY a JSON object in this exact format:
{{
    "generated_resume": "Full resume text here with \\n for line breaks",
    "match_score": 72,
    "matched_skills": ["Python", "SQL", "REST APIs"],
    "missing_skills": ["Kubernetes", "Terraform", "AWS Lambda"],
    "suggestions": [
        "Learn Docker and container orchestration basics (1-2 weeks)",
        "Build a project using AWS services — start with S3 and Lambda",
        "Add a system design project to showcase backend architecture skills"
    ]
}}

The generated_resume must be a complete, properly formatted resume ready to copy-paste.
Return ONLY the JSON. No explanation. No markdown. No preamble."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)

    # Validate required keys
    required = ["generated_resume", "match_score", "matched_skills", "missing_skills", "suggestions"]
    for key in required:
        if key not in result:
            if key == "match_score":
                result[key] = 0
            else:
                result[key] = [] if key != "generated_resume" else ""

    return result
