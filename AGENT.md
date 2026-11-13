# SafePulse AI — AI Agent & Developer Architecture Guide (AGENT.md)

> **Context**: This document serves as the primary system manual and operational directive for AI coding agents (such as Antigravity, Cursor, Claude Code, GitHub Copilot, and SWE agents) working on the SafePulse AI codebase. Read this file completely before planning or making any changes.

---

## 1. Project Overview & Philosophy

**SafePulse AI** (developed for the *AdtU Innovation Mela 2026*, Assam down town University, India) is an AI-powered, bilingual (**English & Bengali**) cybersecurity SaaS platform engineered specifically for non-technical small and medium-sized enterprises (SMEs), local retail stores, pharmacies, diagnostic clinics, and startups.

### Core Problems Addressed
1. **Rising Regional Attacks**: High prevalence of localized UPI PIN scams, fake bank KYC SMS, courier fee traps, GST penalty lures, and WhatsApp CEO/owner impersonation.
2. **Accessibility Barrier**: Enterprise tools (EDRs, SIEMs, SOC services) are cost-prohibitive, complex, and English-only.
3. **Actionability Gap**: Small businesses lack IT departments; they need plain-language explanations, actionable check-offs, and emergency guidance (such as India Cybercrime Helpline **1930** and `cybercrime.gov.in`).

### Key Design Tenets for AI Agents
- **Explainability Over Black-Box AI**: Never output a raw number without explaining *why*. All ML predictions must be paired with human-readable heuristic rules and exact inline phrase offsets.
- **SSRF-Safe & Zero-Target-Execution**: Never fetch or execute submitted URLs via HTTP/HTTPS. All external URL analysis must be strictly lexical, structural, and read-only DNS (SPF/DMARC/A). Internal and private IP addresses must be rejected before and after DNS resolution.
- **Strict Tenant & Workspace Isolation**: Every data query must be explicitly scoped by `business_id` linked to the authenticated user.
- **Bilingual Parity**: Any new user-facing prompt, questionnaire item, scenario guidance, or UI text must support both English (`en`) and Bengali (`bn`).
- **Responsible AI Claims**: SafePulse AI is a **triage and decision-support tool**, not a replacement for out-of-band human verification (e.g., calling a bank or supplier directly) or certified incident responders. Never claim 100% detection accuracy.

---

## 2. High-Level System Architecture

```mermaid
flowchart TD
    Client["Client Layer\nReact 18 + TypeScript + Vite + Tailwind CSS\n(Bilingual EN/BN, Recharts, Lucide Icons)"]
    
    API["API Gateway & Web Layer\nFastAPI (Uvicorn)\n- Argon2 Password Hashing\n- HS256 JWT Authentication\n- Sliding-Window Rate Limiting\n- Security Headers Middleware"]
    
    subgraph CoreEngines["SafePulse AI Core Engines"]
        MLEngine["AI Phishing Engine\n- TF-IDF (Word + Char-wb N-grams)\n- Logistic Regression (Balanced)\n- Explainable Heuristic Rules\n- Phrase Highlighter"]
        
        URLEngine["SSRF-Safe URL Scanner\n- Strict IP/Scheme Whitelist\n- Posix/Hex/Octal IP Sanitizer\n- Read-Only DNS A/SPF/DMARC\n- Brand Impersonation Rules"]
        
        HealthEngine["Business Posture Engine\n- 10 CERT-In MSME Domains\n- Weighted Scoring (0-100)\n- Gap & Weak Area Analytics"]
        
        IncidentEngine["Incident Response Engine\n- 7 SME Playbook Scenarios\n- 6-Phase Interactive Checklists\n- Timeline & Evidence Notes"]
        
        AwarenessEngine["Cyber Awareness Engine\n- Micro-Lessons\n- Labeled Simulations\n- Interactive Graded Quizzes"]
        
        PDFEngine["ReportLab Generator\n- Phishing/URL Analysis PDF\n- Assessment Action Plan PDF\n- Incident Triage Checklist PDF\n- Monthly Governance PDF"]
    end
    
    DB[("Relational Database\nSQLAlchemy 2.0 ORM\n- SQLite (Local Dev: safepulse.db)\n- PostgreSQL (Production Ready)")]
    
    DNSResolver["Public DNS Resolver\n(dnspython TXT/A queries only)"]

    Client -->|"/api/* JSON + JWT + X-Business-Id"| API
    API --> CoreEngines
    URLEngine -.->|"Safe Read-Only DNS\n(Never connects via HTTP)"| DNSResolver
    CoreEngines --> DB
```

