/* ==========================================================================
   CHNeoWave Maritime Interface - Gestion des Graphiques
   Visualisations de données avec Chart.js et animations maritimes
   ========================================================================== */

// ==========================================================================
// CONFIGURATION GLOBALE DES GRAPHIQUES
// ==========================================================================

const ChartConfig = {
  // Couleurs maritimes
  colors: {
    primary: '#2E86AB',
    secondary: '#A23B72',
    accent: '#F18F01',
    success: '#C73E1D',
    wave: '#4A90E2',
    foam: '#E8F4FD',
    deep: '#0A1929'
  },
  
  // Configuration par défaut
  defaults: {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 750,
      easing: 'easeInOutQuart'
    },
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            family: 'Inter, sans-serif',
            size: 12
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(10, 25, 41, 0.9)',
        titleColor: '#E8F4FD',
        bodyColor: '#E8F4FD',
        borderColor: '#2E86AB',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        mode: 'index',
        intersect: false
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(46, 134, 171, 0.1)',
          drawBorder: false
        },
        ticks: {
          color: '#64748B',
          font: {
            family: 'Inter, sans-serif',
            size: 11
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(46, 134, 171, 0.1)',
          drawBorder: false
        },
        ticks: {
          color: '#64748B',
          font: {
            family: 'Inter, sans-serif',
            size: 11
          }
        }
      }
    }
  }
};

// ==========================================================================
// INITIALISATION DES GRAPHIQUES
// ==========================================================================

function initializeCharts() {
  // Configuration globale de Chart.js
  Chart.defaults.font.family = 'Inter, sans-serif';
  Chart.defaults.color = '#64748B';
  
  console.log('Initialisation des graphiques CHNeoWave');
}

// ==========================================================================
// GRAPHIQUES DU TABLEAU DE BORD
// ==========================================================================

function initializeDashboardCharts() {
  createWaveChart();
  
  // Mise à jour périodique des données
  setInterval(updateWaveChart, CHNeoWave.config.chartUpdateInterval);
}

function createWaveChart() {
  const canvas = document.getElementById('waveChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Génération de données simulées
  const timeLabels = generateTimeLabels(50);
  const waveData = generateWaveData(50);
  
  window.waveChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: timeLabels,
      datasets: [
        {
          label: 'Hauteur des Vagues (m)',
          data: waveData.height,
          borderColor: ChartConfig.colors.primary,
          backgroundColor: ChartConfig.colors.primary + '20',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 6
        },
        {
          label: 'Période (s)',
          data: waveData.period,
          borderColor: ChartConfig.colors.accent,
          backgroundColor: ChartConfig.colors.accent + '20',
          borderWidth: 2,
          fill: false,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 6,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      ...ChartConfig.defaults,
      scales: {
        ...ChartConfig.defaults.scales,
        y: {
          ...ChartConfig.defaults.scales.y,
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Hauteur (m)',
            color: ChartConfig.colors.primary,
            font: {
              weight: 'bold'
            }
          },
          min: 0,
          max: 5
        },
        y1: {
          ...ChartConfig.defaults.scales.y,
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Période (s)',
            color: ChartConfig.colors.accent,
            font: {
              weight: 'bold'
            }
          },
          grid: {
            drawOnChartArea: false
          },
          min: 0,
          max: 15
        }
      },
      plugins: {
        ...ChartConfig.defaults.plugins,
        title: {
          display: false
        }
      },
      interaction: {
        mode: 'index',
        intersect: false
      }
    }
  });
}

function updateWaveChart() {
  if (!window.waveChart) return;
  
  const chart = window.waveChart;
  const newTime = new Date().toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
  
  // Ajout de nouvelles données
  chart.data.labels.push(newTime);
  chart.data.datasets[0].data.push(generateRandomWaveHeight());
  chart.data.datasets[1].data.push(generateRandomPeriod());
  
  // Limitation du nombre de points affichés
  if (chart.data.labels.length > 50) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
    chart.data.datasets[1].data.shift();
  }
  
  chart.update('none');
}

// ==========================================================================
// GRAPHIQUES DE CALIBRATION
// ==========================================================================

function initializeCalibrationWizard() {
  createLinearityChart();
}

