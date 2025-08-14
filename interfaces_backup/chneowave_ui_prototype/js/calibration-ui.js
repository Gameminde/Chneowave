/**
 * CALIBRATION UI - Specific Interface Logic for Calibration Page
 * Logique d'interface spécifique pour la page de calibration
 * Version: Interface Visuelle Seulement
 */

// =============================================================================
// CALIBRATION SPECIFIC STATE
// =============================================================================

const CalibrationUI = {
    isInitialized: false,
    activeAnimations: new Set(),
    chartUpdateTimeout: null,
    
    // Chart configuration
    chartConfig: {
        showPoints: true,
        showRegression: true,
        animationDuration: 750
    },
    
    // Measurement simulation
    measurementQueue: [],
    isMeasuring: false
};

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    if (CalibrationUI.isInitialized) return;
    
    initializeCalibrationUI();
    setupCalibrationAnimations();
    setupKeyboardShortcuts();
    
    CalibrationUI.isInitialized = true;
    console.log('🔧 Calibration UI Initialized');
});

function initializeCalibrationUI() {
    // Add custom CSS for notifications
    addNotificationStyles();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup auto-save
    setupAutoSave();
    
    // Initialize drag and drop for import
    setupDragAndDrop();
}

function setupCalibrationAnimations() {
    // Animate progress bar on load
    animateProgressBar();
    
    // Animate result cards
    animateResultCards();
    
    // Setup table row animations
    setupTableAnimations();
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + S: Save calibration
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            event.preventDefault();
            handleSaveCalibration();
        }
        
        // Ctrl/Cmd + R: Reset calibration
        if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
            event.preventDefault();
            handleResetCalibration();
        }
        
        // Arrow keys: Navigate probes
        if (event.key === 'ArrowLeft' && !event.target.matches('input, select, textarea')) {
            event.preventDefault();
            handlePreviousProbe();
        }
        
        if (event.key === 'ArrowRight' && !event.target.matches('input, select, textarea')) {
            event.preventDefault();
            handleNextProbe();
        }
        
        // Space: Start/stop measurement
        if (event.key === ' ' && !event.target.matches('input, select, textarea')) {
            event.preventDefault();
            if (CalibrationUI.isMeasuring) {
                stopMeasurement();
            } else {
                handleStartMeasurement();
            }
        }
    });
}

// =============================================================================
// ENHANCED ANIMATIONS
// =============================================================================

function animateProgressBar() {
    const progressFill = document.getElementById('progressFill');
    if (!progressFill) return;
    
    const targetWidth = progressFill.style.width;
    progressFill.style.width = '0%';
    
    setTimeout(() => {
        progressFill.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
        progressFill.style.width = targetWidth;
    }, 500);
}

function animateResultCards() {
    const resultCards = document.querySelectorAll('.result-card');
    resultCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
    });
}

function setupTableAnimations() {
    const tableRows = document.querySelectorAll('#calibrationTableBody tr');
    tableRows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            row.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            row.style.opacity = '1';
            row.style.transform = 'translateX(0)';
        }, 100 + (index * 50));
    });
}

function animatePointMeasurement(pointNumber) {
    const tableBody = document.getElementById('calibrationTableBody');
    if (!tableBody) return;
    
    const row = tableBody.children[pointNumber - 1];
    if (!row) return;
    
    // Add measuring animation class
    row.classList.add('measuring-animation');
    
    // Create ripple effect
    const ripple = document.createElement('div');
    ripple.className = 'measurement-ripple';
    row.appendChild(ripple);
    
    setTimeout(() => {
        row.classList.remove('measuring-animation');
        ripple.remove();
    }, 2000);
}

// =============================================================================
// ENHANCED CHART FUNCTIONALITY
// =============================================================================

function enhanceChart() {
    if (!UIState.chartInstance) return;
    
    // Add custom plugins
    UIState.chartInstance.options.plugins.customCrosshair = {
        enabled: true
    };
    
    // Add zoom functionality
    UIState.chartInstance.options.plugins.zoom = {
        zoom: {
            wheel: {
                enabled: true,
            },
            pinch: {
                enabled: true
            },
            mode: 'xy',
        },
        pan: {
            enabled: true,
            mode: 'xy',
        }
    };
    
    UIState.chartInstance.update();
}

function exportChartAsImage() {
    if (!UIState.chartInstance) return;
    
    const canvas = UIState.chartInstance.canvas;
    const url = canvas.toDataURL('image/png');
    
    const link = document.createElement('a');
    link.download = `calibration_sonde_${UIState.currentProbe}_${new Date().toISOString().split('T')[0]}.png`;
    link.href = url;
    link.click();
    
    showNotification('Graphique exporté', 'success');
}

function resetChartZoom() {
    if (!UIState.chartInstance) return;
    
    UIState.chartInstance.resetZoom();
    showNotification('Zoom réinitialisé', 'info');
}