---

## 3. Technology Stack Matrix

| Component | Technology | Version | Purpose / Responsibilities |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | Python / FastAPI | `Python 3.10+`, `fastapi 0.143.0` | Async REST API, OpenAPI generation, lifespan orchestration |
| **Server** | Uvicorn | `0.52.4` | ASGI application server |
| **ORM & Database** | SQLAlchemy | `2.0.44` | SQLite (dev) / PostgreSQL (prod) compatible schema |
| **Validation** | Pydantic v2 | `2.11.5` | Request and response schema serialization & validation |
| **Cryptography** | `argon2-cffi` | `25.1.0` | High-memory Argon2id password hashing |
| **Authentication** | `PyJWT` | `2.10.1` | HS256 signed stateless JWT session tokens |
| **Machine Learning** | `scikit-learn`, `joblib` | `sklearn 1.7.2`, `joblib 1.6.0` | FeatureUnion TF-IDF vectorizer + LogisticRegression model |
| **Data Processing** | `pandas`, `numpy` | `pandas 2.3.3`, `numpy 2.2.6` | Dataset curation, feature extraction, evaluation metrics |
| **Network & DNS** | `dnspython`, `httpx` | `dnspython 2.7.0`, `httpx 0.28.1` | SSRF-safe DNS lookups, external threat intelligence (optional) |
| **PDF Generation** | `reportlab` | `4.4.1` | Dynamic multi-page branded PDF reports |
| **Frontend Framework** | React + TypeScript | `React 18.3.1`, `TS 5.7.2` | Single Page Application (SPA) architecture |
| **Build Tool** | Vite | `6.0.5` | Fast HMR dev server & optimized Rollup production builds |
| **Styling** | Tailwind CSS | `3.4.17` | Utility-first responsive design, dark slate theme |
| **Routing** | React Router DOM | `6.28.1` | Client-side routing with lazy loading & protected route guard |
| **Charts** | Recharts | `2.15.0` | Posture score gauges, threat distributions, score trends |
| **Icons** | Lucide React | `0.469.0` | Consistent, accessible iconography |

---

## 4. Repository Structure

