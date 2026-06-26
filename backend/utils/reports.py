import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def generate_markdown_report(data: dict) -> str:
    """Generate a clean markdown report from board outcome data."""
    title = data.get("title", "Strategic Business Evaluation Report")
    summary = data.get("executive_summary", "No summary provided.")
    swot = data.get("swot", {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []})
    risks = data.get("risks", [])
    financials = data.get("financials", {})
    tech_review = data.get("tech_review", {})
    decision_score = data.get("decision_score", 75)
    recommendation = data.get("recommendation", "Proceed with caution.")
    action_plan = data.get("action_plan", [])
    
    md = f"""# {title}

## Executive Summary
{summary}

## Decision Score: {decision_score}/100
**Overall Board Recommendation:** {recommendation}

## SWOT Analysis
| Category | Details |
|---|---|
| **Strengths** | {", ".join(swot.get("strengths", [])) or "None identified."} |
| **Weaknesses** | {", ".join(swot.get("weaknesses", [])) or "None identified."} |
| **Opportunities** | {", ".join(swot.get("opportunities", [])) or "None identified."} |
| **Threats** | {", ".join(swot.get("threats", [])) or "None identified."} |

## Risk Matrix
| Risk Description | Severity | Likelihood | Mitigation |
|---|---|---|---|
"""
    for risk in risks:
        md += f"| {risk.get('description', '')} | {risk.get('severity', '')} | {risk.get('likelihood', '')} | {risk.get('mitigation', '')} |\n"
        
    md += f"""
## Financial Projection & ROI
* **Initial Budget Required:** {financials.get('budget', 'TBD')}
* **Estimated Annual Revenue:** {financials.get('estimated_revenue', 'TBD')}
* **Projected 3-Year ROI:** {financials.get('roi_3yr', 'TBD')}
* **Cost Analysis Details:** {financials.get('cost_details', 'TBD')}

## Technical Feasibility Review
* **Feasibility Rating:** {tech_review.get('feasibility', 'Medium')}
* **Recommended Technology Stack:** {tech_review.get('tech_stack', 'TBD')}
* **Estimated Engineering Effort:** {tech_review.get('effort', 'TBD')}
* **Feasibility Details:** {tech_review.get('details', 'TBD')}

## Proposed Action Plan
"""
    for idx, action in enumerate(action_plan, 1):
        md += f"{idx}. **{action.get('phase', f'Phase {idx}')}**: {action.get('details', '')} (Timeline: {action.get('timeline', 'TBD')})\n"
        
    return md

def generate_pdf_report(data: dict, filepath: str) -> None:
    """Generate a high-quality PDF report using ReportLab."""
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0284C7'),
        spaceAfter=15
    )

    story = []
    
    # Title
    story.append(Paragraph(data.get("title", "Strategic Business Evaluation Report"), title_style))
    story.append(Paragraph(f"Boardroom AI Decision Score: {data.get('decision_score', 75)}/100 | Recommendation: {data.get('recommendation', 'Proceed')}", meta_style))
    story.append(Spacer(1, 15))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", section_heading))
    story.append(Paragraph(data.get("executive_summary", "No summary provided."), body_style))
    story.append(Spacer(1, 10))
    
    # SWOT
    story.append(Paragraph("SWOT Analysis", section_heading))
    swot = data.get("swot", {})
    swot_data = [
        [Paragraph("<b>Strengths</b>", body_style), Paragraph(", ".join(swot.get("strengths", [])), body_style)],
        [Paragraph("<b>Weaknesses</b>", body_style), Paragraph(", ".join(swot.get("weaknesses", [])), body_style)],
        [Paragraph("<b>Opportunities</b>", body_style), Paragraph(", ".join(swot.get("opportunities", [])), body_style)],
        [Paragraph("<b>Threats</b>", body_style), Paragraph(", ".join(swot.get("threats", [])), body_style)]
    ]
    t_swot = Table(swot_data, colWidths=[100, 400])
    t_swot.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F1F5F9')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_swot)
    story.append(Spacer(1, 15))
    
    # Risks
    story.append(Paragraph("Risk Matrix", section_heading))
    risk_table_data = [["Risk Description", "Severity", "Likelihood", "Mitigation"]]
    for r in data.get("risks", []):
        risk_table_data.append([
            Paragraph(r.get("description", ""), body_style),
            Paragraph(r.get("severity", ""), body_style),
            Paragraph(r.get("likelihood", ""), body_style),
            Paragraph(r.get("mitigation", ""), body_style)
        ])
    t_risk = Table(risk_table_data, colWidths=[150, 60, 60, 230])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    # For header text color in TableStyle, ReportLab wraps it in Paragraph, so we handle it gracefully.
    story.append(t_risk)
    story.append(Spacer(1, 15))
    
    # Financials
    story.append(Paragraph("Financial Analysis", section_heading))
    fin = data.get("financials", {})
    fin_text = f"<b>Initial Budget:</b> {fin.get('budget', 'TBD')}<br/>" \
               f"<b>Estimated Revenue:</b> {fin.get('estimated_revenue', 'TBD')}<br/>" \
               f"<b>Projected 3-Year ROI:</b> {fin.get('roi_3yr', 'TBD')}<br/>" \
               f"<b>Details:</b> {fin.get('cost_details', 'TBD')}"
    story.append(Paragraph(fin_text, body_style))
    story.append(Spacer(1, 10))
    
    # Technical Review
    story.append(Paragraph("Technical Feasibility & Stack", section_heading))
    tech = data.get("tech_review", {})
    tech_text = f"<b>Feasibility Rating:</b> {tech.get('feasibility', 'Medium')}<br/>" \
                f"<b>Technology Stack:</b> {tech.get('tech_stack', 'TBD')}<br/>" \
                f"<b>Engineering Effort:</b> {tech.get('effort', 'TBD')}<br/>" \
                f"<b>Details:</b> {tech.get('details', 'TBD')}"
    story.append(Paragraph(tech_text, body_style))
    story.append(Spacer(1, 15))
    
    # Action Plan
    story.append(Paragraph("Action Plan", section_heading))
    for idx, act in enumerate(data.get("action_plan", []), 1):
        act_text = f"<b>{idx}. {act.get('phase', f'Phase {idx}')}</b> (Timeline: {act.get('timeline', 'TBD')}): {act.get('details', '')}"
        story.append(Paragraph(act_text, body_style))
        
    doc.build(story)