function createLinearityChart() {
  const canvas = document.getElementById('linearityChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Données de linéarité simulées
  const referenceValues = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0];
  const measuredValues = referenceValues.map(val => 
    val + (Math.random() - 0.5) * 0.05 // Erreur de ±2.5%
  );
  
  window.linearityChart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Mesures',
          data: referenceValues.map((ref, i) => ({
            x: ref,
            y: measuredValues[i]
          })),
          backgroundColor: ChartConfig.colors.primary,
          borderColor: ChartConfig.colors.primary,
          pointRadius: 6,
          pointHoverRadius: 8
        },
        {
          label: 'Linéarité Parfaite',
          data: [
            { x: 0, y: 0 },
            { x: 4, y: 4 }
          ],
          type: 'line',
          borderColor: ChartConfig.colors.success,
          borderWidth: 2,
          borderDash: [5, 5],
          pointRadius: 0,
          fill: false
        }
      ]
    },
    options: {
      ...ChartConfig.defaults,
      scales: {
        x: {
          ...ChartConfig.defaults.scales.x,
          title: {
            display: true,
            text: 'Valeur de Référence (m)',
            font: {
              weight: 'bold'
            }
          },
          min: 0,
          max: 4.5
        },
        y: {
          ...ChartConfig.defaults.scales.y,
          title: {
            display: true,
            text: 'Valeur Mesurée (m)',
            font: {
              weight: 'bold'
            }
          },
          min: 0,
          max: 4.5
        }
      },
      plugins: {
        ...ChartConfig.defaults.plugins,
        title: {
          display: true,
          text: 'Courbe de Linéarité des Capteurs',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    }
  });
}

// ==========================================================================
// GRAPHIQUES D'ACQUISITION
// ==========================================================================

function initializeAcquisitionInterface() {
  createRealtimeChart();
  startRealtimeSimulation();
}

function createRealtimeChart() {
  const canvas = document.getElementById('realtimeChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  window.realtimeChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Signal Temps Réel',
          data: [],
          borderColor: ChartConfig.colors.wave,
          backgroundColor: ChartConfig.colors.wave + '10',
          borderWidth: 1.5,
          fill: true,
          tension: 0.1,
          pointRadius: 0
        }
      ]
    },
    options: {
      ...ChartConfig.defaults,
      animation: false, // Désactivé pour les données temps réel
      scales: {
        x: {
          ...ChartConfig.defaults.scales.x,
          display: false // Masqué pour le temps réel
        },
        y: {
          ...ChartConfig.defaults.scales.y,
          title: {
            display: true,
            text: 'Amplitude (m)',
            font: {
              weight: 'bold'
            }
          },
          min: -3,
          max: 3
        }
      },
      plugins: {
        ...ChartConfig.defaults.plugins,
        legend: {
          display: false
        }
      }
    }
  });
}

function startRealtimeSimulation() {
  let time = 0;
  const frequency = 0.5; // Hz
  const amplitude = 2; // m
  
  const updateInterval = setInterval(() => {
    if (!window.realtimeChart) {
      clearInterval(updateInterval);
      return;
    }
    
    const chart = window.realtimeChart;
    const value = amplitude * Math.sin(2 * Math.PI * frequency * time / 100) + 
                  0.5 * Math.sin(2 * Math.PI * frequency * 3 * time / 100) +
                  (Math.random() - 0.5) * 0.2; // Bruit
    
    chart.data.labels.push(time);
    chart.data.datasets[0].data.push(value);
    
    // Limitation à 200 points pour les performances
    if (chart.data.labels.length > 200) {
      chart.data.labels.shift();
      chart.data.datasets[0].data.shift();
    }
    
    chart.update('none');
    
    // Mise à jour des statistiques temps réel
    updateRealtimeStats(value, chart.data.datasets[0].data.length);
    
    time++;
  }, 50); // 20 Hz
  
  // Stockage de l'intervalle pour pouvoir l'arrêter
  window.realtimeInterval = updateInterval;
}

function updateRealtimeStats(currentValue, sampleCount) {
  const heightElement = document.getElementById('currentHeight');
  const freqElement = document.getElementById('currentFreq');
  const countElement = document.getElementById('sampleCount');
  
  if (heightElement) {
    heightElement.textContent = `${currentValue.toFixed(2)} m`;
  }
  
  if (freqElement) {
    freqElement.textContent = `${(20).toFixed(1)} Hz`; // Fréquence d'échantillonnage
  }
  
  if (countElement) {
    countElement.textContent = sampleCount.toLocaleString();
  }
}