```
SafePulse-AI/
├── .env.example                     # Root reference environment variables
├── .gitignore                       # Git ignore rules for Python, Node, DB, artifacts
├── AGENT.md                         # This file (AI agent operational instructions)
├── README.md                        # Primary developer & user documentation
├── start_safepulse.bat              # One-click Windows dev launcher (Backend + Frontend)
├── docs/                            # Comprehensive engineering and demo documentation
│   ├── API_DOCUMENTATION.md         # Full REST API endpoint specifications
│   ├── ARCHITECTURE.md              # Architectural overview and security boundaries
│   ├── HACKATHON_DEMO_SCRIPT.md     # 4-5 minute live hackathon pitch guide
│   ├── ML_EVALUATION_REPORT.md      # Held-out dataset metrics, ROC-AUC, confusion matrix
│   ├── PRESENTATION_OUTLINE.md      # Pitch deck slide structure
│   └── ROADMAP.md                   # Completed MVP & future engineering milestones
├── backend/
│   ├── .env.example                 # Backend environment variable template
│   ├── render.yaml                  # Render cloud deployment blueprint
│   ├── requirements.txt             # Python dependency manifest
│   ├── artifacts/                   # Persisted ML model weights and metrics
│   │   ├── phishing_model.joblib    # Trained FeatureUnion + Logistic Regression pipeline
│   │   └── phishing_metrics.json    # Pre-calculated held-out evaluation & CV metrics
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                # Settings dataclass loading env variables
│   │   ├── database.py              # Engine, SessionLocal, Base, schema migration helper
│   │   ├── main.py                  # FastAPI app factory, lifespan, CORS, security headers
│   │   ├── models.py                # 15 SQLAlchemy ORM models across 11 core tables
│   │   ├── schemas.py               # Pydantic request/response models
│   │   ├── security.py              # Argon2, JWT, sliding window rate limiter, auth dependencies
│   │   ├── ml/                      # Machine learning subsystem
│   │   │   ├── __init__.py
│   │   │   ├── dataset.py           # 128 curated SME-specific labeled message corpus
│   │   │   ├── trainer.py           # Pipeline training, 5-fold CV, metrics evaluation
│   │   │   └── predictor.py         # Heuristic rules, offset calculation, inference engine
│   │   ├── services/                # Business logic engines
│   │   │   ├── __init__.py
│   │   │   ├── assessment_engine.py # 10 CERT-In MSME domain assessment logic & scoring
│   │   │   ├── awareness_engine.py  # Lessons, labeled simulations, 3 quiz definitions
│   │   │   ├── demo_seeder.py       # Seeds demo pharmacy workspace and sample data
│   │   │   ├── governance_engine.py # Subscriptions, default controls, integration catalog
│   │   │   ├── incident_engine.py   # 7 incident scenarios, 6-phase checklists, recovery steps
│   │   │   ├── pdf_report.py        # ReportLab PDF report generation
│   │   │   └── url_analyzer.py      # SSRF validation, lexical parsing, DNS SPF/DMARC
│   │   └── routers/                 # API endpoint route handlers
│   │       ├── __init__.py
│   │       ├── assessment.py        # /api/assessments/*
│   │       ├── auth.py              # /api/auth/*
│   │       ├── awareness.py         # /api/awareness/*
│   │       ├── dashboard.py         # /api/dashboard/*
│   │       ├── governance.py        # /api/governance/*
│   │       ├── history.py           # /api/history/*
│   │       ├── incidents.py         # /api/incidents/*
│   │       ├── phishing.py          # /api/phishing/*
│   │       └── url_scanner.py       # /api/urls/*
│   └── tests/                       # Pytest test suite
│       ├── conftest.py              # Test database fixtures, isolated client, auth helper
│       ├── test_assessment.py       # Assessment scoring & recommendation tests
│       ├── test_auth_security.py    # Auth, registration, rate limiting, audit log tests
│       ├── test_dashboard_history.py# Dashboard aggregation & history tests
│       ├── test_governance_and_upgrades.py # Governance, controls, team member tests
│       ├── test_incidents_awareness.py # Incident playbooks & awareness quiz tests
│       ├── test_phishing_ml.py      # ML inference, heuristic triggers, evaluation tests
│       └── test_url_ssrf.py         # SSRF protection, DNS SPF/DMARC, URL scanning tests
└── frontend/
    ├── .env.example                 # Frontend environment variable template
    ├── index.html                   # HTML entry point with metadata
    ├── package.json                 # Node dependencies and scripts
    ├── postcss.config.js            # PostCSS configuration
    ├── tailwind.config.js           # Tailwind CSS configuration with custom palette
    ├── tsconfig.json                # TypeScript project configuration
    ├── vercel.json                  # SPA rewrite rules for Vercel deployment
    ├── vite.config.ts               # Vite configuration with chunk splitting & proxy
    ├── public/
    │   └── safepulse-logo.svg       # Brand vector logo
    └── src/
        ├── App.tsx                  # Root routing, lazy page loading, protected routes
        ├── index.css                # Tailwind directives and base theme styling
        ├── main.tsx                 # React DOM mount point
        ├── vite-env.d.ts            # Vite client type declarations
        ├── components/
        │   ├── layout/
        │   │   ├── AppShell.tsx     # Sidebar, topbar, demo indicator, navigation
        │   │   └── Logo.tsx         # Reusable SafePulse brand icon & text
        │   └── ui/
        │       ├── Primitives.tsx   # Card, Button, Input, Select, Badge, Skeleton, Alert
        │       └── ProgressRing.tsx # Reusable animated SVG radial progress ring
        ├── context/
        │   └── AuthContext.tsx      # Auth state, login/demo session, multi-business switcher
        ├── i18n/
        │   ├── LanguageContext.tsx  # Bilingual state hook (`useLanguage`)
        │   └── translations.ts      # English & Bengali comprehensive translation dictionary
        ├── lib/
        │   ├── api.ts               # Authenticated fetch wrapper, error handling, PDF downloader
        │   └── utils.ts             # Tailwind class merger (`cn`), date & risk formatting helpers
        ├── pages/
        │   ├── AssessmentPage.tsx   # 10-domain CERT-In assessment questionnaire & results
        │   ├── AuthPage.tsx         # Login, Registration, and Demo mode launch
        │   ├── AwarenessPage.tsx    # Cyber training lessons, simulations, interactive quizzes
        │   ├── DocsPage.tsx         # Built-in help docs, emergency contacts (Helpline 1930)
        │   ├── GovernancePage.tsx   # Team MFA tracking, offline backup checklist, roadmap
        │   ├── HistoryPage.tsx      # Unified scan timeline and security audit logs
        │   ├── IncidentsPage.tsx    # 7 incident scenarios, 6-phase interactive triage playbooks
        │   ├── LandingPage.tsx      # Public landing page with bilingual hero & feature cards
        │   ├── OverviewPage.tsx     # Main dashboard with aggregated scores and metrics
        │   ├── PhishingDetectorPage.tsx # AI phishing analysis, phrase highlighting, ML metrics tab
        │   ├── ReportsPage.tsx      # Central hub for downloading PDF reports
        │   ├── SettingsPage.tsx     # Business profile update, language preference, workspace create
        │   └── UrlScannerPage.tsx   # SSRF-safe URL inspector & DNS reputation analyzer
        └── test/
            ├── App.test.tsx         # Frontend integration tests
            └── setup.ts             # Test environment polyfills (matchMedia, ResizeObserver)
```

