#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de certificats de calibration PDF pour CHNeoWave v1.1.0-RC
Pour laboratoires d'études maritimes en modèle réduit
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import json

# Import conditionnel pour la génération PDF
try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.platypus import PageBreak, KeepTogether
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Line
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics.charts.axes import XCategoryAxis, YValueAxis
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab non disponible - génération PDF désactivée")

@dataclass
class CalibrationData:
    """Données de calibration pour un capteur"""
    sensor_id: str
    sensor_type: str  # 'wave_probe', 'pressure', 'force'
    channel: int
    
    # Données de calibration
    reference_values: List[float]  # Valeurs de référence (unités physiques)
    measured_values: List[float]   # Valeurs mesurées (volts)
    
    # Résultats de calibration
    slope: float
    intercept: float
    r_squared: float
    
    # Métadonnées
    calibration_date: datetime
    operator: str
    equipment_used: str
    environmental_conditions: Dict[str, Any]
    
    # Limites et spécifications
    measurement_range: Tuple[float, float]
    accuracy_spec: float  # Précision spécifiée (%)
    linearity_spec: float  # Linéarité spécifiée (%)
    
    def __post_init__(self):
        if len(self.reference_values) != len(self.measured_values):
            raise ValueError("Les listes de valeurs de référence et mesurées doivent avoir la même longueur")

@dataclass
class CertificateConfig:
    """Configuration pour la génération de certificat"""
    laboratory_name: str
    laboratory_address: str
    certificate_number: str
    
    # Informations client
    client_name: str = ""
    client_address: str = ""
    
    # Informations sur l'équipement calibré
    equipment_model: str = "CHNeoWave"
    equipment_serial: str = ""
    
    # Validité du certificat
    validity_period_months: int = 12
    
    # Logo et signature
    logo_path: Optional[str] = None
    signature_path: Optional[str] = None
    
    # Normes de référence
    reference_standards: List[str] = None
    
    def __post_init__(self):
        if self.reference_standards is None:
            self.reference_standards = [
                "ISO/IEC 17025:2017",
                "ITTC Recommended Procedures 7.5-02-07-02.1"
            ]

