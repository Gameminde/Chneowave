# Détecteur de Cartes MCC DAQ - Interface Graphique

## Description

Interface graphique moderne pour la détection et le test des cartes MCC DAQ (Measurement Computing Data Acquisition). Cette application utilise PyQt6 pour fournir une interface utilisateur intuitive avec des indicateurs LED visuels et des fenêtres de détection en temps réel.

## Fonctionnalités

### 🔍 Détection Automatique
- Détection des cartes USB MCC
- Détection des cartes UDP MCC
- Test de connectivité en temps réel
- Indicateurs LED visuels (vert = connecté, rouge = déconnecté)

### 🎨 Interface Moderne
- Design moderne avec PyQt6
- Onglets séparés pour USB et UDP
- Barre de progression en temps réel
- Logs détaillés des opérations
- Statistiques en temps réel

### 📊 Informations Détaillées
- Nom et type de carte
- Numéro de série
- Nombre de canaux
- Résolution et taux d'échantillonnage
- Temps de réponse (pour UDP)
- Statut de connexion

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Windows (pour la compatibilité avec les DLLs MCC)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancement de l'application
```bash
python mcc_detector_gui.py
```

### Interface Utilisateur

#### En-tête
- **Titre** : Nom de l'application
- **LED Globale** : Indicateur de l'état global du système
- **Statut** : Texte descriptif de l'état actuel

#### Contrôles
- **🔍 Détecter les Cartes** : Lance la détection automatique
- **⏹️ Arrêter** : Arrête la détection en cours
- **Barre de Progression** : Affiche l'avancement de la détection

#### Onglets de Détection
- **🔌 Cartes USB** : Liste des cartes USB détectées
- **🌐 Cartes UDP** : Liste des cartes UDP détectées

#### Colonnes des Tableaux
1. **Nom** : Nom de la carte
2. **Type** : USB ou UDP
3. **Statut** : Connectée/Déconnectée
4. **LED** : Indicateur visuel
5. **Série** : Numéro de série
6. **Canaux** : Nombre de canaux
7. **Actions** : Bouton de test

#### Panneau de Détails
- **Logs** : Historique des opérations
- **Informations de la Carte** : Détails de la carte sélectionnée
- **Statistiques** : Résumé des cartes détectées

## Fonctionnalités Techniques

### Détection USB
- Simulation de détection des cartes USB-1608G et USB-1208HS
- Test de connectivité automatique
- Affichage des spécifications techniques

### Détection UDP
- Scan des ports UDP (8000-8005)
- Test de connectivité réseau
- Mesure du temps de réponse
- Simulation de cartes UDP-1208HS et UDP-1608G

### Threading
- Détection asynchrone pour éviter le gel de l'interface
- Signaux PyQt6 pour la communication thread-interface
- Gestion propre des erreurs

## Structure du Code

```
mcc_detector_gui.py
├── LEDIndicator          # Widget LED personnalisé
├── MCCDetectorThread     # Thread de détection
└── MCCDetectorGUI        # Interface principale
    ├── create_header()   # En-tête
    ├── create_controls() # Contrôles
    ├── create_detection_panel() # Panneau de détection
    └── create_details_panel()   # Panneau de détails
```

## Simulation

L'application utilise actuellement des données simulées pour démontrer les fonctionnalités :

### Cartes USB Simulées
- **USB-1608G** : 16 canaux, 16-bit, 100kS/s
- **USB-1208HS** : 8 canaux, 12-bit, 50kS/s

### Cartes UDP Simulées
- **UDP-1208HS** : Connectée, IP 192.168.1.100:8000
- **UDP-1608G** : Déconnectée, IP 192.168.1.101:8001

## Intégration avec les DLLs MCC

L'application est conçue pour intégrer les DLLs Measurement Computing :
- `HAL.dll`
- `ULx.dll`
- `HAL.UL.dll`

Ces DLLs doivent être présentes dans le dossier `Measurement Computing/DAQami/` pour une détection réelle.

## Logs

L'application génère des logs détaillés dans le fichier `mcc_gui_detector.log` :
- Détection des cartes
- Tests de connectivité
- Erreurs et avertissements
- Statistiques de performance

## Développement

### Ajout de Nouvelles Cartes
Pour ajouter de nouvelles cartes simulées, modifiez les listes dans :
- `detect_usb_cards()` pour les cartes USB
- `detect_udp_cards()` pour les cartes UDP

### Personnalisation de l'Interface
- Modifiez les styles CSS dans les méthodes `create_*()`
- Ajustez les couleurs des LEDs dans `LEDIndicator`
- Personnalisez les icônes et emojis

## Dépannage

### Problèmes Courants
1. **PyQt6 non installé** : `pip install PyQt6`
2. **Erreur de DLL** : Vérifiez la présence des DLLs MCC
3. **Interface gelée** : La détection s'exécute en arrière-plan

### Logs de Débogage
Consultez le fichier `mcc_gui_detector.log` pour les détails techniques.

## Licence

Ce projet est développé pour l'intégration avec CHNeoWave et les cartes MCC DAQ.

## Support

Pour toute question ou problème, consultez la documentation CHNeoWave ou contactez l'équipe de développement.




