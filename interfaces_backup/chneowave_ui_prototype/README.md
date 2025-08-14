# CHNeoWave - Interface Utilisateur Maritime

## 🌊 Vue d'ensemble

CHNeoWave est un prototype d'interface utilisateur moderne et ergonomique destiné aux laboratoires d'étude maritime sur modèles réduits en Méditerranée. Cette interface visuelle permet la gestion complète des projets d'acquisition de données de houle, de la calibration des sondes à l'analyse des résultats.

## 📋 Fonctionnalités Principales

### 🏠 Tableau de Bord Maritime
- **Visualisation en temps réel** des données de houle
- **KPI dynamiques** : hauteur de vague, période moyenne, taux d'acquisition
- **Graphiques interactifs** avec Chart.js
- **Système de notifications** en temps réel
- **Thème maritime** adaptatif (clair/sombre)

### 🚀 Gestion de Projets
- **Création de projets** avec assistant pas-à-pas
- **Configuration d'acquisition** personnalisable
- **Import/Export** de configurations
- **Validation automatique** des paramètres
- **Sauvegarde automatique** des brouillons

### 🔧 Calibration des Sondes
- **Interface de calibration** intuitive et guidée
- **Mesures bidirectionnelles** (montée/descente)
- **Calcul automatique** de la linéarité (R²)
- **Visualisation graphique** des résultats
- **Export des données** de calibration

### 🎨 Design et Ergonomie
- **Design responsive** adapté à tous les écrans
- **Animations fluides** et transitions CSS
- **Accessibilité** optimisée
- **Raccourcis clavier** pour une utilisation efficace
- **Thème maritime** avec palette de couleurs océaniques

## 🏗️ Structure du Projet

```
chneowave_ui_prototype/
├── index.html                 # Tableau de bord principal
├── project-start.html         # Page d'accueil des projets
├── project-create.html        # Formulaire de création de projet
├── calibration.html           # Interface de calibration
├── css/
│   ├── maritime_system.css    # Système de design maritime
│   ├── components.css         # Composants réutilisables
│   ├── layouts.css           # Layouts et grilles
│   ├── themes.css            # Thèmes clair/sombre
│   ├── project-pages.css     # Styles des pages de projet
│   ├── project-form.css      # Styles du formulaire de création
│   └── calibration.css       # Styles de l'interface de calibration
├── js/
│   ├── app.js                # Application principale
│   ├── components.js         # Composants UI
│   ├── animations.js         # Animations et transitions
│   ├── data-simulation.js    # Simulation de données
│   ├── project-navigation.js # Navigation entre projets
│   ├── project-form.js       # Logique du formulaire
│   ├── ui-interactions.js    # Interactions de calibration
│   ├── calibration-ui.js     # Interface avancée de calibration
│   └── dashboard-ui.js       # Interface avancée du tableau de bord
└── README.md                 # Documentation du projet
```

## 🎨 Système de Design Maritime

### Palette de Couleurs
- **Ocean Deep** (`#1a365d`) - Couleur principale sombre
- **Harbor Blue** (`#2e86ab`) - Couleur principale
- **Wave Crest** (`#a8dadc`) - Couleur secondaire
- **Foam White** (`#f1faee`) - Couleur de fond
- **Emerald Success** (`#457b9d`) - Couleur de succès

### Typographie
- **Police principale** : Inter (moderne et lisible)
- **Hiérarchie** claire avec des tailles définies
- **Espacement** basé sur le ratio doré (1.618)

### Composants
- **Cartes KPI** avec animations et tendances
- **Tableaux maritimes** avec tri et filtrage
- **Boutons** avec états interactifs
- **Badges de statut** colorés
- **Graphiques** Chart.js personnalisés

## 🚀 Installation et Utilisation

### Prérequis
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)
- Serveur web local (optionnel pour le développement)

### Lancement
1. **Cloner ou télécharger** le projet
2. **Ouvrir** `index.html` dans un navigateur
3. **Explorer** les différentes pages via la navigation

### Développement Local
```bash
# Avec Python
python -m http.server 8000

# Avec Node.js
npx http-server

# Avec PHP
php -S localhost:8000
```

## 🎯 Fonctionnalités Détaillées

