/**
 * CHNeoWave - Script Principal
 * Gestion de l'interactivité, navigation, graphiques et animations
 * Design Maritime Professionnel 2025
 */

// Configuration globale
const CHNEOWAVE_CONFIG = {
    theme: 'dark',
    currentView: 'project',
    charts: {},
    animations: {},
    dataRefreshInterval: 1000, // 1 seconde
    waveAnimationSpeed: 4000,  // 4 secondes
    projectData: {
        name: '',
        code: '',
        manager: '',
        engineer: '',
        location: '',
        date: '',
        probeCount: 16,
        samplingRate: 256
    }
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌊 CHNeoWave - Initialisation du prototype maritime');
    
    initializeNavigation();
    initializeThemeToggle();
    initializeSidebarToggle();
    initializeProjectCreation();
    initializeCharts();
    initializeAnimations();
    initializeDataRefresh();
    setupEventListeners();
    
    console.log('✅ CHNeoWave - Prototype initialisé avec succès');
});

/**
 * Gestion de la navigation entre les vues
 */
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const moduleContents = document.querySelectorAll('.module-content');
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');
    
    // Mapping des vues vers leurs titres
    const viewTitles = {
        'project': {
            title: 'Création de Projet',
            subtitle: 'Configurez les paramètres de votre projet maritime'
        },
        'dashboard': {
            title: 'Dashboard Maritime',
            subtitle: 'Vue d\'ensemble du projet CHNeoWave'
        },
        'calibration': {
            title: 'Calibration des Sondes',
            subtitle: 'Étalonnage et validation des capteurs'
        },
        'acquisition': {
            title: 'Acquisition Temps Réel',
            subtitle: 'Mesure et enregistrement des données'
        },
        'analysis': {
            title: 'Analyse des Données',
            subtitle: 'Traitement et analyse spectrale'
        },
        'export': {
            title: 'Export et Rapports',
            subtitle: 'Génération de rapports et export'
        }
    };
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetView = this.getAttribute('data-view');
            
            // Mise à jour de la navigation active
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Changement de vue avec animation
            switchView(targetView);
            
            // Mise à jour des titres
            if (viewTitles[targetView]) {
                pageTitle.textContent = viewTitles[targetView].title;
                pageSubtitle.textContent = viewTitles[targetView].subtitle;
            }
            
            // Mise à jour de la configuration
            CHNEOWAVE_CONFIG.currentView = targetView;
            
            console.log(`🔄 Navigation vers: ${targetView}`);
        });
    });
}

/**
 * Changement de vue avec animation fluide
 */
function switchView(targetView) {
    const moduleContents = document.querySelectorAll('.module-content');
    
    // Animation de sortie
    moduleContents.forEach(content => {
        if (content.classList.contains('active')) {
            content.style.opacity = '0';
            content.style.transform = 'translateY(10px)';
            setTimeout(() => {
                content.classList.remove('active');
            }, 150);
        }
    });
    
    // Animation d'entrée
    setTimeout(() => {
        const targetContent = document.getElementById(`${targetView}-view`);
        if (targetContent) {
            targetContent.classList.add('active');
            targetContent.style.opacity = '1';
            targetContent.style.transform = 'translateY(0)';
        }
    }, 200);
}

/**
 * Gestion du basculement de thème
 */
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    themeToggle.addEventListener('click', function() {
        const isDark = body.getAttribute('data-theme') === 'light';
        
        if (isDark) {
            body.setAttribute('data-theme', 'dark');
            this.innerHTML = '<i class="fas fa-moon"></i><span>Thème Sombre</span>';
            CHNEOWAVE_CONFIG.theme = 'dark';
        } else {
            body.setAttribute('data-theme', 'light');
            this.innerHTML = '<i class="fas fa-sun"></i><span>Thème Clair</span>';
            CHNEOWAVE_CONFIG.theme = 'light';
        }
        
        // Mise à jour des graphiques pour le nouveau thème
        updateChartsTheme();
        
        console.log(`🎨 Changement de thème vers: ${CHNEOWAVE_CONFIG.theme}`);
    });
}

/**
 * Gestion du toggle du sidebar
 */
function initializeSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        
        // Mise à jour de la position du bouton toggle
        if (sidebar.classList.contains('collapsed')) {
            this.style.left = '40px';
        } else {
            this.style.left = '280px';
        }
        
        console.log('🔄 Toggle sidebar');
    });
}

