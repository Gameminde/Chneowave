# Guide Utilisateur CHNeoWave v1.1.0-beta

**Logiciel d'acquisition et d'analyse de données maritimes**  
*Spécialement conçu pour les laboratoires d'études maritimes modèle réduit*

---

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Nouvelles Fonctionnalités v1.1.0-beta](#nouvelles-fonctionnalités)
3. [Export HDF5 Scientifique](#export-hdf5)
4. [Certificats PDF de Calibration](#certificats-pdf)
5. [Interface Utilisateur Améliorée](#interface-améliorée)
6. [Workflows Recommandés](#workflows)
7. [Dépannage](#dépannage)
8. [Annexes](#annexes)

---

## 🎯 Introduction

CHNeoWave v1.1.0-beta introduit des fonctionnalités avancées d'exportation scientifique et de certification, transformant votre workflow de laboratoire. Cette version est spécialement optimisée pour les études en bassins et canaux méditerranéens.

### Nouveautés Principales
- 📊 **Export HDF5 traçable** avec signature cryptographique
- 📄 **Certificats PDF de calibration** conformes aux standards
- 🎨 **Interface utilisateur polie** avec indicateurs visuels
- 🔧 **Outils de validation** automatisés

---

## 🚀 Nouvelles Fonctionnalités v1.1.0-beta

### Vue d'Ensemble

Cette version beta ajoute deux fonctionnalités majeures qui répondent aux besoins des laboratoires de recherche maritime :

1. **Export scientifique HDF5** pour l'interopérabilité avec les outils d'analyse
2. **Certification automatique** des calibrations pour la traçabilité

### Bénéfices Utilisateur

- **Traçabilité renforcée** : Chaque export inclut une signature cryptographique
- **Interopérabilité** : Données compatibles MATLAB, Python, R
- **Conformité** : Certificats PDF conformes aux exigences de laboratoire
- **Efficacité** : Génération automatique des documents de validation

---

## 📊 Export HDF5 Scientifique

### Qu'est-ce que HDF5 ?

HDF5 (Hierarchical Data Format 5) est le format standard pour les données scientifiques, utilisé par :
- **MATLAB** : Lecture native avec `h5read()`
- **Python** : Compatible avec pandas, numpy, h5py
- **R** : Support via packages rhdf5, hdf5r
- **Outils de visualisation** : ParaView, VisIt, HDFView

### Comment Utiliser l'Export HDF5

#### 1. Accès à la Fonctionnalité

1. Terminez votre acquisition de données
2. Allez dans **Fichier > Exporter les résultats**
3. Dans l'onglet **Options d'exportation**
4. Cochez **"📊 Données HDF5 (scientifique)"** (cochée par défaut)

#### 2. Configuration de l'Export

```
┌─ Options d'exportation ─────────────────┐
│ ☑ Rapport PDF                          │
│ ☑ Données Excel                        │
│ ☑ Données CSV                          │
│ ☑ Données JSON                         │
│ ☑ 📊 Données HDF5 (scientifique)       │
│ ☑ Images des graphiques                │
└─────────────────────────────────────────┘
```

#### 3. Processus d'Export

1. Cliquez **"Exporter Tout"**
2. Sélectionnez le dossier de destination
3. L'export HDF5 se lance automatiquement
4. Un fichier `session_YYYYMMDD_HHMMSS.h5` est créé

#### 4. Vérification d'Intégrité

Chaque fichier HDF5 inclut :
- **Hash SHA-256** des données
- **Métadonnées de session** complètes
- **Informations de calibration**
- **Timestamp de création**

### Structure du Fichier HDF5

```
session_20241215_143022.h5
├── /data/
│   ├── /raw_data          # Données brutes d'acquisition
│   ├── /processed_data    # Données traitées
│   └── /calibration       # Données de calibration
├── /metadata/
│   ├── session_info       # Informations de session
│   ├── acquisition_params # Paramètres d'acquisition
│   └── calibration_info   # Informations de calibration
└── /integrity/
    ├── data_hash          # Hash SHA-256 des données
    ├── creation_time      # Timestamp de création
    └── software_version   # Version CHNeoWave
```

### Lecture des Données HDF5

#### MATLAB
```matlab
% Lire les données brutes
raw_data = h5read('session_20241215_143022.h5', '/data/raw_data');

% Lire les métadonnées
session_info = h5readatt('session_20241215_143022.h5', '/metadata', 'session_info');

% Vérifier l'intégrité
data_hash = h5read('session_20241215_143022.h5', '/integrity/data_hash');
```

#### Python
```python
import h5py
import numpy as np

# Ouvrir le fichier
with h5py.File('session_20241215_143022.h5', 'r') as f:
    # Lire les données
    raw_data = f['data/raw_data'][:]
    
    # Lire les métadonnées
    session_info = dict(f['metadata'].attrs)
    
    # Vérifier l'intégrité
    data_hash = f['integrity/data_hash'][()].decode()
```

#### R
```r
library(rhdf5)

# Lire les données
raw_data <- h5read("session_20241215_143022.h5", "/data/raw_data")

# Lire les métadonnées
session_info <- h5readAttributes("session_20241215_143022.h5", "/metadata")

# Fermer le fichier
H5close()
```

---

## 📄 Certificats PDF de Calibration

### Pourquoi des Certificats PDF ?

Les certificats de calibration sont essentiels pour :
- **Traçabilité réglementaire** : Conformité aux normes de laboratoire
- **Validation des mesures** : Preuve de la qualité des calibrations
- **Archivage** : Documentation permanente des procédures
- **Audit** : Vérification par des organismes externes

### Comment Générer un Certificat

#### 1. Prérequis

- Calibration complète de tous les capteurs
- Coefficient de détermination R² ≥ 0.998 pour chaque capteur
- Session de calibration sauvegardée

#### 2. Génération du Certificat

1. Dans la vue **Calibration**
2. Vérifiez que tous les capteurs sont calibrés (voyants verts)
3. Cliquez sur **"📄 Certificat PDF"**
4. Sélectionnez l'emplacement de sauvegarde
5. Le certificat est généré automatiquement

#### 3. Activation du Bouton

Le bouton "📄 Certificat PDF" n'est activé que si :
```
✅ Tous les capteurs sont calibrés
✅ R² ≥ 0.998 pour chaque capteur
✅ Données de calibration valides
```

### Contenu du Certificat

#### Page 1 : Informations Générales
- **En-tête laboratoire** avec logo
- **Informations de session** (date, opérateur, projet)
- **Liste des capteurs** calibrés
- **Résumé des performances** (R² moyen, écart-type)

#### Page 2 : Détails Techniques
- **Tableau des coefficients** de calibration
- **Statistiques de qualité** par capteur
- **Paramètres d'acquisition** utilisés
- **Conditions environnementales**

#### Page 3 : Graphiques de Linéarité
- **Courbes de calibration** pour chaque capteur
- **Points de mesure** avec barres d'erreur
- **Droites de régression** avec équations
- **Coefficients de détermination** R²

#### Page 4 : Validation et Signature
- **Hash SHA-256** des données de calibration
- **Timestamp** de génération
- **Version logiciel** utilisée
- **Espace signature** pour validation manuelle

### Exemple de Certificat

```
┌─────────────────────────────────────────────────────────┐
│                CERTIFICAT DE CALIBRATION                │
│                                                         │
│  Laboratoire d'Études Maritimes Modèle Réduit         │
│  Bassin Méditerranéen - Canal d'Essais                 │
│                                                         │
│  Session: CAL_20241215_001                              │
│  Date: 15/12/2024 14:30:22                             │
│  Opérateur: Dr. Marine Researcher                      │
│                                                         │
│  CAPTEURS CALIBRÉS:                                    │
│  • Capteur 1 (Pression): R² = 0.9995                  │
│  • Capteur 2 (Vitesse): R² = 0.9998                   │
│  • Capteur 3 (Force): R² = 0.9997                     │
│                                                         │
│  SIGNATURE NUMÉRIQUE:                                  │
│  SHA-256: a1b2c3d4e5f6...                             │
│                                                         │
│  Généré par CHNeoWave v1.1.0-beta                     │
└─────────────────────────────────────────────────────────┘
```

### Vérification de l'Intégrité

Chaque certificat inclut un hash SHA-256 qui permet de vérifier :
- **Authenticité** : Les données n'ont pas été modifiées
- **Intégrité** : Le certificat correspond aux données originales
- **Traçabilité** : Lien direct avec la session de calibration

---

## 🎨 Interface Utilisateur Améliorée

### Nouvelles Icônes et Indicateurs

#### Export HDF5
- **Icône** : 📊 (graphique de données)
- **Tooltip** : "Export des données brutes au format HDF5 scientifique avec traçabilité SHA-256"
- **État** : Cochée par défaut

#### Certificat PDF
- **Icône** : 📄 (document)
- **Tooltip** : "Générer un certificat PDF de calibration avec signature numérique"
- **État** : Activé seulement si calibration valide

### Indicateurs de Statut

#### Calibration
```
Capteur 1: ✅ R² = 0.9995 (Excellent)
Capteur 2: ✅ R² = 0.9998 (Excellent)  
Capteur 3: ⚠️  R² = 0.9970 (Acceptable)
Capteur 4: ❌ Non calibré
```

#### Export
```
📊 Export HDF5: ✅ Terminé (2.3 MB)
📄 Certificat PDF: ✅ Généré (127 kB)
📈 Graphiques: ✅ Exportés (8 fichiers)
```

### Barres de Progression

Les exports affichent maintenant :
- **Progression en temps réel** avec pourcentage
- **Étapes détaillées** ("Préparation données...", "Écriture fichier...")
- **Temps estimé** restant
- **Taille finale** du fichier

---

## 🔄 Workflows Recommandés

### Workflow Standard de Laboratoire

#### 1. Préparation
```
1. Démarrer CHNeoWave
2. Créer nouveau projet
3. Configurer les capteurs
4. Vérifier les connexions
```

#### 2. Calibration
```
1. Aller dans vue Calibration
2. Effectuer calibration 3 points minimum
3. Vérifier R² ≥ 0.998 pour tous capteurs
4. Générer certificat PDF
5. Archiver le certificat
```

#### 3. Acquisition
```
1. Configurer paramètres d'acquisition
2. Lancer l'acquisition
3. Surveiller les données en temps réel
4. Arrêter et sauvegarder
```

#### 4. Export et Archivage
```
1. Exporter tous les formats (PDF, Excel, HDF5)
2. Vérifier l'intégrité des fichiers HDF5
3. Archiver sur serveur de laboratoire
4. Documenter dans cahier de laboratoire
```

### Workflow de Validation Réglementaire

#### Pour Audits et Certifications

1. **Documentation complète**
   - Certificats PDF de toutes les calibrations
   - Exports HDF5 avec signatures cryptographiques
   - Rapports PDF détaillés

2. **Vérification d'intégrité**
   - Contrôle des hash SHA-256
   - Validation des timestamps
   - Vérification des versions logiciel

3. **Archivage sécurisé**
   - Stockage redondant des fichiers HDF5
   - Sauvegarde des certificats PDF
   - Traçabilité des modifications

### Workflow de Recherche Collaborative

#### Partage de Données avec Partenaires

1. **Export HDF5 standardisé**
   - Format universel lisible par tous les outils
   - Métadonnées complètes incluses
   - Vérification d'intégrité possible

2. **Documentation associée**
   - Certificats de calibration
   - Rapports de session
   - Notes expérimentales

3. **Validation croisée**
   - Vérification des hash par les partenaires
   - Reproduction des analyses
   - Validation des résultats

---

## 🔧 Dépannage

### Problèmes d'Export HDF5

#### Erreur : "Module h5py non trouvé"
**Solution** :
```bash
pip install h5py
```

#### Erreur : "Fichier HDF5 corrompu"
**Diagnostic** :
1. Vérifier l'espace disque disponible
2. Contrôler les permissions d'écriture
3. Relancer l'export dans un autre dossier

#### Erreur : "Hash SHA-256 invalide"
**Actions** :
1. Vérifier l'intégrité des données source
2. Relancer l'acquisition si nécessaire
3. Contacter le support technique

### Problèmes de Certificats PDF

#### Bouton "Certificat PDF" grisé
**Vérifications** :
- [ ] Tous les capteurs sont-ils calibrés ?
- [ ] R² ≥ 0.998 pour chaque capteur ?
- [ ] Session de calibration sauvegardée ?

#### Erreur : "Génération PDF échouée"
**Solutions** :
1. Vérifier l'espace disque (minimum 10 MB)
2. Contrôler les permissions du dossier
3. Redémarrer CHNeoWave
4. Relancer la calibration si nécessaire

#### PDF trop volumineux (> 150 kB)
**Optimisations** :
- Réduire le nombre de points de calibration affichés
- Compresser les graphiques
- Contacter le support pour ajustements

### Problèmes d'Interface

#### Icônes manquantes
**Solution** :
1. Redémarrer CHNeoWave
2. Vérifier l'installation complète
3. Réinstaller si nécessaire

#### Tooltips en anglais
**Note** : Problème connu, correction prévue en v1.2.0

### Problèmes de Performance

#### Export HDF5 lent
**Optimisations** :
- Fermer les autres applications
- Utiliser un SSD pour l'export
- Réduire la taille des données si possible

#### Génération PDF lente
**Solutions** :
- Vérifier la RAM disponible (minimum 4 GB)
- Fermer les graphiques inutiles
- Redémarrer CHNeoWave

---

## 📚 Annexes

### Annexe A : Formats de Fichiers

#### Extensions Générées
- `.h5` : Fichiers HDF5 scientifiques
- `.pdf` : Certificats de calibration
- `.xlsx` : Données Excel
- `.csv` : Données CSV
- `.json` : Métadonnées JSON
- `.png` : Graphiques exportés

#### Tailles Typiques
- **HDF5** : 1-50 MB selon durée acquisition
- **PDF Certificat** : 50-150 kB
- **PDF Rapport** : 500 kB - 2 MB
- **Excel** : 100 kB - 10 MB

### Annexe B : Compatibilité Logiciels

#### Lecture HDF5
| Logiciel | Version | Commande/Package |
|----------|---------|------------------|
| MATLAB | R2018b+ | `h5read()` natif |
| Python | 3.6+ | `h5py`, `pandas` |
| R | 3.5+ | `rhdf5`, `hdf5r` |
| OriginPro | 2019+ | Import natif |
| Igor Pro | 8.0+ | HDF5 Browser |

#### Visualisation PDF
- Adobe Acrobat Reader (recommandé)
- Foxit Reader
- Navigateurs web modernes
- Visionneuses système (Windows, macOS, Linux)

### Annexe C : Spécifications Techniques

#### Hash SHA-256
- **Algorithme** : SHA-256 (256 bits)
- **Longueur** : 64 caractères hexadécimaux
- **Sécurité** : Cryptographiquement sûr
- **Usage** : Vérification d'intégrité uniquement

#### Format HDF5
- **Version** : HDF5 1.10+
- **Compression** : gzip niveau 6
- **Chunking** : Optimisé pour lecture séquentielle
- **Métadonnées** : UTF-8, JSON-compatible

#### Génération PDF
- **Bibliothèque** : ReportLab 3.6+
- **Format** : PDF/A-1b (archivage)
- **Résolution** : 300 DPI pour graphiques
- **Polices** : Intégrées (Helvetica, Times)

### Annexe D : Contacts et Support

#### Support Technique
- **Documentation** : `/docs/` dans l'installation
- **Tests** : `run_smoke_tests.py` pour diagnostic
- **Logs** : Niveau DEBUG dans les paramètres

#### Développement
- **Architecte Logiciel** : Spécialiste maritime
- **Domaine** : Laboratoires modèle réduit méditerranéens
- **Mission** : Solution de référence pour études maritimes

---

**CHNeoWave v1.1.0-beta** - Guide Utilisateur  
*Logiciel d'acquisition et d'analyse de données maritimes*  
*Développé pour les laboratoires d'études maritimes modèle réduit en Méditerranée*

*Version beta stable - Recommandée pour tests utilisateur en production*