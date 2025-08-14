/* ==========================================================================
   CHNeoWave Maritime Interface - Application Principal
   Gestion de la navigation, thèmes et interactions principales
   ========================================================================== */

// ==========================================================================
// CONFIGURATION GLOBALE
// ==========================================================================

const CHNeoWave = {
  // État de l'application
  state: {
    currentView: 'dashboard',
    theme: localStorage.getItem('chneowave-theme') || 'light',
    isLoading: false,
    systemStatus: 'operational'
  },
  
  // Configuration
  config: {
    animationDuration: 300,
    chartUpdateInterval: 2000,
    autoSaveInterval: 30000
  },
  
  // Vues disponibles
  views: {
    dashboard: 'Tableau de Bord',
    calibration: 'Calibration',
    acquisition: 'Acquisition',
    analysis: 'Analyse',
    export: 'Export'
  }
};

// ==========================================================================
// INITIALISATION DE L'APPLICATION
// ==========================================================================

document.addEventListener('DOMContentLoaded', function() {
  console.log('CHNeoWave Maritime Interface - Initialisation...');
  
  // Initialisation des modules
  initializeTheme();
  initializeNavigation();
  initializeEventListeners();
  initializeCharts();
  updateSystemStatus();
  
  // Chargement de la vue par défaut
  showView(CHNeoWave.state.currentView);
  
  console.log('CHNeoWave Maritime Interface - Prêt');
});

// ==========================================================================
// GESTION DES THÈMES
// ==========================================================================

function initializeTheme() {
  const html = document.documentElement;
  html.setAttribute('data-theme', CHNeoWave.state.theme);
  
  // Mise à jour de l'icône du bouton thème
  updateThemeButton();
}

function toggleTheme() {
  const newTheme = CHNeoWave.state.theme === 'light' ? 'dark' : 'light';
  CHNeoWave.state.theme = newTheme;
  
  // Application du nouveau thème
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('chneowave-theme', newTheme);
  
  // Mise à jour de l'interface
  updateThemeButton();
  
  console.log(`Thème changé vers: ${newTheme}`);
}

function updateThemeButton() {
  const themeBtn = document.querySelector('.theme-btn');
  if (themeBtn) {
    const icon = themeBtn.querySelector('i');
    if (CHNeoWave.state.theme === 'dark') {
      icon.className = 'fas fa-sun';
      themeBtn.title = 'Passer au thème clair';
    } else {
      icon.className = 'fas fa-moon';
      themeBtn.title = 'Passer au thème sombre';
    }
  }
}

// ==========================================================================
// GESTION DE LA NAVIGATION
// ==========================================================================

function initializeNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  
  navItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const viewName = this.getAttribute('data-view');
      if (viewName) {
        showView(viewName);
      }
    });
  });
}

function showView(viewName) {
  console.log(`Navigation vers: ${viewName}`);
  
  // Mise à jour de l'état
  CHNeoWave.state.currentView = viewName;
  
  // Mise à jour de la navigation active
  updateActiveNavigation(viewName);
  
  // Mise à jour du contenu
  updateMainContent(viewName);
  
  // Mise à jour du titre
  updatePageTitle(viewName);
}

