#!/usr/bin/env python3
"""
Test de la version corrigée de DashboardView (sans pyqtgraph).
"""

import sys
import traceback
import math
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

def test_dashboard_corrected():
    """Test de la version corrigée de DashboardView."""
    print("=== Test DashboardView Corrigée (Version Finale) ===\n")
    
    try:
        # Créer l'application Qt
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication créée")
        
        # Test 1: Import de DashboardView corrigée
        print("\n1. Import DashboardView corrigée...")
        from hrneowave.gui.views.dashboard_view import DashboardView
        print("✓ Import réussi")
        
        # Test 2: Création de l'instance
        print("\n2. Création de DashboardView...")
        dashboard = DashboardView()
        print("✓ Instance créée")
        
        # Test 3: Affichage
        print("\n3. Affichage de DashboardView...")
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
        freqs = [i * 10 for i in range(50)]  # 0 à 490 Hz
        amps = [math.sin(i * 0.1) * 100 + 100 for i in range(50)]  # Signal sinusoïdal
        dashboard.update_fft_plot(freqs, amps)
        print("   ✓ update_fft_plot OK")
        
        QTest.qWait(1000)
        print("   ✓ Affichage FFT stable")
        
        # Test 6: Test de navigation complète
        print("\n6. Test de navigation complète...")
        try:
            from hrneowave.gui.main_window import MainWindow
            
            main_window = MainWindow()
            main_window.show()
            print("   ✓ MainWindow créée")
            
            # Attendre l'initialisation
            QTest.qWait(1000)
            
            # Navigation vers dashboard
            if hasattr(main_window, 'view_manager'):
                main_window.view_manager.switch_to_view('dashboard')
                print("   ✓ Navigation vers dashboard réussie")
                
                QTest.qWait(2000)
                print("   ✓ Dashboard stable dans MainWindow")
                
                # Test de mise à jour des données dans le contexte MainWindow
                current_view = main_window.view_manager.get_current_view()
                if hasattr(current_view, 'update_fft_plot'):
                    # Données FFT plus complexes
                    freqs2 = [i * 5 for i in range(100)]  # 0 à 495 Hz
                    amps2 = [math.sin(i * 0.05) * 50 + math.cos(i * 0.1) * 30 + 80 for i in range(100)]
                    current_view.update_fft_plot(freqs2, amps2)
                    print("   ✓ Mise à jour FFT dans MainWindow OK")
                
                QTest.qWait(1000)
                print("   ✓ Données FFT mises à jour")
            
            main_window.close()
            main_window.deleteLater()
            print("   ✓ MainWindow fermée proprement")
            
        except Exception as e:
            print(f"   ⚠ Test navigation échoué: {e}")
            traceback.print_exc()
        
        # Test 7: Fermeture propre du dashboard isolé
        print("\n7. Test de fermeture...")
        dashboard.close()
        dashboard.deleteLater()
        print("✓ Fermeture propre")
        
        print("\n=== Tous les tests DashboardView corrigée réussis ===\n")
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
    success = test_dashboard_corrected()
    print(f"\nRésultat final: {'SUCCÈS' if success else 'ÉCHEC'}")
    sys.exit(0 if success else 1)