/**
 * Gestion de la création de projet
 */
function initializeProjectCreation() {
    const createProjectBtn = document.getElementById('create-project-btn');
    const loadProjectBtn = document.getElementById('load-project-btn');
    
    if (createProjectBtn) {
        createProjectBtn.addEventListener('click', function() {
            // Récupération des données du formulaire
            const projectName = document.getElementById('project-name').value;
            const projectCode = document.getElementById('project-code').value;
            const projectManager = document.getElementById('project-manager').value;
            const projectEngineer = document.getElementById('project-engineer').value;
            const testLocation = document.getElementById('test-location').value;
            const projectDate = document.getElementById('project-date').value;
            const probeCount = document.getElementById('probe-count').value;
            const samplingRate = document.getElementById('sampling-rate').value;
            
            // Validation des champs obligatoires
            if (!projectName || !projectCode || !projectManager || !testLocation) {
                alert('Veuillez remplir tous les champs obligatoires');
                return;
            }
            
            // Sauvegarde des données du projet
            CHNEOWAVE_CONFIG.projectData = {
                name: projectName,
                code: projectCode,
                manager: projectManager,
                engineer: projectEngineer,
                location: testLocation,
                date: projectDate,
                probeCount: parseInt(probeCount),
                samplingRate: parseInt(samplingRate)
            };
            
            // Mise à jour du dashboard avec les informations du projet
            updateDashboardWithProjectData();
            
            // Navigation vers le dashboard
            switchView('dashboard');
            
            // Mise à jour de la navigation active
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            document.querySelector('[data-view="dashboard"]').classList.add('active');
            
            // Mise à jour des titres
            const pageTitle = document.getElementById('page-title');
            const pageSubtitle = document.getElementById('page-subtitle');
            pageTitle.textContent = 'Dashboard Maritime';
            pageSubtitle.textContent = 'Vue d\'ensemble du projet CHNeoWave';
            
            console.log('✅ Projet créé avec succès:', CHNEOWAVE_CONFIG.projectData);
        });
    }
    
    if (loadProjectBtn) {
        loadProjectBtn.addEventListener('click', function() {
            // Simulation du chargement d'un projet existant
            alert('Fonctionnalité de chargement de projet à implémenter');
        });
    }
}

/**
 * Mise à jour du dashboard avec les données du projet
 */
function updateDashboardWithProjectData() {
    const projectData = CHNEOWAVE_CONFIG.projectData;
    
    // Mise à jour des informations du projet dans le dashboard
    const dashboardProjectName = document.getElementById('dashboard-project-name');
    const dashboardProjectCode = document.getElementById('dashboard-project-code');
    const dashboardProjectManager = document.getElementById('dashboard-project-manager');
    const dashboardProjectEngineer = document.getElementById('dashboard-project-engineer');
    const dashboardTestLocation = document.getElementById('dashboard-test-location');
    const dashboardProjectDate = document.getElementById('dashboard-project-date');
    const dashboardProbeCount = document.getElementById('dashboard-probe-count');
    const dashboardSamplingRate = document.getElementById('dashboard-sampling-rate');
    
    if (dashboardProjectName) dashboardProjectName.textContent = projectData.name;
    if (dashboardProjectCode) dashboardProjectCode.textContent = projectData.code;
    if (dashboardProjectManager) dashboardProjectManager.textContent = projectData.manager;
    if (dashboardProjectEngineer) dashboardProjectEngineer.textContent = projectData.engineer;
    if (dashboardTestLocation) dashboardTestLocation.textContent = projectData.location;
    if (dashboardProjectDate) dashboardProjectDate.textContent = formatDate(projectData.date);
    if (dashboardProbeCount) dashboardProbeCount.textContent = projectData.probeCount;
    if (dashboardSamplingRate) dashboardSamplingRate.textContent = projectData.samplingRate;
}

/**
 * Formatage de la date
 */
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
}

/**
 * Initialisation des graphiques Chart.js
 */