function updateActiveNavigation(activeView) {
  const navItems = document.querySelectorAll('.nav-item');
  
  navItems.forEach(item => {
    const viewName = item.getAttribute('data-view');
    if (viewName === activeView) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
}

function updatePageTitle(viewName) {
  const titleElement = document.querySelector('.header-title h1');
  if (titleElement && CHNeoWave.views[viewName]) {
    titleElement.textContent = CHNeoWave.views[viewName];
  }
}

// ==========================================================================
// GESTION DU CONTENU PRINCIPAL
// ==========================================================================

function updateMainContent(viewName) {
  const contentArea = document.querySelector('.content-area');
  if (!contentArea) return;
  
  // Animation de sortie
  contentArea.style.opacity = '0';
  
  setTimeout(() => {
    // Génération du nouveau contenu
    switch(viewName) {
      case 'dashboard':
        contentArea.innerHTML = generateDashboardContent();
        break;
      case 'calibration':
        contentArea.innerHTML = generateCalibrationContent();
        break;
      case 'acquisition':
        contentArea.innerHTML = generateAcquisitionContent();
        break;
      case 'analysis':
        contentArea.innerHTML = generateAnalysisContent();
        break;
      case 'export':
        contentArea.innerHTML = generateExportContent();
        break;
      default:
        contentArea.innerHTML = generateDashboardContent();
    }
    
    // Animation d'entrée
    contentArea.style.opacity = '1';
    
    // Initialisation des composants spécifiques à la vue
    initializeViewComponents(viewName);
    
  }, CHNeoWave.config.animationDuration / 2);
}

// ==========================================================================
// GÉNÉRATEURS DE CONTENU PAR VUE
// ==========================================================================

function generateDashboardContent() {
  return `
    <!-- KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon"><i class="fas fa-wave-square"></i></div>
        <div class="kpi-content">
          <div class="kpi-number">2.45m</div>
          <div class="kpi-label">Hauteur Moyenne</div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon"><i class="fas fa-tachometer-alt"></i></div>
        <div class="kpi-content">
          <div class="kpi-number">1.2s</div>
          <div class="kpi-label">Période Dominante</div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon"><i class="fas fa-compass"></i></div>
        <div class="kpi-content">
          <div class="kpi-number">245°</div>
          <div class="kpi-label">Direction</div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon"><i class="fas fa-thermometer-half"></i></div>
        <div class="kpi-content">
          <div class="kpi-number">18.5°C</div>
          <div class="kpi-label">Température</div>
        </div>
      </div>
    </div>
    
    <!-- Visualisation des données -->
    <div class="data-visualization">
      <div class="chart-container">
        <div class="chart-header">
          <h3>Évolution des Vagues en Temps Réel</h3>
          <select class="chart-timeframe">
            <option value="1h">1 Heure</option>
            <option value="6h" selected>6 Heures</option>
            <option value="24h">24 Heures</option>
            <option value="7d">7 Jours</option>
          </select>
        </div>
        <div class="chart-canvas-container">
          <canvas id="waveChart" class="chart-canvas"></canvas>
          <div class="chart-loading" style="display: none;">
            <div class="loading-spinner"></div>
            <p>Chargement des données...</p>
          </div>
        </div>
        <div class="chart-legend">
          <div class="legend-item">
            <span class="legend-color" style="background: var(--harbor-blue);"></span>
            <span>Hauteur (m)</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: var(--tidal-cyan);"></span>
            <span>Période (s)</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background: var(--coral-accent);"></span>
            <span>Direction (°)</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Actions rapides -->
    <div class="quick-actions">
      <div class="action-card" onclick="showView('calibration')">
        <div class="action-icon"><i class="fas fa-cog"></i></div>
        <div class="action-content">
          <h4>Calibration</h4>
          <p>Calibrer les capteurs et instruments</p>
        </div>
      </div>
      <div class="action-card" onclick="showView('acquisition')">
        <div class="action-icon"><i class="fas fa-play"></i></div>
        <div class="action-content">
          <h4>Nouvelle Acquisition</h4>
          <p>Démarrer une session d'acquisition</p>
        </div>
      </div>
      <div class="action-card" onclick="showView('analysis')">
        <div class="action-icon"><i class="fas fa-chart-line"></i></div>
        <div class="action-content">
          <h4>Analyse</h4>
          <p>Analyser les données collectées</p>
        </div>
      </div>
      <div class="action-card" onclick="showView('export')">
        <div class="action-icon"><i class="fas fa-download"></i></div>
        <div class="action-content">
          <h4>Export</h4>
          <p>Exporter les résultats</p>
        </div>
      </div>
    </div>
  `;
}

function generateCalibrationContent() {
  return `
    <div class="calibration-wizard">
      <div class="wizard-sidebar">
        <h3>Assistant de Calibration</h3>
        <div class="wizard-steps">
          <div class="step active" data-step="1">
            <div class="step-number">1</div>
            <div class="step-title">Préparation</div>
          </div>
          <div class="step" data-step="2">
            <div class="step-number">2</div>
            <div class="step-title">Capteurs</div>
          </div>
          <div class="step" data-step="3">
            <div class="step-number">3</div>
            <div class="step-title">Linéarité</div>
          </div>
          <div class="step" data-step="4">
            <div class="step-number">4</div>
            <div class="step-title">Validation</div>
          </div>
        </div>
      </div>
      
      <div class="wizard-content">
        <div class="step-content" id="step-1">
          <h2>Préparation de la Calibration</h2>
          <p>Vérifiez que tous les équipements sont correctement connectés et que le bassin est dans les conditions optimales.</p>
          
          <div class="checklist">
            <label class="checkbox-item">
              <input type="checkbox" checked>
              <span class="checkmark"></span>
              Capteurs de hauteur connectés
            </label>
            <label class="checkbox-item">
              <input type="checkbox" checked>
              <span class="checkmark"></span>
              Système d'acquisition opérationnel
            </label>
            <label class="checkbox-item">
              <input type="checkbox">
              <span class="checkmark"></span>
              Bassin stabilisé (température, niveau)
            </label>
            <label class="checkbox-item">
              <input type="checkbox">
              <span class="checkmark"></span>
              Étalons de référence disponibles
            </label>
          </div>
        </div>
        
        <div class="linearity-chart">
          <h3>Courbe de Linéarité</h3>
          <canvas id="linearityChart" class="chart-canvas"></canvas>
        </div>
      </div>
      
      <div class="wizard-actions">
        <button class="btn btn-secondary" onclick="previousStep()">Précédent</button>
        <button class="btn btn-primary" onclick="nextStep()">Suivant</button>
      </div>
    </div>
  `;
}

function generateAcquisitionContent() {
  return `
    <div class="acquisition-interface">
      <div class="acquisition-controls">
        <div class="control-group">
          <h4>Paramètres d'Acquisition</h4>
          <div class="control-row">
            <label>Fréquence d'échantillonnage:</label>
            <select class="control-input">
              <option value="10">10 Hz</option>
              <option value="50" selected>50 Hz</option>
              <option value="100">100 Hz</option>
              <option value="200">200 Hz</option>
            </select>
          </div>
          <div class="control-row">
            <label>Durée d'acquisition:</label>
            <input type="number" class="control-input" value="300" min="10" max="3600">
            <span class="unit">secondes</span>
          </div>
          <div class="control-row">
            <label>Mode d'acquisition:</label>
            <select class="control-input">
              <option value="continuous" selected>Continu</option>
              <option value="triggered">Déclenché</option>
              <option value="burst">Rafale</option>
            </select>
          </div>
        </div>
        
        <div class="control-group">
          <h4>État du Système</h4>
          <div class="status-indicators">
            <div class="status-item">
              <span class="status-dot status-ok"></span>
              <span>Capteurs: Opérationnels</span>
            </div>
            <div class="status-item">
              <span class="status-dot status-ok"></span>
              <span>Acquisition: Prête</span>
            </div>
            <div class="status-item">
              <span class="status-dot status-warning"></span>
              <span>Stockage: 78% libre</span>
            </div>
          </div>
        </div>
        
        <div class="acquisition-actions">
          <button class="btn btn-primary btn-large" onclick="startAcquisition()">
            <i class="fas fa-play"></i>
            Démarrer l'Acquisition
          </button>
          <button class="btn btn-secondary" onclick="stopAcquisition()" disabled>
            <i class="fas fa-stop"></i>
            Arrêter
          </button>
        </div>
      </div>
      
      <div class="realtime-display">
        <div class="realtime-chart">
          <div class="chart-title">
            <h3>Données en Temps Réel</h3>
            <div class="recording-indicator" style="display: none;">
              <span class="recording-dot"></span>
              <span>Enregistrement en cours...</span>
            </div>
          </div>
          <canvas id="realtimeChart" class="chart-canvas"></canvas>
        </div>
        
        <div class="realtime-stats">
          <div class="stat-card">
            <div class="stat-label">Hauteur Actuelle</div>
            <div class="stat-value" id="currentHeight">0.00 m</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Fréquence Instantanée</div>
            <div class="stat-value" id="currentFreq">0.00 Hz</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Échantillons</div>
            <div class="stat-value" id="sampleCount">0</div>
          </div>
        </div>
      </div>
    </div>
  `;
}

function generateAnalysisContent() {
  return `
    <div class="analysis-interface">
      <div class="analysis-controls">
        <div class="control-group">
          <h4>Sélection des Données</h4>
          <div class="control-row">
            <label>Fichier de données:</label>
            <select class="control-input">
              <option>acquisition_2024_01_15_14h30.dat</option>
              <option>acquisition_2024_01_15_10h15.dat</option>
              <option>acquisition_2024_01_14_16h45.dat</option>
            </select>
          </div>
          <div class="control-row">
            <label>Type d'analyse:</label>
            <select class="control-input">
              <option value="spectral" selected>Analyse Spectrale</option>
              <option value="statistical">Analyse Statistique</option>
              <option value="directional">Analyse Directionnelle</option>
              <option value="extreme">Valeurs Extrêmes</option>
            </select>
          </div>
        </div>
        
        <div class="analysis-actions">
          <button class="btn btn-primary" onclick="runAnalysis()">
            <i class="fas fa-play"></i>
            Lancer l'Analyse
          </button>
          <button class="btn btn-secondary" onclick="exportResults()">
            <i class="fas fa-download"></i>
            Exporter
          </button>
        </div>
      </div>
      
      <div class="analysis-results">
        <div class="result-card">
          <div class="result-header">
            <h4 class="result-title">Hauteur Significative</h4>
          </div>
          <div class="result-content">
            <div class="result-value">2.45 m</div>
            <div class="result-description">Hs calculée sur 20 minutes</div>
          </div>
        </div>
        
        <div class="result-card">
          <div class="result-header">
            <h4 class="result-title">Période de Pic</h4>
          </div>
          <div class="result-content">
            <div class="result-value">8.2 s</div>
            <div class="result-description">Tp du spectre de puissance</div>
          </div>
        </div>
        
        <div class="result-card">
          <div class="result-header">
            <h4 class="result-title">Direction Moyenne</h4>
          </div>
          <div class="result-content">
            <div class="result-value">245°</div>
            <div class="result-description">Direction pondérée par l'énergie</div>
          </div>
        </div>
        
        <div class="result-card">
          <div class="result-header">
            <h4 class="result-title">Étalement Directionnel</h4>
          </div>
          <div class="result-content">
            <div class="result-value">15°</div>
            <div class="result-description">Écart-type directionnel</div>
          </div>
        </div>
      </div>
      
      <div class="spectrum-chart">
        <h3>Spectre de Puissance</h3>
        <canvas id="spectrumChart" class="chart-canvas"></canvas>
      </div>
    </div>
  `;
}

function generateExportContent() {
  return `
    <div class="export-interface">
      <div class="export-options">
        <div class="option-group">
          <h4>Format d'Export</h4>
          <label class="radio-item">
            <input type="radio" name="format" value="pdf" checked>
            <span class="radio-mark"></span>
            Rapport PDF
          </label>
          <label class="radio-item">
            <input type="radio" name="format" value="excel">
            <span class="radio-mark"></span>
            Fichier Excel
          </label>
          <label class="radio-item">
            <input type="radio" name="format" value="csv">
            <span class="radio-mark"></span>
            Données CSV
          </label>
          <label class="radio-item">
            <input type="radio" name="format" value="matlab">
            <span class="radio-mark"></span>
            Format MATLAB
          </label>
        </div>
        
        <div class="option-group">
          <h4>Contenu à Inclure</h4>
          <label class="checkbox-item">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
            Données brutes
          </label>
          <label class="checkbox-item">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
            Résultats d'analyse
          </label>
          <label class="checkbox-item">
            <input type="checkbox" checked>
            <span class="checkmark"></span>
            Graphiques
          </label>
          <label class="checkbox-item">
            <input type="checkbox">
            <span class="checkmark"></span>
            Métadonnées
          </label>
        </div>
        
        <div class="export-actions">
          <button class="btn btn-primary" onclick="generateExport()">
            <i class="fas fa-file-export"></i>
            Générer l'Export
          </button>
        </div>
      </div>
      
      <div class="export-preview">
        <div class="preview-header">
          <h3>Aperçu du Rapport</h3>
        </div>
        <div class="preview-content">
          <div class="preview-page">
            <h1>Rapport d'Analyse Maritime</h1>
            <h2>CHNeoWave - Laboratoire d'Études Maritimes</h2>
            
            <div class="preview-section">
              <h3>Résumé Exécutif</h3>
              <p>Analyse des conditions de houle du 15 janvier 2024...</p>
            </div>
            
            <div class="preview-section">
              <h3>Paramètres Principaux</h3>
              <table class="preview-table">
                <tr><td>Hauteur Significative</td><td>2.45 m</td></tr>
                <tr><td>Période de Pic</td><td>8.2 s</td></tr>
                <tr><td>Direction Moyenne</td><td>245°</td></tr>
              </table>
            </div>
            
            <div class="preview-section">
              <h3>Graphiques</h3>
              <div class="preview-chart">[Graphique du spectre]</div>
              <div class="preview-chart">[Série temporelle]</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

// ==========================================================================
// INITIALISATION DES COMPOSANTS PAR VUE
// ==========================================================================

function initializeViewComponents(viewName) {
  switch(viewName) {
    case 'dashboard':
      initializeDashboardCharts();
      break;
    case 'calibration':
      initializeCalibrationWizard();
      break;
    case 'acquisition':
      initializeAcquisitionInterface();
      break;
    case 'analysis':
      initializeAnalysisCharts();
      break;
    case 'export':
      initializeExportPreview();
      break;
  }
}

// ==========================================================================
// GESTION DES ÉVÉNEMENTS
// ==========================================================================

function initializeEventListeners() {
  // Bouton de changement de thème
  const themeBtn = document.querySelector('.theme-btn');
  if (themeBtn) {
    themeBtn.addEventListener('click', toggleTheme);
  }
  
  // Gestion du redimensionnement
  window.addEventListener('resize', handleResize);
  
  // Gestion des raccourcis clavier
  document.addEventListener('keydown', handleKeyboardShortcuts);
}

function handleResize() {
  // Redimensionnement des graphiques
  if (window.waveChart) {
    window.waveChart.resize();
  }
  if (window.realtimeChart) {
    window.realtimeChart.resize();
  }
}

function handleKeyboardShortcuts(e) {
  // Ctrl/Cmd + 1-5 pour navigation rapide
  if ((e.ctrlKey || e.metaKey) && e.key >= '1' && e.key <= '5') {
    e.preventDefault();
    const views = Object.keys(CHNeoWave.views);
    const viewIndex = parseInt(e.key) - 1;
    if (views[viewIndex]) {
      showView(views[viewIndex]);
    }
  }
  
  // Ctrl/Cmd + T pour changer de thème
  if ((e.ctrlKey || e.metaKey) && e.key === 't') {
    e.preventDefault();
    toggleTheme();
  }
}

// ==========================================================================
// GESTION DU STATUT SYSTÈME
// ==========================================================================

function updateSystemStatus() {
  const statusElement = document.querySelector('.status-text');
  if (statusElement) {
    statusElement.textContent = getSystemStatusText();
  }
  
  // Mise à jour périodique
  setTimeout(updateSystemStatus, 5000);
}

function getSystemStatusText() {
  const now = new Date();
  const timeString = now.toLocaleTimeString('fr-FR');
  
  switch(CHNeoWave.state.systemStatus) {
    case 'operational':
      return `Système opérationnel - ${timeString}`;
    case 'calibrating':
      return `Calibration en cours - ${timeString}`;
    case 'acquiring':
      return `Acquisition en cours - ${timeString}`;
    case 'error':
      return `Erreur système - ${timeString}`;
    default:
      return `État inconnu - ${timeString}`;
  }
}

// ==========================================================================
// UTILITAIRES
// ==========================================================================

function showLoading(element) {
  if (element) {
    const loadingDiv = element.querySelector('.chart-loading');
    if (loadingDiv) {
      loadingDiv.style.display = 'flex';
    }
  }
}

function hideLoading(element) {
  if (element) {
    const loadingDiv = element.querySelector('.chart-loading');
    if (loadingDiv) {
      loadingDiv.style.display = 'none';
    }
  }
}

function formatNumber(value, decimals = 2) {
  return parseFloat(value).toFixed(decimals);
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString('fr-FR');
}

// ==========================================================================
// EXPORT DES FONCTIONS GLOBALES
// ==========================================================================

// Fonctions accessibles globalement
window.CHNeoWave = CHNeoWave;
window.showView = showView;
window.toggleTheme = toggleTheme;

console.log('CHNeoWave App.js chargé avec succès');