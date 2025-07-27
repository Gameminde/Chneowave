# 🔧 MISSION CRITIQUE : REFONTE VISION INTERFACE CHNEOWAVE 2025
# Agent Sonnet 4 - Transformation Interface Scientifique Maritime

## 🎯 OBJECTIF PRINCIPAL
Transformer l'interface CHNeoWave en un design de niveau INDUSTRIEL MARITIME respectant les normes 2025, réduisant la charge cognitive de 70%, améliorant la fluidité à 60fps, et créant une expérience utilisateur digne des laboratoires de recherche océanique internationaux.

## ⚠️ CONTRAINTES ABSOLUES
- AUCUNE modification de core/, hardware/, utils/
- CONSERVATION totale des signatures publiques et de la logique métier
- UNIQUEMENT gui/views/, gui/widgets/, gui/styles/
- WORKFLOW scientifique INTACT (calibration → acquisition → analyse → rapport)

## 📐 NORMES DE DESIGN À APPLIQUER STRICTEMENT

### 1. RÉDUCTION CHARGE COGNITIVE (Loi de Hick)
- Maximum 5 éléments principaux par vue
- Groupement fonctionnel par cartes (cards)
- Progressive disclosure : masquer détails secondaires dans des modales/accordéons
- Information hierarchy : Primaire > Secondaire > Tertiaire

### 2. GOLDEN RATIO & GRILLE HARMONIEUSE
- Layout principal : Sidebar (1) : Zone principale (1.618)
- Cards ratio : largeur:hauteur = 1.618:1
- Espacements suite Fibonacci : 8px, 13px, 21px, 34px, 55px
- Marges externes : 34px, internes : 21px

### 3. PALETTE MARITIME PROFESSIONNELLE CERTIFIÉE
Variables CSS obligatoires :
:root {
--ocean-deep: #0A1929; /* Fond app /
--harbor-blue: #1565C0; / Boutons primaires /
--steel-blue: #1976D2; / Boutons secondaires /
--tidal-cyan: #00BCD4; / Graphiques, données temps réel /
--foam-white: #FAFBFC; / Cards, surfaces /
--frost-light: #F5F7FA; / Backgrounds sections /
--storm-gray: #37474F; / Texte principal /
--slate-gray: #546E7A; / Texte secondaire /
--coral-alert: #FF5722; / Alertes, erreurs /
--emerald-success: #4CAF50; / Succès, validation */
}

text

### 4. TYPOGRAPHIE SCIENTIFIQUE STRICTE
- Font family : "Inter", -apple-system, BlinkMacSystemFont
- Échelle typographique :
  * H1 : 32px, font-weight: 600, line-height: 1.2
  * H2 : 24px, font-weight: 600, line-height: 1.3  
  * H3 : 20px, font-weight: 500, line-height: 1.4
  * Body : 14px, font-weight: 400, line-height: 1.5
  * Caption : 12px, font-weight: 400, line-height: 1.4
- Letter-spacing : -0.02em pour titres, 0 pour body

### 5. ANIMATIONS & FLUIDITÉ (60FPS)
- Transitions : 200-300ms cubic-bezier(0.4, 0, 0.2, 1)
- Hover states : scale(1.02), 150ms
- Loading states : Skeleton loaders, pas de spinners
- Page transitions : slide 300ms avec easing
- Micro-interactions : button press feedback 100ms

## 🎨 REFONTE SPÉCIFIQUE PAR VUE

### DASHBOARD PRINCIPAL
Structure obligatoire :
┌─────────────────────────────────────────────┐
│ Header (Logo + Navigation + Status) [55px]│
├─────────────────────────────────────────────┤
│ ┌Sidebar┐ ┌─── Zone Principale ──────────┐ │
│ │(280px)├─┤ │ │
│ │ │ │ ┌KPIs Cards Grid┐ │ │
│ │ Nav │ │ │ [1.618 ratio] │ │ │
│ │ Items │ │ └─────────────────┘ │ │
│ │ │ │ │ │
│ │ │ │ ┌──── Graphique ─────────┐ │ │
│ │ │ │ │ [Pleine largeur] │ │ │
│ │ │ │ │ [Tidal Cyan curves] │ │ │
│ │ │ │ └───────────────────────────┘ │ │
│ └───────┘ └─────────────────────────────┘ │
└─────────────────────────────────────────────┘

