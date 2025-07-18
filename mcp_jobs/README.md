# 🚀 Système de Lancement Local CHNeoWave

Ce répertoire contient le système de lancement local pour CHNeoWave, conçu pour les laboratoires d'étude maritime en mode offline avec validation matérielle complète.

## 📁 Structure

```
mcp_jobs/
├── launch_local.yml     # Configuration principale YAML
├── launcher.py          # Moteur d'exécution Python
├── start_chneowave.bat  # Script de démarrage Windows
└── README.md           # Cette documentation
```

## 🎯 Fonctionnalités

### ✅ Mode Offline Strict
- Aucune connexion réseau requise
- Installation depuis packages locaux
- Validation matérielle autonome
- Sécurité renforcée

### 🔧 Validation Matérielle
- Vérification des sondes (3-11 kHz)
- Contrôle anti-aliasing (< 250 Hz)
- Validation géométrie bassin
- Rapport de conformité automatique

### 📊 Surveillance Système
- Monitoring CPU/RAM/Disque en temps réel
- Alertes de seuils configurables
- Gestion automatique des ressources
- Logs détaillés d'exécution

### 🛠️ Configuration Flexible
- Variables d'environnement
- Paramètres modifiables à chaud
- Support 3-16 sondes
- Fréquences 100Hz-2kHz

## 🚀 Démarrage Rapide

### Option 1: Script Windows (Recommandé)
```cmd
cd c:\Users\LEM\Desktop\chneowave
mcp_jobs\start_chneowave.bat
```

### Option 2: Lancement Python Direct
```bash
cd c:\Users\LEM\Desktop\chneowave
python mcp_jobs\launcher.py --config mcp_jobs\launch_local.yml
```

### Option 3: Tâche Spécifique
```bash
# Validation matérielle uniquement
python mcp_jobs\launcher.py --task validate_hw

# Lancement direct du logiciel
python mcp_jobs\launcher.py --task launch_chneowave
```

## ⚙️ Configuration

### Variables d'Environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `CHNW_MODE` | `offline` | Mode de fonctionnement |
| `CHNW_FS` | `500` | Fréquence d'échantillonnage (Hz) |
| `CHNW_N_PROBES` | `16` | Nombre de sondes |
| `CHNW_GEOM` | `config/probes_geom.json` | Fichier géométrie |
| `CHNW_LOG_LEVEL` | `INFO` | Niveau de logging |
| `CHNW_BUFFER_SIZE` | `8192` | Taille buffer circulaire |
| `CHNW_CACHE_SIZE` | `256` | Cache FFT/Goda (MB) |

### Modification à la Volée
```cmd
set CHNW_FS=1000
set CHNW_N_PROBES=8
python mcp_jobs\launcher.py
```

## 📋 Tâches Disponibles

### 1. Installation Offline (`install_offline`)
- Installation des optimisations depuis `local_packages/`
- Vérification des dépendances
- Configuration automatique

### 2. Validation Matérielle (`validate_hw`)
- Contrôle des spécifications sondes
- Validation géométrie bassin
- Génération rapport de conformité

### 3. Préparation Config (`prepare_config`)
- Création fichiers de configuration
- Validation géométrie
- Paramètres par défaut

### 4. Test Performance (`performance_check`)
- Benchmarks rapides
- Validation optimisations
- Rapport de performance

### 5. Lancement Principal (`launch_chneowave`)
- Démarrage interface CHNeoWave
- Mode laboratoire complet
- Surveillance continue

## 🔍 Diagnostic et Dépannage

### Lister les Tâches
```bash
python mcp_jobs\launcher.py --list-tasks
```

### Simulation (Dry Run)
```bash
python mcp_jobs\launcher.py --dry-run
```

### Diagnostic Complet
```bash
python -m __fixes__.validate_optimizations --diagnose
```

### Vérification Matérielle
```bash
python -m __fixes__.hardware_requirements --validate --report
```