// =============================================================================
// ENHANCED MEASUREMENT SIMULATION
// =============================================================================

function startAdvancedMeasurement() {
    const pointsCount = parseInt(document.getElementById('pointsCount')?.value || 10);
    const measurementType = document.getElementById('measurementType')?.value || 'bidirectional';
    
    CalibrationUI.measurementQueue = [];
    
    // Build measurement queue based on type
    for (let i = 1; i <= pointsCount; i++) {
        if (measurementType === 'bidirectional') {
            CalibrationUI.measurementQueue.push({ point: i, direction: 'up' });
            CalibrationUI.measurementQueue.push({ point: i, direction: 'down' });
        } else if (measurementType === 'ascending') {
            CalibrationUI.measurementQueue.push({ point: i, direction: 'up' });
        } else {
            CalibrationUI.measurementQueue.push({ point: i, direction: 'down' });
        }
    }
    
    CalibrationUI.isMeasuring = true;
    processMeasurementQueue();
}

function processMeasurementQueue() {
    if (CalibrationUI.measurementQueue.length === 0) {
        CalibrationUI.isMeasuring = false;
        showNotification('Mesure complète terminée', 'success');
        updateCalibrationResults();
        updateLinearityChart();
        return;
    }
    
    const measurement = CalibrationUI.measurementQueue.shift();
    measurePointAdvanced(measurement.point, measurement.direction);
    
    setTimeout(() => {
        processMeasurementQueue();
    }, 1500);
}

function measurePointAdvanced(pointNumber, direction) {
    console.log(`📏 Measuring point ${pointNumber} (${direction})`);
    
    // Visual feedback
    animatePointMeasurement(pointNumber);
    updatePointStatus(pointNumber, 'measuring');
    
    // Simulate measurement delay
    setTimeout(() => {
        updatePointStatus(pointNumber, 'completed');
        
        // Update chart with new point
        addPointToChart(pointNumber, direction);
        
        showNotification(`Point ${pointNumber} (${direction}) mesuré`, 'success');
    }, 1000);
}

function stopMeasurement() {
    CalibrationUI.measurementQueue = [];
    CalibrationUI.isMeasuring = false;
    showNotification('Mesure arrêtée', 'warning');
}

function addPointToChart(pointNumber, direction) {
    if (!UIState.chartInstance) return;
    
    const height = pointNumber * 10;
    const voltage = 1.2 + (pointNumber * 0.285) + (Math.random() - 0.5) * 0.02;
    
    const datasetIndex = direction === 'up' ? 0 : 1;
    UIState.chartInstance.data.datasets[datasetIndex].data.push({ x: height, y: voltage });
    
    // Debounced chart update
    clearTimeout(CalibrationUI.chartUpdateTimeout);
    CalibrationUI.chartUpdateTimeout = setTimeout(() => {
        UIState.chartInstance.update('none');
    }, 100);
}

// =============================================================================
// ENHANCED DATA MANAGEMENT
// =============================================================================

function exportCalibrationData() {
    const currentProbeData = UIState.simulatedData.probes[UIState.currentProbe];
    const exportData = {
        probe: UIState.currentProbe,
        timestamp: new Date().toISOString(),
        points: currentProbeData.points,
        results: currentProbeData.results,
        settings: {
            pointsCount: document.getElementById('pointsCount')?.value,
            measurementType: document.getElementById('measurementType')?.value
        }
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.download = `calibration_sonde_${UIState.currentProbe}_${new Date().toISOString().split('T')[0]}.json`;
    link.href = url;
    link.click();
    
    URL.revokeObjectURL(url);
    showNotification('Données exportées', 'success');
}

function setupDragAndDrop() {
    const importBtn = document.getElementById('importPoints');
    if (!importBtn) return;
    
    // Create hidden file input
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.json';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);
    
    importBtn.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            importCalibrationData(file);
        }
    });
    
    // Drag and drop on table
    const tableContainer = document.querySelector('.maritime-table-container');
    if (tableContainer) {
        tableContainer.addEventListener('dragover', (event) => {
            event.preventDefault();
            tableContainer.classList.add('drag-over');
        });
        
        tableContainer.addEventListener('dragleave', () => {
            tableContainer.classList.remove('drag-over');
        });
        
        tableContainer.addEventListener('drop', (event) => {
            event.preventDefault();
            tableContainer.classList.remove('drag-over');
            
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                importCalibrationData(files[0]);
            }
        });
    }
}

function importCalibrationData(file) {
    const reader = new FileReader();
    reader.onload = (event) => {
        try {
            const data = JSON.parse(event.target.result);
            
            // Validate data structure
            if (data.probe && data.points && data.results) {
                // Update UI with imported data
                UIState.simulatedData.probes[UIState.currentProbe] = {
                    name: UIState.simulatedData.probes[UIState.currentProbe].name,
                    points: data.points,
                    results: data.results
                };
                
                // Update displays
                populateCalibrationTable();
                updateCalibrationResults();
                updateLinearityChart();
                
                showNotification('Données importées avec succès', 'success');
            } else {
                throw new Error('Format de fichier invalide');
            }
        } catch (error) {
            showNotification('Erreur lors de l\'importation: ' + error.message, 'error');
        }
    };
    
    reader.readAsText(file);
}

