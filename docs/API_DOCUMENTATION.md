# CyberShield AI — REST API Documentation

Base URL (local dev): `http://127.0.0.1:8000`  
Interactive OpenAPI / Swagger UI: `http://127.0.0.1:8000/docs`

All endpoints except `/api/health`, `/api/auth/register`, `/api/auth/login`, and `/api/auth/demo` require `Authorization: Bearer <token>`.

## Authentication & Business Profile
- `POST /api/auth/register` — Register owner account + business profile (Argon2 hashed password, returns JWT).
- `POST /api/auth/login` — Authenticate with email + password (rate-limited).
- `POST /api/auth/demo` — Launch isolated, clearly labeled Hackathon Demo Mode workspace.
- `POST /api/auth/logout` — Record logout in audit log.
- `GET /api/auth/me` — Get current authenticated user and business profile.
- `PUT /api/auth/business` — Update business metadata & default language (`en` | `bn`).

## Dashboard
- `GET /api/dashboard/overview?language=en|bn` — Aggregated DB metrics: Business Security Score, Total Threat Analyses, High-Risk Findings, Completed Assessments, Score Trend, Risk Distribution, Recent Phishing & URL Scans, Recommendations, Incident Activity.

## Module 1: AI Phishing & Scam Detector
- `GET /api/phishing/samples` — List sample demo messages.
- `GET /api/phishing/model-evaluation` — Return held-out test metrics (Precision, Recall, F1, ROC-AUC, Confusion Matrix, 5-fold CV, dataset description, limitations).
- `POST /api/phishing/analyze` — Analyze message (`message`, `channel`, `sender_hint`, `language`), persist result, return risk score (0–100), risk category, ML probability, calibrated confidence, highlighted phrase offsets, reasons, recommendations.
- `GET /api/phishing/history` — List recent phishing analyses for current business.
- `GET /api/phishing/{analysis_id}/report.pdf` — Download ReportLab PDF report.

## Module 2: Smart URL Security Scanner
- `GET /api/urls/samples` — List sample demo URLs.
- `POST /api/urls/scan` — SSRF-safe lexical + DNS (A, SPF, DMARC) URL analysis. Returns HTTP 400 if localhost, private/loopback/link-local IP, or non-HTTP scheme is submitted.
- `GET /api/urls/history` — List recent URL scans for current business.
- `GET /api/urls/{scan_id}/report.pdf` — Download ReportLab PDF report.

## Module 3: Business Security Health Check
- `GET /api/assessments/questions?language=en|bn` — Return 10 CERT-In MSME aligned security questions.
- `POST /api/assessments/submit` — Score answers (`yes` | `partial` | `no`), compute weighted 0–100 score, weak areas, critical gaps, prioritized recommendations, and persist.
- `GET /api/assessments/latest` — Retrieve most recent business assessment.
- `GET /api/assessments/history` — List past assessments.
- `GET /api/assessments/{assessment_id}/report.pdf` — Download ReportLab PDF report.

## Module 4: Cyber Incident Response Center
- `GET /api/incidents/scenarios?language=en|bn` — List 7 supported SME incident scenarios.
- `GET /api/incidents` — List business incidents with progress metrics.
- `POST /api/incidents` — Open an incident playbook and generate 6-phase checklist items.
- `GET /api/incidents/{incident_id}` — Get incident detail and checklist items.
- `PATCH /api/incidents/{incident_id}/items/{item_id}` — Toggle checklist completion (`is_completed`), automatically updating progress and incident status (`in_progress` / `resolved`).
- `GET /api/incidents/{incident_id}/report.pdf` — Download ReportLab PDF checklist.

## Module 5: Employee Cyber Awareness
- `GET /api/awareness/overview?language=en|bn` — Return lessons, clearly labeled training simulations, quizzes, and user progress.
- `POST /api/awareness/quizzes/{slug}/submit?language=en|bn` — Grade quiz answers and persist score.

## History & Audit Logs
- `GET /api/history/unified` — Combined timeline of phishing scans, URL scans, assessments, and incidents.
- `GET /api/history/audit-logs` — Security audit log entries for current business.
- `DELETE /api/history/{record_type}/{record_id}` — Delete a scoped business record.