function initializeCharts() {
    // Configuration globale Chart.js
    Chart.defaults.font.family = 'Inter, sans-serif';
    Chart.defaults.font.size = 12;
    Chart.defaults.color = getComputedStyle(document.documentElement).getPropertyValue('--text-secondary');
    
    // Graphique de calibration
    createCalibrationChart();
    
    // Graphiques d'acquisition
    createAcquisitionCharts();
    
    // Graphiques d'acquisition temps réel
    createRealTimeAcquisitionCharts();
    
    // Graphiques d'analyse
    createAnalysisCharts();
    
    console.log('📊 Graphiques initialisés');
}

/**
 * Création du graphique de calibration
 */
function createCalibrationChart() {
    const ctx = document.getElementById('calibration-chart');
    if (!ctx) return;
    
    const calibrationData = {
        labels: ['0.0', '10.0', '20.0', '30.0', '40.0'],
        datasets: [{
            label: 'Montée',
            data: [null, 24.38, null, 73.38, null],
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            pointBackgroundColor: '#3b82f6',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 6,
            tension: 0.1
        }, {
            label: 'Descente',
            data: [-0.12, null, 48.88, null, 97.88],
            borderColor: '#06b6d4',
            backgroundColor: 'rgba(6, 182, 212, 0.1)',
            pointBackgroundColor: '#06b6d4',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 6,
            tension: 0.1
        }, {
            label: 'Régression Linéaire',
            data: [-0.12, 24.38, 48.88, 73.38, 97.88],
            borderColor: '#10b981',
            backgroundColor: 'transparent',
            pointRadius: 0,
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false
        }]
    };
    
    CHNEOWAVE_CONFIG.charts.calibration = new Chart(ctx, {
        type: 'scatter',
        data: calibrationData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#3b82f6',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Hauteur (cm)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Tension (V)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    }
                }
            }
        }
    });
}

/**
 * Création des graphiques d'acquisition temps réel
 */
function createAcquisitionCharts() {
    // Graphique Sonde A
    const ctxA = document.getElementById('probe-a-chart');
    if (ctxA) {
        CHNEOWAVE_CONFIG.charts.probeA = createRealTimeChart(ctxA, 'Sonde #1', '#3b82f6');
    }
    
    // Graphique Sonde B
    const ctxB = document.getElementById('probe-b-chart');
    if (ctxB) {
        CHNEOWAVE_CONFIG.charts.probeB = createRealTimeChart(ctxB, 'Sonde #4', '#06b6d4');
    }
    
    // Graphique Multi-sondes
    const ctxMulti = document.getElementById('multi-probe-chart');
    if (ctxMulti) {
        CHNEOWAVE_CONFIG.charts.multiProbe = createMultiProbeChart(ctxMulti);
    }
}

/**
 * Création des graphiques d'acquisition temps réel (nouvelle interface)
 */
function createRealTimeAcquisitionCharts() {
    // Graphique 1 - Signal individuel
    const ctx1 = document.getElementById('acquisition-graph1');
    if (ctx1) {
        CHNEOWAVE_CONFIG.charts.acquisitionGraph1 = createAcquisitionSignalChart(ctx1, 'Signal 1', '#3b82f6');
    }
    
    // Graphique 2 - Module de traitement
    const ctx2 = document.getElementById('acquisition-graph2');
    if (ctx2) {
        CHNEOWAVE_CONFIG.charts.acquisitionGraph2 = createAcquisitionSignalChart(ctx2, 'Signal 1', '#06b6d4');
    }
    
    // Graphique Global - Vue multi-sondes
    const ctxGlobal = document.getElementById('acquisition-global');
    if (ctxGlobal) {
        CHNEOWAVE_CONFIG.charts.acquisitionGlobal = createAcquisitionGlobalChart(ctxGlobal);
    }
}

/**
 * Création d'un graphique de signal d'acquisition
 */
function createAcquisitionSignalChart(ctx, label, color) {
    const timeLabels = Array.from({length: 100}, (_, i) => i * 0.1);
    const initialData = Array.from({length: 100}, () => Math.random() * 8 - 4);
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: label,
                data: initialData,
                borderColor: color,
                backgroundColor: color + '20',
                borderWidth: 2,
                fill: false,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 0
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Temps (s)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    },
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amplitude (m)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    },
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    },
                    min: -4,
                    max: 4
                }
            }
        }
    });
}

/**
 * Création du graphique global d'acquisition
 */
