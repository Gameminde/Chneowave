#!/usr/bin/env python3
# demo_enhanced_ui.py - Démonstration de l'interface principale améliorée
"""
Démonstration de l'interface CHNeoWave améliorée avec:
- Navigation par onglets fluide
- Validation des champs obligatoires
- Thème sombre/clair
- Transitions automatiques
- Feedback utilisateur
"""

import sys
import os
from typing import Dict, Any

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor

try:
    from hrneowave.gui.enhanced_main_ui import EnhancedMainUI
    from hrneowave.gui.theme import set_light_mode, set_dark_mode
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Assurez-vous que tous les modules sont présents dans src/hrneowave/gui/")
    sys.exit(1)

def create_splash_screen():
    """Crée un écran de démarrage"""
    # Créer une image de splash simple
    pixmap = QPixmap(400, 300)
    pixmap.fill(QColor(45, 52, 54))
    
    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 255))
    
    # Titre
    title_font = QFont("Arial", 24, QFont.Bold)
    painter.setFont(title_font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter | Qt.AlignTop, "CHNeoWave")
    
    # Sous-titre
    subtitle_font = QFont("Arial", 12)
    painter.setFont(subtitle_font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "Laboratoire d'Étude Maritime\nModèles Réduits")
    
    # Version
    version_font = QFont("Arial", 10)
    painter.setFont(version_font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter | Qt.AlignBottom, "Version 2.0.0 - Interface Améliorée")
    
    painter.end()
    
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    return splash

def show_demo_info():
    """Affiche les informations de démonstration"""
    info_text = """
<h3>🚀 Démonstration CHNeoWave Interface Améliorée</h3>

<p><b>Fonctionnalités démontrées :</b></p>
<ul>
<li>✅ <b>Navigation par onglets</b> : Accueil → Calibration → Acquisition → Analyse</li>
<li>✅ <b>Validation des champs obligatoires</b> : Impossible de passer à l'onglet suivant sans remplir les champs requis</li>
<li>✅ <b>Thème sombre/clair</b> : Bouton de basculement dans la barre d'outils</li>
<li>✅ <b>Layout responsive</b> : Optimisé pour 1024×640 minimum, sans scroll vertical</li>
<li>✅ <b>Transitions automatiques</b> : Basculement automatique vers l'analyse après acquisition</li>
<li>✅ <b>Feedback utilisateur</b> : Barre de statut, messages, animations</li>
</ul>

<p><b>Instructions :</b></p>
<ol>
<li>Commencez par l'onglet <b>Accueil</b> et remplissez les champs obligatoires</li>
<li>Passez à la <b>Calibration</b> et configurez les paramètres</li>
<li>Lancez une <b>Acquisition</b> et observez les transitions automatiques</li>
<li>Consultez les résultats dans l'onglet <b>Analyse</b></li>
<li>Testez le basculement de thème avec le bouton 🌙/☀️</li>
</ol>

<p><b>Raccourcis clavier :</b></p>
<ul>
<li><b>Ctrl+T</b> : Basculer le thème</li>
<li><b>F11</b> : Plein écran</li>
<li><b>Ctrl+N</b> : Nouveau projet</li>
<li><b>Ctrl+S</b> : Sauvegarder</li>
</ul>
"""
    
    msg = QMessageBox()
    msg.setWindowTitle("Démonstration CHNeoWave")
    msg.setTextFormat(Qt.RichText)
    msg.setText(info_text)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def main():
    """Fonction principale de démonstration"""
    # Créer l'application
    app = QApplication(sys.argv)
    app.setApplicationName("CHNeoWave Demo")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Laboratoire d'Étude Maritime")
    
    # Écran de démarrage
    splash = create_splash_screen()
    splash.show()
    
    # Simuler le chargement
    splash.showMessage("Initialisation des modules...", Qt.AlignBottom | Qt.AlignCenter, QColor(255, 255, 255))
    app.processEvents()
    QTimer.singleShot(1000, lambda: splash.showMessage("Chargement de l'interface...", Qt.AlignBottom | Qt.AlignCenter, QColor(255, 255, 255)))
    QTimer.singleShot(2000, lambda: splash.showMessage("Prêt!", Qt.AlignBottom | Qt.AlignCenter, QColor(255, 255, 255)))
    
    # Configuration de démonstration
    demo_config = {
        'sample_rate': 32.0,
        'n_channels': 4,
        'max_duration': 300,
        'demo_mode': True,
        'auto_fill_demo_data': True
    }
    
    # Créer l'interface principale
    try:
        main_window = EnhancedMainUI(demo_config)
        
        # Fermer le splash et afficher la fenêtre principale
        QTimer.singleShot(3000, lambda: (
            splash.close(),
            main_window.show(),
            show_demo_info()
        ))
        
        # Démarrer l'application
        return app.exec_()
        
    except Exception as e:
        splash.close()
        QMessageBox.critical(None, "Erreur", f"Impossible de démarrer l'interface:\n{str(e)}")
        return 1

if __name__ == "__main__":
    print("🚀 Démarrage de la démonstration CHNeoWave...")
    print("📋 Interface améliorée avec navigation par onglets")
    print("🎨 Thème sombre/clair et validation des champs")
    print("⚡ Transitions automatiques et feedback utilisateur")
    print()
    
    exit_code = main()
    
    print("\n✅ Démonstration terminée")
    print("Merci d'avoir testé CHNeoWave Interface Améliorée!")
    
    sys.exit(exit_code)