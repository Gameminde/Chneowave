#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHNeoWave - Application principale CORRIGÉE
Version: 1.1.0
"""

import sys
import logging
import traceback
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('src/hrneowave/chneowave_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('chneowave')

def main():
    """Point d'entrée principal de l'application CORRIGÉE"""
    try:
        print("[LAUNCH] Lancement de CHNeoWave v1.1.0 - Version Corrigee")
        print("=" * 60)
        
        # Ajouter le chemin du projet
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        print("[STEP 1] Creation QApplication")
        print("-" * 30)
        
        # Import et création de QApplication
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QTimer
        
        # Créer QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            app.setApplicationName("CHNeoWave Corrigé")
            app.setApplicationVersion("1.1.0")
            app.setOrganizationName("CHNeoWave")
        
        print("[OK] QApplication cree")
        
        print("[STEP 2] Application du theme")
        print("-" * 30)
        
        # Application du thème
        try:
            from hrneowave.gui.styles.theme_manager import ThemeManager
            theme_manager = ThemeManager(app=app)
            theme_manager.apply_theme('maritime_modern')
            print("✅ Thème 'maritime_modern' appliqué avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'application du thème: {e}")
            print("⚠️ Continuation sans thème...")
        
        print("✅ Thème maritime appliqué")
        
        print("📋 ÉTAPE 3: Création MainWindow")
        print("-" * 30)
        
        # Import et création de l'écran de lancement
        print("🔄 Import de l'écran de lancement...")
        from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        from PySide6.QtCore import QUrl
        from PySide6.QtWebEngineWidgets import QWebEngineView
        print("✅ Modules d'interface importés")
        
        print("🔄 Création de l'écran de lancement...")
        
        class LaunchScreen(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("CHNeoWave - Écran de Lancement")
                self.setGeometry(100, 100, 1400, 900)
                
                # Widget central avec WebEngine pour afficher launch-screen.html
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                
                layout = QVBoxLayout(central_widget)
                
                # WebEngineView pour afficher l'écran de lancement HTML
                self.web_view = QWebEngineView()
                
                # Charger le fichier launch-screen.html
                html_path = Path(__file__).parent / "launch-screen.html"
                if html_path.exists():
                    self.web_view.load(QUrl.fromLocalFile(str(html_path.absolute())))
                else:
                    # Fallback si le fichier n'existe pas
                    self.web_view.setHtml("""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>CHNeoWave - Écran de Lancement</title>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; }
                            .container { max-width: 1200px; margin: 0 auto; text-align: center; }
                            h1 { font-size: 3em; margin-bottom: 20px; }
                            .subtitle { font-size: 1.2em; margin-bottom: 40px; opacity: 0.9; }
                            .actions { display: flex; justify-content: center; gap: 20px; margin: 40px 0; }
                            .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; min-width: 200px; cursor: pointer; transition: transform 0.3s; }
                            .card:hover { transform: translateY(-5px); }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>🌊 CHNeoWave</h1>
                            <p class="subtitle">Laboratoire Maritime - Interface de Houle</p>
                            <div class="actions">
                                <div class="card" onclick="createProject()">
                                    <h3>📋 Nouveau Projet</h3>
                                    <p>Créer un nouveau projet d'étude maritime</p>
                                </div>
                                <div class="card" onclick="openProject()">
                                    <h3>📂 Ouvrir Projet</h3>
                                    <p>Ouvrir un projet existant</p>
                                </div>
                            </div>
                        </div>
                        <script>
                            function createProject() { alert('Création de nouveau projet'); }
                            function openProject() { alert('Ouverture de projet'); }
                        </script>
                    </body>
                    </html>
                    """)
                
                layout.addWidget(self.web_view)
        
        main_window = LaunchScreen()
        print("✅ Écran de lancement créé")
        
        print("📋 ÉTAPE 4: Configuration de l'affichage")
        print("-" * 30)
        
        # Configuration de l'affichage
        main_window.setWindowTitle("CHNeoWave - Écran de Lancement")
        main_window.resize(1400, 900)
        
        # Centrer la fenêtre
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = main_window.geometry()
        
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        main_window.move(x, y)
        
        print("✅ Fenêtre configurée et centrée")
        
        print("📋 ÉTAPE 5: Affichage de l'interface")
        print("-" * 30)
        
        # Affichage de l'interface
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        
        # Vérifier la visibilité
        visible = main_window.isVisible()
        print(f"✅ MainWindow visible: {visible}")
        
        if not visible:
            print("⚠️ Fenêtre non visible, tentative de correction...")
            main_window.showNormal()
            main_window.show()
            visible = main_window.isVisible()
            print(f"✅ MainWindow visible après correction: {visible}")
        
        print("✅ Interface affichée avec succès")
        print("🎉 CHNeoWave est maintenant opérationnel !")
        print("🔍 Vérifiez que la fenêtre est visible sur votre écran")
        
        print("📋 ÉTAPE 6: Lancement de la boucle d'événements")
        print("-" * 30)
        
        # Timer pour fermeture automatique après 30 secondes (optionnel)
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(30000)  # 30 secondes
        
        print("🔄 Lancement de la boucle d'événements (30 secondes)...")
        
        # Lancer la boucle d'événements
        exit_code = app.exec()
        print(f"[SUCCESS] Application terminee (code: {exit_code})")
        return exit_code
        
    except Exception as e:
        print(f"[ERROR] Erreur lors de la creation de MainWindow: {e}")
        print("[DEBUG] Traceback complet:")
        traceback.print_exc()
        print(f"[CRITICAL] ERREUR CRITIQUE: {e}")
        print("[DEBUG] Traceback complet:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