function createAcquisitionGlobalChart(ctx) {
    const timeLabels = Array.from({length: 100}, (_, i) => i * 0.1);
    const colors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b'];
    
    const datasets = colors.map((color, index) => ({
        label: `Sonde ${index}`,
        data: Array.from({length: 100}, () => Math.random() * 8 - 4),
        borderColor: color,
        backgroundColor: color + '20',
        borderWidth: 1.5,
        fill: false,
        tension: 0.4,
        pointRadius: 0
    }));
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 0
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Temps (s)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amplitude (m)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    },
                    min: -4,
                    max: 4
                }
            }
        }
    });
}

/**
 * Création d'un graphique temps réel
 */
function createRealTimeChart(ctx, label, color) {
    const timeLabels = Array.from({length: 50}, (_, i) => i);
    const initialData = Array.from({length: 50}, () => Math.random() * 20 - 10);
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: label,
                data: initialData,
                borderColor: color,
                backgroundColor: color + '20',
                borderWidth: 2,
                fill: false,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 0
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    },
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    }
                }
            }
        }
    });
}

/**
 * Création du graphique multi-sondes
 */
function createMultiProbeChart(ctx) {
    const timeLabels = Array.from({length: 100}, (_, i) => i);
    const colors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b'];
    
    const datasets = colors.map((color, index) => ({
        label: `Sonde #${index + 1}`,
        data: Array.from({length: 100}, () => Math.random() * 30 - 15),
        borderColor: color,
        backgroundColor: color + '20',
        borderWidth: 1.5,
        fill: false,
        tension: 0.4,
        pointRadius: 0
    }));
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 0
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Temps (s)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Hauteur (cm)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    }
                }
            }
        }
    });
}

/**
 * Création des graphiques d'analyse
 */
function createAnalysisCharts() {
    // Spectre de puissance
    const ctxPower = document.getElementById('power-spectrum-chart');
    if (ctxPower) {
        CHNEOWAVE_CONFIG.charts.powerSpectrum = createPowerSpectrumChart(ctxPower);
    }
    
    // Distribution des hauteurs
    const ctxHeight = document.getElementById('height-distribution-chart');
    if (ctxHeight) {
        CHNEOWAVE_CONFIG.charts.heightDistribution = createHeightDistributionChart(ctxHeight);
    }
    
    // Rose de houle
    const ctxRose = document.getElementById('wave-rose-chart');
    if (ctxRose) {
        CHNEOWAVE_CONFIG.charts.waveRose = createWaveRoseChart(ctxRose);
    }
    
    // Analyse JONSWAP
    const ctxJonswap = document.getElementById('jonswap-chart');
    if (ctxJonswap) {
        CHNEOWAVE_CONFIG.charts.jonswap = createJonswapChart(ctxJonswap);
    }
}

/**
 * Création du spectre de puissance
 */
function createPowerSpectrumChart(ctx) {
    const frequencies = Array.from({length: 50}, (_, i) => i * 0.1);
    const powerData = frequencies.map(f => Math.exp(-f) * Math.random() * 10);
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: frequencies.map(f => f.toFixed(1)),
            datasets: [{
                label: 'Spectre de Puissance',
                data: powerData,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Fréquence (Hz)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Puissance (m²/Hz)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                }
            }
        }
    });
}

/**
 * Création de la distribution des hauteurs
 */
function createHeightDistributionChart(ctx) {
    const heights = Array.from({length: 20}, (_, i) => i * 2 - 20);
    const distribution = heights.map(h => Math.exp(-(h - 5) ** 2 / 50) * 100);
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: heights.map(h => h.toFixed(1)),
            datasets: [{
                label: 'Distribution',
                data: distribution,
                backgroundColor: '#06b6d4',
                borderColor: '#0891b2',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Hauteur (cm)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Fréquence (%)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                }
            }
        }
    });
}

/**
 * Création de la rose de houle
 */
function createWaveRoseChart(ctx) {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const heights = directions.map(() => Math.random() * 20 + 5);
    
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: directions,
            datasets: [{
                label: 'Hauteur Significative',
                data: heights,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-secondary')
                    },
                    grid: {
                        color: getComputedStyle(document.documentElement).getPropertyValue('--border')
                    }
                }
            }
        }
    });
}

/**
 * Création de l'analyse JONSWAP
 */