---

## 5. Core Modules & Technical Implementation

### Module 1: AI Phishing & Scam Detector (`app/ml/`, `app/routers/phishing.py`)
- **Pipeline Architecture**:
  - `FeatureUnion` combining:
    1. **Word TF-IDF**: `ngram_range=(1, 2)`, max 4,500 features.
    2. **Character-wb TF-IDF**: `ngram_range=(3, 5)`, max 4,500 features (captures typo-squatting, disguised TLDs, and punctuation tricks).
  - Classification: `LogisticRegression(C=2.0, max_iter=1000, class_weight="balanced")`.
- **Explainability & Heuristic Rules**:
  - 7 transparent heuristic patterns (`urgency_pressure`, `credential_or_otp_request`, `suspicious_payment_or_upi_scam`, `impersonation_authority`, `remote_access_or_malware`, `suspicious_link_or_shortener`, `secrecy_or_bypass`).
  - **Benign Dampening Pattern**: Reduces false positives when genuine protective notices appear (e.g., *"Never share your OTP with anyone"*).
  - Exact regex character spans (`[start, end]`) returned for inline UI highlighting.
- **Risk Score Mapping (0–100)**:
  - `0–24`: **Low Risk** (Normal business communications).
  - `25–49`: **Moderate Risk** (Unusual phrasing or unverified external links).
  - `50–74`: **High Risk** (Pressure tactics or payment redirection).
  - `75–100`: **Critical Risk** (Credential/OTP requests, fake KYC, remote-access malware lures).
