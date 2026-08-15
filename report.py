from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from ..config import get_settings

def make_pdf(ev):
    out = Path(get_settings().report_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"vbcua_evaluation_{ev.id}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("VBCUA — Voice-Based Concept Understanding Analysis", styles["Title"]),
        Spacer(1, 8),
        Paragraph(f"<b>Concept:</b> {ev.concept_title}", styles["Normal"]),
        Paragraph(f"<b>Classification:</b> {ev.classification}", styles["Normal"]),
        Paragraph(f"<b>Score:</b> {ev.score}/100", styles["Normal"]),
        Spacer(1, 10),
        Paragraph("Metrics", styles["Heading2"])
    ]
    data = [
        ["Metric", "Value"],
        ["Semantic similarity", f"{ev.semantic_similarity*100:.2f}%"],
        ["Filler count", str(ev.filler_count)],
        ["Filler ratio", f"{ev.filler_ratio*100:.2f}%"],
        ["Pause ratio", f"{ev.pause_ratio*100:.2f}%"],
        ["RMS energy", f"{ev.rms_energy:.5f}"],
        ["Duration", f"{ev.duration_seconds:.2f} sec"],
        ["Speaking rate", f"{ev.speaking_rate_wpm:.1f} WPM"],
    ]
    table = Table(data, colWidths=[80*mm, 80*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#244a73")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), .5, colors.grey),
        ("PADDING", (0,0), (-1,-1), 6)
    ]))
    story += [table, Spacer(1,10), Paragraph("Transcript", styles["Heading2"]),
              Paragraph(ev.transcript or "No transcript.", styles["BodyText"]),
              Spacer(1,10), Paragraph("Recommendations", styles["Heading2"])]
    for tip in ev.recommendations:
        story.append(Paragraph("• " + tip, styles["BodyText"]))
    doc.build(story)
    return path