function createJonswapChart(ctx) {
    const frequencies = Array.from({length: 100}, (_, i) => i * 0.05);
    const jonswapData = frequencies.map(f => {
        const peakFreq = 0.3;
        const gamma = 3.3;
        const sigma = f <= peakFreq ? 0.07 : 0.09;
        const alpha = 0.0081;
        
        return alpha * Math.exp(-1.25 * (peakFreq / f) ** 4) * gamma ** Math.exp(-(f - peakFreq) ** 2 / (2 * sigma ** 2 * peakFreq ** 2));
    });
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: frequencies.map(f => f.toFixed(2)),
            datasets: [{
                label: 'JONSWAP',
                data: jonswapData,
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Fréquence (Hz)',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Densité Spectrale',
                        color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary')
                    }
                }
            }
        }
    });
}

/**
 * Mise à jour du thème des graphiques
 */
function updateChartsTheme() {
    const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-primary');
    const gridColor = getComputedStyle(document.documentElement).getPropertyValue('--border');
    
    Object.values(CHNEOWAVE_CONFIG.charts).forEach(chart => {
        if (chart && chart.options) {
            // Mise à jour des couleurs des axes
            if (chart.options.scales) {
                Object.values(chart.options.scales).forEach(scale => {
                    if (scale.ticks) {
                        scale.ticks.color = textColor;
                    }
                    if (scale.grid) {
                        scale.grid.color = gridColor;
                    }
                });
            }
            
            // Mise à jour des titres
            if (chart.options.scales) {
                Object.values(chart.options.scales).forEach(scale => {
                    if (scale.title) {
                        scale.title.color = textColor;
                    }
                });
            }
            
            chart.update('none');
        }
    });
}

/**
 * Initialisation des animations
 */
function initializeAnimations() {
    // Animation des vagues
    animateWaves();
    
    // Animation des métriques
    animateMetrics();
    
    // Animation des indicateurs de statut
    animateStatusIndicators();
    
    console.log('🎬 Animations initialisées');
}

/**
 * Animation des vagues
 */
function animateWaves() {
    const waveLines = document.querySelectorAll('.wave-line');
    
    waveLines.forEach((line, index) => {
        line.style.animationDelay = `${index * -1}s`;
    });
}

/**
 * Animation des métriques
 */
function animateMetrics() {
    const metricValues = document.querySelectorAll('.metric-value');
    
    metricValues.forEach(value => {
        const finalValue = value.textContent;
        const numericValue = parseFloat(finalValue);
        
        if (!isNaN(numericValue)) {
            animateNumber(value, 0, numericValue, 2000);
        }
    });
}

/**
 * Animation d'un nombre
 */
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    const difference = end - start;
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = start + (difference * progress);
        element.textContent = current.toFixed(1);
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

/**
 * Animation des indicateurs de statut
 */
function animateStatusIndicators() {
    const statusIndicators = document.querySelectorAll('.status-indicator');
    
    statusIndicators.forEach(indicator => {
        indicator.style.animation = 'pulse 2s infinite';
    });
}

/**
 * Initialisation du rafraîchissement des données
 */
function initializeDataRefresh() {
    setInterval(() => {
        updateRealTimeData();
        updateSystemMetrics();
    }, CHNEOWAVE_CONFIG.dataRefreshInterval);
}

/**
 * Mise à jour des données temps réel
 */
function updateRealTimeData() {
    // Mise à jour des graphiques temps réel
    if (CHNEOWAVE_CONFIG.charts.probeA) {
        updateRealTimeChart(CHNEOWAVE_CONFIG.charts.probeA);
    }
    
    if (CHNEOWAVE_CONFIG.charts.probeB) {
        updateRealTimeChart(CHNEOWAVE_CONFIG.charts.probeB);
    }
    
    if (CHNEOWAVE_CONFIG.charts.multiProbe) {
        updateMultiProbeChart(CHNEOWAVE_CONFIG.charts.multiProbe);
    }
    
    // Mise à jour des nouveaux graphiques d'acquisition
    if (CHNEOWAVE_CONFIG.charts.acquisitionGraph1) {
        updateAcquisitionSignalChart(CHNEOWAVE_CONFIG.charts.acquisitionGraph1);
    }
    
    if (CHNEOWAVE_CONFIG.charts.acquisitionGraph2) {
        updateAcquisitionSignalChart(CHNEOWAVE_CONFIG.charts.acquisitionGraph2);
    }
    
    if (CHNEOWAVE_CONFIG.charts.acquisitionGlobal) {
        updateAcquisitionGlobalChart(CHNEOWAVE_CONFIG.charts.acquisitionGlobal);
    }
    
    // Mise à jour des métriques d'acquisition
    updateAcquisitionMetrics();
}