- **Evaluation Transparency**:
  - The API exposes real held-out test set metrics (`/api/phishing/model-evaluation`): 87.5% Accuracy, 92.9% Precision, 81.3% Recall, 86.7% F1-score, and 0.953 ROC-AUC on a 32-sample held-out split with 5-fold cross-validation.

### Module 2: SSRF-Safe Smart URL Security Scanner (`app/services/url_analyzer.py`)
- **Strict SSRF Prevention Invariants**:
  1. Schemes strictly restricted to `http` or `https`. Rejects `file://`, `ftp://`, `gopher://`, etc.
  2. Immediate string inspection blocks `localhost`, `localhost.localdomain`, `ip6-localhost`, `metadata.google.internal`, and private suffixes (`.local`, `.internal`, `.localhost`, `.lan`, `.home`, `.arpa`).
  3. Pre-resolution parsing blocks IPv4 and IPv6 loopbacks, link-local (`169.254.0.0/16`), private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), multicast, and reserved IPs.
  4. Decodes obfuscated IP representations (e.g., POSIX octal `0177.0.0.1`, hex `0x7f.0.0.1`, single 32-bit integers, and IPv6-mapped IPv4 `::ffff:127.0.0.1`).
  5. Post-resolution check: Resolves DNS A records and validates resolved IPs against forbidden IP ranges before proceeding.
  6. **Zero Target HTTP Connections**: Never performs HTTP GET/POST or downloads assets from the target domain.
- **DNS & Reputation Checks**:
  - Queries public DNS for A records.
  - Queries domain TXT records for SPF (`v=spf1`).
  - Queries `_dmarc.<domain>` for DMARC policy (`v=DMARC1`).
  - Highlights brand impersonation (e.g., `sbi`, `hdfc`, `gst`, `incometax` keywords within non-official domains).
  - Explicit user notices: **"HTTPS ≠ Safe"** and **"Unknown ≠ Safe"**.

### Module 3: Business Security Health Check (`app/services/assessment_engine.py`)
- Aligned directly with **CERT-In Cyber Security Guidelines for MSMEs**:
  1. **Password Security** (Weight 10)
  2. **Multi-Factor Authentication** (Weight 14)
  3. **Email Security** (Weight 10)
  4. **Employee Access Permissions** (Weight 10)
  5. **Software Updates** (Weight 10)
  6. **Data Backup** (Weight 12)
  7. **Data Protection & Encryption** (Weight 10)
  8. **Device & Endpoint Security** (Weight 8)
  9. **Wi-Fi & Network Security** (Weight 8)
  10. **Incident Readiness & Reporting** (Weight 8)
- Scoring: Answers are scored as `yes` (100%), `partial` (50%), or `no` (0%), multiplied by question weight, normalized to a 0–100 score.
- Output identifies overall score, category band, weak areas, critical gaps, and prioritized bilingual remediation actions.

### Module 4: Cyber Incident Response Center (`app/services/incident_engine.py`)
- 7 Tailored SME Scenarios:
  1. `suspicious_email`: Suspicious Email Received
  2. `phishing_link_clicked`: Phishing Link Clicked / Credentials Entered
  3. `bec_compromised`: Business Email Compromise / Account Takeover
  4. `social_media_compromised`: Social Media / WhatsApp Business Compromise
  5. `suspicious_transaction`: Suspicious Transaction / UPI Scam
  6. `ransomware_suspected`: Suspected Ransomware / File Lock
  7. `sensitive_data_exposure`: Lost Device / Data Exposure
- 6 Interactive Lifecycle Phases per scenario:
  1. *Immediate Actions* (first 15 minutes)
  2. *Containment Steps* (isolate device, freeze netbanking/UPI)
  3. *Account Protection* (revoke sessions, rotate credentials, enable MFA)
  4. *Evidence Preservation* (preserve headers, transaction IDs, screenshots)
  5. *Recovery Guidance* (clean reinstall, restore from offline backup)
  6. *Reporting Recommendations* (National Cyber Crime Portal `cybercrime.gov.in`, Helpline **1930**, bank ombudsman)
