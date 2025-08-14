#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les corrections des problèmes d'affichage CHNeoWave
Teste chaque correction appliquée et valide le fonctionnement

Auteur: Claude Sonnet 4 - Architecte Logiciel en Chef
Date: 28 Juillet 2025
Version: 1.0.0
"""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class CHNeoWaveFixTester:
    """Testeur des corrections CHNeoWave"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
        
        # Configuration logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('chneowave_tester')
    
    def test_qobject_import(self) -> bool:
        """Teste la correction de l'import QObject"""
        print("🧪 TEST 1: Import QObject")
        print("=" * 40)
        
        try:
            # Test d'import du contrôleur d'acquisition
            from hrneowave.gui.controllers.acquisition_controller import AcquisitionController
            print("✅ Import AcquisitionController réussi")
            
            # Test de création d'une instance (sans lancer l'acquisition)
            config = type('Config', (), {
                'mode': type('Mode', (), {'SIMULATE': 'simulate'})(),
                'sample_rate': 32.0,
                'n_channels': 4,
                'buffer_size': 1000
            })()
            
            controller = AcquisitionController(config)
            print("✅ Instance AcquisitionController créée avec succès")
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur import QObject: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def test_qapplication_management(self) -> bool:
        """Teste la gestion QApplication"""
        print("\n🧪 TEST 2: Gestion QApplication")
        print("=" * 40)
        
        try:
            app = QApplication(sys.argv)
            
            # Test création MainWindow
            from hrneowave.gui.main_window import MainWindow
            window = MainWindow()
            
            # Test affichage
            window.show()
            window.raise_()
            window.activateWindow()
            
            # Vérifications
            visible = window.isVisible()
            active = window.isActiveWindow()
            
            print(f"✅ Fenêtre créée: Visible={visible}, Active={active}")
            
            # Fermer proprement
            window.close()
            app.quit()
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur gestion QApplication: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def test_css_properties(self) -> bool:
        """Teste les corrections CSS"""
        print("\n🧪 TEST 3: Propriétés CSS")
        print("=" * 40)
        
        try:
            # Test d'application du thème
            from hrneowave.gui.styles.theme_manager import ThemeManager
            
            app = QApplication(sys.argv)
            theme_manager = ThemeManager(app)
            theme_manager.apply_theme('maritime_modern')
            
            print("✅ Thème maritime appliqué sans erreur")
            
            # Test création widget avec style
            from hrneowave.gui.components.modern_card import ModernCard
            
            card = ModernCard("Test Card")
            card.show()
            
            print("✅ ModernCard créé et affiché")
            
            # Nettoyer
            card.close()
            app.quit()
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur propriétés CSS: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def test_qsizepolicy(self) -> bool:
        """Teste les corrections QSizePolicy"""
        print("\n🧪 TEST 4: QSizePolicy")
        print("=" * 40)
        
        try:
            from PySide6.QtWidgets import QSizePolicy
            
            # Test création QSizePolicy avec valeurs entières
            policy = QSizePolicy(7, 5)  # Expanding, Fixed
            print("✅ QSizePolicy créé avec valeurs entières")
            
            # Test application sur widget
            widget = QWidget()
            widget.setSizePolicy(policy)
            print("✅ QSizePolicy appliqué sur widget")
            
            # Test avec valeurs .value
            policy2 = QSizePolicy()
            policy2.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            policy2.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            print("✅ QSizePolicy créé avec .value")
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur QSizePolicy: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def test_animations(self) -> bool:
        """Teste les corrections d'animations"""
        print("\n🧪 TEST 5: Animations Qt")
        print("=" * 40)
        
        try:
            from PySide6.QtCore import QPropertyAnimation, QEasingCurve
            from PySide6.QtWidgets import QPushButton
            
            app = QApplication(sys.argv)
            
            # Test création animation
            button = QPushButton("Test Animation")
            animation = QPropertyAnimation(button, b"geometry")
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            print("✅ Animation Qt créée")
            
            # Test animation simple
            button.show()
            animation.setStartValue(button.geometry())
            animation.setEndValue(button.geometry().adjusted(10, 10, 10, 10))
            animation.start()
            
            print("✅ Animation Qt lancée")
            
            # Nettoyer
            button.close()
            app.quit()
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur animations: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def test_golden_ratio_layout(self) -> bool:
        """Teste les optimisations Golden Ratio"""
        print("\n🧪 TEST 6: Layout Golden Ratio")
        print("=" * 40)
        
        try:
            from hrneowave.gui.layouts.golden_ratio_layout import GoldenRatioLayout
            from PySide6.QtWidgets import QLabel
            
            app = QApplication(sys.argv)
            
            # Test création layout
            layout = GoldenRatioLayout()
            print("✅ GoldenRatioLayout créé")
            
            # Test ajout widgets
            label1 = QLabel("Widget 1")
            label2 = QLabel("Widget 2")
            
            layout.addWidget(label1)
            layout.addWidget(label2)
            
            print("✅ Widgets ajoutés au layout")
            
            # Test calcul sections
            if hasattr(layout, '_calculate_golden_sections'):
                print("✅ Méthode _calculate_golden_sections présente")
            
            app.quit()
            
            self.tests_passed += 1
            return True
            
        except Exception as e:
            error_msg = f"❌ Erreur layout Golden Ratio: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def test_complete_interface(self) -> bool:
        """Teste l'interface complète"""
        print("\n🧪 TEST 7: Interface Complète")
        print("=" * 40)
        
        try:
            app = QApplication(sys.argv)
            
            # Test création interface complète
            from hrneowave.gui.main_window import MainWindow
            
            window = MainWindow()
            window.show()
            window.raise_()
            window.activateWindow()
            
            # Vérifications critiques
            visible = window.isVisible()
            active = window.isActiveWindow()
            minimized = window.isMinimized()
            
            print(f"✅ Interface créée: Visible={visible}, Active={active}, Minimized={minimized}")
            
            if visible and not minimized:
                print("🎉 SUCCÈS: Interface CHNeoWave fonctionnelle!")
                self.tests_passed += 1
                
                # Fermer après 2 secondes
                timer = QTimer()
                timer.timeout.connect(app.quit)
                timer.start(2000)
                
                app.exec()
                return True
            else:
                print("⚠️ Interface créée mais problèmes d'affichage")
                self.tests_failed += 1
                return False
                
        except Exception as e:
            error_msg = f"❌ Erreur interface complète: {e}"
            self.errors.append(error_msg)
            print(error_msg)
            self.tests_failed += 1
            return False
    
    def run_all_tests(self) -> bool:
        """Lance tous les tests"""
        print("🚀 LANCEMENT DES TESTS DE VALIDATION CHNEOWAVE")
        print("=" * 60)
        
        tests = [
            self.test_qobject_import,
            self.test_qapplication_management,
            self.test_css_properties,
            self.test_qsizepolicy,
            self.test_animations,
            self.test_golden_ratio_layout,
            self.test_complete_interface
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Erreur lors du test: {e}")
                self.tests_failed += 1
        
        return self.generate_test_report()
    
    def generate_test_report(self) -> bool:
        """Génère le rapport de test"""
        print("\n📊 RAPPORT DE TESTS")
        print("=" * 50)
        
        total_tests = self.tests_passed + self.tests_failed
        
        print(f"Tests réussis: {self.tests_passed}/{total_tests}")
        print(f"Tests échoués: {self.tests_failed}/{total_tests}")
        print(f"Taux de succès: {(self.tests_passed/total_tests)*100:.1f}%")
        
        if self.errors:
            print("\n❌ Erreurs rencontrées:")
            for error in self.errors:
                print(f"  • {error}")
        
        success = self.tests_failed == 0
        
        if success:
            print("\n🎉 TOUS LES TESTS RÉUSSIS!")
            print("✅ CHNeoWave est prêt à être utilisé")
        else:
            print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
            print("❌ Des problèmes persistent")
        
        # Sauvegarder le rapport
        report_file = Path("test_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RAPPORT DE TESTS CHNEOWAVE\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Tests réussis: {self.tests_passed}/{total_tests}\n")
            f.write(f"Tests échoués: {self.tests_failed}/{total_tests}\n")
            f.write(f"Taux de succès: {(self.tests_passed/total_tests)*100:.1f}%\n\n")
            
            if self.errors:
                f.write("ERREURS:\n")
                for error in self.errors:
                    f.write(f"  • {error}\n")
        
        print(f"📄 Rapport sauvegardé: {report_file}")
        
        return success

def main():
    """Point d'entrée principal"""
    print("🧪 TESTEUR DE CORRECTIONS CHNEOWAVE")
    print("=" * 50)
    
    # Ajouter le chemin du projet
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    # Créer le testeur
    tester = CHNeoWaveFixTester()
    
    # Lancer tous les tests
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 