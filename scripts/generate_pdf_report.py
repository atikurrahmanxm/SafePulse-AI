import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_path = os.path.join(BASE_DIR, "PROJECT_REPORT.pdf")

doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()

navy = colors.HexColor("#080D1B")
indigo = colors.HexColor("#4F46E5")
cyan = colors.HexColor("#0891B2")
slate = colors.HexColor("#334155")
muted = colors.HexColor("#64748B")
light_bg = colors.HexColor("#F8FAFC")

title_style = ParagraphStyle("RepTitle", parent=styles["Heading1"], fontSize=18, leading=22, textColor=navy, spaceAfter=2)
sub_style = ParagraphStyle("RepSub", parent=styles["Normal"], fontSize=10.5, leading=13, textColor=cyan, spaceAfter=4, fontName="Helvetica-Bold")
h2_style = ParagraphStyle("RepH2", parent=styles["Heading2"], fontSize=11, leading=14, textColor=indigo, spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
body_style = ParagraphStyle("RepBody", parent=styles["Normal"], fontSize=8.5, leading=11.5, textColor=slate, spaceAfter=3)
meta_style = ParagraphStyle("RepMeta", parent=styles["Normal"], fontSize=8, leading=11, textColor=muted)

story = [
    Paragraph("PROJECT REPORT: SAFEPULSE AI", title_style),
    Paragraph("Smart Cybersecurity. Simple Protection. Safer Businesses.", sub_style),
    Paragraph("<b>Event:</b> AdtU Innovation Mela 2026 (14th Nov 2026) | <b>Venue:</b> Jironee, C Block | <b>Problem:</b> Small Business Cybersecurity Platform", meta_style),
    Paragraph("<b>Team:</b> VenoX | <b>GitHub:</b> https://github.com/atikurrahmanxm/SafePulse-AI", meta_style),
    Spacer(1, 4),
    HRFlowable(width="100%", thickness=1.5, color=indigo, spaceAfter=5),
]

team_data = [
    ["Role", "Name", "Enrollment ID", "Department"],
    ["Team Leader", "MD SAMIUR RAHMAN TANIM", "ADTU/0/2023-27/BTCS/212", "B.Tech CSE (2023-27)"],
    ["Member", "ATIKUR RAHMAN", "ADTU/0/2023-27/BTCS/191", "B.Tech CSE (2023-27)"],
    ["Member", "MAHIDUL AHASAN", "ADTU/0/2023-27/BTCS/174", "B.Tech CSE (2023-27)"],
    ["Member", "MD AMIT HASAN ROBI", "ADTU/0/2023-27/BTCS/210", "B.Tech CSE (2023-27)"]
]
t = Table(team_data, colWidths=[80, 170, 160, 130])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), indigo),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ("BACKGROUND", (0, 1), (-1, -1), light_bg),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
]))
story.append(t)
story.append(Spacer(1, 6))

story.append(Paragraph("1. Problem Statement & Background Context", h2_style))
story.append(Paragraph("India's 63M+ MSMEs face aggressive cyber threats: UPI PIN collect scams, fake bank KYC SMS, malicious GST zip.exe invoices, and WhatsApp owner impersonation. Existing enterprise SOC tools are cost-prohibitive (50k-200k/year), English-only, jargon-heavy, and lack actionable emergency response guidance.", body_style))

story.append(Paragraph("2. Proposed Solution: SafePulse AI", h2_style))
story.append(Paragraph("<b>SafePulse AI</b> is an explainable, bilingual (English & Bengali) cybersecurity SaaS tailored for non-technical retail shops, pharmacies, and clinics in Assam and Eastern India.", body_style))
story.append(Paragraph("• <b>AI Phishing Detector:</b> FeatureUnion Word + Char TF-IDF with balanced Logistic Regression, 7 regex heuristic rules, inline phrase highlighting, and PDF reports.<br/>• <b>SSRF-Safe URL Scanner:</b> Strict rejection of localhost, private/loopback IPs, and cloud metadata before and after DNS lookup. Zero target HTTP connections.<br/>• <b>CERT-In MSME 10-Domain Audit:</b> Weighted 0-100 posture scoring aligned with official CERT-In guidance and downloadable action plans.<br/>• <b>Incident Response Center:</b> 7 SME playbooks across 6 lifecycle phases with India Helpline 1930 escalation.<br/>• <b>Data Breach & Awareness:</b> Proactive domain exposure alerts, labeled simulations, and interactive quizzes.", body_style))

story.append(Paragraph("3. Machine Learning Evaluation Metrics", h2_style))
story.append(Paragraph("Evaluated on a 32-sample held-out stratified test split: <b>Accuracy: 87.5%</b> | <b>Precision: 92.9%</b> | <b>Recall: 81.3%</b> | <b>F1-Score: 86.7%</b> | <b>ROC-AUC: 0.9531</b> | <b>5-Fold Cross-Validation: 89.3%</b>.", body_style))

story.append(Paragraph("4. Technical Architecture & Testing Verification", h2_style))
story.append(Paragraph("• <b>Frontend:</b> React 18, TypeScript, Vite 6, Tailwind CSS, Recharts, Bilingual Context (EN/BN).<br/>• <b>Backend:</b> FastAPI, SQLAlchemy 2.0 (SQLite/PostgreSQL), Argon2id, HS256 JWT, Sliding-Window Rate Limiting.<br/>• <b>Test Verification:</b> 36 of 36 backend pytest suites passed; 8 of 8 frontend vitest suites passed. Production build clean.", body_style))

story.append(Paragraph("5. Working MVP Readiness & Launchers", h2_style))
story.append(Paragraph("Fully functional working MVP running live at Jironee, C Block. 1-click launchers provided: <b>start_safepulse.bat</b> (local backend + frontend) and <b>start_tunnel.bat</b> (Cloudflare HTTPS tunnel for external/mobile judge demonstration).", body_style))

doc.build(story)
print(f"ReportLab PDF created successfully at: {pdf_path}")