- Tracks completion status dynamically and allows owners to append dated timeline notes.

### Module 5: Employee Cyber Awareness (`app/services/awareness_engine.py`)
- 4 Core Micro-Lessons (Phishing recognition, password/MFA hygiene, safe browsing & APK risks, boss impersonation).
- Clearly labeled **"TRAINING SIMULATION — SAFE EDUCATIONAL EXAMPLE"** phishing cards to train staff on red flags without deceptive simulation tricks.
- 3 Interactive Quizzes (`phishing-defense-essentials`, `password-mfa-essentials`, `safe-payments-devices`) with instant bilingual feedback, scoring, and explanation.

### Module 6: Governance, Team & Multi-Tenant Isolation (`app/services/governance_engine.py`, `app/security.py`)
- **Tenant Hierarchy**: `User` -> `Business` -> Child Entities (`PhishingAnalysis`, `URLScan`, `SecurityAssessment`, `Incident`, `BusinessMember`, `BusinessControl`, `AuditLog`).
- Support for multiple workspaces per user with header switching via `X-Business-Id`.
- Self-attested staff MFA adoption tracker and offline backup monitoring.
- Enterprise subscription tier modeling (`free`, `pro_sme`, `enterprise_ready`) with monthly scan quota enforcement.

---

## 6. Database Schema & Models Reference

All 15 models reside in `backend/app/models.py`:

```
User (users)
 ├── id, email, full_name, password_hash, role, preferred_language, is_demo, created_at, updated_at
 └── 1:N -> Business (owner)
 └── 1:N -> QuizResult

Business (businesses)
 ├── id, owner_id (FK -> users.id), name, industry, employee_count, city, primary_email_domain,
 │   is_demo_workspace, subscription_tier, monthly_scan_quota, created_at, updated_at
 ├── 1:N -> PhishingAnalysis (phishing_analyses)
 ├── 1:N -> URLScan (url_scans)
 ├── 1:N -> SecurityAssessment (security_assessments)
 │            └── 1:N -> AssessmentAnswer (assessment_answers)
 ├── 1:N -> Incident (incidents)
 │            ├── 1:N -> IncidentChecklistItem (incident_checklist_items)
 │            └── 1:N -> IncidentNote (incident_notes)
 ├── 1:N -> BusinessMember (business_members)
 ├── 1:N -> BusinessControl (business_controls)
 └── 1:N -> IntegrationConfig (integration_configs)

AwarenessQuiz (awareness_quizzes)
 ├── id, slug, title, topic, difficulty, questions_count, created_at
 └── 1:N -> QuizResult (quiz_results)

AuditLog (audit_logs)
 └── id, user_id, business_id, action, resource_type, resource_id, summary, ip_address, created_at
```

*Note on Database Migrations*: In development, SQLite creates tables automatically via `Base.metadata.create_all(bind=engine)` and `ensure_schema_extensions(engine)`. In PostgreSQL, foreign keys and indexes (`ix_phishing_business_created`, `ix_url_business_created`, etc.) are created natively.

---

## 7. Developer & Operational Commands

### Prerequisites
- Python 3.10+ (tested with Python 3.12)
- Node.js 20+ and npm

### Local Environment Setup

#### 1. Backend Setup
```bash
cd backend
# Create virtual environment (recommended)
python -m venv .venv
# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1
# Or Windows CMD: .venv\Scripts\activate.bat
# Or Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env

# Run FastAPI server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

#### 2. Frontend Setup
```bash
cd frontend
# Create .env from template
cp .env.example .env

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
- Frontend application URL: `http://localhost:5173`
- Dev server automatically proxies `/api/*` requests to `http://127.0.0.1:8000`.

