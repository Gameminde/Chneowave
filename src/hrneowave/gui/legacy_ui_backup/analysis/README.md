# Module d'Analyse CHNeoWave - Architecture Modulaire

## Vue d'ensemble

Ce module représente la refactorisation complète de `analysis_view.py` vers une architecture modulaire, respectant les principes SOLID et les meilleures pratiques de développement logiciel pour les laboratoires d'études maritimes.

## Architecture

### Structure des fichiers

```
analysis/
├── __init__.py                 # Point d'entrée du module
├── analysis_view_v2.py         # Vue principale refactorisée
├── analysis_controller.py      # Contrôleur central
├── spectral_analysis.py        # Widget d'analyse spectrale
├── goda_analysis.py           # Widget d'analyse de Goda
├── statistics_analysis.py     # Widget d'analyse statistique
├── summary_report.py          # Widget de rapport de synthèse
├── migrate_analysis_view.py   # Script de migration
├── test_analysis_modules.py   # Tests unitaires
└── README.md                  # Cette documentation
```

### Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AnalysisViewV2                          │
│                   (Vue principale)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                AnalysisController                           │
│              (Orchestrateur central)                       │
└─────┬─────────┬─────────┬─────────┬─────────────────────────┘
      │         │         │         │
      ▼         ▼         ▼         ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Spectral │ │   Goda   │ │Statistics│ │   Summary    │
│ Analysis │ │ Analysis │ │ Analysis │ │   Report     │
│  Widget  │ │  Widget  │ │  Widget  │ │   Widget     │
└──────────┘ └──────────┘ └──────────┘ └──────────────┘
```

## Composants principaux

### 1. AnalysisViewV2

**Responsabilité** : Interface utilisateur principale intégrant tous les widgets d'analyse.

**Caractéristiques** :
- Architecture en onglets pour une navigation claire
- Intégration transparente avec le contrôleur
- Gestion des signaux Qt pour la communication inter-widgets
- Interface compatible avec l'ancienne version

**Utilisation** :
```python
from hrneowave.gui.views.analysis import AnalysisViewV2

view = AnalysisViewV2(parent)
view.setSessionData(session_data)
view.startCompleteAnalysis()
```

### 2. AnalysisController

**Responsabilité** : Orchestration des analyses et gestion des données.

**Fonctionnalités** :
- Coordination des widgets spécialisés
- Gestion centralisée des données de session
- Agrégation des résultats d'analyse
- Gestion des erreurs et de la progression
- Émission de signaux pour la communication

**Signaux émis** :
- `analysisStarted()` : Début d'une analyse
- `analysisProgress(int)` : Progression (0-100%)
- `analysisFinished()` : Fin d'analyse
- `analysisError(str)` : Erreur d'analyse

### 3. SpectralAnalysisWidget

**Responsabilité** : Analyse spectrale des signaux de vagues.

**Fonctionnalités** :
- Calcul de la FFT avec fenêtrage configurable
- Densité spectrale de puissance (PSD)
- Fonctions de cohérence entre capteurs
- Statistiques spectrales (fréquence de pic, largeur spectrale)
- Visualisation interactive des spectres

**Paramètres configurables** :
- Taille de fenêtre (512, 1024, 2048, 4096)
- Type de fenêtre (Hann, Hamming, Blackman, Kaiser)
- Taux de recouvrement (0-90%)

### 4. GodaAnalysisWidget

**Responsabilité** : Analyse statistique des vagues selon la méthode de Goda.

**Fonctionnalités** :
- Détection des vagues (zero-crossing, peak-to-trough, enveloppe)
- Calcul des hauteurs de vagues
- Statistiques de Goda (Hmax, Hmean, H1/3, H1/10)
- Distribution de probabilité des hauteurs
- Analyse temporelle des événements

**Méthodes de détection** :
- **Zero-crossing** : Détection par passage par zéro
- **Peak-to-trough** : Détection pic-à-creux
- **Enveloppe** : Détection par enveloppe du signal

### 5. StatisticsAnalysisWidget

**Responsabilité** : Analyse statistique approfondie des données.

**Fonctionnalités** :
- Statistiques descriptives complètes
- Tests de normalité (Shapiro-Wilk, Kolmogorov-Smirnov)
- Détection d'outliers (IQR, Z-score, isolation forest)
- Visualisations statistiques (histogrammes, Q-Q plots)
- Tests d'hypothèses avec intervalles de confiance

### 6. SummaryReportWidget

**Responsabilité** : Génération de rapports de synthèse.

**Fonctionnalités** :
- Rapports multi-formats (complet, exécutif, technique)
- Support multilingue (français, anglais)
- Export PDF et JSON
- Templates personnalisables
- Intégration des graphiques et tableaux

## Utilisation

### Intégration dans l'application principale

```python
# Dans main_window.py
from hrneowave.gui.views.analysis import AnalysisViewV2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analysis_view = AnalysisViewV2(self)
        
        # Connexion des signaux
        self.analysis_view.analysisFinished.connect(self._on_analysis_finished)
        self.analysis_view.analysisError.connect(self._on_analysis_error)
    
    def _on_analysis_finished(self):
        results = self.analysis_view.getAnalysisResults()
        # Traitement des résultats
    
    def _on_analysis_error(self, error_message):
        # Gestion des erreurs
        pass
