#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de l'interface CHNeoWave
Vérifie que l'application démarre correctement et que l'interface est visible
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_interface():
    """Test de l'interface utilisateur"""
    print("🔍 Test de l'interface CHNeoWave...")
    
    try:
        # Import de Qt
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        # Création de l'application Qt
        app = QApplication(sys.argv)
        
        # Import des modules CHNeoWave
        from src.hrneowave.gui.views.welcome_view import WelcomeView
        from src.hrneowave.gui.view_manager import get_view_manager
        from src.hrneowave.gui.theme import get_stylesheet
        
        print("✅ Imports réussis")
        
        # Test de création de la vue d'accueil
        welcome_view = WelcomeView()
        print(f"✅ WelcomeView créée: {welcome_view}")
        print(f"   - Taille: {welcome_view.size()}")
        print(f"   - Visible: {welcome_view.isVisible()}")
        
        # Test du thème
        stylesheet = get_stylesheet()
        print(f"✅ Thème chargé: {len(stylesheet)} caractères")
        
        # Affichage de la vue
        welcome_view.show()
        welcome_view.raise_()
        print(f"   - Visible après show(): {welcome_view.isVisible()}")
        
        # Timer pour fermer automatiquement
        def close_app():
            print("🔚 Fermeture automatique du test")
            app.quit()
        
        timer = QTimer()
        timer.timeout.connect(close_app)
        timer.start(2000)  # 2 secondes
        
        print("🚀 Lancement de l'interface de test...")
        result = app.exec()
        
        print(f"✅ Test terminé avec code: {result}")
        return result == 0
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_interface()
    if success:
        print("🎉 Test de l'interface réussi !")
    else:
        print("💥 Test de l'interface échoué !")
    sys.exit(0 if success else 1)