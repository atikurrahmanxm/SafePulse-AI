"""
Update Slide 12 of SafePulse_AI_VenoX_Presentation.pptx to a modern Thank You slide
with project GitHub link and Team VenoX details.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

COLOR_BG = RGBColor(8, 13, 27)           # Deep cyber navy #080D1B
COLOR_CARD = RGBColor(16, 24, 43)        # Slate card #10182B
COLOR_CARD_BORDER = RGBColor(30, 41, 59) # Border #1E293B
COLOR_CYAN = RGBColor(6, 182, 212)        # Electric cyan #06B6D4
COLOR_CYAN_LIGHT = RGBColor(34, 211, 238) # Light cyan #22D3EE
COLOR_INDIGO = RGBColor(99, 102, 241)     # Indigo #6366F1
COLOR_EMERALD = RGBColor(16, 185, 129)    # Emerald green #10B981
COLOR_AMBER = RGBColor(245, 158, 11)      # Amber #F59E0B
COLOR_TEXT_MAIN = RGBColor(248, 250, 252) # White #F8FAFC
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)# Slate #94A3B8
COLOR_TEXT_DIM = RGBColor(100, 116, 139)  # Dim slate #64748B

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTX_PATH = os.path.join(BASE_DIR, "SafePulse_AI_VenoX_Presentation.pptx")

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

def main():
    prs = Presentation(PPTX_PATH)
    slide = prs.slides[11]  # 12th slide

    # Remove existing shapes except background shape (shape 0)
    for sh in list(slide.shapes)[1:]:
        sp = sh._element
        sp.getparent().remove(sp)

    # Decorative main container card
    add_card(slide, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1), RGBColor(14, 22, 40), RGBColor(40, 56, 85))

    # Top Pill Badge
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.1), Inches(6.2), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(28, 25, 60)
    pill.line.color.rgb = COLOR_INDIGO
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.alignment = PP_ALIGN.CENTER
    r_pill = p_pill.add_run()
    r_pill.text = "ADTU INNOVATION MELA 2026 • JIRONEE, C BLOCK"
    r_pill.font.name = "Segoe UI"
    r_pill.font.size = Pt(10)
    r_pill.font.bold = True
    r_pill.font.color.rgb = COLOR_CYAN_LIGHT

    # Hero "Thank You!" Headline
    t_box = slide.shapes.add_textbox(Inches(1.3), Inches(1.6), Inches(10.7), Inches(1.5))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = "Thank You!"
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(46)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_TEXT_MAIN

    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "SafePulse AI — Smart Cybersecurity. Simple Protection. Safer Businesses."
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(16)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_CYAN

    p3 = tf.add_paragraph()
    p3.space_before = Pt(4)
    r3 = p3.add_run()
    r3.text = "Working MVP is live and actively ready for demonstration & evaluator interaction."
    r3.font.name = "Segoe UI"
    r3.font.size = Pt(11)
    r3.font.color.rgb = COLOR_EMERALD

    # GitHub Repository Card (Left Bottom)
    gh_card = add_card(slide, Inches(1.3), Inches(3.45), Inches(5.2), Inches(3.05), RGBColor(12, 19, 36), COLOR_CYAN)
    gh_tf = gh_card.text_frame
    gh_tf.word_wrap = True

    gp1 = gh_tf.paragraphs[0]
    gr1 = gp1.add_run()
    gr1.text = "PROJECT GITHUB REPOSITORY\n"
    gr1.font.bold = True
    gr1.font.size = Pt(11)
    gr1.font.color.rgb = COLOR_CYAN_LIGHT

    gp2 = gh_tf.add_paragraph()
    gp2.space_before = Pt(8)
    gr_url = gp2.add_run()
    gr_url.text = "https://github.com/atikurrahmanxm/SafePulse-AI\n"
    gr_url.font.name = "Segoe UI"
    gr_url.font.bold = True
    gr_url.font.size = Pt(12)
    gr_url.font.color.rgb = COLOR_TEXT_MAIN

    gp3 = gh_tf.add_paragraph()
    gp3.space_before = Pt(8)
    gr3 = gp3.add_run()
    gr3.text = (
        "• Full-Stack Source Code (React 18 + FastAPI + SQLite/PostgreSQL)\n"
        "• Machine Learning Training Pipeline & Held-Out Test Metrics\n"
        "• SSRF-Safe URL Analyzer & CERT-In MSME 10-Domain Audit Engine\n"
        "• 7 Guided Incident Playbooks & ReportLab PDF Generator\n"
        "• Interactive Hackathon Demo Mode & Documentation"
    )
    gr3.font.size = Pt(9)
    gr3.font.color.rgb = COLOR_TEXT_MUTED

    # Team VenoX Credits Card (Right Bottom)
    team_card = add_card(slide, Inches(6.8), Inches(3.45), Inches(5.2), Inches(3.05), RGBColor(12, 19, 36), COLOR_INDIGO)
    team_tf = team_card.text_frame
    team_tf.word_wrap = True

    tp1 = team_tf.paragraphs[0]
    tr1 = tp1.add_run()
    tr1.text = "TEAM VENOX — ADTU INNOVATION MELA 2026\n"
    tr1.font.bold = True
    tr1.font.size = Pt(11)
    tr1.font.color.rgb = COLOR_INDIGO

    tp_sub = team_tf.add_paragraph()
    tp_sub.space_before = Pt(4)
    tr_sub = tp_sub.add_run()
    tr_sub.text = "Problem Statement: Small Business Cybersecurity Platform\n"
    tr_sub.font.bold = True
    tr_sub.font.size = Pt(9.5)
    tr_sub.font.color.rgb = COLOR_AMBER

    members = [
        ("MAHIDUL AHASAN", "ADTU/0/2023-27/BTCS/174"),
        ("ATIKUR RAHMAN", "ADTU/0/2023-27/BTCS/191"),
        ("MD AMIT HASAN ROBI", "ADTU/0/2023-27/BTCS/210"),
        ("MD SAMIUR RAHMAN TANIM", "ADTU/0/2023-27/BTCS/212"),
    ]
    for name, roll in members:
        p_m = team_tf.add_paragraph()
        p_m.space_before = Pt(4)
        rm_n = p_m.add_run()
        rm_n.text = f"•  {name}  "
        rm_n.font.bold = True
        rm_n.font.size = Pt(9.5)
        rm_n.font.color.rgb = COLOR_TEXT_MAIN
        rm_r = p_m.add_run()
        rm_r.text = f"- ({roll})"
        rm_r.font.size = Pt(9)
        rm_r.font.color.rgb = COLOR_TEXT_MUTED

    p_uni = team_tf.add_paragraph()
    p_uni.space_before = Pt(8)
    r_uni = p_uni.add_run()
    r_uni.text = "Assam down town University (AdtU) • B.Tech CSE (2023–2027)"
    r_uni.font.size = Pt(9)
    r_uni.font.italic = True
    r_uni.font.color.rgb = COLOR_TEXT_DIM

    prs.save(PPTX_PATH)
    print("Slide 12 updated successfully with Thank You & GitHub repository link!")

if __name__ == "__main__":
    main()
