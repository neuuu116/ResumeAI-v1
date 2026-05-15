from groq import Groq
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_resume_with_ai(profile: dict, job_description: str, company_name: str, job_title: str) -> dict:

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

WORK EXPERIENCE:
{json.dumps(profile.get('experience', []), indent=2)}

CERTIFICATIONS:
{json.dumps(profile.get('certifications', []), indent=2)}
"""

    prompt = f"""You are a professional ATS resume writer. Your job is to write a complete, job-specific resume — not a summary, not an overview. A FULL RESUME.

{profile_summary}

JOB DESCRIPTION:
Company: {company_name}
Role: {job_title}
{job_description}

STRICT RULES — FOLLOW EVERY SINGLE ONE:

BANNED WORDS — never use these, ever:
- "highly motivated", "detail-oriented", "passionate", "dynamic", "hardworking"
- "team player", "fast learner", "go-getter", "results-driven"
- Any generic adjective that does not show proof

RESUME STRUCTURE — write ALL sections:

1. CONTACT
   Full name, email, phone, LinkedIn, GitHub on separate lines

2. SUMMARY (3 lines max)
   - Line 1: Your role + years/level + top 2-3 specific technologies
   - Line 2: One specific achievement with a number
   - Line 3: What you bring to THIS specific company and role
   - NO cliche words. Only facts and technologies.

3. SKILLS
   - Group by category: Languages | Frameworks | Databases | Tools | Cloud
   - Only include skills relevant to THIS job description
   - Format: Languages: Python, C++ | Frameworks: FastAPI, Flask | Databases: SQLite, MySQL

4. PROJECTS (most important section — treat as experience)
   - For EACH project write 3-4 bullet points
   - Bullet format: [Action verb] + [what exactly you built] + [technology used] + [measurable result]
   - Example: "Engineered a FastAPI backend with 6 REST endpoints handling resume generation, reducing manual effort by 80%"
   - NEVER write one-line project descriptions
   - Include tech stack, architecture decisions, and impact

5. EDUCATION
   - Degree, Institution, Year, CGPA
   - Include ALL institutions (college + IIT Madras if present)
   - Include relevant coursework if it matches the JD

6. CERTIFICATIONS
   - Name, Issuer, Year
   - Only include certs relevant to the job

7. EXPERIENCE (if exists in profile)
   - Same bullet format as projects
   - If no formal experience, SKIP this section — do NOT write "EXPERIENCE" with nothing under it

FORMATTING RULES:
- Use plain text only
- Section headers in CAPS
- Bullets start with strong past-tense action verbs: Built, Engineered, Designed, Implemented, Optimized, Developed, Architected, Automated
- Every bullet must have a technology name and a result
- No tables, no columns, no special characters
- Total length: 400-600 words

RETURN FORMAT:
Return ONLY this JSON. No explanation before or after. No markdown fences.
{{"generated_resume": "full resume here, use \\n for line breaks", "match_score": 75, "matched_skills": ["Python", "FastAPI"], "missing_skills": ["Docker"], "suggestions": ["Learn Docker basics in 2 weeks", "Build one AWS Lambda project"]}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]

    raw = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', raw)
    raw = raw.strip()

    result = json.loads(raw)

    required = ["generated_resume", "match_score", "matched_skills", "missing_skills", "suggestions"]
    for key in required:
        if key not in result:
            if key == "match_score":
                result[key] = 0
            else:
                result[key] = [] if key != "generated_resume" else ""

    return result