/**
 * Mise à jour d'un graphique de signal d'acquisition
 */
function updateAcquisitionSignalChart(chart) {
    const newData = Math.random() * 8 - 4;
    
    chart.data.datasets[0].data.shift();
    chart.data.datasets[0].data.push(newData);
    
    chart.update('none');
}

/**
 * Mise à jour du graphique global d'acquisition
 */
function updateAcquisitionGlobalChart(chart) {
    chart.data.datasets.forEach(dataset => {
        const newData = Math.random() * 8 - 4;
        dataset.data.shift();
        dataset.data.push(newData);
    });
    
    chart.update('none');
}

/**
 * Mise à jour des métriques d'acquisition
 */
function updateAcquisitionMetrics() {
    // Mise à jour du compteur d'échantillons
    const sampleCount = document.getElementById('sample-count');
    if (sampleCount) {
        const currentCount = parseInt(sampleCount.textContent);
        sampleCount.textContent = Math.min(currentCount + 1, 1920);
    }
    
    // Mise à jour du temps écoulé
    const elapsedTime = document.getElementById('elapsed-time');
    if (elapsedTime) {
        const currentTime = elapsedTime.textContent;
        const [minutes, seconds] = currentTime.split(':').map(Number);
        const newSeconds = seconds + 1;
        const newMinutes = minutes + Math.floor(newSeconds / 60);
        const finalSeconds = newSeconds % 60;
        elapsedTime.textContent = `${String(newMinutes).padStart(2, '0')}:${String(finalSeconds).padStart(2, '0')}`;
    }
    
    // Mise à jour des FPS et latence
    const fpsValue = document.getElementById('fps-value');
    const latencyValue = document.getElementById('latency-value');
    if (fpsValue) {
        fpsValue.textContent = Math.floor(Math.random() * 10 + 50);
    }
    if (latencyValue) {
        latencyValue.textContent = Math.floor(Math.random() * 5 + 15);
    }
    
    // Mise à jour des statistiques des sondes
    updateProbeStatistics();
}

/**
 * Mise à jour des statistiques des sondes
 */
function updateProbeStatistics() {
    const probeStatsBody = document.getElementById('probe-stats-body');
    if (probeStatsBody) {
        const rows = probeStatsBody.querySelectorAll('tr');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 3) {
                // Mise à jour Hmax
                const hmaxCell = cells[1];
                const currentHmax = parseFloat(hmaxCell.textContent);
                const newHmax = Math.max(0.1, currentHmax + (Math.random() - 0.5) * 0.02);
                hmaxCell.textContent = newHmax.toFixed(2);
                
                // Mise à jour Tmean
                const tmeanCell = cells[2];
                const currentTmean = parseFloat(tmeanCell.textContent);
                const newTmean = Math.max(1.5, currentTmean + (Math.random() - 0.5) * 0.1);
                tmeanCell.textContent = newTmean.toFixed(1);
            }
        });
    }
}

/**
 * Mise à jour d'un graphique temps réel
 */
function updateRealTimeChart(chart) {
    const newData = Math.random() * 20 - 10;
    
    chart.data.datasets[0].data.shift();
    chart.data.datasets[0].data.push(newData);
    
    chart.update('none');
}

/**
 * Mise à jour du graphique multi-sondes
 */
function updateMultiProbeChart(chart) {
    chart.data.datasets.forEach(dataset => {
        const newData = Math.random() * 30 - 15;
        dataset.data.shift();
        dataset.data.push(newData);
    });
    
    chart.update('none');
}

/**
 * Mise à jour des métriques système
 */
function updateSystemMetrics() {
    const performanceMetric = document.querySelector('.metric-card:nth-child(1) .metric-value');
    const memoryMetric = document.querySelector('.metric-card:nth-child(2) .metric-value');
    
    if (performanceMetric) {
        const currentValue = parseFloat(performanceMetric.textContent);
        const newValue = Math.max(85, Math.min(100, currentValue + (Math.random() - 0.5) * 2));
        performanceMetric.textContent = newValue.toFixed(1) + '%';
    }
    
    if (memoryMetric) {
        const currentValue = parseFloat(memoryMetric.textContent);
        const newValue = Math.max(1.5, Math.min(4.0, currentValue + (Math.random() - 0.5) * 0.1));
        memoryMetric.textContent = newValue.toFixed(1) + ' GB';
    }
}