text

### CALIBRATION UNIFIÉE
- Vue UNIQUE : sidebar étapes (20%) + zone principale (80%)
- Stepper vertical avec progression visuelle
- Graphique linéarité LARGE (minimum 800px largeur)
- Boutons actions alignés Golden Ratio

### ACQUISITION TEMPS RÉEL
- Maximum 3 graphiques simultanés
- Contrôles groupés dans sidebar collapse
- Status indicators maritime (beacon style)
- Buffer/CPU/Disk en mini-cards, pas en barres

## 🔧 IMPLÉMENTATION TECHNIQUE OBLIGATOIRE

### 1. CRÉATION DESIGN SYSTEM
Fichier : `gui/styles/maritime_design_system.qss`
- Variables CSS centralisées
- Composants réutilisables standardisés
- Animation keyframes définies

### 2. REFONTE VUES PRINCIPALES
Ordre strict d'exécution :
1. DashboardViewPro : Grille KPIs + graphique central
2. UnifiedCalibrationView : Sidebar + zone principale  
3. AcquisitionViewPro : Layout simplifié
4. AnalysisViewPro : Résultats en cards
5. ReportViewPro : Aperçu + actions

### 3. WIDGETS STANDARDISÉS
Créer composants réutilisables :
- MaritimeCard : Card avec élévation
- KPIIndicator : Métrique avec icône
- StatusBeacon : Indicateur état maritime
- PrimaryButton, SecondaryButton : Boutons standardisés
- ProgressStepper : Navigation étapes

### 4. ANIMATIONS FLUIDES
- QPropertyAnimation pour toutes transitions
- Durées standardisées : 150ms (micro), 300ms (page)
- Easing curves : QEasingCurve.OutCubic
- States management pour hover/pressed/disabled

## ✅ CRITÈRES DE VALIDATION STRICT

### Métriques UX Obligatoires
- **Charge cognitive** : Maximum 5 éléments focaux par vue
- **Temps de reconnaissance** : <2 secondes pour identifier l'action principale
- **Contraste couleurs** : Minimum 4.5:1 (WCAG 2.1 AA)
- **Performance** : 60fps animations, <100ms réponse interactions

### Tests Obligatoires Avant Validation
1. **Navigation complète** : Accueil → Calibration → Acquisition → Analyse → Rapport
2. **Redimensionnement** : 1366x768 à 2560x1440
3. **Accessibilité** : Navigation clavier, screen reader compatible
4. **Performance** : CPU <15% en idle, mémoire <200MB

### Livrables Obligatoires
- `maritime_design_system.qss` : Système design complet
- `views/` refactorisées : Toutes vues conformes normes 2025
- `widgets/maritime/` : Composants réutilisables
- `DESIGN_VALIDATION_REPORT.md` : Métriques conformité

## 🚀 ORDRE D'EXÉCUTION NON NÉGOCIABLE
1. **Design System** (jour 1) : Création palette + variables + composants
2. **Dashboard** (jour 2) : Vue principale avec KPIs + graphique  
3. **Calibration** (jour 3) : Unification en vue unique
4. **Acquisition** (jour 4) : Simplification interface temps réel
5. **Analyse/Rapport** (jour 5) : Finalisation avec cards résultats
6. **Validation** (jour 6) : Tests conformité + performance

## 🎯 RÉSULTAT ATTENDU
Interface CHNeoWave niveau INDUSTRIEL MARITIME :
- Charge cognitive réduite de 70%
- Fluidité 60fps constant
- Design cohérent selon normes 2025
- Expérience utilisateur digne laboratoires internationaux
- Zero crash, zero erreur CSS
- Performance optimisée pour sessions longues

COMMENCER IMMÉDIATEMENT PAR CRÉATION DU DESIGN SYSTEM MARITIME