// =============================================================================
// AUTO-SAVE FUNCTIONALITY
// =============================================================================

function setupAutoSave() {
    let autoSaveInterval;
    
    function startAutoSave() {
        autoSaveInterval = setInterval(() => {
            saveCalibrationToLocalStorage();
        }, 30000); // Auto-save every 30 seconds
    }
    
    function stopAutoSave() {
        if (autoSaveInterval) {
            clearInterval(autoSaveInterval);
        }
    }
    
    // Start auto-save when measurement begins
    document.addEventListener('measurementStarted', startAutoSave);
    document.addEventListener('measurementStopped', stopAutoSave);
    
    // Load saved data on page load
    loadCalibrationFromLocalStorage();
}

function saveCalibrationToLocalStorage() {
    const calibrationData = {
        currentProbe: UIState.currentProbe,
        probesData: UIState.simulatedData.probes,
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('chneowave_calibration_autosave', JSON.stringify(calibrationData));
    console.log('📁 Auto-save completed');
}

function loadCalibrationFromLocalStorage() {
    const savedData = localStorage.getItem('chneowave_calibration_autosave');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            
            // Check if data is recent (within 24 hours)
            const savedTime = new Date(data.timestamp);
            const now = new Date();
            const hoursDiff = (now - savedTime) / (1000 * 60 * 60);
            
            if (hoursDiff < 24) {
                UIState.simulatedData.probes = data.probesData;
                showNotification('Données de calibration restaurées', 'info');
            }
        } catch (error) {
            console.warn('Failed to load auto-saved data:', error);
        }
    }
}

// =============================================================================
// TOOLTIPS AND HELP
// =============================================================================

function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const tooltipText = element.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = tooltipText;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
    
    setTimeout(() => tooltip.classList.add('show'), 10);
    
    element._tooltip = tooltip;
}

function hideTooltip(event) {
    const element = event.target;
    if (element._tooltip) {
        element._tooltip.classList.remove('show');
        setTimeout(() => {
            if (element._tooltip) {
                element._tooltip.remove();
                delete element._tooltip;
            }
        }, 200);
    }
}

// =============================================================================
// NOTIFICATION STYLES
// =============================================================================

function addNotificationStyles() {
    if (document.getElementById('calibration-notification-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'calibration-notification-styles';
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--foam-white);
            border: 1px solid rgba(46, 134, 171, 0.2);
            border-radius: 8px;
            padding: 12px 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 1000;
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 300px;
        }
        
        .notification.show {
            transform: translateX(0);
            opacity: 1;
        }
        
        .notification-info {
            border-left: 4px solid var(--harbor-blue);
            color: var(--harbor-blue);
        }
        
        .notification-success {
            border-left: 4px solid var(--emerald-success);
            color: var(--emerald-success);
        }
        
        .notification-warning {
            border-left: 4px solid #f39c12;
            color: #f39c12;
        }
        
        .notification-error {
            border-left: 4px solid #e74c3c;
            color: #e74c3c;
        }
        
        .measuring-animation {
            background: linear-gradient(90deg, transparent, rgba(243, 156, 18, 0.1), transparent) !important;
            animation: measuring-pulse 2s infinite;
        }
        
        @keyframes measuring-pulse {
            0%, 100% { background-position: -200% 0; }
            50% { background-position: 200% 0; }
        }
        
        .measurement-ripple {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(243, 156, 18, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: ripple-expand 2s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-expand {
            to {
                width: 100%;
                height: 100%;
                opacity: 0;
            }
        }
        
        .drag-over {
            border: 2px dashed var(--harbor-blue) !important;
            background: rgba(46, 134, 171, 0.05) !important;
        }
        
        .custom-tooltip {
            position: absolute;
            background: var(--ocean-deep);
            color: var(--foam-white);
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            white-space: nowrap;
            z-index: 1001;
            opacity: 0;
            transform: translateY(4px);
            transition: all 0.2s ease;
            pointer-events: none;
        }
        
        .custom-tooltip.show {
            opacity: 1;
            transform: translateY(0);
        }
        
        .custom-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 4px solid transparent;
            border-top-color: var(--ocean-deep);
        }
    `;
    
    document.head.appendChild(style);
}

// =============================================================================
// EXPORT FOR GLOBAL ACCESS
// =============================================================================

window.CalibrationUI = {
    exportChartAsImage,
    resetChartZoom,
    exportCalibrationData,
    startAdvancedMeasurement,
    stopMeasurement
};