#### 3. One-Click Windows Dev Launcher
From the repository root, run:
```bat
start_safepulse.bat
```
This script launches two separate terminal windows for the backend (port 8000) and frontend (port 5173).

---

## 8. Automated Testing & Verification

### Running Backend Unit & Integration Tests
Backend tests use `pytest` with an in-memory or temporary isolated SQLite database.
```bash
cd backend
python -m pytest -v
```

**Test Coverage Summary**:
- `test_phishing_ml.py`: ML pipeline inference, regex heuristic triggers, risk category calculation, model evaluation output.
- `test_url_ssrf.py`: Strict rejection of `localhost`, IPv4/IPv6 private ranges, POSIX octal/hex IPs, DNS SPF/DMARC analysis.
- `test_assessment.py`: 10-domain CERT-In assessment scoring, weak area detection, PDF action plan generation.
- `test_auth_security.py`: Argon2 password hashing, JWT expiration, sliding-window rate limiter, audit log generation.
- `test_incidents_awareness.py`: 7 incident playbooks, checklist toggle progress, quiz grading and results.
- `test_governance_and_upgrades.py`: Team member management, control status toggling, subscription usage limits.
- `test_dashboard_history.py`: Dashboard metric aggregation and unified audit trail deletion.

### Running Frontend Tests & Production Build
```bash
cd frontend
# Run vitest test suite
npm test

# Verify production TypeScript compilation & build
npm run build
```

---

## 9. Security & Coding Rules for AI Agents

When authoring or modifying code in this repository, strictly adhere to the following rules:

### 1. SSRF & Network Security Invariants
- **NEVER** use `requests.get()`, `httpx.get()`, `urllib.request`, or any HTTP client to connect to a user-submitted URL in `url_analyzer.py`.
- **NEVER** weaken `_is_forbidden_ip()` or allow bypassing of loopback, private, or link-local checks.
- If adding external threat API integrations (e.g., Google Safe Browsing), connect **ONLY** to the official vendor API endpoint using the configured API key; never connect to the target domain directly.

### 2. Multi-Tenant Data Isolation Invariants
- **NEVER** query `PhishingAnalysis`, `URLScan`, `SecurityAssessment`, `Incident`, `BusinessMember`, or `AuditLog` without filtering by `business_id == business.id`.
- Always use the `get_current_business` dependency in route handlers that touch tenant data:
  ```python
  @router.get("/my-endpoint")
  def my_endpoint(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
      user, business = ctx
      # Queries MUST be filtered by business.id
  ```

### 3. Bilingual Parity Requirement
- SafePulse AI is deployed for local shop owners in Assam and Bengal. All user-facing copy must have translations.
- In backend engines: Provide `_en` and `_bn` fields for prompts, descriptions, and recommendations.
- In frontend: Update both `translations.en` and `translations.bn` in `frontend/src/i18n/translations.ts`.

### 4. Machine Learning Modification Workflow
- Training data is stored in `backend/app/ml/dataset.py`.
- If you add or modify training samples in `dataset.py`, you **MUST** retrain and update the artifacts:
  ```bash
  cd backend
  python -c "from app.ml.trainer import train_and_persist_model; train_and_persist_model()"
  ```
- Verify that `backend/artifacts/phishing_model.joblib` and `backend/artifacts/phishing_metrics.json` are regenerated, and run `pytest tests/test_phishing_ml.py`.

### 5. Responsible AI & Threat Triage Integrity
- Do not claim automatic remediation or removal of malware; SafePulse AI guides humans through containment and recovery.
- Always include emergency contact guidance (**Helpline 1930** and `cybercrime.gov.in`) for financial and serious cyber fraud incidents.
- Preserve the Demo Workspace (`is_demo_workspace = True`, `demo@safepulseai.org`) so evaluators can test the system without registration.

---

## 10. Production Deployment Configuration