```

### Configuration d'une analyse

```python
# Configuration des données de session
session_data = SessionData()
session_data.sampling_frequency = 100.0
session_data.sensor_data = {...}

# Configuration de la vue
analysis_view.setSessionData(session_data)

# Lancement d'analyses spécifiques
analysis_view.startSpectralAnalysis()
analysis_view.startGodaAnalysis()
analysis_view.startStatisticsAnalysis()

# Ou analyse complète
analysis_view.startCompleteAnalysis()
```

### Récupération des résultats

```python
results = analysis_view.getAnalysisResults()

# Structure des résultats
{
    'spectral': {
        'frequencies': array([...]),
        'psd': array([...]),
        'peak_frequency': float,
        'mean_frequency': float,
        'spectral_width': float
    },
    'goda': {
        'wave_heights': array([...]),
        'h_max': float,
        'h_mean': float,
        'h_13': float,
        'h_110': float,
        'wave_periods': array([...])
    },
    'statistics': {
        'mean': float,
        'std': float,
        'skewness': float,
        'kurtosis': float,
        'normality_tests': {...},
        'outliers': array([...])
    }
}
```

## Migration depuis l'ancienne version

### Script de migration automatique

```bash
# Exécution de la migration
python migrate_analysis_view.py --project-root /path/to/chneowave

# Vérification seulement
python migrate_analysis_view.py --verify-only

# Rollback en cas de problème
python migrate_analysis_view.py --rollback
```

### Migration manuelle

1. **Sauvegarde** : Créer une copie de `analysis_view.py`
2. **Imports** : Mettre à jour les imports dans les fichiers utilisateurs
3. **Interface** : Adapter les appels de méthodes si nécessaire
4. **Tests** : Valider le fonctionnement avec les nouveaux modules

### Couche de compatibilité

Une couche de compatibilité est automatiquement créée pour maintenir l'interface legacy :

```python
# L'ancienne interface continue de fonctionner
from hrneowave.gui.views.analysis_view_compat import AnalysisView

# Mais émet un avertissement de dépréciation
view = AnalysisView()  # DeprecationWarning
```

## Tests

### Exécution des tests

```bash
# Tests complets
python test_analysis_modules.py