class CalibrationCertificateGenerator:
    """Générateur de certificats de calibration PDF"""
    
    def __init__(self):
        self.available = REPORTLAB_AVAILABLE
        if not self.available:
            print("Générateur PDF non disponible - ReportLab requis")
    
    def generate_certificate(self, calibration_data: List[CalibrationData], 
                           config: CertificateConfig, 
                           output_path: str) -> bool:
        """
        Génère un certificat de calibration PDF
        
        Args:
            calibration_data: Liste des données de calibration par capteur
            config: Configuration du certificat
            output_path: Chemin de sortie du PDF
            
        Returns:
            True si la génération a réussi
        """
        if not self.available:
            print("Génération PDF non disponible")
            return False
        
        try:
            # Créer le document PDF
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Construire le contenu
            story = []
            
            # Page de titre
            story.extend(self._create_title_page(config))
            story.append(PageBreak())
            
            # Résumé exécutif
            story.extend(self._create_executive_summary(calibration_data, config))
            story.append(PageBreak())
            
            # Détails de calibration pour chaque capteur
            for i, calib in enumerate(calibration_data):
                story.extend(self._create_sensor_details(calib, config))
                if i < len(calibration_data) - 1:
                    story.append(PageBreak())
            
            # Annexes
            story.append(PageBreak())
            story.extend(self._create_appendices(calibration_data, config))
            
            # Générer le PDF
            doc.build(story)
            
            print(f"Certificat de calibration généré: {output_path}")
            return True
            
        except Exception as e:
            print(f"Erreur génération certificat: {e}")
            return False
    
    def _create_title_page(self, config: CertificateConfig) -> List:
        """Crée la page de titre"""
        styles = getSampleStyleSheet()
        story = []
        
        # Logo si disponible
        if config.logo_path and Path(config.logo_path).exists():
            try:
                logo = Image(config.logo_path, width=3*inch, height=1.5*inch)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 0.5*inch))
            except:
                pass
        
        # Titre principal
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph("CERTIFICAT DE CALIBRATION", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Sous-titre
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=16,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph("Système d'Acquisition CHNeoWave", subtitle_style))
        story.append(Paragraph("Laboratoire d'Études Maritimes en Modèle Réduit", subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Informations du certificat
        cert_info = [
            ["Numéro de certificat:", config.certificate_number],
            ["Date d'émission:", datetime.now().strftime("%d/%m/%Y")],
            ["Validité:", f"{config.validity_period_months} mois"],
            ["Date d'expiration:", (datetime.now() + timedelta(days=config.validity_period_months*30)).strftime("%d/%m/%Y")]
        ]
        
        cert_table = Table(cert_info, colWidths=[3*inch, 2*inch])
        cert_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(cert_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Informations laboratoire
        lab_style = ParagraphStyle(
            'LabInfo',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        story.append(Paragraph(f"<b>{config.laboratory_name}</b>", lab_style))
        story.append(Paragraph(config.laboratory_address, lab_style))
        
        return story
    
    def _create_executive_summary(self, calibration_data: List[CalibrationData], 
                                config: CertificateConfig) -> List:
        """Crée le résumé exécutif"""
        styles = getSampleStyleSheet()
        story = []
        
        # Titre de section
        story.append(Paragraph("RÉSUMÉ EXÉCUTIF", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informations générales
        general_info = [
            ["Équipement calibré:", config.equipment_model],
            ["Numéro de série:", config.equipment_serial or "N/A"],
            ["Client:", config.client_name or "Laboratoire interne"],
            ["Nombre de capteurs:", str(len(calibration_data))],
            ["Date de calibration:", calibration_data[0].calibration_date.strftime("%d/%m/%Y") if calibration_data else "N/A"]
        ]
        
        info_table = Table(general_info, colWidths=[3*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Tableau de résumé des résultats
        story.append(Paragraph("Résultats de Calibration", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        # En-têtes du tableau
        headers = ["Capteur", "Canal", "Type", "R²", "Précision", "Statut"]
        results_data = [headers]
        
        for calib in calibration_data:
            # Calculer la précision réelle
            precision = self._calculate_precision(calib)
            status = "✓ Conforme" if precision <= calib.accuracy_spec else "✗ Non conforme"
            
            row = [
                calib.sensor_id,
                str(calib.channel),
                calib.sensor_type,
                f"{calib.r_squared:.4f}",
                f"{precision:.2f}%",
                status
            ]
            results_data.append(row)
        
        results_table = Table(results_data, colWidths=[1.2*inch, 0.8*inch, 1.2*inch, 0.8*inch, 1*inch, 1.2*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Conclusion
        story.append(Paragraph("Conclusion", styles['Heading2']))
        
        conforming_sensors = sum(1 for calib in calibration_data 
                               if self._calculate_precision(calib) <= calib.accuracy_spec)
        total_sensors = len(calibration_data)
        
        conclusion_text = f"""
        La calibration a été effectuée selon les procédures du laboratoire et les normes internationales.
        {conforming_sensors} capteur(s) sur {total_sensors} respecte(nt) les spécifications de précision.
        
        Les capteurs conformes peuvent être utilisés pour les mesures dans la plage de calibration spécifiée.
        """
        
        story.append(Paragraph(conclusion_text, styles['Normal']))
        
        return story
    
    def _create_sensor_details(self, calib: CalibrationData, config: CertificateConfig) -> List:
        """Crée les détails pour un capteur"""
        styles = getSampleStyleSheet()
        story = []
        
        # Titre du capteur
        sensor_title = f"CAPTEUR {calib.sensor_id} - CANAL {calib.channel}"
        story.append(Paragraph(sensor_title, styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        # Informations du capteur
        sensor_info = [
            ["Type de capteur:", calib.sensor_type],
            ["Plage de mesure:", f"{calib.measurement_range[0]} - {calib.measurement_range[1]}"],
            ["Date de calibration:", calib.calibration_date.strftime("%d/%m/%Y %H:%M")],
            ["Opérateur:", calib.operator],
            ["Équipement utilisé:", calib.equipment_used]
        ]
        
        info_table = Table(sensor_info, colWidths=[2.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Conditions environnementales
        if calib.environmental_conditions:
            story.append(Paragraph("Conditions Environnementales", styles['Heading2']))
            
            env_data = []
            for key, value in calib.environmental_conditions.items():
                env_data.append([key.replace('_', ' ').title(), str(value)])
            
            env_table = Table(env_data, colWidths=[2.5*inch, 3.5*inch])
            env_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            story.append(env_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Résultats de calibration
        story.append(Paragraph("Résultats de Calibration", styles['Heading2']))
        
        precision = self._calculate_precision(calib)
        linearity = self._calculate_linearity(calib)
        
        results_info = [
            ["Pente (Sensibilité):", f"{calib.slope:.6f}"],
            ["Ordonnée à l'origine:", f"{calib.intercept:.6f}"],
            ["Coefficient de corrélation (R²):", f"{calib.r_squared:.6f}"],
            ["Précision mesurée:", f"{precision:.3f}%"],
            ["Linéarité:", f"{linearity:.3f}%"],
            ["Spécification précision:", f"{calib.accuracy_spec:.1f}%"],
            ["Spécification linéarité:", f"{calib.linearity_spec:.1f}%"]
        ]
        
        results_table = Table(results_info, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(results_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Graphique de calibration (si matplotlib disponible)
        try:
            graph_path = self._create_calibration_graph(calib)
            if graph_path:
                story.append(Paragraph("Courbe de Calibration", styles['Heading2']))
                graph_img = Image(graph_path, width=5*inch, height=3.5*inch)
                graph_img.hAlign = 'CENTER'
                story.append(graph_img)
                
                # Nettoyer le fichier temporaire
                Path(graph_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Erreur création graphique: {e}")
        
        return story
    
    def _create_appendices(self, calibration_data: List[CalibrationData], 
                          config: CertificateConfig) -> List:
        """Crée les annexes"""
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph("ANNEXES", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        # Normes de référence
        story.append(Paragraph("Normes de Référence", styles['Heading2']))
        
        for standard in config.reference_standards:
            story.append(Paragraph(f"• {standard}", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Procédure de calibration
        story.append(Paragraph("Procédure de Calibration", styles['Heading2']))
        
        procedure_text = """
        1. Vérification de l'état des équipements de mesure
        2. Stabilisation thermique (minimum 30 minutes)
        3. Vérification du zéro
        4. Application des valeurs de référence par points croissants
        5. Répétition en points décroissants
        6. Calcul de la droite de régression
        7. Évaluation de la linéarité et de la répétabilité
        """
        
        story.append(Paragraph(procedure_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Signature
        if config.signature_path and Path(config.signature_path).exists():
            try:
                signature = Image(config.signature_path, width=2*inch, height=1*inch)
                signature.hAlign = 'RIGHT'
                story.append(Spacer(1, 0.5*inch))
                story.append(signature)
            except:
                pass
        
        # Informations de contact
        story.append(Spacer(1, 0.3*inch))
        contact_style = ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER
        )
        
        story.append(Paragraph(f"Ce certificat est émis par {config.laboratory_name}", contact_style))
        story.append(Paragraph(config.laboratory_address, contact_style))
        
        return story
    
    def _calculate_precision(self, calib: CalibrationData) -> float:
        """Calcule la précision en pourcentage"""
        if not calib.reference_values or not calib.measured_values:
            return 100.0
        
        # Calculer les valeurs prédites
        predicted = np.array(calib.measured_values) * calib.slope + calib.intercept
        reference = np.array(calib.reference_values)
        
        # Erreur relative moyenne
        relative_errors = np.abs((predicted - reference) / reference) * 100
        return np.mean(relative_errors)
    
    def _calculate_linearity(self, calib: CalibrationData) -> float:
        """Calcule la linéarité en pourcentage"""
        if len(calib.reference_values) < 3:
            return 0.0
        
        # Écart maximum par rapport à la droite de régression
        predicted = np.array(calib.measured_values) * calib.slope + calib.intercept
        reference = np.array(calib.reference_values)
        
        max_deviation = np.max(np.abs(predicted - reference))
        full_scale = max(calib.measurement_range) - min(calib.measurement_range)
        
        return (max_deviation / full_scale) * 100 if full_scale > 0 else 0.0
    
    def _create_calibration_graph(self, calib: CalibrationData) -> Optional[str]:
        """Crée un graphique de calibration"""
        try:
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Points de mesure
            ax.scatter(calib.measured_values, calib.reference_values, 
                      color='blue', s=50, alpha=0.7, label='Points de mesure')
            
            # Droite de régression
            x_line = np.linspace(min(calib.measured_values), max(calib.measured_values), 100)
            y_line = x_line * calib.slope + calib.intercept
            ax.plot(x_line, y_line, 'r-', linewidth=2, label=f'Régression (R² = {calib.r_squared:.4f})')
            
            # Mise en forme
            ax.set_xlabel('Valeur mesurée (V)')
            ax.set_ylabel('Valeur de référence')
            ax.set_title(f'Calibration {calib.sensor_id} - Canal {calib.channel}')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Équation de la droite
            equation = f'y = {calib.slope:.4f}x + {calib.intercept:.4f}'
            ax.text(0.05, 0.95, equation, transform=ax.transAxes, 
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            # Sauvegarder temporairement
            temp_path = f'temp_calib_graph_{calib.sensor_id}_{calib.channel}.png'
            plt.savefig(temp_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return temp_path
            
        except Exception as e:
            print(f"Erreur création graphique: {e}")
            return None

# Factory functions
def create_calibration_certificate_generator() -> CalibrationCertificateGenerator:
    """Crée un générateur de certificats"""
    return CalibrationCertificateGenerator()

def create_sample_calibration_data() -> List[CalibrationData]:
    """Crée des données d'exemple pour test"""
    # Données d'exemple pour 4 capteurs de houle
    sample_data = []
    
    for i in range(4):
        # Valeurs de référence (hauteurs d'eau en mm)
        ref_values = [0, 50, 100, 150, 200, 250, 300]
        # Valeurs mesurées simulées (volts) avec un peu de bruit
        measured_values = [0.1 + val * 0.02 + np.random.normal(0, 0.001) for val in ref_values]
        
        # Régression linéaire
        slope, intercept = np.polyfit(measured_values, ref_values, 1)
        r_squared = np.corrcoef(measured_values, ref_values)[0, 1] ** 2
        
        calib = CalibrationData(
            sensor_id=f"WP{i+1:02d}",
            sensor_type="wave_probe",
            channel=i,
            reference_values=ref_values,
            measured_values=measured_values,
            slope=slope,
            intercept=intercept,
            r_squared=r_squared,
            calibration_date=datetime.now(),
            operator="Technicien Calibration",
            equipment_used="Étalon de hauteur d'eau certifié",
            environmental_conditions={
                "température": "20.5°C",
                "humidité": "45%",
                "pression": "1013.2 hPa"
            },
            measurement_range=(0, 300),
            accuracy_spec=1.0,  # 1%
            linearity_spec=0.5   # 0.5%
        )
        
        sample_data.append(calib)
    
    return sample_data