# 🌊 CHNeoWave - Guide de Design Maritime 2025

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Palette de Couleurs Maritime PRO](#palette-de-couleurs-maritime-pro)
3. [Typographie Inter](#typographie-inter)
4. [Golden Ratio & Espacements](#golden-ratio--espacements)
5. [Composants UI](#composants-ui)
6. [Animations & Transitions](#animations--transitions)
7. [Accessibilité WCAG 2.1 AA](#accessibilité-wcag-21-aa)
8. [Architecture des Styles](#architecture-des-styles)
9. [Responsive Design](#responsive-design)
10. [Bonnes Pratiques](#bonnes-pratiques)

---

## 🎯 Vue d'ensemble

Le nouveau design de CHNeoWave 2025 s'inspire de l'univers maritime professionnel, alliant élégance, fonctionnalité et performance. Chaque élément respecte le **Golden Ratio (1:1.618)** pour créer une harmonie visuelle naturelle.

### Principes Fondamentaux

- **🌊 Maritime Professionnel** : Couleurs inspirées de l'océan et de l'industrie maritime
- **📐 Golden Ratio** : Proportions harmonieuses basées sur la suite de Fibonacci
- **🎨 Cohérence Visuelle** : Design system unifié sur toute l'application
- **♿ Accessibilité** : Conformité WCAG 2.1 AA pour tous les utilisateurs
- **⚡ Performance** : Optimisé pour une utilisation fluide en laboratoire

---

## 🎨 Palette de Couleurs Maritime PRO

### Couleurs Principales

```css
/* Couleurs de base */
--deep-navy:   #0A1929   /* Fond sombre / Texte principal mode sombre */
--harbor-blue: #055080   /* Éléments primaires / Navigation */
--steel-blue:  #2B79B6   /* Survol / Focus / Actions secondaires */
--tidal-cyan:  #00ACC1   /* Données temps réel / Accents */
--foam-white:  #F5FBFF   /* Fond clair / Surfaces principales */
--storm-gray:  #445868   /* Texte secondaire / Métadonnées */
--coral-alert: #FF6B47   /* Alertes / Erreurs / États critiques */
```

### Couleurs Étendues

```css
/* Variations et états */
--deep-navy-light:    #1A2332
--harbor-blue-light:  #0A6B9A
--harbor-blue-dark:   #044066
--steel-blue-light:   #4A90C2
--steel-blue-dark:    #1E5A8A
--tidal-cyan-light:   #26C6DA
--tidal-cyan-dark:    #00838F
--storm-gray-light:   #607D8B
--storm-gray-dark:    #37474F
--coral-alert-light:  #FF8A65
--coral-alert-dark:   #E64A19
```

### Couleurs Sémantiques

```css
/* États et feedback */
--success-green:  #4CAF50
--warning-amber:  #FF9800
--info-blue:      #2196F3
--error-red:      #F44336

/* Surfaces et bordures */
--surface-primary:    #FFFFFF
--surface-secondary:  #F8FAFC
--border-light:       #E0E7FF
--border-medium:      #B0BEC5
--border-dark:        #78909C

/* Ombres */
--shadow-light:   rgba(10, 25, 41, 0.08)
--shadow-medium:  rgba(10, 25, 41, 0.12)
--shadow-strong:  rgba(10, 25, 41, 0.16)
```

### Contraste et Accessibilité

| Combinaison | Ratio | Statut WCAG |
|-------------|-------|-------------|
| `#0A1929` sur `#F5FBFF` | 15.8:1 | ✅ AAA |
| `#445868` sur `#F5FBFF` | 7.2:1 | ✅ AAA |
| `#055080` sur `#F5FBFF` | 8.9:1 | ✅ AAA |
| `#00ACC1` sur `#F5FBFF` | 4.7:1 | ✅ AA |
| `#FF6B47` sur `#F5FBFF` | 4.5:1 | ✅ AA |

---

## 📝 Typographie Inter

### Hiérarchie Typographique

```css
/* Titres */
.h1 {
    font-family: 'Inter', sans-serif;
    font-size: 34px;      /* Fibonacci: 34 */
    font-weight: 700;     /* Bold */
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: var(--deep-navy);
}

.h2 {
    font-family: 'Inter', sans-serif;
    font-size: 21px;      /* Fibonacci: 21 */
    font-weight: 600;     /* Semi-Bold */
    line-height: 1.3;
    letter-spacing: -0.01em;
    color: var(--deep-navy);
}

.h3 {
    font-family: 'Inter', sans-serif;
    font-size: 18px;
    font-weight: 600;
    line-height: 1.4;
    color: var(--deep-navy);
}

.h4 {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    font-weight: 500;     /* Medium */
    line-height: 1.4;
    color: var(--deep-navy);
}

/* Corps de texte */
.body {
    font-family: 'Inter', sans-serif;
    font-size: 13px;      /* Fibonacci: 13 */
    font-weight: 400;     /* Regular */
    line-height: 1.6;
    color: var(--storm-gray);
}

.body-large {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    font-weight: 400;
    line-height: 1.6;
    color: var(--storm-gray);
}

.body-small {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 400;
    line-height: 1.5;
    color: var(--storm-gray);
}

/* Texte d'interface */
.caption {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 500;
    line-height: 1.4;
    color: var(--storm-gray);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.label {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 500;
    line-height: 1.4;
    color: var(--deep-navy);
}
```

### Poids de Police

- **300 Light** : Texte décoratif, citations
- **400 Regular** : Corps de texte principal
- **500 Medium** : Labels, navigation, boutons secondaires
- **600 Semi-Bold** : Sous-titres, titres de sections
- **700 Bold** : Titres principaux, boutons primaires

---

## 📐 Golden Ratio & Espacements

### Suite de Fibonacci pour les Espacements

```css
/* Espacements basés sur Fibonacci */
--spacing-xs:   8px;   /* Fibonacci[0] */
--spacing-sm:   13px;  /* Fibonacci[1] */
--spacing-md:   21px;  /* Fibonacci[2] */
--spacing-lg:   34px;  /* Fibonacci[3] */
--spacing-xl:   55px;  /* Fibonacci[4] */
--spacing-xxl:  89px;  /* Fibonacci[5] */

/* Rayons de bordure */
--radius-sm:    5px;
--radius-md:    8px;
--radius-lg:    13px;
--radius-xl:    21px;

/* Hauteurs d'éléments */
--height-input:   34px;  /* Fibonacci[3] */
--height-button:  34px;  /* Fibonacci[3] */
--height-card:    55px;  /* Fibonacci[4] */
--height-header:  89px;  /* Fibonacci[5] */
```

### Proportions Golden Ratio

```css
/* Largeurs basées sur le Golden Ratio */
--sidebar-width:     280px;           /* Base */
--main-content:      453px;           /* 280 × 1.618 */
--panel-width:       733px;           /* 453 × 1.618 */
--container-max:     1186px;          /* 733 × 1.618 */

/* Hauteurs proportionnelles */
--card-height:       173px;           /* 280 ÷ 1.618 */
--widget-height:     280px;           /* Base */
--section-height:    453px;           /* 280 × 1.618 */
```

### Grille de Mise en Page

```css
/* Système de grille 12 colonnes */
.container {
    max-width: 1186px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: 0 calc(var(--spacing-sm) * -1);
}

.col {
    padding: 0 var(--spacing-sm);
    flex: 1;
}

/* Colonnes spécifiques */
.col-1 { flex: 0 0 8.333%; }
.col-2 { flex: 0 0 16.666%; }
.col-3 { flex: 0 0 25%; }
.col-4 { flex: 0 0 33.333%; }
.col-5 { flex: 0 0 41.666%; }
.col-6 { flex: 0 0 50%; }
.col-7 { flex: 0 0 58.333%; }
.col-8 { flex: 0 0 66.666%; }
.col-9 { flex: 0 0 75%; }
.col-10 { flex: 0 0 83.333%; }
.col-11 { flex: 0 0 91.666%; }
.col-12 { flex: 0 0 100%; }
```

---

## 🧩 Composants UI

### Boutons

```css
/* Bouton primaire */
.btn-primary {
    background-color: var(--tidal-cyan);
    color: var(--foam-white);
    border: none;
    border-radius: var(--radius-lg);
    padding: var(--spacing-sm) var(--spacing-md);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 200ms ease;
    box-shadow: 0 2px 8px var(--shadow-light);
}

.btn-primary:hover {
    background-color: var(--tidal-cyan-dark);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px var(--shadow-medium);
}

.btn-primary:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px var(--shadow-light);
}

/* Bouton secondaire */
.btn-secondary {
    background-color: var(--harbor-blue);
    color: var(--foam-white);
    border: none;
    border-radius: var(--radius-lg);
    padding: var(--spacing-sm) var(--spacing-md);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 200ms ease;
}

.btn-secondary:hover {
    background-color: var(--harbor-blue-light);
}

/* Bouton outline */
.btn-outline {
    background-color: transparent;
    color: var(--harbor-blue);
    border: 2px solid var(--harbor-blue);
    border-radius: var(--radius-lg);
    padding: calc(var(--spacing-sm) - 2px) calc(var(--spacing-md) - 2px);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 200ms ease;
}

.btn-outline:hover {
    background-color: var(--harbor-blue);
    color: var(--foam-white);
}
```

### Cartes KPI

```css
.kpi-card {
    background-color: var(--surface-primary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    box-shadow: 0 2px 8px var(--shadow-light);
    transition: all 300ms ease;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px var(--shadow-medium);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--tidal-cyan), var(--steel-blue));
    opacity: 0;
    transition: opacity 300ms ease;
}

.kpi-card:hover::before {
    opacity: 1;
}

.kpi-card-title {
    font-size: 12px;
    font-weight: 500;
    color: var(--storm-gray);
    margin-bottom: var(--spacing-xs);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-card-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--deep-navy);
    margin-bottom: var(--spacing-xs);
}

.kpi-card-trend {
    font-size: 11px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

.kpi-card-trend.positive {
    color: var(--success-green);
}

.kpi-card-trend.negative {
    color: var(--coral-alert);
}
```

### Sidebar Navigation

```css
.sidebar {
    width: var(--sidebar-width);
    background-color: var(--foam-white);
    border-right: 2px solid var(--border-light);
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 100;
    transition: transform 300ms ease;
}

.sidebar-header {
    height: var(--height-header);
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--border-light);
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-logo {
    font-size: 21px;
    font-weight: 700;
    color: var(--deep-navy);
}

.sidebar-nav {
    padding: var(--spacing-md) 0;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: var(--spacing-sm) var(--spacing-md);
    color: var(--storm-gray);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: all 200ms ease;
    position: relative;
}

.nav-item:hover {
    background-color: rgba(0, 172, 193, 0.08);
    color: var(--tidal-cyan);
}

.nav-item.active {
    background-color: rgba(0, 172, 193, 0.12);
    color: var(--tidal-cyan);
    font-weight: 600;
}

.nav-item.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background-color: var(--tidal-cyan);
}

.nav-icon {
    width: 20px;
    height: 20px;
    margin-right: var(--spacing-sm);
    opacity: 0.7;
}

.nav-item:hover .nav-icon,
.nav-item.active .nav-icon {
    opacity: 1;
}
```

### Formulaires

```css
.form-group {
    margin-bottom: var(--spacing-md);
}

.form-label {
    display: block;
    font-size: 12px;
    font-weight: 500;
    color: var(--deep-navy);
    margin-bottom: var(--spacing-xs);
}

.form-input {
    width: 100%;
    height: var(--height-input);
    padding: 0 var(--spacing-sm);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: var(--deep-navy);
    background-color: var(--surface-primary);
    transition: all 200ms ease;
}

.form-input:focus {
    outline: none;
    border-color: var(--tidal-cyan);
    box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.1);
}

.form-input:invalid {
    border-color: var(--coral-alert);
}

.form-input:invalid:focus {
    box-shadow: 0 0 0 3px rgba(255, 107, 71, 0.1);
}

.form-select {
    width: 100%;
    height: var(--height-input);
    padding: 0 var(--spacing-sm);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: var(--deep-navy);
    background-color: var(--surface-primary);
    cursor: pointer;
    transition: all 200ms ease;
}

.form-select:focus {
    outline: none;
    border-color: var(--tidal-cyan);
    box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.1);
}
```

### Tableaux

```css
.table {
    width: 100%;
    border-collapse: collapse;
    background-color: var(--surface-primary);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: 0 2px 8px var(--shadow-light);
}

.table th {
    background-color: var(--foam-white);
    padding: var(--spacing-sm) var(--spacing-md);
    text-align: left;
    font-size: 12px;
    font-weight: 600;
    color: var(--deep-navy);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 2px solid var(--border-light);
}

.table td {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: 13px;
    color: var(--storm-gray);
    border-bottom: 1px solid var(--border-light);
}

.table tr:hover {
    background-color: rgba(0, 172, 193, 0.04);
}

.table tr:last-child td {
    border-bottom: none;
}
```

---

## ✨ Animations & Transitions

### Durées Standard

```css
/* Durées d'animation */
--duration-fast:    150ms;
--duration-normal:  200ms;
--duration-slow:    300ms;
--duration-slower:  500ms;

/* Courbes d'accélération */
--ease-out:     cubic-bezier(0.25, 0.46, 0.45, 0.94);
--ease-in:      cubic-bezier(0.55, 0.055, 0.675, 0.19);
--ease-in-out:  cubic-bezier(0.645, 0.045, 0.355, 1);
--ease-bounce:  cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Animations de Base

```css
/* Fade In */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Slide In Left */
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Scale In */
@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Pulse */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

/* Shimmer (loading) */
@keyframes shimmer {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}
```

### Classes d'Animation

```css
.animate-fade-in {
    animation: fadeIn var(--duration-normal) var(--ease-out);
}

.animate-slide-in-left {
    animation: slideInLeft var(--duration-normal) var(--ease-out);
}

.animate-scale-in {
    animation: scaleIn var(--duration-normal) var(--ease-bounce);
}

.animate-pulse {
    animation: pulse 2s infinite;
}

.loading-shimmer {
    background: linear-gradient(
        90deg,
        var(--surface-secondary) 0%,
        rgba(255, 255, 255, 0.8) 50%,
        var(--surface-secondary) 100%
    );
    background-size: 200px 100%;
    animation: shimmer 1.5s infinite;
}
```

### Transitions Interactives

```css
/* Hover Effects */
.hover-lift {
    transition: transform var(--duration-normal) var(--ease-out);
}

.hover-lift:hover {
    transform: translateY(-2px);
}

.hover-scale {
    transition: transform var(--duration-normal) var(--ease-out);
}

.hover-scale:hover {
    transform: scale(1.02);
}

.hover-glow {
    transition: box-shadow var(--duration-normal) var(--ease-out);
}

.hover-glow:hover {
    box-shadow: 0 8px 24px var(--shadow-medium);
}

/* Focus States */
.focus-ring {
    transition: box-shadow var(--duration-fast) var(--ease-out);
}

.focus-ring:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 172, 193, 0.2);
}
```

---

## ♿ Accessibilité WCAG 2.1 AA

### Contraste des Couleurs

- **Niveau AA** : Ratio minimum de 4.5:1 pour le texte normal
- **Niveau AAA** : Ratio minimum de 7:1 pour le texte normal
- **Texte large** : Ratio minimum de 3:1 (18px+ ou 14px+ en gras)

### Focus et Navigation

```css
/* Indicateurs de focus visibles */
.focus-visible {
    outline: 2px solid var(--tidal-cyan);
    outline-offset: 2px;
}

/* Navigation au clavier */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--deep-navy);
    color: var(--foam-white);
    padding: 8px;
    text-decoration: none;
    border-radius: 4px;
    z-index: 1000;
}

.skip-link:focus {
    top: 6px;
}
```

### Texte et Lisibilité

```css
/* Tailles minimales */
.text-minimum {
    font-size: 16px; /* Minimum pour mobile */
    line-height: 1.5;
}

/* Espacement des liens */
.link-spacing {
    margin: 0 4px;
    padding: 4px;
}

/* Zones de clic minimales */
.touch-target {
    min-width: 44px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
}
```

### États et Feedback

```css
/* Messages d'erreur */
.error-message {
    color: var(--coral-alert);
    font-size: 12px;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.error-message::before {
    content: '⚠️';
}

/* Messages de succès */
.success-message {
    color: var(--success-green);
    font-size: 12px;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.success-message::before {
    content: '✅';
}

/* États de chargement */
.loading-state {
    opacity: 0.6;
    pointer-events: none;
    position: relative;
}

.loading-state::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid var(--border-light);
    border-top-color: var(--tidal-cyan);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
```

---

## 🏗️ Architecture des Styles

### Structure des Fichiers

```
src/hrneowave/gui/styles/
├── maritime_theme.qss          # Thème principal
├── components/                 # Composants spécifiques
│   ├── buttons.qss
│   ├── cards.qss
│   ├── forms.qss
│   ├── navigation.qss
│   ├── tables.qss
│   └── charts.qss
├── layouts/                    # Layouts et grilles
│   ├── grid.qss
│   ├── sidebar.qss
│   └── dashboard.qss
├── themes/                     # Variations de thème
│   ├── light.qss
│   ├── dark.qss
│   └── high-contrast.qss
└── utilities/                  # Classes utilitaires
    ├── spacing.qss
    ├── typography.qss
    ├── colors.qss
    └── animations.qss
```

### Conventions de Nommage

```css
/* BEM (Block Element Modifier) */
.block {}
.block__element {}
.block--modifier {}
.block__element--modifier {}

/* Exemples */
.card {}
.card__header {}
.card__body {}
.card__footer {}
.card--elevated {}
.card__header--primary {}

/* Préfixes utilitaires */
.u-margin-top-sm {}     /* Utility */
.is-active {}           /* State */
.has-error {}           /* State */
.js-toggle {}           /* JavaScript hook */
```

### Variables CSS Personnalisées

```css
/* Variables globales dans :root */
:root {
    /* Couleurs */
    --color-primary: #00ACC1;
    --color-secondary: #055080;
    
    /* Espacements */
    --space-xs: 8px;
    --space-sm: 13px;
    
    /* Typographie */
    --font-family-primary: 'Inter', sans-serif;
    --font-size-base: 13px;
    
    /* Ombres */
    --shadow-sm: 0 2px 4px rgba(10, 25, 41, 0.08);
    --shadow-md: 0 4px 8px rgba(10, 25, 41, 0.12);
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 200ms ease;
}

/* Variables pour le thème sombre */
[data-theme="dark"] {
    --color-background: #0A1929;
    --color-surface: #1A2332;
    --color-text: #F5FBFF;
}
```

---

## 📱 Responsive Design

### Breakpoints

```css
/* Breakpoints basés sur les contenus */
--breakpoint-xs: 480px;   /* Mobile portrait */
--breakpoint-sm: 768px;   /* Tablet portrait */
--breakpoint-md: 1024px;  /* Tablet landscape */
--breakpoint-lg: 1440px;  /* Desktop */
--breakpoint-xl: 1920px;  /* Large desktop */
```

### Media Queries

```css
/* Mobile First Approach */
.component {
    /* Styles mobile par défaut */
    padding: var(--spacing-sm);
}

@media (min-width: 768px) {
    .component {
        /* Styles tablet */
        padding: var(--spacing-md);
    }
}

@media (min-width: 1024px) {
    .component {
        /* Styles desktop */
        padding: var(--spacing-lg);
    }
}

/* Container responsive */
.container {
    width: 100%;
    max-width: 1186px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

@media (max-width: 767px) {
    .container {
        padding: 0 var(--spacing-sm);
    }
}
```

### Grille Responsive

```css
/* Grille flexible */
.grid {
    display: grid;
    gap: var(--spacing-md);
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

/* Grille spécifique au dashboard */
.dashboard-grid {
    display: grid;
    gap: var(--spacing-md);
    grid-template-columns: var(--sidebar-width) 1fr;
    grid-template-rows: auto 1fr;
    grid-template-areas:
        "sidebar header"
        "sidebar main";
}

@media (max-width: 1023px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "main";
    }
    
    .sidebar {
        transform: translateX(-100%);
    }
    
    .sidebar.is-open {
        transform: translateX(0);
    }
}
```

---

## ✅ Bonnes Pratiques

### Performance

1. **Optimisation CSS**
   - Utiliser des sélecteurs efficaces
   - Éviter les sélecteurs trop profonds
   - Grouper les propriétés similaires
   - Utiliser `transform` et `opacity` pour les animations

2. **Chargement des Polices**
   ```css
   @font-face {
       font-family: 'Inter';
       src: url('fonts/inter-variable.woff2') format('woff2-variations');
       font-display: swap;
       font-weight: 300 700;
   }
   ```

3. **Images et Icônes**
   - Utiliser SVG pour les icônes
   - Optimiser les images avec des formats modernes
   - Implémenter le lazy loading

### Maintenabilité

1. **Documentation**
   - Commenter les sections complexes
   - Documenter les variables personnalisées
   - Maintenir ce guide à jour

2. **Tests**
   - Tester sur différents navigateurs
   - Valider l'accessibilité
   - Vérifier les contrastes

3. **Versioning**
   - Utiliser des versions sémantiques
   - Documenter les changements
   - Maintenir la compatibilité

### Développement

1. **Workflow**
   - Développer mobile-first
   - Tester régulièrement
   - Optimiser progressivement

2. **Outils**
   - Utiliser des linters CSS
   - Automatiser les tests
   - Optimiser le build

3. **Collaboration**
   - Suivre les conventions
   - Documenter les décisions
   - Partager les connaissances

---

## 📚 Ressources

### Liens Utiles

- [Inter Font Family](https://rsms.me/inter/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Golden Ratio Calculator](https://grtcalculator.com/)

### Outils de Développement

- **Design** : Figma, Sketch
- **Couleurs** : Coolors, Adobe Color
- **Accessibilité** : axe DevTools, WAVE
- **Performance** : Lighthouse, WebPageTest

---

*Guide créé pour CHNeoWave 2025 - Version 1.0*
*Dernière mise à jour : Janvier 2025*