# Project Report: SafePulse AI
### Smart Cybersecurity. Simple Protection. Safer Businesses.
**Event**: AdtU Innovation Mela 2026 (14th November 2026)  
**Venue**: Jironee, C Block, Assam down town University (AdtU), Guwahati, India  
**Problem Statement**: Small Business Cybersecurity Platform  
**GitHub Repository**: [https://github.com/atikurrahmanxm/SafePulse-AI](https://github.com/atikurrahmanxm/SafePulse-AI)

---

## 1. Team Profile (Team VenoX)

| Role | Name | Enrollment Number | Department |
| :--- | :--- | :--- | :--- |
| **Team Leader** | **MD SAMIUR RAHMAN TANIM** | ADTU/0/2023-27/BTCS/212 | B.Tech CSE (2023–2027) |
| **Member** | **ATIKUR RAHMAN** | ADTU/0/2023-27/BTCS/191 | B.Tech CSE (2023–2027) |
| **Member** | **MAHIDUL AHASAN** | ADTU/0/2023-27/BTCS/174 | B.Tech CSE (2023–2027) |
| **Member** | **MD AMIT HASAN ROBI** | ADTU/0/2023-27/BTCS/210 | B.Tech CSE (2023–2027) |

---

## 2. Problem Statement & Background

India's 63+ million Micro, Small, and Medium Enterprises (MSMEs) contribute over 30% to national GDP. However, **94% of small businesses operate without dedicated IT staff or cybersecurity protection**. Local pharmacies, diagnostic clinics, grocery stores, and startups are increasingly targeted by:
1. **UPI "Collect Request" PIN Traps**: Attackers send debit requests disguised as incoming advance payments.
2. **Fake Bank KYC Suspension SMS**: Pressure messages impersonating SBI, HDFC, or PNB demanding immediate credential verification.
3. **Malicious GST / Tax Notices**: Emails with `.zip.exe` ransomware and spyware payloads.
4. **WhatsApp Owner Impersonation**: Fraudsters messaging staff claiming the boss is in a hospital/meeting asking for urgent vendor payments.

### Why Existing Solutions Fail MSMEs:
- **Cost**: Enterprise SOC and EDR subscriptions cost ₹50,000 to ₹2,00,000+ per year.
- **Language & Jargon Barrier**: Security tools present confusing CVE alerts, SIEM logs, and English-only jargon that local shopkeepers cannot understand.
- **No Incident Action Plan**: When an employee clicks a bad link, owners panic without knowing how to contain the breach or escalate to authorities.

---

## 3. Proposed Solution: SafePulse AI

**SafePulse AI** is a lightweight, explainable, and bilingual (**English & Bengali**) cybersecurity SaaS platform built specifically for non-technical small businesses in Assam and Eastern India.

### Key Innovations:
- **Plain-Language Explainability**: No black-box scores. Every prediction provides transparent reasoning and highlights exact suspicious phrases directly in the text.
- **Zero-Target-Execution Security**: Scans links safely without ever loading or executing target URLs, guaranteeing zero malware infection or tracking triggers.
- **Bilingual Parity**: Full English and Bengali interface for local shopkeepers and pharmacy counters.
- **Integrated Emergency Escalation**: Embedded playbooks connecting directly to the **National Cybercrime Helpline 1930** and `cybercrime.gov.in`.

---

## 4. System Architecture & Core Capabilities

```
[ SME User / Shop Counter ]
           │
           ▼
[ React 18 + TypeScript + Tailwind CSS Frontend (Vite) ]
           │  (Authenticated JSON + JWT + Language Header)
           ▼
[ FastAPI Backend Gateway (Argon2id + Rate Limiter + Security Headers) ]
           │
 ┌─────────┼───────────────┬─────────────────┬─────────────────┐
 ▼         ▼               ▼                 ▼                 ▼
AI Phishing  SSRF-Safe URL   CERT-In 10-Domain  7-Scenario Incident  Data Breach &
Detector     Security Engine Posture Audit     Response Playbooks   Awareness Engine
(NLP+Rules)  (DNS TXT/A)     (Weighted 0-100)  (6 Phases + 1930)    (Quizzes & Demos)
           │
           ▼
[ SQLAlchemy ORM (SQLite / PostgreSQL) + ReportLab PDF Generator ]
```

### Module Breakdown:
1. **Explainable AI Phishing Detector**:
   - `FeatureUnion` combining Word TF-IDF (`ngram_range=(1,2)`) and Character-wb TF-IDF (`ngram_range=(3,5)`), classified with balanced Logistic Regression.
   - 7 regex-based social engineering heuristics (`urgency_pressure`, `credential_request`, `upi_payment_trap`, `authority_impersonation`, `remote_access`, `suspicious_tld`, `secrecy_bypass`).
   - Protective dampening to prevent false alarms on genuine security notices.
2. **SSRF-Safe Smart URL Security Scanner**:
   - Strict IP defense rejecting `localhost`, cloud metadata (`169.254.169.254`), private subnets (`10.x`, `172.16.x`, `192.168.x`), and obfuscated octal/hex IP notation.
   - Authoritative read-only DNS queries for SPF (`v=spf1`) and DMARC (`v=DMARC1`) records.
   - Explicit **"HTTPS ≠ Safe"** education notice.
3. **CERT-In MSME 10-Domain Health Check**:
   - Aligned with official CERT-In Cyber Security Guidelines for MSMEs (Passwords, MFA, Email, Access, Updates, 3-2-1 Backups, Data Protection, Endpoint, Wi-Fi, Readiness).
   - Generates weighted 0–100 posture score, weak area alerts, and downloadable PDF action plans.
4. **Cyber Incident Response Center**:
   - 7 practical playbooks covering phishing clicks, unauthorized UPI debits, ransomware, and lost devices.
   - 6 sequential containment phases with checklist progress tracking and timeline evidence notes.
5. **Data Breach Monitor & Cyber Awareness**:
   - Proactive business domain and email exposure checks.
   - Labeled educational simulations and interactive quizzes for counter staff.

---

## 5. Machine Learning Evaluation Results

Trained and evaluated on a curated 128-sample SME threat benchmark across Email, SMS, and WhatsApp:

| Metric | Held-Out Test Score (32 Samples) |
| :--- | :---: |
| **Accuracy** | **87.5%** |
| **Precision (Phishing)** | **92.9%** |
| **Recall (Phishing)** | **81.3%** |
| **F1-Score** | **86.7%** |
| **ROC-AUC** | **0.9531** |
| **5-Fold Cross-Validation F1** | **89.3% ± 7.2%** |

*Confusion Matrix*: True Negatives = 15, False Positives = 1, False Negatives = 3, True Positives = 13.

---

## 6. Project Readiness & Verification

- **Automated Backend Tests (`pytest`)**: **36 of 36 unit/integration tests passed** (`backend/tests/`).
- **Automated Frontend Tests (`vitest`)**: **8 of 8 UI integration tests passed** (`frontend/src/test/`).
- **Production Build**: Zero TypeScript errors (`npm run build` generates optimized vendor chunks).
- **One-Click Launchers**:
  - `start_safepulse.bat`: Automated backend and frontend launcher.
  - `start_tunnel.bat`: Instant Cloudflare HTTPS Tunnel forwarding for mobile/external evaluator access.

---

## 7. Commercial Potential & Impact

- **Target Market**: 63+ Million MSMEs in India; estimated ₹1,800+ Cr addressable regional market.
- **Pricing Strategy**:
  - *Free Tier*: 50 scans/month, posture check, and incident checklists for micro-retailers.
  - *Pro Tier (₹499/month)*: 500 scans/month, multi-branch tracking, and team MFA compliance for pharmacies and clinics.
- **Go-To-Market**: Distribution partnerships with Regional Cooperative Banks and Guwahati Pharmaceutical Associations.

---

## 8. Conclusion

**SafePulse AI** delivers an operational, production-grade Minimum Viable Product (MVP) directly addressing the *Small Business Cybersecurity Platform* problem statement. By combining explainable AI, strict SSRF immunity, CERT-In compliance, and bilingual access, it empowers small businesses in Assam and Eastern India to defend themselves against modern digital fraud.

*Team VenoX — Assam down town University (AdtU) — 14th November 2026*
