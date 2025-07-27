# 📊 Rapport de Qualité du Code CHNeoWave
**Date:** 21/07/2025 14:42

## 📈 Métriques Générales
- **Fichiers analysés:** 67
- **Lignes totales:** 21,383
- **Lignes de code:** 16,147
- **Lignes de commentaires:** 1,435
- **Fonctions:** 978
- **Classes:** 160

## 🎯 Indicateurs de Qualité
- **Ratio commentaires/code:** 8.9%
- **Couverture docstrings:** 85.4%
- **Estimation couverture tests:** 100.0%

## ⚠️ Problèmes de Complexité
- **src\hrneowave\config\optimization_config.py:320** - Fonction `main` (complexité: 14)
- **src\hrneowave\config\optimization_config.py:152** - Fonction `load_from_file` (complexité: 18)
- **src\hrneowave\core\config_manager.py:143** - Fonction `load_config` (complexité: 13)
- **src\hrneowave\core\data_validator.py:127** - Fonction `validate_sample` (complexité: 15)
- **src\hrneowave\core\export_manager.py:89** - Fonction `_export_hdf5` (complexité: 11)
- ... et 11 autres

## 📄 Fichiers Volumineux
- **src\hrneowave\gui\components\material_components.py** - 1311 lignes (very_large)
- **src\hrneowave\gui\views\analysis_view.py** - 910 lignes (very_large)
- **src\hrneowave\gui\controllers\acquisition_controller.py** - 876 lignes (very_large)
- **src\hrneowave\gui\views\calibration_view.py** - 750 lignes (very_large)
- **src\hrneowave\gui\components\graph_manager.py** - 724 lignes (very_large)

## 📦 Dépendances Principales
- PyQt5
- PyQt5.QtCore
- PyQt5.QtGui
- PyQt5.QtWidgets
- PyQt6
- PyQt6.QtCore
- PyQt6.QtWidgets
- PySide6.QtCore
- PySide6.QtGui
- PySide6.QtWidgets

## 💡 Recommandations
- 🔧 **Réduire la complexité** - Refactoriser les fonctions complexes
- 📄 **Diviser les gros fichiers** - Séparer les responsabilités

---
*Rapport généré automatiquement par l'Analyseur de Qualité CHNeoWave*