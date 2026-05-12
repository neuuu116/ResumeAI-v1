from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from database import init_db, get_profile, save_profile, save_resume_history, get_all_history, get_history_by_id, delete_history_by_id
from models import UserProfile, GenerateRequest, GenerateResponse, HistoryItem
from ai_engine import generate_resume_with_ai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ResumeAI v2", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
async def startup():
    init_db()
    logger.info("ResumeAI v2 Backend started ✅")


# ─────────────────────────────────────────
# PROFILE ENDPOINTS
# ─────────────────────────────────────────

@app.get("/profile")
async def get_user_profile():
    """Get the stored user profile"""
    profile = get_profile()
    return profile

@app.post("/profile")
async def save_user_profile(profile: UserProfile):
    """Save/update user profile"""
    try:
        data = profile.model_dump()
        save_profile(data)
        return {"success": True, "message": "Profile saved successfully"}
    except Exception as e:
        logger.error(f"Profile save error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# RESUME GENERATION ENDPOINT
# ─────────────────────────────────────────

@app.post("/generate", response_model=GenerateResponse)
async def generate_resume(req: GenerateRequest):
    """Generate a tailored resume for a specific job description"""
    try:
        # Load profile
        profile = get_profile()
        
        if not profile.get('name') or not profile.get('skills'):
            raise HTTPException(
                status_code=400,
                detail="Please complete your profile first (name + skills are required)"
            )

        # Generate via AI
        result = generate_resume_with_ai(
            profile=profile,
            job_description=req.job_description,
            company_name=req.company_name,
            job_title=req.job_title
        )

        # Save to history
        history_id = save_resume_history({
            "company_name": req.company_name,
            "job_title": req.job_title,
            "job_description": req.job_description,
            "generated_resume": result["generated_resume"],
            "match_score": result["match_score"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "suggestions": result["suggestions"]
        })

        return GenerateResponse(
            generated_resume=result["generated_resume"],
            match_score=result["match_score"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            suggestions=result["suggestions"],
            history_id=history_id
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


# ─────────────────────────────────────────
# HISTORY ENDPOINTS
# ─────────────────────────────────────────

@app.get("/history")
async def get_history():
    """Get all generated resume history"""
    try:
        history = get_all_history()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{record_id}")
async def get_history_record(record_id: int):
    """Get a specific resume from history"""
    record = get_history_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.delete("/history/{record_id}")
async def delete_history_record(record_id: int):
    """Delete a resume from history"""
    try:
        delete_history_by_id(record_id)
        return {"success": True, "message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "app": "ResumeAI v2",
        "status": "online",
        "endpoints": [
            "GET  /profile",
            "POST /profile",
            "POST /generate",
            "GET  /history",
            "GET  /history/{id}",
            "DELETE /history/{id}"
        ]
    }
