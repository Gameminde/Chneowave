#!/usr/bin/env python3
"""
Script de polissage interface utilisateur CHNeoWave v1.1.0-beta
Amélioration de l'expérience utilisateur et finalisation des détails visuels
"""

import os
import sys
from pathlib import Path
import re

def polish_export_view():
    """Améliore l'interface d'exportation"""
    export_view_path = Path('src/hrneowave/gui/views/export_view.py')
    
    if not export_view_path.exists():
        print("❌ Fichier export_view.py non trouvé")
        return False
    
    with open(export_view_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Améliorations de l'interface d'exportation
    improvements = [
        # Améliorer les tooltips
        {
            'pattern': r'self\.export_hdf5_check\.setToolTip\("[^"]*"\)',
            'replacement': 'self.export_hdf5_check.setToolTip("Export des données brutes au format HDF5 scientifique avec traçabilité SHA-256")'
        },
        # Améliorer le texte du bouton PDF calibration
        {
            'pattern': r'"Données HDF5 \(scientifique\)"',
            'replacement': '"📊 Données HDF5 (scientifique)"'
        }
    ]
    
    modified = False
    for improvement in improvements:
        if re.search(improvement['pattern'], content):
            content = re.sub(improvement['pattern'], improvement['replacement'], content)
            modified = True
    
    if modified:
        with open(export_view_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Interface d'exportation améliorée")
    
    return True

def polish_calibration_view():
    """Améliore l'interface de calibration"""
    calib_view_path = Path('src/hrneowave/gui/views/calibration_view.py')
    
    if not calib_view_path.exists():
        print("❌ Fichier calibration_view.py non trouvé")
        return False
    
    with open(calib_view_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Améliorations de l'interface de calibration
    improvements = [
        # Améliorer le texte du bouton PDF
        {
            'pattern': r'"Exporter PDF"',
            'replacement': '"📄 Certificat PDF"'
        },
        # Améliorer le tooltip du bouton PDF
        {
            'pattern': r'self\.export_pdf_btn\.setToolTip\("[^"]*"\)',
            'replacement': 'self.export_pdf_btn.setToolTip("Générer un certificat PDF de calibration avec signature numérique")'
        }
    ]
    
    modified = False
    for improvement in improvements:
        if re.search(improvement['pattern'], content):
            content = re.sub(improvement['pattern'], improvement['replacement'], content)
            modified = True
    
    # Ajouter tooltip si pas présent
    if 'self.export_pdf_btn.setToolTip' not in content:
        # Chercher la ligne après la création du bouton
        pattern = r'(self\.export_pdf_btn = QPushButton\("[^"]*"\))'
        replacement = r'\1\n        self.export_pdf_btn.setToolTip("Générer un certificat PDF de calibration avec signature numérique")'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
    
    if modified:
        with open(calib_view_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Interface de calibration améliorée")
    
    return True

def add_status_indicators():
    """Ajoute des indicateurs de statut visuels"""
    # Créer un fichier de styles CSS pour l'application
    styles_content = """
/* CHNeoWave v1.1.0-beta - Styles d'interface */

/* Boutons d'action principaux */
QPushButton[class="primary"] {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton[class="primary"]:hover {
    background-color: #1976D2;
}

QPushButton[class="primary"]:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

/* Boutons de succès */
QPushButton[class="success"] {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}

QPushButton[class="success"]:hover {
    background-color: #388E3C;
}

/* Boutons d'export */
QPushButton[class="export"] {
    background-color: #FF9800;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}

QPushButton[class="export"]:hover {
    background-color: #F57C00;
}

/* Cases à cocher avec icônes */
QCheckBox[class="feature"] {
    font-weight: 500;
    spacing: 8px;
}

QCheckBox[class="feature"]::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox[class="feature"]::indicator:checked {
    background-color: #4CAF50;
    border: 2px solid #4CAF50;
    border-radius: 3px;
}

QCheckBox[class="feature"]::indicator:unchecked {
    background-color: white;
    border: 2px solid #BDBDBD;
    border-radius: 3px;
}

/* Barres de progression */
QProgressBar {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    text-align: center;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 3px;
}

/* Labels de statut */
QLabel[class="status-success"] {
    color: #4CAF50;
    font-weight: bold;
}

QLabel[class="status-error"] {
    color: #F44336;
    font-weight: bold;
}

QLabel[class="status-warning"] {
    color: #FF9800;
    font-weight: bold;
}

/* Groupes de contrôles */
QGroupBox {
    font-weight: bold;
    border: 2px solid #BDBDBD;
    border-radius: 8px;
    margin-top: 1ex;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}
"""
    
    styles_path = Path('src/hrneowave/gui/styles/app_styles.css')
    styles_path.parent.mkdir(exist_ok=True)
    
    with open(styles_path, 'w', encoding='utf-8') as f:
        f.write(styles_content)
    
    print("✅ Fichier de styles CSS créé")
    return True

def create_icons_module():
    """Crée un module d'icônes SVG intégrées"""
    icons_content = '''
"""
Module d'icônes SVG pour CHNeoWave v1.1.0-beta
Icônes vectorielles intégrées pour l'interface utilisateur
"""

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray, QSize

# Icônes SVG en base64 ou directement en XML
ICONS = {
    'export_hdf5': '''
    <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="2" width="12" height="12" rx="2" fill="#2196F3" stroke="#1976D2" stroke-width="1"/>
        <text x="8" y="10" text-anchor="middle" fill="white" font-size="6" font-weight="bold">H5</text>
    </svg>
    ''',
    
    'export_pdf': '''
    <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="1" width="10" height="14" rx="1" fill="#F44336" stroke="#D32F2F" stroke-width="1"/>
        <text x="7" y="9" text-anchor="middle" fill="white" font-size="5" font-weight="bold">PDF</text>
    </svg>
    ''',
    
    'calibration': '''
    <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
        <circle cx="8" cy="8" r="6" fill="#4CAF50" stroke="#388E3C" stroke-width="1"/>
        <path d="M5 8 L7 10 L11 6" stroke="white" stroke-width="2" fill="none" stroke-linecap="round"/>
    </svg>
    ''',
    
    'acquisition': '''
    <svg width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
        <rect x="1" y="12" width="2" height="3" fill="#2196F3"/>
        <rect x="4" y="8" width="2" height="7" fill="#2196F3"/>
        <rect x="7" y="4" width="2" height="11" fill="#2196F3"/>
        <rect x="10" y="6" width="2" height="9" fill="#2196F3"/>
        <rect x="13" y="10" width="2" height="5" fill="#2196F3"/>
    </svg>
    '''
}

def create_icon(icon_name, size=16):
    """
    Crée une QIcon à partir d'un SVG
    
    Args:
        icon_name (str): Nom de l'icône dans le dictionnaire ICONS
        size (int): Taille de l'icône en pixels
    
    Returns:
        QIcon: Icône prête à utiliser
    """
    if icon_name not in ICONS:
        return QIcon()  # Icône vide si non trouvée
    
    svg_data = ICONS[icon_name].encode('utf-8')
    renderer = QSvgRenderer(QByteArray(svg_data))
    
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

def get_icon(name, size=16):
    """Raccourci pour créer une icône"""
    return create_icon(name, size)
'''
    
    icons_path = Path('src/hrneowave/gui/icons.py')
    
    with open(icons_path, 'w', encoding='utf-8') as f:
        f.write(icons_content)
    
    print("✅ Module d'icônes SVG créé")
    return True

def update_version_info():
    """Met à jour les informations de version"""
    version_files = [
        'src/hrneowave/__init__.py',
        'src/hrneowave/core/version.py'
    ]
    
    for version_file in version_files:
        file_path = Path(version_file)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Mettre à jour la version
            content = re.sub(
                r'__version__\s*=\s*["\'][^"\']["\']',
                '__version__ = "1.1.0-beta"',
                content
            )
            
            # Ajouter des métadonnées si nécessaire
            if 'CHNeoWave' not in content:
                metadata = '''
# CHNeoWave - Logiciel d'acquisition et d'analyse de données maritimes
# Version 1.1.0-beta - Laboratoire d'études maritimes modèle réduit
# Développé pour les bassins et canaux méditerranéens
'''
                content = metadata + '\n' + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Version mise à jour: {version_file}")
    
    return True

def main():
    """Fonction principale de polissage"""
    print("🎨 CHNeoWave v1.1.0-beta - Polissage Interface Utilisateur")
    print("Amélioration de l'expérience utilisateur\n")
    
    tasks = [
        ("Interface d'exportation", polish_export_view),
        ("Interface de calibration", polish_calibration_view),
        ("Indicateurs de statut", add_status_indicators),
        ("Module d'icônes", create_icons_module),
        ("Informations de version", update_version_info)
    ]
    
    success_count = 0
    
    for task_name, task_func in tasks:
        print(f"🔧 {task_name}...")
        try:
            if task_func():
                success_count += 1
            else:
                print(f"⚠️  Problème avec: {task_name}")
        except Exception as e:
            print(f"❌ Erreur {task_name}: {e}")
    
    print(f"\n✨ Polissage terminé: {success_count}/{len(tasks)} tâches réussies")
    
    if success_count == len(tasks):
        print("🎉 Interface utilisateur entièrement polie!")
        return True
    else:
        print("⚠️  Certaines améliorations ont échoué")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)