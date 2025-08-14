import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './main-simple.js'  // Point d'entrée JavaScript simplifié (version ultra-sécurisée)
import './index.css'
import Router from './Router'
import { UnifiedAppProvider } from './contexts/UnifiedAppContext'

// 🔄 INTÉGRATION UNIFIÉE selon prompt ultra-précis
// Une seule source de vérité : UnifiedAppProvider remplace ThemeProvider
// Gère : Thèmes + État + Données temps réel + Adaptateurs Backend

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UnifiedAppProvider>
      <Router />
    </UnifiedAppProvider>
  </StrictMode>,
)
