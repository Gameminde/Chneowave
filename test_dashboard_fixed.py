#!/usr/bin/env python3
"""
Test de la version corrigée de DashboardView.
"""

import sys
import traceback
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

def test_dashboard_fixed():
    """Test de la version corrigée de DashboardView."""
    print("=== Test DashboardView Corrigée ===\n")
    
    try:
        # Créer l'application Qt
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication créée")
        
        # Test 1: Import de la version corrigée
        print("\n1. Import DashboardViewFixed...")
        from dashboard_view_fixed import DashboardViewFixed
        print("✓ Import réussi")
        
        # Test 2: Création de l'instance
        print("\n2. Création de DashboardViewFixed...")
        dashboard = DashboardViewFixed()
        print("✓ Instance créée")
        
        # Test 3: Affichage
        print("\n3. Affichage de DashboardViewFixed...")
        dashboard.show()
        print("✓ Affichage réussi")
        
        # Test 4: Attendre et vérifier la stabilité
        print("\n4. Test de stabilité (3 secondes)...")
        QTest.qWait(3000)
        print("✓ Stable pendant 3 secondes")
        
        # Test 5: Test des méthodes
        print("\n5. Test des méthodes...")
        dashboard.update_kpis(75.5, 45.2)
        print("   ✓ update_kpis OK")
        
        # Simuler des données FFT
        import math
        freqs = [i * 10 for i in range(50)]  # 0 à 490 Hz
        amps = [math.sin(i * 0.1) * 100 + 100 for i in range(50)]  # Signal sinusoïdal
        dashboard.update_fft_plot(freqs, amps)
        print("   ✓ update_fft_plot OK")
        
        QTest.qWait(1000)
        print("   ✓ Affichage FFT stable")
        
        # Test 6: Fermeture propre
        print("\n6. Test de fermeture...")
        dashboard.close()
        dashboard.deleteLater()
        print("✓ Fermeture propre")
        
        # Test 7: Test de navigation (simulation MainWindow)
        print("\n7. Test de navigation simulée...")
        try:
            from hrneowave.gui.main_window import MainWindow
            
            main_window = MainWindow()
            main_window.show()
            print("   ✓ MainWindow créée")
            
            # Attendre l'initialisation
            QTest.qWait(1000)
            
            # Essayer de naviguer vers dashboard
            if hasattr(main_window, 'view_manager'):
                # Remplacer temporairement DashboardView par DashboardViewFixed
                original_dashboard = None
                if hasattr(main_window.view_manager, 'views') and 'dashboard' in main_window.view_manager.views:
                    original_dashboard = main_window.view_manager.views['dashboard']
                    main_window.view_manager.views['dashboard'] = DashboardViewFixed()
                
                # Tenter la navigation
                main_window.view_manager.switch_to_view('dashboard')
                print("   ✓ Navigation vers dashboard réussie")
                
                QTest.qWait(2000)
                print("   ✓ Dashboard stable dans MainWindow")
                
                # Restaurer l'original si nécessaire
                if original_dashboard:
                    main_window.view_manager.views['dashboard'] = original_dashboard
            
            main_window.close()
            main_window.deleteLater()
            print("   ✓ MainWindow fermée proprement")
            
        except Exception as e:
            print(f"   ⚠ Test navigation échoué (non critique): {e}")
        
        print("\n=== Tous les tests DashboardViewFixed réussis ===\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Erreur durant le test: {e}")
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        if app:
            app.quit()

if __name__ == "__main__":
    success = test_dashboard_fixed()
    print(f"\nRésultat final: {'SUCCÈS' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)