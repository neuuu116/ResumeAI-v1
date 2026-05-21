
# ResumeAI v1

An AI-powered resume generation system that matches your profile to a job description and generates an ATS-optimized resume with a match score.

## Features

- User profile management (skills, experience, education, projects)
- Paste any Job Description → AI analyzes and matches your profile
- Generates tailored resume content via Claude/Groq LLM API
- ATS match score with missing skills breakdown
- Resume history tracking per user
- REST API backend with 6 endpoints

## Tech Stack

- **Backend:** FastAPI, Python
- **Database:** SQLite (via SQLAlchemy)
- **AI:** Anthropic Claude API / Groq (llama-3.3-70b-versatile)
- **Frontend:** HTML, CSS, JavaScript (4 pages)
- **Deployment:** Render (backend) + Netlify (frontend)

## Project Structure

```
ResumeAI-v1/
├── backend-api/
│   ├── main.py          # 6 REST endpoints
│   ├── database.py      # SQLite setup, user_profile + resume_history tables
│   ├── models.py        # Pydantic models
│   └── ai_engine.py     # LLM integration + resume generation logic
├── frontend-demo/
│   ├── index.html       # Dashboard
│   ├── profile.html     # Profile management
│   ├── generate.html    # JD input + resume generation (split-panel + score circle)
│   └── history.html     # Resume history
└── README.md
```

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/neuuu116/ResumeAI-v1.git
cd ResumeAI-v1
```

### 2. Setup virtual environment
```bash
cd backend-api
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
```bash
# Create a .env file in backend-api/
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/profile` | Save user profile |
| GET | `/profile/{user_id}` | Get user profile |
| POST | `/generate` | Generate resume from JD |
| GET | `/history/{user_id}` | Get resume history |
| GET | `/score/{resume_id}` | Get ATS match score |
| DELETE | `/history/{resume_id}` | Delete resume entry |

## Live Demo

- Backend: [Render deployment](https://resumeai-backend.onrender.com)
- Frontend: [Netlify deployment](https://resumeai-v1.netlify.app)

---

## What's coming in ResumeAI v2

v2 is a complete rebuild focused on real-world usability:

- **PDF upload** → Claude auto-extracts your profile (no manual form filling)
- **JD matching** → Structured JSON generation (name, summary, skills, experience, projects, education)
- **Harvard/Jake's format** → 1-page PDF output via WeasyPrint
- **Missing skills flagging** → Shows exactly what you lack for a role
- **ATS scoring** → Quantified match percentage
- **PostgreSQL + JWT auth** → Multi-user persistent profiles
- **AWS EC2 deployment**

> v2 execution begins post June 2026. Follow this repo for updates.

---

## Author

**Neha Mhatre** — [LinkedIn](https://www.linkedin.com/in/neha-mhatre-693055336) | [GitHub](https://github.com/neuuu116)
EOF
Output
# ResumeAI v1

An AI-powered resume generation system that matches your profile to a job description and generates an ATS-optimized resume with a match score.

## Features

- User profile management (skills, experience, education, projects)
- Paste any Job Description → AI analyzes and matches your profile
- Generates tailored resume content via Claude/Groq LLM API
- ATS match score with missing skills breakdown
- Resume history tracking per user
- REST API backend with 6 endpoints

## Tech Stack

- **Backend:** FastAPI, Python
- **Database:** SQLite (via SQLAlchemy)
- **AI:** Anthropic Claude API / Groq (llama-3.3-70b-versatile)
- **Frontend:** HTML, CSS, JavaScript (4 pages)
- **Deployment:** Render (backend) + Netlify (frontend)

## Project Structure

```
ResumeAI-v1/
├── backend-api/
│   ├── main.py          # 6 REST endpoints
│   ├── database.py      # SQLite setup, user_profile + resume_history tables
│   ├── models.py        # Pydantic models
│   └── ai_engine.py     # LLM integration + resume generation logic
├── frontend-demo/
│   ├── index.html       # Dashboard
│   ├── profile.html     # Profile management
│   ├── generate.html    # JD input + resume generation (split-panel + score circle)
│   └── history.html     # Resume history
└── README.md
```

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/neuuu116/ResumeAI-v1.git
cd ResumeAI-v1
```

### 2. Setup virtual environment
```bash
cd backend-api
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
```bash
# Create a .env file in backend-api/
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/profile` | Save user profile |
| GET | `/profile/{user_id}` | Get user profile |
| POST | `/generate` | Generate resume from JD |
| GET | `/history/{user_id}` | Get resume history |
| GET | `/score/{resume_id}` | Get ATS match score |
| DELETE | `/history/{resume_id}` | Delete resume entry |

## Live Demo

- Backend: [Render deployment](https://resumeai-backend.onrender.com)
- Frontend: [Netlify deployment](https://resumeai-v1.netlify.app)

---

## What's coming in ResumeAI v2

v2 is a complete rebuild focused on real-world usability:

- **PDF upload** → Claude auto-extracts your profile (no manual form filling)
- **JD matching** → Structured JSON generation (name, summary, skills, experience, projects, education)
- **Harvard/Jake's format** → 1-page PDF output via WeasyPrint
- **Missing skills flagging** → Shows exactly what you lack for a role
- **ATS scoring** → Quantified match percentage
- **PostgreSQL + JWT auth** → Multi-user persistent profiles
- **AWS EC2 deployment**

> v2 execution begins post June 2026. Follow this repo for updates.

---

## Author

**Neha Mhatre** — [LinkedIn](https://www.linkedin.com/in/neha-mhatre-693055336) | [GitHub](https://github.com/neuuu116)