### Tableau de Bord
- **Mise à jour en temps réel** des KPI toutes les 2 secondes
- **Graphique de houle** avec 50 points de données
- **Cartes d'action rapide** pour accéder aux fonctionnalités
- **Indicateurs de santé système** avec monitoring de performance

### Création de Projet
- **Assistant en 3 étapes** : Informations, Configuration, Validation
- **Validation en temps réel** des champs
- **Auto-génération** du code projet
- **Sauvegarde automatique** dans le localStorage

### Calibration
- **Sélection de sonde** avec navigation fluide
- **Configuration flexible** du nombre de points
- **Mesures simulées** avec animations
- **Calcul de linéarité** avec visualisation R²
- **Export des résultats** en JSON

## ⌨️ Raccourcis Clavier

### Globaux
- `Ctrl/Cmd + R` : Actualiser les données
- `Ctrl/Cmd + D` : Basculer le thème
- `F11` : Mode plein écran

### Calibration
- `Ctrl/Cmd + S` : Sauvegarder la calibration
- `Ctrl/Cmd + R` : Réinitialiser la calibration
- `←/→` : Navigation entre sondes
- `Espace` : Démarrer/arrêter la mesure

## 📱 Responsive Design

### Points de Rupture
- **Mobile** : < 768px
- **Tablette** : 768px - 1024px
- **Desktop** : > 1024px

### Adaptations
- **Grilles flexibles** qui s'adaptent à la taille d'écran
- **Navigation mobile** avec menu hamburger
- **Cartes empilées** sur petits écrans
- **Graphiques redimensionnables** automatiquement

## 🔧 Technologies Utilisées

### Frontend
- **HTML5** - Structure sémantique
- **CSS3** - Styles modernes avec variables CSS
- **JavaScript ES6+** - Logique interactive
- **Chart.js** - Graphiques et visualisations
- **Font Awesome** - Icônes vectorielles

### Fonctionnalités Avancées
- **CSS Grid & Flexbox** - Layouts modernes
- **CSS Animations** - Transitions fluides
- **LocalStorage** - Persistance des données
- **Responsive Images** - Optimisation mobile
- **Progressive Enhancement** - Amélioration progressive

## 🎨 Personnalisation

### Thèmes
Le système de thème utilise des variables CSS pour une personnalisation facile :

```css
:root {
  --ocean-deep: #1a365d;
  --harbor-blue: #2e86ab;
  --wave-crest: #a8dadc;
  --foam-white: #f1faee;
  --emerald-success: #457b9d;
}
```

### Composants
Tous les composants sont modulaires et réutilisables :
- Cartes KPI
- Tableaux de données
- Formulaires
- Boutons et contrôles
- Graphiques

## 📊 Simulation de Données

Le prototype inclut un système complet de simulation :
- **Données de houle** réalistes
- **Variations temporelles** naturelles
- **Sondes multiples** avec caractéristiques uniques
- **Résultats de calibration** calculés
- **Tendances et statistiques** dynamiques

## 🔮 Évolutions Futures

### Fonctionnalités Prévues
- **Connexion backend** pour données réelles
- **Authentification utilisateur** et gestion des rôles
- **Rapports automatisés** en PDF
- **API REST** pour intégration
- **Mode hors ligne** avec synchronisation

### Améliorations Techniques
- **Progressive Web App** (PWA)
- **WebSockets** pour temps réel
- **Service Workers** pour cache
- **Tests automatisés** (Jest, Cypress)
- **Build system** (Webpack, Vite)

## 🤝 Contribution

Ce projet est un prototype d'interface visuelle. Pour contribuer :

1. **Respecter** la structure existante
2. **Suivre** les conventions de nommage
3. **Tester** sur différents navigateurs
4. **Documenter** les nouvelles fonctionnalités

## 📄 Licence

Ce projet est développé pour les laboratoires d'étude maritime. Tous droits réservés.

## 📞 Support

Pour toute question ou suggestion concernant l'interface :
- Consulter la documentation intégrée
- Vérifier les commentaires dans le code
- Tester les fonctionnalités interactives

---

**CHNeoWave** - Interface Maritime Moderne pour l'Acquisition de Données de Houle

*Développé avec passion pour les sciences marines* 🌊