#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Qt Minimal avec Debug Complet
Pour diagnostiquer pourquoi aucune fenêtre n'apparaît
"""

import sys
import os
import platform
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QScreen

class TestQtMinimal(QMainWindow):
    """Test Qt le plus simple possible"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.debug_info()
        
    def setup_ui(self):
        """Configuration UI minimale"""
        self.setWindowTitle("🚨 TEST QT MINIMAL - CETTE FENÊTRE DOIT ÊTRE VISIBLE 🚨")
        self.setGeometry(100, 100, 600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titre très visible
        titre = QLabel("🔥 SI VOUS VOYEZ CECI, QT FONCTIONNE! 🔥")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont("Arial", 20, QFont.Bold))
        titre.setStyleSheet("""
            QLabel {
                background: #FF0000;
                color: #FFFFFF;
                padding: 30px;
                border: 5px solid #000000;
                border-radius: 15px;
                margin: 20px;
            }
        """)
        layout.addWidget(titre)
        
        # Message d'état
        self.message = QLabel("⏳ Initialisation...")
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFont(QFont("Arial", 14))
        self.message.setStyleSheet("""
            QLabel {
                background: #FFFF00;
                color: #000000;
                padding: 20px;
                border: 3px solid #FF0000;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.message)
        
        # Bouton test
        btn_test = QPushButton("🎯 CLIQUEZ ICI POUR TESTER")
        btn_test.setFont(QFont("Arial", 16, QFont.Bold))
        btn_test.setStyleSheet("""
            QPushButton {
                background: #00FF00;
                color: #000000;
                border: 4px solid #0000FF;
                padding: 20px;
                border-radius: 12px;
                margin: 15px;
            }
            QPushButton:hover {
                background: #00AA00;
            }
        """)
        btn_test.clicked.connect(self.test_clique)
        layout.addWidget(btn_test)
        
        # Info système
        self.info_systeme = QLabel("📊 Chargement des informations système...")
        self.info_systeme.setWordWrap(True)
        self.info_systeme.setFont(QFont("Courier", 10))
        self.info_systeme.setStyleSheet("""
            QLabel {
                background: #F0F0F0;
                border: 2px solid #808080;
                padding: 15px;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.info_systeme)
        
        # Démarrer le timer pour les infos
        QTimer.singleShot(1000, self.afficher_infos_systeme)
        
    def debug_info(self):
        """Afficher les informations de debug"""
        print("\n" + "="*60)
        print("🔍 DEBUG QT MINIMAL")
        print("="*60)
        print(f"✅ Fenêtre créée: {self.windowTitle()}")
        print(f"✅ Géométrie: {self.geometry()}")
        print(f"✅ Visible: {self.isVisible()}")
        print(f"✅ Actif: {self.isActiveWindow()}")
        print("="*60)
        
    def test_clique(self):
        """Test du clic"""
        self.message.setText("✅ BOUTON CLIQUÉ! L'INTERFACE FONCTIONNE!")
        self.message.setStyleSheet("""
            QLabel {
                background: #00FF00;
                color: #000000;
                padding: 20px;
                border: 3px solid #0000FF;
                border-radius: 10px;
                margin: 10px;
                font-weight: bold;
            }
        """)
        print("🎯 BOUTON CLIQUÉ - INTERFACE INTERACTIVE!")
        
    def afficher_infos_systeme(self):
        """Afficher les informations système"""
        try:
            app = QApplication.instance()
            
            infos = []
            infos.append(f"🖥️ Système: {platform.system()} {platform.release()}")
            infos.append(f"🐍 Python: {sys.version.split()[0]}")
            infos.append(f"🎨 Qt Platform: {app.platformName()}")
            infos.append(f"📺 Écrans: {len(app.screens())}")
            
            for i, screen in enumerate(app.screens()):
                geom = screen.geometry()
                infos.append(f"   Écran {i+1}: {geom.width()}x{geom.height()} @ ({geom.x()}, {geom.y()})")
            
            infos.append(f"🪟 Fenêtre visible: {self.isVisible()}")
            infos.append(f"🪟 Fenêtre active: {self.isActiveWindow()}")
            infos.append(f"🪟 Position: ({self.x()}, {self.y()})")
            infos.append(f"🪟 Taille: {self.width()}x{self.height()}")
            
            # Variables d'environnement importantes
            env_vars = ['QT_QPA_PLATFORM', 'DISPLAY', 'QT_SCALE_FACTOR', 'QT_AUTO_SCREEN_SCALE_FACTOR']
            for var in env_vars:
                value = os.getenv(var, 'Non défini')
                infos.append(f"🔧 {var}: {value}")
            
            self.info_systeme.setText("\n".join(infos))
            self.message.setText("📊 Informations système chargées")
            
            # Afficher aussi dans la console
            print("\n📊 INFORMATIONS SYSTÈME:")
            for info in infos:
                print(f"   {info}")
                
        except Exception as e:
            error_msg = f"❌ Erreur lors du chargement des infos: {e}"
            self.info_systeme.setText(error_msg)
            print(error_msg)
    
    def showEvent(self, event):
        """Événement d'affichage"""
        super().showEvent(event)
        print(f"🎯 showEvent déclenché - Fenêtre affichée!")
        print(f"   Visible: {self.isVisible()}")
        print(f"   Géométrie: {self.geometry()}")
    
    def closeEvent(self, event):
        """Événement de fermeture"""
        print("🔚 Fermeture de la fenêtre de test")
        super().closeEvent(event)

def main():
    """Fonction principale"""
    print("\n" + "🚨"*30)
    print("🔥 TEST QT MINIMAL - DIAGNOSTIC COMPLET")
    print("🚨"*30)
    print("🎯 OBJECTIF: Vérifier si Qt peut afficher une fenêtre")
    print("👀 REGARDEZ VOTRE ÉCRAN - Une fenêtre ROUGE doit apparaître")
    print("🔍 Si aucune fenêtre n'apparaît, le problème vient de Qt/système")
    print("✅ Si une fenêtre apparaît, le problème vient de CHNeoWave")
    print("")
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    print(f"✅ QApplication créée")
    print(f"   Platform: {app.platformName()}")
    print(f"   Écrans disponibles: {len(app.screens())}")
    
    # Créer la fenêtre de test
    window = TestQtMinimal()
    
    print(f"✅ Fenêtre de test créée")
    
    # Afficher la fenêtre
    window.show()
    window.raise_()
    window.activateWindow()
    
    print(f"✅ show() appelé")
    print(f"   Visible après show(): {window.isVisible()}")
    print(f"   Géométrie: {window.geometry()}")
    print("")
    print("🔍 VÉRIFIEZ MAINTENANT VOTRE ÉCRAN!")
    print("   → Une fenêtre avec un fond ROUGE doit être visible")
    print("   → Si vous la voyez, cliquez sur le bouton vert")
    print("   → Si vous ne la voyez pas, il y a un problème Qt/système")
    print("")
    
    # Lancer la boucle d'événements
    exit_code = app.exec()
    
    print(f"\n🏁 Application fermée avec code: {exit_code}")
    return exit_code

if __name__ == "__main__":
    try:
        exit_code = main()
        print(f"\n✅ Test terminé normalement (code: {exit_code})")
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)