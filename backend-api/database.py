import sqlite3
import json
from datetime import datetime

DB_PATH = "resumeai.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # DATABASE 1: User Profile (single row, updated as user edits)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY DEFAULT 1,
            name TEXT DEFAULT '',
            email TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            linkedin TEXT DEFAULT '',
            github TEXT DEFAULT '',
            portfolio TEXT DEFAULT '',
            skills TEXT DEFAULT '[]',
            projects TEXT DEFAULT '[]',
            education TEXT DEFAULT '[]',
            experience TEXT DEFAULT '[]',
            certifications TEXT DEFAULT '[]',
            updated_at TEXT DEFAULT ''
        )
    """)

    # Insert default empty profile if not exists
    cursor.execute("""
        INSERT OR IGNORE INTO user_profile (id, updated_at)
        VALUES (1, ?)
    """, (datetime.now().isoformat(),))

    # DATABASE 2: Resume History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT DEFAULT '',
            job_title TEXT DEFAULT '',
            job_description TEXT DEFAULT '',
            generated_resume TEXT DEFAULT '',
            match_score INTEGER DEFAULT 0,
            matched_skills TEXT DEFAULT '[]',
            missing_skills TEXT DEFAULT '[]',
            suggestions TEXT DEFAULT '[]',
            created_at TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

# --- Profile CRUD ---

def get_profile():
    conn = get_db()
    row = conn.execute("SELECT * FROM user_profile WHERE id = 1").fetchone()
    conn.close()
    if not row:
        return {}
    profile = dict(row)
    # Parse JSON fields
    for field in ['skills', 'projects', 'education', 'experience', 'certifications']:
        try:
            profile[field] = json.loads(profile[field])
        except:
            profile[field] = []
    return profile

def save_profile(data: dict):
    conn = get_db()
    # Serialize JSON fields
    for field in ['skills', 'projects', 'education', 'experience', 'certifications']:
        if field in data and isinstance(data[field], (list, dict)):
            data[field] = json.dumps(data[field])
    
    data['updated_at'] = datetime.now().isoformat()
    
    conn.execute("""
        UPDATE user_profile SET
            name = :name, email = :email, phone = :phone,
            linkedin = :linkedin, github = :github, portfolio = :portfolio,
            skills = :skills, projects = :projects, education = :education,
            experience = :experience, certifications = :certifications,
            updated_at = :updated_at
        WHERE id = 1
    """, data)
    conn.commit()
    conn.close()

# --- History CRUD ---

def save_resume_history(data: dict):
    conn = get_db()
    for field in ['matched_skills', 'missing_skills', 'suggestions']:
        if field in data and isinstance(data[field], list):
            data[field] = json.dumps(data[field])
    data['created_at'] = datetime.now().isoformat()
    
    cursor = conn.execute("""
        INSERT INTO resume_history 
        (company_name, job_title, job_description, generated_resume, 
         match_score, matched_skills, missing_skills, suggestions, created_at)
        VALUES (:company_name, :job_title, :job_description, :generated_resume,
                :match_score, :matched_skills, :missing_skills, :suggestions, :created_at)
    """, data)
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_all_history():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM resume_history ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    results = []
    for row in rows:
        item = dict(row)
        for field in ['matched_skills', 'missing_skills', 'suggestions']:
            try:
                item[field] = json.loads(item[field])
            except:
                item[field] = []
        results.append(item)
    return results

def get_history_by_id(record_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM resume_history WHERE id = ?", (record_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    for field in ['matched_skills', 'missing_skills', 'suggestions']:
        try:
            item[field] = json.loads(item[field])
        except:
            item[field] = []
    return item

def delete_history_by_id(record_id: int):
    conn = get_db()
    conn.execute("DELETE FROM resume_history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