def generate_pptx_report(data: dict, filepath: str) -> None:
    """Generate a PowerPoint Presentation summarizing the board's decision."""
    prs = Presentation()
    
    # Cover Slide
    slide_layout = prs.slide_layouts[0] # Cover Layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = data.get("title", "Strategic Board Evaluation")
    subtitle.text = f"Prepared by BoardRoom AI\nRecommendation: {data.get('recommendation', 'Proceed')}\nScore: {data.get('decision_score', 75)}/100"
    
    # Executive Summary Slide
    slide_layout = prs.slide_layouts[1] # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Executive Summary"
    tx_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = data.get("executive_summary", "No summary provided.")
    p.font.size = Pt(18)
    
    # SWOT Slide
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "SWOT Analysis"
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(9), Inches(4.8))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    swot = data.get("swot", {})
    for cat in ["strengths", "weaknesses", "opportunities", "threats"]:
        p = tf.add_paragraph()
        p.text = f"{cat.capitalize()}:"
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(2, 132, 199)
        
        items = swot.get(cat, [])
        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"  ? {item}"
            p_item.font.size = Pt(14)
            
    # Financials & Tech Slide
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Financials & Technical Review"
    tx_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    fin = data.get("financials", {})
    tech = data.get("tech_review", {})
    
    p = tf.add_paragraph()
    p.text = "Financial Feasibility:"
    p.font.bold = True
    p.font.size = Pt(16)
    
    for k, v in [("Budget", fin.get("budget")), ("ROI", fin.get("roi_3yr")), ("Rev Estimate", fin.get("estimated_revenue"))]:
        p = tf.add_paragraph()
        p.text = f"  ? {k}: {v}"
        p.font.size = Pt(14)
        
    p = tf.add_paragraph()
    p.text = "\nTechnical Feasibility:"
    p.font.bold = True
    p.font.size = Pt(16)
    
    for k, v in [("Feasibility", tech.get("feasibility")), ("Stack", tech.get("tech_stack")), ("Engineering Effort", tech.get("effort"))]:
        p = tf.add_paragraph()
        p.text = f"  ? {k}: {v}"
        p.font.size = Pt(14)
        
    # Recommendations & Action Slide
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Recommendations & Actions"
    tx_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.add_paragraph()
    p.text = f"Overall Recommendation: {data.get('recommendation')}"
    p.font.bold = True
    p.font.size = Pt(16)
    
    p = tf.add_paragraph()
    p.text = "\nProposed Timeline Phases:"
    p.font.bold = True
    p.font.size = Pt(16)
    
    for act in data.get("action_plan", []):
        p = tf.add_paragraph()
        p.text = f"  ? {act.get('phase')}: {act.get('details')} (Timeline: {act.get('timeline')})"
        p.font.size = Pt(14)
        
    prs.save(filepath)
