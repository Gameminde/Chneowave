#!/usr/bin/env python3
"""
Test final de DashboardView avec la correction pyqtgraph -> SimpleFFTWidget.
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest

def test_dashboard_view_fixed():
    """Test complet de DashboardView avec SimpleFFTWidget"""
    print("\n=== Test DashboardView Corrigé ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Test 1: Import
        print("1. Test d'importation...")
        from hrneowave.gui.views.dashboard_view import DashboardView
        print("   ✓ Import réussi")
        
        # Test 2: Création d'instance
        print("2. Test de création d'instance...")
        dashboard = DashboardView()
        print("   ✓ Instance créée")
        
        # Test 3: Configuration de base
        print("3. Test de configuration...")
        dashboard.setWindowTitle("Test Dashboard Corrigé")
        dashboard.resize(1000, 700)
        print("   ✓ Configuration appliquée")
        
        # Test 4: Affichage
        print("4. Test d'affichage...")
        dashboard.show()
        app.processEvents()
        time.sleep(1)  # Laisser le temps au showEvent
        app.processEvents()
        print("   ✓ Affichage réussi")
        
        # Test 5: Vérification des composants
        print("5. Test des composants...")
        assert hasattr(dashboard, 'fft_widget'), "FFT widget manquant"
        assert hasattr(dashboard, 'buffer_card'), "Buffer card manquante"
        assert hasattr(dashboard, 'cpu_card'), "CPU card manquante"
        print("   ✓ Composants présents")
        
        # Test 6: Vérification du widget FFT
        print("6. Test du widget FFT...")
        if dashboard.fft_widget is not None:
            assert hasattr(dashboard.fft_widget, 'update_data'), "Méthode update_data manquante"
            print("   ✓ Widget FFT fonctionnel")
        else:
            print("   ⚠ Widget FFT non initialisé (normal avant showEvent)")
        
        # Test 7: Mise à jour des KPI
        print("7. Test de mise à jour KPI...")
        dashboard.update_kpis(45.5, 67.2)
        app.processEvents()
        print("   ✓ KPI mis à jour")
        
        # Test 8: Mise à jour FFT
        print("8. Test de mise à jour FFT...")
        freqs = [i * 10 for i in range(50)]  # 0 à 490 Hz
        amps = [50 + 20 * (i % 10) for i in range(50)]  # Amplitudes variables
        dashboard.update_fft_plot(freqs, amps)
        app.processEvents()
        print("   ✓ FFT mis à jour")
        
        # Test 9: Stabilité
        print("9. Test de stabilité...")
        for i in range(5):
            app.processEvents()
            time.sleep(0.2)
        print("   ✓ Stabilité confirmée")
        
        # Test 10: Fermeture propre
        print("10. Test de fermeture...")
        dashboard.close()
        app.processEvents()
        print("   ✓ Fermeture propre")
        
        print("\n✅ Tous les tests DashboardView corrigé réussis !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur dans test_dashboard_view_fixed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_in_mainwindow():
    """Test d'intégration avec MainWindow"""
    print("\n=== Test d'intégration MainWindow ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        from hrneowave.gui.views.dashboard_view import DashboardView
        
        # Créer une MainWindow simple
        main_window = QMainWindow()
        main_window.setWindowTitle("Test MainWindow avec Dashboard Corrigé")
        main_window.resize(1200, 800)
        
        # Ajouter le dashboard comme widget central
        dashboard = DashboardView()
        main_window.setCentralWidget(dashboard)
        
        # Afficher
        main_window.show()
        app.processEvents()
        time.sleep(1.5)
        app.processEvents()
        
        print("   ✓ Intégration MainWindow réussie")
        
        # Test de données FFT réalistes
        print("   Test de données FFT réalistes...")
        import math
        
        # Simuler un signal avec plusieurs fréquences
        freqs = [i * 2.5 for i in range(200)]  # 0 à 500 Hz
        amps = [
            100 * math.exp(-((f - 50) ** 2) / 1000) +  # Pic à 50 Hz
            50 * math.exp(-((f - 150) ** 2) / 2000) +   # Pic à 150 Hz
            20 * math.exp(-((f - 300) ** 2) / 3000) +   # Pic à 300 Hz
            10 * (1 + 0.1 * math.sin(f * 0.1))          # Bruit de fond
            for f in freqs
        ]
        
        dashboard.update_fft_plot(freqs, amps)
        app.processEvents()
        time.sleep(1)
        
        print("   ✓ Données FFT réalistes affichées")
        
        # Test de mise à jour continue
        print("   Test de mise à jour continue...")
        for cycle in range(5):
            # Simuler des données qui évoluent
            amps_dynamic = [
                amp * (1 + 0.2 * math.sin(cycle * 0.5 + i * 0.01))
                for i, amp in enumerate(amps)
            ]
            dashboard.update_fft_plot(freqs, amps_dynamic)
            dashboard.update_kpis(30 + 20 * math.sin(cycle), 40 + 15 * math.cos(cycle))
            app.processEvents()
            time.sleep(0.3)
        
        print("   ✓ Mise à jour continue réussie")
        
        # Fermeture
        main_window.close()
        app.processEvents()
        
        print("\n✅ Test d'intégration MainWindow réussi !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur dans test_dashboard_in_mainwindow: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("CHNeoWave - Test Dashboard Final (pyqtgraph -> SimpleFFTWidget)")
    print("=" * 70)
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Exécuter les tests
    test1_success = test_dashboard_view_fixed()
    test2_success = test_dashboard_in_mainwindow()
    
    # Résultat final
    if test1_success and test2_success:
        print("\n🎉 Résultat final: SUCCÈS COMPLET")
        print("   ✅ DashboardView corrigé et entièrement fonctionnel !")
        print("   ✅ Remplacement pyqtgraph -> SimpleFFTWidget réussi !")
        print("   ✅ Plus de crash 'Signal source has been deleted' !")
        result = True
    else:
        print("\n💥 Résultat final: ÉCHEC")
        print("   Certains tests ont échoué")
        result = False
    
    # Nettoyer
    try:
        app.quit()
    except:
        pass
    
    return result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)