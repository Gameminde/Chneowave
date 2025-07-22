"""
Module pour la génération de rapports de calibration au format PDF.
"""

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import datetime

def generate_calibration_report(filename, calibration_data):
    """
    Génère un rapport de calibration PDF.

    Args:
        filename (str): Le chemin du fichier PDF à créer.
        calibration_data (dict): Un dictionnaire contenant les données de calibration.
            Exemple:
            {
                'sonde_id': 1,
                'date': '2023-10-27',
                'slope': 0.1,
                'intercept': 0.01,
                'r2': 0.999,
                'points': [(1, 0.11), (2, 0.21)],
                'graph_path': 'path/to/graph.png'
            }
    """
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Titre
    title = Paragraph(f"Rapport de Calibration - Sonde {calibration_data['sonde_id']}", styles['h1'])
    story.append(title)
    story.append(Spacer(1, 1 * cm))

    # Informations générales
    story.append(Paragraph(f"Date de calibration: {calibration_data['date']}", styles['Normal']))
    story.append(Spacer(1, 0.5 * cm))

    # Résultats de la régression
    story.append(Paragraph("<b>Résultats de la régression linéaire</b>", styles['h2']))
    story.append(Paragraph(f"Pente (facteur de calibration): {calibration_data['slope']:.4f}", styles['Normal']))
    story.append(Paragraph(f"Ordonnée à l'origine: {calibration_data['intercept']:.4f}", styles['Normal']))
    story.append(Paragraph(f"Coefficient de détermination (R²): {calibration_data['r2']:.4f}", styles['Normal']))
    story.append(Spacer(1, 1 * cm))

    # Tableau des points de calibration
    story.append(Paragraph("<b>Points de calibration</b>", styles['h2']))
    table_data = [['Hauteur (m)', 'Tension (V)'], *calibration_data['points']]
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 1 * cm))

    # Graphique
    if 'graph_path' in calibration_data and calibration_data['graph_path']:
        story.append(Paragraph("<b>Graphique de calibration</b>", styles['h2']))
        img = Image(calibration_data['graph_path'], width=15*cm, height=10*cm)
        story.append(img)

    doc.build(story)