// ==========================================================================
// GRAPHIQUES D'ANALYSE
// ==========================================================================

function initializeAnalysisCharts() {
  createSpectrumChart();
}

function createSpectrumChart() {
  const canvas = document.getElementById('spectrumChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Génération d'un spectre de puissance simulé
  const frequencies = [];
  const spectrum = [];
  
  for (let f = 0.05; f <= 2.0; f += 0.01) {
    frequencies.push(f);
    // Spectre JONSWAP simplifié
    const fp = 0.8; // Fréquence de pic
    const gamma = 3.3;
    const alpha = 0.0081;
    
    let S = alpha * Math.pow(2 * Math.PI, -4) * Math.pow(f, -5) * 
            Math.exp(-1.25 * Math.pow(fp / f, 4));
    
    if (f <= fp) {
      S *= Math.pow(gamma, Math.exp(-0.5 * Math.pow((f - fp) / (0.07 * fp), 2)));
    } else {
      S *= Math.pow(gamma, Math.exp(-0.5 * Math.pow((f - fp) / (0.09 * fp), 2)));
    }
    
    spectrum.push(S * 100); // Facteur d'échelle pour la visualisation
  }
  
  window.spectrumChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: frequencies.map(f => f.toFixed(2)),
      datasets: [
        {
          label: 'Densité Spectrale (m²/Hz)',
          data: spectrum,
          borderColor: ChartConfig.colors.primary,
          backgroundColor: ChartConfig.colors.primary + '20',
          borderWidth: 2,
          fill: true,
          tension: 0.1,
          pointRadius: 0
        }
      ]
    },
    options: {
      ...ChartConfig.defaults,
      scales: {
        x: {
          ...ChartConfig.defaults.scales.x,
          title: {
            display: true,
            text: 'Fréquence (Hz)',
            font: {
              weight: 'bold'
            }
          },
          type: 'linear'
        },
        y: {
          ...ChartConfig.defaults.scales.y,
          title: {
            display: true,
            text: 'Densité Spectrale (m²/Hz)',
            font: {
              weight: 'bold'
            }
          },
          type: 'logarithmic'
        }
      },
      plugins: {
        ...ChartConfig.defaults.plugins,
        title: {
          display: true,
          text: 'Spectre de Puissance des Vagues',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    }
  });
}

// ==========================================================================
// GRAPHIQUES D'EXPORT
// ==========================================================================

function initializeExportPreview() {
  // Initialisation de l'aperçu d'export
  console.log('Initialisation de l\'aperçu d\'export');
}

// ==========================================================================
// FONCTIONS UTILITAIRES POUR LES DONNÉES
// ==========================================================================

function generateTimeLabels(count) {
  const labels = [];
  const now = new Date();
  
  for (let i = count - 1; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60000); // Intervalles de 1 minute
    labels.push(time.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    }));
  }
  
  return labels;
}

function generateWaveData(count) {
  const height = [];
  const period = [];
  
  for (let i = 0; i < count; i++) {
    height.push(generateRandomWaveHeight());
    period.push(generateRandomPeriod());
  }
  
  return { height, period };
}

function generateRandomWaveHeight() {
  // Distribution de Rayleigh simplifiée pour les hauteurs de vagues
  const Hs = 2.5; // Hauteur significative
  const random = Math.random();
  return Hs * Math.sqrt(-2 * Math.log(random)) * 0.5;
}

function generateRandomPeriod() {
  // Période avec variation réaliste
  const Tp = 8.0; // Période de pic
  return Tp + (Math.random() - 0.5) * 2;
}

// ==========================================================================
// FONCTIONS D'INTERACTION UTILISATEUR
// ==========================================================================

// Fonctions appelées par l'interface utilisateur
function startAcquisition() {
  console.log('Démarrage de l\'acquisition');
  CHNeoWave.state.systemStatus = 'acquiring';
  
  // Mise à jour de l'interface
  const startBtn = document.querySelector('button[onclick="startAcquisition()"]');
  const stopBtn = document.querySelector('button[onclick="stopAcquisition()"]');
  const indicator = document.querySelector('.recording-indicator');
  
  if (startBtn) startBtn.disabled = true;
  if (stopBtn) stopBtn.disabled = false;
  if (indicator) indicator.style.display = 'flex';
}