## 📊 Surveillance et Logs

### Fichiers de Logs
- `logs/launcher_YYYYMMDD_HHMMSS.log` - Log principal
- `logs/execution_report_YYYYMMDD_HHMMSS.json` - Rapport d'exécution
- `logs/hw_report.json` - Rapport validation matérielle
- `logs/perf_check.json` - Résultats performance

### Monitoring Temps Réel
Le système surveille automatiquement :
- **CPU** : Seuil 80%
- **RAM** : Seuil 85%
- **Disque** : Seuil 90%
- **Intervalle** : 30 secondes

## 🛡️ Sécurité

### Mode Offline Strict
- Désactivation complète du réseau
- Restriction d'accès aux fichiers
- Répertoires autorisés uniquement
- Validation des commandes

### Répertoires Autorisés
- `${PWD}` (racine projet)
- `${PWD}/config`
- `${PWD}/logs`
- `${PWD}/exports`
- `${PWD}/__fixes__`
- `${PWD}/HRNeoWave`

## 🔧 Personnalisation

### Modifier la Configuration
Éditez `launch_local.yml` pour :
- Ajouter/supprimer des tâches
- Modifier les seuils de surveillance
- Changer les timeouts
- Personnaliser l'environnement

### Exemple de Tâche Personnalisée
```yaml
- name: custom_analysis
  description: "Analyse personnalisée des données"
  depends_on: ["launch_chneowave"]
  timeout: 300
  env:
    CUSTOM_PARAM: "valeur"
  run: >
    python scripts/custom_analysis.py
    --input exports/
    --output results/
```

## 📈 Performance

### Optimisations Automatiques
- Cache FFT intelligent
- Algorithme Goda-SVD optimisé
- Buffer circulaire lock-free
- Parallélisation multi-thread

### Gains Attendus
- **FFT** : 1.8x à 3.5x plus rapide
- **Goda** : 5x à 50x plus rapide
- **Acquisition** : Support 16 sondes à 2 kHz
- **Latence** : < 10ms pour traitement temps réel

## 🆘 Support et Dépannage

### Problèmes Courants

#### 1. Erreur "Python non trouvé"
```cmd
# Activer l'environnement virtuel
venv\Scripts\activate
# Ou ajouter Python au PATH
```

#### 2. Validation matérielle échouée
```bash
# Voir les exigences détaillées
python -m __fixes__.hardware_requirements --requirements-only
```

#### 3. Échec d'installation
```bash
# Vérifier les packages locaux
dir local_packages
# Réinstaller les dépendances
python -m __fixes__.install_optimizations --force-reinstall
```

#### 4. Performance dégradée
```bash
# Lancer les benchmarks
python -m __fixes__.benchmark_performance --quick-test
# Vérifier la configuration
python -m __fixes__.optimization_config --validate
```

### Contacts Support
- **Équipe CHNeoWave** : Laboratoire d'étude maritime
- **Documentation** : `__fixes__/README.md`
- **Issues** : Voir logs dans `logs/`

## 📝 Changelog

### Version 1.0.0 (2025-01-15)
- ✅ Système de lancement initial
- ✅ Mode offline strict
- ✅ Validation matérielle automatique
- ✅ Surveillance système temps réel
- ✅ Configuration flexible
- ✅ Scripts de démarrage Windows
- ✅ Documentation complète

## 🎯 Roadmap

### Version 1.1.0 (Q2 2025)
- [ ] Support Linux/macOS
- [ ] Interface web de monitoring
- [ ] Export automatique des résultats
- [ ] Intégration bases de données

### Version 1.2.0 (Q3 2025)
- [ ] Clustering multi-laboratoires
- [ ] Synchronisation temps réel
- [ ] API REST complète
- [ ] Dashboard analytics

---

**CHNeoWave** - Système d'acquisition et d'analyse de houle pour laboratoires maritimes  
*Optimisé pour les environnements méditerranéens - Bassins et canaux*