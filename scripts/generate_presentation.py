"""
Generate a modern, high-impact presentation for AdtU Innovation Mela 2026.
Team: VenoX
Project: SafePulse AI (Small Business Cybersecurity Platform)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# --- Color Palette ---
COLOR_BG = RGBColor(8, 13, 27)         # Deep cyber navy #080D1B
COLOR_CARD = RGBColor(16, 24, 43)      # Slate card #10182B
COLOR_CARD_BORDER = RGBColor(30, 41, 59) # Border #1E293B
COLOR_CYAN = RGBColor(6, 182, 212)      # Electric cyan #06B6D4
COLOR_CYAN_LIGHT = RGBColor(34, 211, 238) # Light cyan #22D3EE
COLOR_INDIGO = RGBColor(99, 102, 241)   # Indigo #6366F1
COLOR_EMERALD = RGBColor(16, 185, 129)  # Emerald green #10B981
COLOR_AMBER = RGBColor(245, 158, 11)    # Amber #F59E0B
COLOR_RED = RGBColor(239, 68, 68)       # Coral red #EF4444
COLOR_TEXT_MAIN = RGBColor(248, 250, 252) # White #F8FAFC
COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate #94A3B8
COLOR_TEXT_DIM = RGBColor(100, 116, 139) # Dim slate #64748B

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_BG
        bg_shape.line.fill.background()
        return bg_shape

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.2)
        else:
            card.line.fill.background()
        return card

    def add_header(slide, pill_text, title, subtitle=None):
        # Category pill badge
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.45), Inches(3.2), Inches(0.35))
        pill.fill.solid()
        pill.fill.fore_color.rgb = RGBColor(20, 28, 55)
        pill.line.color.rgb = COLOR_INDIGO
        pill.line.width = Pt(1)
        tf_pill = pill.text_frame
        tf_pill.word_wrap = True
        tf_pill.margin_left = tf_pill.margin_right = tf_pill.margin_top = tf_pill.margin_bottom = 0
        p = tf_pill.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = pill_text.upper()
        run.font.name = "Segoe UI"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_CYAN_LIGHT

        # Slide Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.7))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED
            p_sub.space_before = Pt(3)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (Cover)
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative glow card behind title
    add_card(s1, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1), RGBColor(14, 22, 40), RGBColor(40, 56, 85))

    # Event Banner Pill
    pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.15), Inches(6.0), Inches(0.38))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = RGBColor(28, 25, 60)
    pill1.line.color.rgb = COLOR_INDIGO
    tf1 = pill1.text_frame
    p = tf1.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "ADTU INNOVATION MELA 2026 • JIRONEE, C BLOCK"
    r.font.name = "Segoe UI"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = COLOR_CYAN_LIGHT

    # Main Project Title
    t_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.65), Inches(10.5), Inches(1.5))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "SafePulse AI"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf.add_paragraph()
    p2.text = "Smart Cybersecurity. Simple Protection. Safer Businesses."
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CYAN

    # Problem Statement Highlight Card
    ps_card = add_card(s1, Inches(1.3), Inches(3.2), Inches(10.7), Inches(1.1), RGBColor(18, 28, 50), COLOR_INDIGO)
    ps_tf = ps_card.text_frame
    ps_tf.word_wrap = True
    ps_p1 = ps_tf.paragraphs[0]
    ps_r1 = ps_p1.add_run()
    ps_r1.text = "OFFICIAL PROBLEM STATEMENT: "
    ps_r1.font.name = "Segoe UI"
    ps_r1.font.size = Pt(10)
    ps_r1.font.bold = True
    ps_r1.font.color.rgb = COLOR_AMBER

    ps_r2 = ps_p1.add_run()
    ps_r2.text = "Small Business Cybersecurity Platform\n"
    ps_r2.font.name = "Segoe UI"
    ps_r2.font.size = Pt(13)
    ps_r2.font.bold = True
    ps_r2.font.color.rgb = COLOR_TEXT_MAIN

    ps_p2 = ps_tf.add_paragraph()
    ps_r3 = ps_p2.add_run()
    ps_r3.text = "\"Develop an affordable cybersecurity solution that helps small businesses detect phishing attempts, malware, suspicious activities, and potential data breaches.\""
    ps_r3.font.name = "Segoe UI"
    ps_r3.font.size = Pt(10.5)
    ps_r3.font.italic = True
    ps_r3.font.color.rgb = COLOR_TEXT_MUTED

    # Team & Presenter Details Card
    team_card = add_card(s1, Inches(1.3), Inches(4.5), Inches(10.7), Inches(1.85), RGBColor(12, 19, 34), RGBColor(30, 44, 70))
    team_tf = team_card.text_frame
    team_tf.word_wrap = True
    
    tp1 = team_tf.paragraphs[0]
    tr1 = tp1.add_run()
    tr1.text = "TEAM: "
    tr1.font.bold = True
    tr1.font.color.rgb = COLOR_CYAN
    tr2 = tp1.add_run()
    tr2.text = "VenoX    |    "
    tr2.font.bold = True
    tr2.font.color.rgb = COLOR_TEXT_MAIN
    tr3 = tp1.add_run()
    tr3.text = "DATE: "
    tr3.font.bold = True
    tr3.font.color.rgb = COLOR_CYAN
    tr4 = tp1.add_run()
    tr4.text = "14th November 2026    |    "
    tr4.font.color.rgb = COLOR_TEXT_MAIN
    tr5 = tp1.add_run()
    tr5.text = "STATUS: "
    tr5.font.bold = True
    tr5.font.color.rgb = COLOR_EMERALD
    tr6 = tp1.add_run()
    tr6.text = "Functional Working MVP Ready"
    tr6.font.bold = True
    tr6.font.color.rgb = COLOR_EMERALD

    tp2 = team_tf.add_paragraph()
    tp2.space_before = Pt(8)
    tr_lead = tp2.add_run()
    tr_lead.text = "Team Leader: "
    tr_lead.font.bold = True
    tr_lead.font.color.rgb = COLOR_INDIGO
    tr_lead_val = tp2.add_run()
    tr_lead_val.text = "MD SAMIUR RAHMAN TANIM  "
    tr_lead_val.font.bold = True
    tr_lead_val.font.color.rgb = COLOR_TEXT_MAIN
    tr_lead_id = tp2.add_run()
    tr_lead_id.text = "(ADTU/0/2023-27/BTCS/212)\n"
    tr_lead_id.font.color.rgb = COLOR_TEXT_MUTED

    tp3 = team_tf.add_paragraph()
    tp3.space_before = Pt(4)
    tr_mem = tp3.add_run()
    tr_mem.text = "Team Members: "
    tr_mem.font.bold = True
    tr_mem.font.color.rgb = COLOR_TEXT_MUTED
    tr_mem_val = tp3.add_run()
    tr_mem_val.text = "• ATIKUR RAHMAN (ADTU/0/2023-27/BTCS/191)   • MAHIDUL AHASAN (ADTU/0/2023-27/BTCS/174)   • MD AMIT HASAN ROBI (ADTU/0/2023-27/BTCS/210)"
    tr_mem_val.font.color.rgb = COLOR_TEXT_MAIN
    tr_mem_val.font.size = Pt(9.5)

    # -------------------------------------------------------------------------
    # SLIDE 2: Problem Statement & Small Business Crisis
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Real-World Challenge", "The Growing SME Cyber Crisis in India", "Why small retailers, local pharmacies, and clinics are the primary targets of cybercrime.")

    # 3 Stat Cards across the top
    stats = [
        ("63M+ MSMEs in India", "Form 30% of Indian GDP, but 94% operate without dedicated IT or security teams.", COLOR_CYAN),
        ("72% Attacks Hit SMEs", "Attackers focus on pharmacies, traders & retail shops due to undefended digital billing.", COLOR_AMBER),
        ("₹2.4 Lakh Avg Loss", "Average direct financial loss from a single UPI / KYC scam or ransomware lock.", COLOR_RED),
    ]
    for idx, (stat_title, stat_desc, col) in enumerate(stats):
        cx = Inches(0.8 + idx * 4.0)
        card = add_card(s2, cx, Inches(1.85), Inches(3.75), Inches(1.7), RGBColor(14, 22, 40))
        ctf = card.text_frame
        ctf.word_wrap = True
        p1 = ctf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = stat_title
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(17)
        r1.font.bold = True
        r1.font.color.rgb = col
        p2 = ctf.add_paragraph()
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = stat_desc
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    # 2 Threat Column Cards on bottom
    left_card = add_card(s2, Inches(0.8), Inches(3.85), Inches(5.75), Inches(3.0))
    ltf = left_card.text_frame
    ltf.word_wrap = True
    lp1 = ltf.paragraphs[0]
    lr1 = lp1.add_run()
    lr1.text = "Common Regional Attack Vectors in Assam & NE India\n"
    lr1.font.size = Pt(13)
    lr1.font.bold = True
    lr1.font.color.rgb = COLOR_TEXT_MAIN
    
    threats = [
        ("UPI Collect PIN Scams", "Fraudsters send fake advance payment requests asking the shopkeeper to enter their UPI PIN to 'receive' money."),
        ("Bank KYC Suspension SMS", "Fake SBI/HDFC/PNB alerts threatening corporate account freezing within 2 hours."),
        ("GST & Tax Notice Invoices", "Phishing emails impersonating GST portal with malicious .zip.exe attachments."),
        ("WhatsApp Boss Impersonation", "Fraudulent messages claiming to be store owner stuck in hospital asking for urgent vendor remittance."),
    ]
    for title, desc in threats:
        p = ltf.add_paragraph()
        p.space_before = Pt(4)
        r_t = p.add_run()
        r_t.text = f"• {title}: "
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = COLOR_CYAN
        r_d = p.add_run()
        r_d.text = desc
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    right_card = add_card(s2, Inches(6.8), Inches(3.85), Inches(5.75), Inches(3.0))
    rtf = right_card.text_frame
    rtf.word_wrap = True
    rp1 = rtf.paragraphs[0]
    rr1 = rp1.add_run()
    rr1.text = "The Root Cause: Why Small Businesses Are Defenseless\n"
    rr1.font.size = Pt(13)
    rr1.font.bold = True
    rr1.font.color.rgb = COLOR_TEXT_MAIN

    gaps = [
        ("No IT or Security Staff", "Managed by sole proprietors, family members, or junior billing operators."),
        ("English Technical Jargon", "Existing alerts speak in CVE codes, SIEM logs, and network topologies shopkeepers cannot read."),
        ("Enterprise Tools are Unaffordable", "Enterprise solutions cost ₹50,000–₹2,00,000/year, requiring dedicated security engineers."),
        ("No Incident Action Plan", "When an employee clicks a malicious link, staff panic without knowing who to call or what to freeze."),
    ]
    for title, desc in gaps:
        p = rtf.add_paragraph()
        p.space_before = Pt(4)
        r_t = p.add_run()
        r_t.text = f"• {title}: "
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = COLOR_RED
        r_d = p.add_run()
        r_d.text = desc
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 3: The Solution — SafePulse AI
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Product Innovation", "Introducing SafePulse AI — Simple, Smart Cyber Defense", "A unified, explainable, and bilingual cybersecurity SaaS platform custom-engineered for non-technical businesses.")

    # 4 Core Pillar Cards
    pillars = [
        ("1. AI Phishing & Scam Detector", "FeatureUnion NLP (Word + Char N-grams) + Logistic Regression model paired with transparent regex social-engineering heuristics and inline phrase highlighting.", COLOR_INDIGO),
        ("2. SSRF-Safe Smart URL Scanner", "Lexical parsing + DNS SPF/DMARC checks with strict blocking of localhost, private IPs, and obfuscated octal/hex notation. 100% zero-target HTTP execution.", COLOR_CYAN),
        ("3. CERT-In MSME 10-Domain Health Check", "Comprehensive security posture audit aligned directly with official CERT-In MSME guidelines, weighted 0–100 scoring, radar/bar analytics, and PDF plans.", COLOR_EMERALD),
        ("4. Guided 6-Phase Incident Playbooks", "Interactive step-by-step containment across 7 SME scenarios (UPI fraud, phishing, ransomware) with direct India Helpline 1930 & cybercrime.gov.in escalation.", COLOR_AMBER),
    ]
    for idx, (p_title, p_desc, col) in enumerate(pillars):
        row = idx // 2
        col_idx = idx % 2
        px = Inches(0.8 + col_idx * 5.95)
        py = Inches(1.85 + row * 2.15)
        c = add_card(s3, px, py, Inches(5.75), Inches(1.95), RGBColor(14, 22, 40))
        ctf = c.text_frame
        ctf.word_wrap = True
        p = ctf.paragraphs[0]
        r = p.add_run()
        r.text = p_title
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = col
        p2 = ctf.add_paragraph()
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = p_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Callout: Bilingual Support (Assam/Guwahati Context)
    b_card = add_card(s3, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.95), RGBColor(18, 25, 48), COLOR_INDIGO)
    btf = b_card.text_frame
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    br1 = bp.add_run()
    br1.text = "BILINGUAL LOCALIZATION (English & Bengali) : "
    br1.font.bold = True
    br1.font.size = Pt(10)
    br1.font.color.rgb = COLOR_CYAN_LIGHT
    br2 = bp.add_run()
    br2.text = "Built specifically for retail and pharmacy shop owners in Assam and Eastern India. Every assessment question, heuristic reason, and incident checklist is fully translated to eliminate the English language barrier."
    br2.font.size = Pt(10)
    br2.font.color.rgb = COLOR_TEXT_MAIN

    # -------------------------------------------------------------------------
    # SLIDE 4: System Architecture & Technical Stack
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Engineering Architecture", "Production-Ready Full-Stack Architecture", "Modern decoupled SaaS architecture designed for speed, privacy, and local deployment independence.")

    # 3 Architecture Tier Cards
    tiers = [
        ("Frontend Client Layer", [
            ("Framework", "React 18 + TypeScript + Vite 6"),
            ("Styling & UI", "Tailwind CSS + Custom Dark Theme"),
            ("Data Visuals", "Recharts (Progress Rings, Trend, Posture)"),
            ("Localization", "Custom React Context (EN & BN Parity)"),
            ("State & Storage", "Context API + Scoped Local Storage"),
        ], COLOR_CYAN),
        ("FastAPI Backend Services", [
            ("API Engine", "Python 3.12 + FastAPI + Uvicorn"),
            ("Security & Auth", "Argon2id Hashing + HS256 JWT Tokens"),
            ("Rate Limiting", "Sliding-Window IP/Route Limiter"),
            ("Database ORM", "SQLAlchemy 2.0 (SQLite / PostgreSQL)"),
            ("Report Engine", "ReportLab Dynamic Multi-Page PDFs"),
        ], COLOR_INDIGO),
        ("AI/ML & Security Engine", [
            ("ML Pipeline", "FeatureUnion (Word + Char N-Grams)"),
            ("Classifier", "Balanced Logistic Regression (Scikit-Learn)"),
            ("SSRF Defense", "POSIX/Hex IP Parser + Zero HTTP Fetch"),
            ("DNS Inspection", "dnspython read-only TXT/A (SPF/DMARC)"),
            ("Tenant Scoping", "Strict business_id scoping on all tables"),
        ], COLOR_EMERALD),
    ]
    for idx, (t_name, bullets, col) in enumerate(tiers):
        tx = Inches(0.8 + idx * 4.0)
        c = add_card(s4, tx, Inches(1.85), Inches(3.75), Inches(4.3), RGBColor(14, 22, 40))
        ctf = c.text_frame
        ctf.word_wrap = True
        p = ctf.paragraphs[0]
        r = p.add_run()
        r.text = t_name
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = col

        for b_name, b_desc in bullets:
            p_b = ctf.add_paragraph()
            p_b.space_before = Pt(8)
            rb_n = p_b.add_run()
            rb_n.text = f"{b_name}\n"
            rb_n.font.size = Pt(9)
            rb_n.font.bold = True
            rb_n.font.color.rgb = COLOR_TEXT_MAIN
            rb_d = p_b.add_run()
            rb_d.text = b_desc
            rb_d.font.size = Pt(9.5)
            rb_d.font.color.rgb = COLOR_TEXT_MUTED

    # Bottom Architectural Invariant Card
    bot_card = add_card(s4, Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.8), RGBColor(12, 18, 32))
    btf = bot_card.text_frame
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    bpr = bp.add_run()
    bpr.text = "PRIVACY & SECURITY GUARANTEE: "
    bpr.font.bold = True
    bpr.font.size = Pt(9.5)
    bpr.font.color.rgb = COLOR_EMERALD
    bpr2 = bp.add_run()
    bpr2.text = "SafePulse AI runs completely offline/locally without requiring paid external APIs. Scanned messages and target links are never executed, shared with third parties, or cached externally."
    bpr2.font.size = Pt(9.5)
    bpr2.font.color.rgb = COLOR_TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 5: AI Phishing Detector (With Live Screenshot)
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Module 1", "AI Phishing & Scam Detector", "Explainable natural language processing with transparent held-out test evaluation metrics.")

    # Left Column: Explanation & Metrics
    left_c = add_card(s5, Inches(0.8), Inches(1.85), Inches(5.2), Inches(5.2), RGBColor(14, 22, 40))
    ltf = left_c.text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    r = p.add_run()
    r.text = "How the Explainable ML Engine Works\n"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_CYAN

    points = [
        ("FeatureUnion Vectorizer", "Word N-grams (1-2) + Character-wb N-grams (3-5) capture subtle character substitutions (e.g., 'paytm' vs 'paytm-kyc.xyz')."),
        ("7 Heuristic Rules", "Detects urgency pressure, credential/OTP requests, UPI PIN traps, brand impersonation, remote-access lures, and secrecy tactics."),
        ("Benign Protective Dampening", "Dampens false positives when legitimate notices appear ('Never share OTP with anyone')."),
        ("Inline Character Offsets", "Highlights exact suspect phrases directly in the browser so the owner learns while reviewing."),
    ]
    for pt, pd in points:
        pb = ltf.add_paragraph()
        pb.space_before = Pt(6)
        r_t = pb.add_run()
        r_t.text = f"• {pt}: "
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = COLOR_TEXT_MAIN
        r_d = pb.add_run()
        r_d.text = pd
        r_d.font.size = Pt(9)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    # Held-out metrics mini table
    p_m = ltf.add_paragraph()
    p_m.space_before = Pt(10)
    rm_t = p_m.add_run()
    rm_t.text = "VERIFIED HELD-OUT TEST METRICS (32 SME Samples):\n"
    rm_t.font.bold = True
    rm_t.font.size = Pt(9.5)
    rm_t.font.color.rgb = COLOR_EMERALD

    metrics_str = "Accuracy: 87.5%   |   Precision: 92.9%   |   Recall: 81.3%\nF1-Score: 86.7%   |   ROC-AUC: 0.9531   |   5-Fold CV: 89.3%"
    p_mv = ltf.add_paragraph()
    rm_v = p_mv.add_run()
    rm_v.text = metrics_str
    rm_v.font.size = Pt(9.5)
    rm_v.font.bold = True
    rm_v.font.color.rgb = COLOR_TEXT_MAIN

    # Right Column: Screenshot
    phish_ss_path = os.path.join(ASSETS_DIR, "screenshot_phishing.png")
    if os.path.exists(phish_ss_path):
        s5.shapes.add_picture(phish_ss_path, Inches(6.2), Inches(1.85), Inches(6.3), Inches(5.2))

    # -------------------------------------------------------------------------
    # SLIDE 6: SSRF-Safe URL Analyzer & Breach Monitor
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Module 2 & 3", "SSRF-Safe URL Scanner & Breach Monitor", "Zero-target execution URL defense and proactive domain credential exposure checks.")

    # Left Column: Explanation
    l_c6 = add_card(s6, Inches(0.8), Inches(1.85), Inches(5.2), Inches(5.2), RGBColor(14, 22, 40))
    ltf6 = l_c6.text_frame
    ltf6.word_wrap = True
    p = ltf6.paragraphs[0]
    r = p.add_run()
    r.text = "Enterprise-Grade URL Security Principles\n"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_CYAN

    url_points = [
        ("Strict SSRF Immunity", "Blocks localhost, private/loopback IP ranges (10.x, 192.168.x, 172.16.x), cloud metadata (169.254.169.254), and POSIX octal/hex obfuscations."),
        ("Zero HTTP Execution", "Never makes an outbound HTTP connection to the target link; eliminates drive-by malware and tracking beacon triggers."),
        ("Read-Only DNS Resolution", "Inspects authoritative DNS records via dnspython: A records, SPF (v=spf1), and DMARC policies for domain spoofing defense."),
        ("'HTTPS ≠ Safe' Education", "Alerts shop owners that fraudulent sites also obtain free SSL certificates; encrypting traffic does not prove legitimacy."),
        ("Data Breach Monitor", "Continuously checks business email domains and credentials against verified compromise databases with actionable password reset playbooks."),
    ]
    for pt, pd in url_points:
        pb = ltf6.add_paragraph()
        pb.space_before = Pt(6)
        r_t = pb.add_run()
        r_t.text = f"• {pt}: "
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = COLOR_TEXT_MAIN
        r_d = pb.add_run()
        r_d.text = pd
        r_d.font.size = Pt(9)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Screenshot
    url_ss_path = os.path.join(ASSETS_DIR, "screenshot_url.png")
    if os.path.exists(url_ss_path):
        s6.shapes.add_picture(url_ss_path, Inches(6.2), Inches(1.85), Inches(6.3), Inches(5.2))

    # -------------------------------------------------------------------------
    # SLIDE 7: CERT-In MSME 10-Domain Health Check
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Module 4", "Business Security Posture Assessment", "Aligned with official CERT-In Cyber Security Guidelines for MSMEs & Small Businesses.")

    # Left Column: Explanation
    l_c7 = add_card(s7, Inches(0.8), Inches(1.85), Inches(5.2), Inches(5.2), RGBColor(14, 22, 40))
    ltf7 = l_c7.text_frame
    ltf7.word_wrap = True
    p = ltf7.paragraphs[0]
    r = p.add_run()
    r.text = "10 CERT-In Posture Domains Evaluated\n"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_EMERALD

    domains = [
        ("1. Password Security", "Weight: 10% — Passphrase length and credential rotation."),
        ("2. Multi-Factor Auth (MFA)", "Weight: 14% — Primary barrier against 99% of takeovers."),
        ("3. Email Security", "Weight: 10% — Anti-phishing rules & SPF/DMARC records."),
        ("4. Employee Access", "Weight: 10% — Least privilege and offboarding checklists."),
        ("5. Software Updates", "Weight: 10% — Automatic billing PC and OS patches."),
        ("6. 3-2-1 Data Backups", "Weight: 12% — Offline/air-gapped Tally and POS backups."),
        ("7. Data Protection", "Weight: 10% — Customer PII & financial record encryption."),
        ("8. Device & Endpoint", "Weight: 8% — Antivirus and billing counter screen locks."),
        ("9. Wi-Fi & Network", "Weight: 8% — Isolated customer guest Wi-Fi."),
        ("10. Incident Readiness", "Weight: 8% — Step-by-step reporting preparedness."),
    ]
    for pt, pd in domains:
        pb = ltf7.add_paragraph()
        pb.space_before = Pt(3)
        r_t = pb.add_run()
        r_t.text = f"• {pt}: "
        r_t.font.bold = True
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = COLOR_TEXT_MAIN
        r_d = pb.add_run()
        r_d.text = pd
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Screenshot
    assess_ss_path = os.path.join(ASSETS_DIR, "screenshot_assessment.png")
    if os.path.exists(assess_ss_path):
        s7.shapes.add_picture(assess_ss_path, Inches(6.2), Inches(1.85), Inches(6.3), Inches(5.2))

    # -------------------------------------------------------------------------
    # SLIDE 8: Incident Response Center (With Live Screenshot)
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Module 5", "Cyber Incident Response Center", "Guided 6-phase triage checklists with India Helpline 1930 and bank escalation workflows.")

    # Left Column: Explanation
    l_c8 = add_card(s8, Inches(0.8), Inches(1.85), Inches(5.2), Inches(5.2), RGBColor(14, 22, 40))
    ltf8 = l_c8.text_frame
    ltf8.word_wrap = True
    p = ltf8.paragraphs[0]
    r = p.add_run()
    r.text = "7 Tailored SME Incident Playbooks\n"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_AMBER

    scenarios = [
        ("1. Phishing Link Clicked", "Credentials entered on fake banking or courier portal."),
        ("2. Suspicious Transaction / UPI Fraud", "Unauthorized debit or fraudulent collect request approved."),
        ("3. Suspected Ransomware", "Files encrypted or billing counter extortion splash screen."),
        ("4. Business Email Compromised (BEC)", "Unauthorized forwarding rules or vendor invoice bank switch."),
        ("5. Social Media / WhatsApp Business Taken Over", "Attacker messaging customers requesting advance payments."),
        ("6. Lost / Stolen Billing Device", "Phone or laptop containing customer data misplaced."),
        ("7. Suspicious Phishing Email Received", "Pre-click inspection and staff containment."),
    ]
    for pt, pd in scenarios:
        pb = ltf8.add_paragraph()
        pb.space_before = Pt(3)
        r_t = pb.add_run()
        r_t.text = f"• {pt}: "
        r_t.font.bold = True
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = COLOR_TEXT_MAIN
        r_d = pb.add_run()
        r_d.text = pd
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    p_phase = ltf8.add_paragraph()
    p_phase.space_before = Pt(8)
    r_ph = p_phase.add_run()
    r_ph.text = "6 Triage Phases: "
    r_ph.font.bold = True
    r_ph.font.size = Pt(9)
    r_ph.font.color.rgb = COLOR_CYAN
    r_ph2 = p_phase.add_run()
    r_ph2.text = "Immediate Actions → Containment → Account Protection → Evidence Preservation → Recovery → Reporting (National Portal 1930)."
    r_ph2.font.size = Pt(8.5)
    r_ph2.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Screenshot
    inc_ss_path = os.path.join(ASSETS_DIR, "screenshot_incidents.png")
    if os.path.exists(inc_ss_path):
        s8.shapes.add_picture(inc_ss_path, Inches(6.2), Inches(1.85), Inches(6.3), Inches(5.2))

    # -------------------------------------------------------------------------
    # SLIDE 9: Live Demo Walkthrough (MVP Proof for Judges)
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Hackathon Demo", "Live Working Prototype Demonstration Plan", "Step-by-step walkthrough of the live functional MVP running on localhost right now.")

    # Left Column: Demo Scenarios
    l_c9 = add_card(s9, Inches(0.8), Inches(1.85), Inches(5.2), Inches(5.2), RGBColor(14, 22, 40))
    ltf9 = l_c9.text_frame
    ltf9.word_wrap = True
    p = ltf9.paragraphs[0]
    r = p.add_run()
    r.text = "4-Minute Live Demonstration Flow\n"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_CYAN_LIGHT

    demo_steps = [
        ("Step 1: 1-Click Demo Launch", "Click 'Launch Interactive Demo' on the landing page to access pre-populated Brahmaputra Care Pharmacy workspace without registration."),
        ("Step 2: Bilingual Switch (EN / বাংলা)", "Toggle the language button to showcase immediate localization for local shopkeepers in Assam/Bengal."),
        ("Step 3: Scenario 1 — Fake Bank KYC SMS", "Analyze urgent SBI KYC suspension SMS. Inspect live risk ring, inline highlighted phrases, and real model metrics."),
        ("Step 4: Scenario 2 — Obfuscated Bank URL", "Scan lookalike bank URL. Show brand impersonation detection, DNS SPF/DMARC checks, and SSRF localhost probe blocking."),
        ("Step 5: Scenario 3 — Incident Playbook & PDF", "Open 'Phishing Link Clicked' playbook, check off containment steps, and generate branded executive PDF report."),
    ]
    for pt, pd in demo_steps:
        pb = ltf9.add_paragraph()
        pb.space_before = Pt(5)
        r_t = pb.add_run()
        r_t.text = f"• {pt}\n"
        r_t.font.bold = True
        r_t.font.size = Pt(9)
        r_t.font.color.rgb = COLOR_TEXT_MAIN
        r_d = pb.add_run()
        r_d.text = pd
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = COLOR_TEXT_MUTED

    # Right Column: Dashboard Screenshot
    dash_ss_path = os.path.join(ASSETS_DIR, "screenshot_dashboard.png")
    if os.path.exists(dash_ss_path):
        s9.shapes.add_picture(dash_ss_path, Inches(6.2), Inches(1.85), Inches(6.3), Inches(5.2))

    # -------------------------------------------------------------------------
    # SLIDE 10: Business Model & Market Sizing
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Commercial Viability", "Market Opportunity & Business Model", "Sustainable freemium economics tailored for India's 63 Million MSME ecosystem.")

    # 3 Plan Cards
    plans = [
        ("Free SME Starter", "₹0 / Month", [
            "Up to 50 Threat Scans / month",
            "10-Domain CERT-In Health Check",
            "7 Interactive Incident Playbooks",
            "Instant PDF Action Plan Downloads",
            "Bilingual (English & Bengali)",
        ], COLOR_TEXT_MUTED, RGBColor(14, 22, 40)),
        ("Pro SME Shield", "₹499 / Month", [
            "500 Phishing & URL Scans / month",
            "Multi-Branch Workspace Management",
            "Team MFA & Awareness Tracking",
            "Monthly Executive PDF Reports",
            "Continuous Breach & Domain Monitoring",
        ], COLOR_CYAN, RGBColor(18, 28, 52)),
        ("Enterprise / Bank Co-Brand", "Custom Pricing", [
            "5,000+ Scans / month + Full API",
            "White-Label for Cooperative Banks",
            "Custom Incident Webhook Integrations",
            "Dedicated Audit Trail Retention",
            "Regional Trade Association Packs",
        ], COLOR_INDIGO, RGBColor(14, 22, 40)),
    ]
    for idx, (p_name, p_price, features, col, bg_c) in enumerate(plans):
        cx = Inches(0.8 + idx * 4.0)
        c = add_card(s10, cx, Inches(1.85), Inches(3.75), Inches(4.2), bg_c, col)
        ctf = c.text_frame
        ctf.word_wrap = True
        
        p = ctf.paragraphs[0]
        r = p.add_run()
        r.text = p_name
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = COLOR_TEXT_MAIN
        
        p2 = ctf.add_paragraph()
        r2 = p2.add_run()
        r2.text = p_price
        r2.font.size = Pt(18)
        r2.font.bold = True
        r2.font.color.rgb = col
        p2.space_before = Pt(4)

        for feat in features:
            pf = ctf.add_paragraph()
            pf.space_before = Pt(6)
            rf = pf.add_run()
            rf.text = f"✓  {feat}"
            rf.font.size = Pt(9.5)
            rf.font.color.rgb = COLOR_TEXT_MAIN

    # Bottom Market Note
    m_card = add_card(s10, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.85), RGBColor(12, 18, 32))
    mtf = m_card.text_frame
    mtf.word_wrap = True
    mp = mtf.paragraphs[0]
    mr = mp.add_run()
    mr.text = "GO-TO-MARKET STRATEGY: "
    mr.font.bold = True
    mr.font.size = Pt(9.5)
    mr.font.color.rgb = COLOR_AMBER
    mr2 = mp.add_run()
    mr2.text = "Partner directly with Regional Rural & Cooperative Banks, Guwahati Pharmaceutical Distributors, and Retail Trade Associations to distribute SafePulse AI as an added-value digital protection bundle."
    mr2.font.size = Pt(9.5)
    mr2.font.color.rgb = COLOR_TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 11: Product Roadmap & Regional Expansion
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Future Vision", "Product Roadmap & Regional Expansion", "Strategic evolution from a hackathon prototype into India's leading SME cyber guard.")

    phases = [
        ("Phase 1: Working MVP (Completed)", [
            "Bilingual React + FastAPI SaaS platform",
            "Explainable TF-IDF + Logistic Regression ML pipeline",
            "SSRF-safe URL & DNS (SPF/DMARC) inspector",
            "10-Domain CERT-In MSME posture assessment",
            "7-Scenario, 6-Phase interactive incident center",
            "ReportLab dynamic PDF reporting engine",
        ], COLOR_EMERALD),
        ("Phase 2: Regional Pilot (Q1-Q2 2027)", [
            "Assamese & Hindi full language localization",
            "Multilingual Indic-NLP scam detection model",
            "Email header (.eml / DKIM / DMARC) parser",
            "Pilot deployment with 50+ Guwahati pharmacy shops",
            "WhatsApp message forwarding triage bot",
        ], COLOR_CYAN),
        ("Phase 3: Scale & Ecosystem (Q3-Q4 2027)", [
            "Co-branded packs with Regional Cooperative Banks",
            "Automated SSL / DMARC drift monitoring alerts",
            "External threat feed connectors (Safe Browsing / VT)",
            "Multi-tenant branch management for retail chains",
            "Insurance audit certification integration",
        ], COLOR_INDIGO),
    ]
    for idx, (ph_name, ph_items, col) in enumerate(phases):
        px = Inches(0.8 + idx * 4.0)
        c = add_card(s11, px, Inches(1.85), Inches(3.75), Inches(5.1), RGBColor(14, 22, 40))
        ctf = c.text_frame
        ctf.word_wrap = True
        p = ctf.paragraphs[0]
        r = p.add_run()
        r.text = ph_name
        r.font.size = Pt(12.5)
        r.font.bold = True
        r.font.color.rgb = col

        for item in ph_items:
            pi = ctf.add_paragraph()
            pi.space_before = Pt(8)
            ri = pi.add_run()
            ri.text = f"• {item}"
            ri.font.size = Pt(9.5)
            ri.font.color.rgb = COLOR_TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 12: Conclusion & Q&A (Team VenoX)
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)

    # Hero Closing Card
    main_c = add_card(s12, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1), RGBColor(14, 22, 40), RGBColor(40, 56, 85))
    mtf12 = main_c.text_frame
    mtf12.word_wrap = True

    p = mtf12.paragraphs[0]
    r = p.add_run()
    r.text = "SafePulse AI\n"
    r.font.name = "Segoe UI"
    r.font.size = Pt(36)
    r.font.bold = True
    r.font.color.rgb = COLOR_TEXT_MAIN

    p_sub = mtf12.add_paragraph()
    r_sub = p_sub.add_run()
    r_sub.text = "Smart Cybersecurity. Simple Protection. Safer Businesses.\n"
    r_sub.font.size = Pt(16)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_CYAN

    p_body = mtf12.add_paragraph()
    p_body.space_before = Pt(10)
    r_b = p_body.add_run()
    r_b.text = (
        "Thank you, Esteemed Judges & Evaluators at AdtU Innovation Mela 2026!\n"
        "Our working prototype is fully set up, tested, and actively running on our laptops at Jironee, C Block.\n"
        "We are ready to demonstrate any live scenario — Phishing Detection, URL Inspection, or Incident Triage.\n"
    )
    r_b.font.size = Pt(11)
    r_b.font.color.rgb = COLOR_TEXT_MUTED

    # Team Grid in Bottom Half
    team_box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(3.6), Inches(10.7), Inches(2.7))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = RGBColor(10, 16, 30)
    team_box.line.color.rgb = COLOR_INDIGO
    t_tf = team_box.text_frame
    t_tf.word_wrap = True

    tp1 = t_tf.paragraphs[0]
    tr1 = tp1.add_run()
    tr1.text = "TEAM VENOX — PROJECT CREDITS & DETAILS\n"
    tr1.font.bold = True
    tr1.font.size = Pt(12)
    tr1.font.color.rgb = COLOR_CYAN_LIGHT

    tp2 = t_tf.add_paragraph()
    tp2.space_before = Pt(6)
    r_tl = tp2.add_run()
    r_tl.text = "TEAM LEADER :  "
    r_tl.font.bold = True
    r_tl.font.size = Pt(11)
    r_tl.font.color.rgb = COLOR_AMBER
    r_tl_v = tp2.add_run()
    r_tl_v.text = "MD SAMIUR RAHMAN TANIM  "
    r_tl_v.font.bold = True
    r_tl_v.font.size = Pt(11)
    r_tl_v.font.color.rgb = COLOR_TEXT_MAIN
    r_tl_id = tp2.add_run()
    r_tl_id.text = "(Enrollment: ADTU/0/2023-27/BTCS/212)\n"
    r_tl_id.font.size = Pt(10)
    r_tl_id.font.color.rgb = COLOR_TEXT_MUTED

    tp3 = t_tf.add_paragraph()
    tp3.space_before = Pt(4)
    r_m = tp3.add_run()
    r_m.text = "TEAM MEMBERS :\n"
    r_m.font.bold = True
    r_m.font.size = Pt(10.5)
    r_m.font.color.rgb = COLOR_INDIGO

    members_list = [
        ("ATIKUR RAHMAN", "ADTU/0/2023-27/BTCS/191"),
        ("MAHIDUL AHASAN", "ADTU/0/2023-27/BTCS/174"),
        ("MD AMIT HASAN ROBI", "ADTU/0/2023-27/BTCS/210"),
    ]
    for m_name, m_id in members_list:
        pm = t_tf.add_paragraph()
        pm.space_before = Pt(2)
        rmn = pm.add_run()
        rmn.text = f"•  {m_name} "
        rmn.font.bold = True
        rmn.font.size = Pt(10)
        rmn.font.color.rgb = COLOR_TEXT_MAIN
        rmi = pm.add_run()
        rmi.text = f"—  Enrollment: {m_id}"
        rmi.font.size = Pt(9.5)
        rmi.font.color.rgb = COLOR_TEXT_MUTED

    output_path = os.path.join(BASE_DIR, "SafePulse_AI_VenoX_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    create_deck()
