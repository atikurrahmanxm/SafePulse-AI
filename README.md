# CyberShield AI

**Smart Cybersecurity. Simple Protection. Safer Businesses.**  
*AdtU Innovation Mela 2026 — Assam down town University (AdtU), India*  
*Problem Statement: Small Business Cybersecurity Platform*

CyberShield AI is an AI-powered, bilingual (English & Bengali) cybersecurity SaaS platform built specifically for small businesses, local retail shops, pharmacies, clinics, startups, and SMEs. It combines an explainable machine-learning phishing detector, an SSRF-safe URL & DNS security analyzer, a CERT-In MSME aligned 10-domain business health assessment, a 6-phase interactive incident response center, employee cyber awareness training, and downloadable PDF reporting.

---

## Key Capabilities

1. **AI Phishing & Scam Detector** — TF-IDF (word + character n-grams) + Logistic Regression pipeline paired with transparent social-engineering rules, inline phrase highlighting, calibrated confidence, 0–100 risk bands, PDF reports, and live held-out evaluation metrics.
2. **SSRF-Safe Smart URL Security Analyzer** — Lexical & domain obfuscation checks, brand-impersonation detection, read-only DNS A/SPF/DMARC lookup (`dnspython`), strict blocking of `localhost`, private/loopback/metadata IP ranges, and explicit "HTTPS ≠ Safe" & "Unknown vs. Safe" notices. Never fetches or executes target URLs.
3. **Business Security Health Check** — Interactive 10-domain posture assessment aligned with CERT-In MSME guidance (Passwords, MFA, Email Security, Access Permissions, Software Updates, Backups, Data Protection, Device Security, Wi-Fi Security, Incident Readiness) with weighted scoring and PDF action plans.
4. **Cyber Incident Response Center** — Guided 6-phase interactive checklists across 7 SME incident scenarios (including phishing clicks, UPI/financial fraud with India Helpline 1930 guidance, BEC, and suspected ransomware).
5. **Employee Cyber Awareness** — Bilingual security micro-lessons, clearly labeled **Training Simulation** phishing examples, and interactive graded quizzes.
6. **Hackathon Demo Mode & Tenant Isolation** — Argon2 password hashing, JWT authentication, sliding-window rate limiting, audit logs, per-business data isolation, and a one-click clearly labeled Demo Workspace.

---

## Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 20+ & npm

### 1. Backend Setup (FastAPI + SQLite + Scikit-learn)

```bash
cd CyberShield-AI/backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- FastAPI automatically initializes the SQLite schema (`cybershield.db`), trains and evaluates the phishing ML model on startup (saving artifacts to `backend/artifacts/`), and seeds the awareness quizzes.
- Interactive Swagger API docs are available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup (React + TypeScript + Vite + Tailwind)

```bash
cd CyberShield-AI/frontend
cp .env.example .env
npm install
npm run dev
```

- Open `http://localhost:5173`. Vite proxies `/api/*` requests directly to `http://127.0.0.1:8000`.
- Click **"Launch Hackathon Demo Mode"** on the landing or login page to explore the pre-populated demo pharmacy workspace without registering.

---

## Running Automated Tests

### Backend Tests (`pytest`)
```bash
cd CyberShield-AI/backend
python -m pytest -v
```

### Frontend Tests (`vitest`) & Production Build
```bash
cd CyberShield-AI/frontend
npm run build
npm test
```

---

## Production Deployment Guide

### Database (PostgreSQL)
Set `DATABASE_URL` in your backend environment to a managed PostgreSQL connection string (e.g., `postgresql+psycopg://...` or `postgresql://...`). All 11 SQLAlchemy models are PostgreSQL-compatible.

### Backend (Render / Railway / Fly.io)
- Root directory: `CyberShield-AI/backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Required env vars: `ENVIRONMENT=production`, `DATABASE_URL`, `JWT_SECRET_KEY` (64+ random chars), `CORS_ORIGINS=https://your-frontend.vercel.app`
- Optional env vars: `GOOGLE_SAFE_BROWSING_API_KEY` (if omitted, the local engine runs with full functionality).

### Frontend (Vercel)
- Root directory: `CyberShield-AI/frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Env var: `VITE_API_BASE_URL=https://your-backend-service.onrender.com/api`
- `vercel.json` is included for SPA client-side routing rewrites.

---

## Documentation Index

- [Architecture Diagram & Overview](docs/ARCHITECTURE.md)
- [ML Model Evaluation Report](docs/ML_EVALUATION_REPORT.md)
- [REST API Documentation](docs/API_DOCUMENTATION.md)
- [Hackathon Live Demo Script](docs/HACKATHON_DEMO_SCRIPT.md)
- [Pitch Presentation Outline](docs/PRESENTATION_OUTLINE.md)
- [Future Product Roadmap](docs/ROADMAP.md)

