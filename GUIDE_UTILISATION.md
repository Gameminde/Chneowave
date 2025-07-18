# 🌊 CHNeoWave - Guide d'Utilisation

## Logiciel d'Étude Maritime - Modèles Réduits
**Laboratoire Méditerranéen - Bassins et Canaux**

---

## 🚀 Lancement du Logiciel

### Méthode 1: Script de lancement (Recommandé)
```bash
# Double-cliquer sur le fichier
launch_chneowave.bat
```

### Méthode 2: Ligne de commande
```bash
# Depuis le répertoire racine
cd "logciel hrneowave"
..\venv\Scripts\python.exe main.py
```

### Méthode 3: Script de démonstration
```bash
# Pour tester les modules sans interface graphique
venv\Scripts\python.exe demo_chneowave.py
```

---

## 🖥️ Interface Utilisateur

L'interface CHNeoWave est organisée en 4 modules principaux :

### 1. 🏠 **Écran d'Accueil (Welcome)**
- Présentation du logiciel
- Sélection du mode (clair/sombre)
- Navigation vers les modules

### 2. ⚙️ **Module de Calibration**
- Configuration des capteurs
- Étalonnage des instruments
- Validation des mesures

### 3. 📊 **Module d'Acquisition**
- Configuration des paramètres d'acquisition
- Acquisition en temps réel
- Sauvegarde des données

### 4. 🔬 **Module de Traitement**
- Analyse spectrale FFT
- Traitement des données de houle
- Génération de rapports

---

## 🧪 Test des Fonctionnalités

### Test 1: Simulation d'Acquisition
1. Lancer l'interface graphique
2. Naviguer vers le module d'acquisition
3. Sélectionner le mode "Simulation"
4. Configurer les paramètres :
   - Fréquence d'échantillonnage : 100 Hz
   - Durée : 10 secondes
   - Nombre de canaux : 4
5. Démarrer l'acquisition

### Test 2: Analyse Spectrale
1. Charger des données d'acquisition
2. Accéder au module de traitement
3. Lancer l'analyse FFT
4. Visualiser le spectre de puissance
5. Exporter les résultats

### Test 3: Calibration des Capteurs
1. Ouvrir le module de calibration
2. Sélectionner un capteur
3. Appliquer une calibration linéaire
4. Valider les coefficients
5. Sauvegarder la configuration

---

## 🔧 Fonctionnalités Avancées

### Buffer Circulaire Optimisé
- **Capacité** : Configurable (défaut: 1000 échantillons)
- **Performance** : Lock-free pour acquisition haute fréquence
- **Mémoire** : Gestion automatique avec mapping mémoire

### Processeur FFT Optimisé
- **Bibliothèque** : FFTW3 avec cache de plans
- **Parallélisation** : Multi-threading automatique
- **Formats** : Support des signaux réels et complexes

### Mode Offline Sécurisé
- **Protection** : Blocage des connexions réseau
- **Isolation** : Fonctionnement en laboratoire fermé
- **Sécurité** : Validation des accès système

---

## 📈 Acquisition de Données Réelles

### Matériel Supporté
- **Cartes NI-DAQ** : Série USB et PCI
- **Arduino** : Uno, Mega, STM32
- **Interfaces série** : USB-RS232, FTDI
- **Capteurs** : Accéléromètres, jauges de contrainte

### Configuration Typique
```
Capteur de houle → Conditionneur → Carte d'acquisition → CHNeoWave
```

### Paramètres Recommandés
- **Fréquence d'échantillonnage** : 50-200 Hz
- **Résolution** : 16 bits minimum
- **Filtrage** : Anti-aliasing à Fs/2.5
- **Calibration** : Étalonnage mensuel

---

## 🛠️ Dépannage

### Problèmes Courants

**Interface ne se lance pas :**
```bash
# Vérifier PyQt5
venv\Scripts\python.exe -c "import PyQt5; print('OK')"

# Réinstaller si nécessaire
venv\Scripts\pip install PyQt5
```

**Erreur d'importation :**
```bash
# Vérifier l'environnement
venv\Scripts\python.exe -c "import hrneowave; print('OK')"

# Ajouter le chemin si nécessaire
set PYTHONPATH=src
```

**Acquisition échoue :**
- Vérifier les permissions USB
- Tester en mode simulation
- Contrôler les drivers matériel

---

## 📊 Formats de Données

### Fichiers d'Entrée
- **CSV** : Données tabulaires
- **NPY** : Arrays NumPy
- **MAT** : Fichiers MATLAB
- **HDF5** : Données volumineuses

### Fichiers de Sortie
- **Rapports** : PDF, HTML
- **Graphiques** : PNG, SVG
- **Données** : CSV, Excel
- **Configuration** : JSON, YAML

---

## 🎯 Cas d'Usage Typiques

### Étude de Houle en Bassin
1. Calibration des sondes de hauteur
2. Acquisition synchronisée multi-points
3. Analyse spectrale directionnelle
4. Calcul des paramètres de houle

### Test de Modèles Réduits
1. Instrumentation du modèle
2. Acquisition des efforts/mouvements
3. Analyse des réponses dynamiques
4. Validation des coefficients hydrodynamiques

### Caractérisation de Canal
1. Mesure de la propagation
2. Analyse de la réflexion
3. Étude de la dispersion
4. Optimisation des absorbeurs

---

## 📞 Support Technique

**Laboratoire d'Études Maritimes (LEM)**
- Email : support@lem-maritime.fr
- Documentation : docs/
- Tests : pytest tests/
- Logs : logs/

---

*CHNeoWave v1.0 - Développé pour les laboratoires d'étude maritime en Méditerranée*