function stopAcquisition() {
  console.log('⏹️ Arrêt de l\'acquisition');
  CHNeoWave.state.systemStatus = 'operational';
  
  // Arrêt de la simulation temps réel
  if (window.realtimeInterval) {
    clearInterval(window.realtimeInterval);
  }
  
  // Mise à jour de l'interface
  const startBtn = document.querySelector('button[onclick="startAcquisition()"]');
  const stopBtn = document.querySelector('button[onclick="stopAcquisition()"]');
  const indicator = document.querySelector('.recording-indicator');
  
  if (startBtn) startBtn.disabled = false;
  if (stopBtn) stopBtn.disabled = true;
  if (indicator) indicator.style.display = 'none';
}

function runAnalysis() {
  console.log('Lancement de l\'analyse');
  
  // Simulation d'une analyse
  const btn = document.querySelector('button[onclick="runAnalysis()"]');
  if (btn) {
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyse en cours...';
    btn.disabled = true;
    
    setTimeout(() => {
      btn.innerHTML = '<i class="fas fa-play"></i> Lancer l\'Analyse';
      btn.disabled = false;
      console.log('Analyse terminée');
    }, 3000);
  }
}

function exportResults() {
  console.log('Export des résultats');
  
  // Simulation d'un export
  const btn = document.querySelector('button[onclick="exportResults()"]');
  if (btn) {
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Export...';
    btn.disabled = true;
    
    setTimeout(() => {
      btn.innerHTML = '<i class="fas fa-download"></i> Exporter';
      btn.disabled = false;
      console.log('Export terminé');
    }, 2000);
  }
}

function generateExport() {
  console.log('Génération de l\'export');
  
  const btn = document.querySelector('button[onclick="generateExport()"]');
  if (btn) {
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Génération...';
    btn.disabled = true;
    
    setTimeout(() => {
      btn.innerHTML = '<i class="fas fa-file-export"></i> Générer l\'Export';
      btn.disabled = false;
      
      // Simulation du téléchargement
      const link = document.createElement('a');
      link.href = '#';
      link.download = 'rapport_chneowave_' + new Date().toISOString().split('T')[0] + '.pdf';
      link.click();
      
      console.log('Export généré');
    }, 3000);
  }
}

// ==========================================================================
// ASSISTANT DE CALIBRATION
// ==========================================================================

let currentStep = 1;
const totalSteps = 4;

function nextStep() {
  if (currentStep < totalSteps) {
    currentStep++;
    updateWizardStep();
  }
}

function previousStep() {
  if (currentStep > 1) {
    currentStep--;
    updateWizardStep();
  }
}

function updateWizardStep() {
  // Mise à jour des étapes visuelles
  const steps = document.querySelectorAll('.step');
  steps.forEach((step, index) => {
    if (index + 1 === currentStep) {
      step.classList.add('active');
    } else {
      step.classList.remove('active');
    }
  });
  
  // Mise à jour du contenu (simulation)
  const content = document.querySelector('.step-content');
  if (content) {
    content.innerHTML = `
      <h2>Étape ${currentStep} sur ${totalSteps}</h2>
      <p>Contenu de l'étape ${currentStep} de la calibration...</p>
    `;
  }
  
  console.log(`Étape de calibration: ${currentStep}/${totalSteps}`);
}

// ==========================================================================
// NETTOYAGE ET DESTRUCTION
// ==========================================================================

function destroyCharts() {
  // Nettoyage des graphiques lors du changement de vue
  if (window.waveChart) {
    window.waveChart.destroy();
    window.waveChart = null;
  }
  
  if (window.realtimeChart) {
    window.realtimeChart.destroy();
    window.realtimeChart = null;
  }
  
  if (window.linearityChart) {
    window.linearityChart.destroy();
    window.linearityChart = null;
  }
  
  if (window.spectrumChart) {
    window.spectrumChart.destroy();
    window.spectrumChart = null;
  }
  
  // Arrêt des intervalles
  if (window.realtimeInterval) {
    clearInterval(window.realtimeInterval);
    window.realtimeInterval = null;
  }
}

// Export des fonctions globales
window.startAcquisition = startAcquisition;
window.stopAcquisition = stopAcquisition;
window.runAnalysis = runAnalysis;
window.exportResults = exportResults;
window.generateExport = generateExport;
window.nextStep = nextStep;
window.previousStep = previousStep;

console.log('CHNeoWave Charts.js chargé avec succès');