### Backend Deployment (Render, Railway, Fly.io, or AWS EC2)
- **Directory**: `backend/`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Mandatory Environment Variables**:
  ```ini
  APP_NAME=SafePulse AI
  ENVIRONMENT=production
  DATABASE_URL=postgresql+psycopg://username:password@hostname:5432/safepulsedb
  JWT_SECRET_KEY=<64+ random hex characters>
  JWT_ALGORITHM=HS256
  JWT_EXPIRE_MINUTES=720
  CORS_ORIGINS=https://safepulse.yourdomain.com
  RATE_LIMIT_PER_MINUTE=90
  ```

### Frontend Deployment (Vercel, Netlify, or Cloudflare Pages)
- **Directory**: `frontend/`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Mandatory Environment Variables**:
  ```ini
  VITE_API_BASE_URL=https://api.yourdomain.com/api
  ```
- **SPA Rewrites**: `frontend/vercel.json` contains `{ "rewrites": [{ "source": "/(.*)", "destination": "/" }] }` to support client-side routing on hard refreshes.

---

## 11. Quick Reference: API Endpoints

| Category | Endpoint | Method | Description |
| :--- | :--- | :---: | :--- |
| **System** | `/api/health` | GET | System status and active environment |
| **Auth** | `/api/auth/register` | POST | Register owner account + business profile |
| | `/api/auth/login` | POST | Sign in with email and password |
| | `/api/auth/demo` | POST | Launch isolated pre-populated Demo Workspace |
| | `/api/auth/me` | GET | Current user profile, business, and workspaces |
| | `/api/auth/business` | PUT | Update business metadata & language |
| **Dashboard** | `/api/dashboard/overview` | GET | Real-time aggregated business posture metrics |
| **Phishing** | `/api/phishing/analyze` | POST | Analyze message with ML + heuristics |
| | `/api/phishing/samples` | GET | Retrieve sample demo messages |
| | `/api/phishing/model-evaluation` | GET | Return held-out test metrics & confusion matrix |
| | `/api/phishing/{id}/report.pdf` | GET | Download phishing analysis PDF report |
| **URL Scanner** | `/api/urls/scan` | POST | SSRF-safe lexical & DNS SPF/DMARC scanner |
| | `/api/urls/samples` | GET | Retrieve sample demo URLs |
| | `/api/urls/{id}/report.pdf` | GET | Download URL inspection PDF report |
| **Assessment** | `/api/assessments/questions` | GET | Retrieve 10 CERT-In MSME domain questions |
| | `/api/assessments/submit` | POST | Submit answers, calculate score, persist assessment |
| | `/api/assessments/latest` | GET | Fetch most recent assessment |
| | `/api/assessments/{id}/report.pdf`| GET | Download business posture action plan PDF |
| **Incidents** | `/api/incidents/scenarios` | GET | List 7 supported incident scenarios |
| | `/api/incidents` | GET/POST | List active incidents or open new playbook |
| | `/api/incidents/{id}/items/{item_id}` | PATCH | Toggle checklist step completion |
| | `/api/incidents/{id}/notes` | POST | Add timestamped evidence note |
| | `/api/incidents/{id}/report.pdf` | GET | Download incident triage checklist PDF |
| **Awareness** | `/api/awareness/overview` | GET | Micro-lessons, simulations, and quiz list |
| | `/api/awareness/quizzes/{slug}/submit` | POST | Grade quiz submission and persist score |
| **Governance** | `/api/governance/overview` | GET | Team MFA, offline backups, roadmap controls |
| | `/api/governance/controls/{id}` | PATCH | Update self-attested control status |
| | `/api/governance/members` | POST | Add team member for MFA tracking |
| | `/api/governance/monthly-report.pdf` | GET | Download executive monthly security PDF |
| **History** | `/api/history/unified` | GET | Unified chronological timeline of events |
| | `/api/history/audit-logs` | GET | Audit log trail for current business |
| | `/api/history/{type}/{id}` | DELETE | Scoped deletion of a business record |

---

*SafePulse AI Architecture & Agent Directive — AdtU Innovation Mela 2026*