# Tests spécifiques
python -m unittest test_analysis_modules.TestSpectralAnalysisWidget
python -m unittest test_analysis_modules.TestGodaAnalysisWidget
```

### Couverture de tests

Les tests couvrent :
- ✅ Fonctionnalités de base de chaque widget
- ✅ Intégration entre composants
- ✅ Gestion des erreurs
- ✅ Validation des données
- ✅ Calculs mathématiques
- ✅ Interface utilisateur (mocks)

## Avantages de la nouvelle architecture

### 1. Maintenabilité
- **Séparation des responsabilités** : Chaque widget a une fonction claire
- **Code modulaire** : Modifications isolées sans impact sur les autres composants
- **Tests unitaires** : Validation indépendante de chaque module

### 2. Extensibilité
- **Nouveaux types d'analyse** : Ajout facile de nouveaux widgets
- **Personnalisation** : Configuration flexible des paramètres
- **Plugins** : Architecture prête pour les extensions

### 3. Performance
- **Chargement paresseux** : Widgets chargés à la demande
- **Calculs optimisés** : Algorithmes spécialisés par domaine
- **Mémoire** : Gestion efficace des grandes datasets

### 4. Utilisabilité
- **Interface claire** : Organisation logique en onglets
- **Feedback utilisateur** : Barres de progression et messages d'état
- **Rapports professionnels** : Export multi-format

## Bonnes pratiques

### Développement

1. **Respect de l'architecture MVC** :
   - Vue : Interface utilisateur uniquement
   - Contrôleur : Logique métier et orchestration
   - Modèle : Données et calculs

2. **Gestion des erreurs** :
   ```python
   try:
       result = self.perform_analysis()
       self.analysisFinished.emit()
   except Exception as e:
       self.analysisError.emit(str(e))
       self.logger.error(f"Erreur d'analyse: {e}")
   ```

3. **Signaux Qt** :
   ```python
   # Émission de signaux pour la communication
   self.progressChanged.emit(progress_value)
   self.dataUpdated.emit(new_data)
   ```

4. **Documentation** :
   - Docstrings détaillées pour toutes les méthodes
   - Commentaires pour les algorithmes complexes
   - Exemples d'utilisation

### Utilisation

1. **Configuration des paramètres** :
   - Valider les paramètres avant analyse
   - Utiliser les valeurs par défaut appropriées
   - Documenter l'impact des paramètres

2. **Gestion des données** :
   - Vérifier la qualité des données d'entrée
   - Gérer les cas de données manquantes
   - Optimiser pour les gros volumes

3. **Interprétation des résultats** :
   - Comprendre les limitations de chaque méthode
   - Valider la cohérence entre analyses
   - Documenter les hypothèses

## Dépannage

### Problèmes courants

1. **Import errors** :
   ```python
   # Vérifier le PYTHONPATH
   import sys
   sys.path.append('/path/to/chneowave/src')
   ```

2. **Données manquantes** :
   ```python
   if not self.session_data:
       raise ValueError("Données de session non configurées")
   ```

3. **Erreurs de calcul** :
   ```python
   # Validation des données d'entrée
   if len(signal) < self.window_size:
       raise ValueError("Signal trop court pour la taille de fenêtre")
   ```

### Logs et debugging

```python
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Dans le code
logger.debug(f"Début analyse spectrale: {len(data)} points")
logger.info(f"Fréquence de pic détectée: {peak_freq} Hz")
logger.warning(f"Qualité du signal faible: SNR = {snr}")
logger.error(f"Erreur de calcul: {error}")
```

## Roadmap

### Version 2.1
- [ ] Support des analyses en temps réel
- [ ] Interface de configuration avancée
- [ ] Export vers formats scientifiques (HDF5, NetCDF)
- [ ] Intégration avec bases de données

### Version 2.2
- [ ] Analyses multi-directionnelles
- [ ] Machine learning pour la détection automatique
- [ ] API REST pour analyses distantes
- [ ] Interface web complémentaire

### Version 3.0
- [ ] Architecture distribuée
- [ ] Support GPU pour calculs intensifs
- [ ] Intégration cloud
- [ ] Collaboration multi-utilisateurs

## Contribution

### Guidelines

1. **Code style** : Suivre PEP 8
2. **Tests** : Couverture minimale de 80%
3. **Documentation** : Docstrings obligatoires
4. **Review** : Validation par pairs

### Processus

1. Fork du repository
2. Création d'une branche feature
3. Développement avec tests
4. Pull request avec description détaillée
5. Review et intégration

## Support

- **Documentation** : Ce README et docstrings
- **Tests** : `test_analysis_modules.py`
- **Exemples** : Dossier `examples/` (à créer)
- **Issues** : GitHub issues pour bugs et features

---

**CHNeoWave Analysis Module v2.0.0**  
*Architecture modulaire pour l'analyse de données maritimes*  
*Laboratoire d'Études Maritimes - Méditerranée*