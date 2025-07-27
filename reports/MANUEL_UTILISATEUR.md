# CHNeoWave - Manuel Utilisateur v1.0.0

## Introduction

Bienvenue dans CHNeoWave, le logiciel d'acquisition et d'analyse de données pour les études maritimes en modèles réduits. Ce manuel vous guidera à travers les fonctionnalités de base de l'application.

## 1. Lancement de l'application

Pour lancer CHNeoWave, exécutez la commande suivante à la racine du projet :

```bash
python src/hrneowave/gui/main.py
```

L'interface principale s'ouvrira, affichant la vue d'accueil.

## 2. Création d'un nouveau projet

Un projet est nécessaire pour organiser vos acquisitions.

1.  Depuis la vue d'accueil, cliquez sur le bouton "Nouveau Projet".
2.  Une boîte de dialogue apparaîtra vous demandant de sélectionner un répertoire pour enregistrer votre projet.
3.  Choisissez un emplacement et donnez un nom à votre projet.
4.  Une fois le projet créé, l'interface principale affichera les différentes vues disponibles (Acquisition, Analyse, etc.).

## 3. Lancer une acquisition de données

L'onglet "Acquisition" vous permet de configurer et de lancer la collecte de données.

1.  **Configuration** : Dans le panneau de configuration de l'acquisition, définissez les paramètres requis, tels que la fréquence d'échantillonnage, la durée de l'acquisition, et les canaux à utiliser.
2.  **Démarrer l'acquisition** : Cliquez sur le bouton "Démarrer l'Acquisition". Le système commencera à collecter les données en utilisant le matériel configuré (ou le simulateur par défaut).
3.  **Visualisation en temps réel** : Un graphique affichera les données en temps réel pendant l'acquisition.
4.  **Arrêter l'acquisition** : Cliquez sur "Arrêter l'Acquisition" pour terminer la collecte. Les données seront automatiquement sauvegardées dans le répertoire de votre projet.

## 4. Analyser les résultats

L'onglet "Analyse" vous permet de traiter et de visualiser les données acquises.

1.  **Charger une acquisition** : Sélectionnez une session d'acquisition précédemment enregistrée dans votre projet.
2.  **Choisir une analyse** : Sélectionnez le type d'analyse que vous souhaitez effectuer (par exemple, analyse spectrale FFT, analyse de Goda).
3.  **Lancer l'analyse** : Cliquez sur "Lancer l'Analyse". Le traitement s'effectuera en arrière-plan.
4.  **Voir les résultats** : Les résultats de l'analyse (graphiques, tableaux de valeurs) s'afficheront dans la zone de visualisation.

## 5. Gestion des configurations

CHNeoWave permet de gérer des configurations de laboratoire prédéfinies pour différents types d'essais (bassin, canal, etc.).

1.  Allez dans l'onglet "Configuration".
2.  Sélectionnez un préréglage dans la liste déroulante (par exemple, "Bassin Méditerranéen - Houle Courte").
3.  Les paramètres de l'application (acquisition, traitement) seront automatiquement ajustés en fonction de ce préréglage.

Pour toute question ou problème, veuillez consulter la documentation du code ou contacter l'équipe de développement.