/**
 * Configuration des écouteurs d'événements
 */
function setupEventListeners() {
    // Gestion des boutons d'action
    setupActionButtons();
    
    // Gestion des formulaires
    setupFormHandlers();
    
    // Gestion des sélecteurs de sondes
    setupProbeSelectors();
    
    console.log('🎯 Écouteurs d\'événements configurés');
}

/**
 * Configuration des boutons d'action
 */
function setupActionButtons() {
    const actionButtons = document.querySelectorAll('.btn, .primary-action');
    
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Animation de clic
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            // Gestion spécifique selon le type de bouton
            const buttonText = this.textContent.trim();
            
            if (buttonText.includes('Démarrer')) {
                handleStartAction(this);
            } else if (buttonText.includes('Arrêter') || buttonText.includes('Pause')) {
                handleStopAction(this);
            } else if (buttonText.includes('Sauvegarder')) {
                handleSaveAction(this);
            } else if (buttonText.includes('Valider')) {
                handleValidateAction(this);
            }
        });
    });
}

/**
 * Gestion des actions de démarrage
 */
function handleStartAction(button) {
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> En cours...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Démarré';
        button.classList.remove('btn-primary');
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-play"></i> Démarrer';
            button.classList.remove('btn-success');
            button.classList.add('btn-primary');
            button.disabled = false;
        }, 2000);
    }, 1500);
}

/**
 * Gestion des actions d'arrêt
 */
function handleStopAction(button) {
    button.innerHTML = '<i class="fas fa-stop"></i> Arrêté';
    button.classList.remove('btn-warning');
    button.classList.add('btn-secondary');
    
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-stop"></i> Arrêter';
        button.classList.remove('btn-secondary');
        button.classList.add('btn-warning');
    }, 2000);
}

/**
 * Gestion des actions de sauvegarde
 */
function handleSaveAction(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sauvegarde...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Sauvegardé';
        button.classList.remove('btn-success');
        button.classList.add('btn-secondary');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-secondary');
            button.classList.add('btn-success');
            button.disabled = false;
        }, 2000);
    }, 1500);
}

/**
 * Gestion des actions de validation
 */
function handleValidateAction(button) {
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validation...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Validé';
        button.classList.remove('btn-success');
        button.classList.add('btn-secondary');
        
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-check"></i> Valider';
            button.classList.remove('btn-secondary');
            button.classList.add('btn-success');
            button.disabled = false;
        }, 2000);
    }, 1500);
}

/**
 * Configuration des gestionnaires de formulaires
 */
function setupFormHandlers() {
    const selects = document.querySelectorAll('select');
    const inputs = document.querySelectorAll('input');
    
    selects.forEach(select => {
        select.addEventListener('change', function() {
            console.log(`📝 Changement de valeur: ${this.id} = ${this.value}`);
        });
    });
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            console.log(`📝 Saisie: ${this.id} = ${this.value}`);
        });
    });
}

/**
 * Configuration des sélecteurs de sondes
 */
function setupProbeSelectors() {
    const probeSelects = document.querySelectorAll('#probe-a-select, #probe-b-select');
    
    probeSelects.forEach(select => {
        select.addEventListener('change', function() {
            const chartId = this.id === 'probe-a-select' ? 'probeA' : 'probeB';
            const chart = CHNEOWAVE_CONFIG.charts[chartId];
            
            if (chart) {
                chart.data.datasets[0].label = `Sonde #${this.value}`;
                chart.update();
            }
        });
    });
}

/**
 * Gestion des erreurs globales
 */
window.addEventListener('error', function(e) {
    console.error('❌ Erreur CHNeoWave:', e.error);
});

/**
 * Gestion de la fermeture de la page
 */
window.addEventListener('beforeunload', function() {
    console.log('👋 Fermeture de CHNeoWave');
});

// Export des fonctions pour utilisation externe
window.CHNEOWAVE = {
    config: CHNEOWAVE_CONFIG,
    switchView: switchView,
    updateChartsTheme: updateChartsTheme,
    charts: CHNEOWAVE_CONFIG.charts
};