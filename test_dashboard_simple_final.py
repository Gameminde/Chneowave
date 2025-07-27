#!/usr/bin/env python3
"""
Test de la version simplifiée de DashboardView sans PerformanceWidget.
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

def test_dashboard_simple():
    """Test complet de DashboardViewSimple"""
    print("\n=== Test DashboardViewSimple ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Test 1: Import
        print("1. Test d'importation...")
        from dashboard_view_simple import DashboardViewSimple
        print("   ✓ Import réussi")
        
        # Test 2: Création d'instance
        print("2. Test de création d'instance...")
        dashboard = DashboardViewSimple()
        print("   ✓ Instance créée")
        
        # Test 3: Configuration de base
        print("3. Test de configuration...")
        dashboard.setWindowTitle("Test Dashboard Simple")
        dashboard.resize(800, 600)
        print("   ✓ Configuration appliquée")
        
        # Test 4: Affichage
        print("4. Test d'affichage...")
        dashboard.show()
        app.processEvents()
        time.sleep(0.5)  # Laisser le temps au showEvent
        app.processEvents()
        print("   ✓ Affichage réussi")
        
        # Test 5: Vérification des composants
        print("5. Test des composants...")
        assert hasattr(dashboard, 'kpi_cards'), "KPI cards manquantes"
        assert hasattr(dashboard, 'fft_widget'), "FFT widget manquant"
        assert len(dashboard.kpi_cards) == 4, f"Nombre de KPI incorrect: {len(dashboard.kpi_cards)}"
        print("   ✓ Composants présents")
        
        # Test 6: Mise à jour des KPI
        print("6. Test de mise à jour KPI...")
        dashboard.update_kpis(45.5, 67.2, 98.1, 89.3)
        app.processEvents()
        print("   ✓ KPI mis à jour")
        
        # Test 7: Mise à jour FFT
        print("7. Test de mise à jour FFT...")
        freqs = [i * 10 for i in range(50)]  # 0 à 490 Hz
        amps = [50 + 20 * (i % 10) for i in range(50)]  # Amplitudes variables
        dashboard.update_fft_plot(freqs, amps)
        app.processEvents()
        print("   ✓ FFT mis à jour")
        
        # Test 8: Simulation automatique
        print("8. Test de simulation automatique...")
        # La simulation devrait déjà être active après showEvent
        assert dashboard.simulation_timer.isActive(), "Timer de simulation inactif"
        
        # Attendre quelques cycles de simulation
        for i in range(3):
            app.processEvents()
            time.sleep(1.1)  # Légèrement plus que l'intervalle du timer
            app.processEvents()
        
        print("   ✓ Simulation automatique fonctionnelle")
        
        # Test 9: Stabilité mémoire
        print("9. Test de stabilité...")
        initial_counter = dashboard.simulation_counter
        
        # Laisser tourner pendant quelques secondes
        for i in range(5):
            app.processEvents()
            time.sleep(0.2)
        
        # Vérifier que la simulation continue
        assert dashboard.simulation_counter > initial_counter, "Simulation arrêtée"
        print("   ✓ Stabilité confirmée")
        
        # Test 10: Fermeture propre
        print("10. Test de fermeture...")
        dashboard.close()
        app.processEvents()
        
        # Vérifier que le timer est arrêté
        assert not dashboard.simulation_timer.isActive(), "Timer non arrêté à la fermeture"
        print("   ✓ Fermeture propre")
        
        print("\n✅ Tous les tests DashboardViewSimple réussis !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur dans test_dashboard_simple: {e}")
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
        from dashboard_view_simple import DashboardViewSimple
        
        # Créer une MainWindow simple
        main_window = QMainWindow()
        main_window.setWindowTitle("Test MainWindow avec Dashboard Simple")
        main_window.resize(1000, 700)
        
        # Ajouter le dashboard comme widget central
        dashboard = DashboardViewSimple()
        main_window.setCentralWidget(dashboard)
        
        # Afficher
        main_window.show()
        app.processEvents()
        time.sleep(1)
        app.processEvents()
        
        print("   ✓ Intégration MainWindow réussie")
        
        # Test de navigation simulée
        print("   Test de navigation...")
        
        # Simuler un changement de vue
        dashboard.hide()
        app.processEvents()
        time.sleep(0.5)
        
        dashboard.show()
        app.processEvents()
        time.sleep(0.5)
        
        print("   ✓ Navigation simulée réussie")
        
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
    print("CHNeoWave - Test Dashboard Simple")
    print("=" * 50)
    
    # Créer l'application Qt
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Exécuter les tests
    test1_success = test_dashboard_simple()
    test2_success = test_dashboard_in_mainwindow()
    
    # Résultat final
    if test1_success and test2_success:
        print("\n🎉 Résultat final: SUCCÈS COMPLET")
        print("   Dashboard Simple entièrement fonctionnel !")
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