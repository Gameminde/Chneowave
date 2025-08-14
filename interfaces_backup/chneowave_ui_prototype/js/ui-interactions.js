/**
 * UI INTERACTIONS - Interface Management without Business Logic
 * Gestion des interactions d'interface pour CHNeoWave
 * Version: Interface Visuelle Seulement
 */

// =============================================================================
// GLOBAL STATE MANAGEMENT
// =============================================================================

const UIState = {
    currentProbe: 1,
    totalProbes: 4,
    calibrationPoints: [],
    isCalibrating: false,
    chartInstance: null,
    
    // Simulated calibration data
    simulatedData: {
        probes: {
            1: { name: 'Avant Tribord', points: [], results: { slope: 2.847, offset: 1.234, r2: 0.9987, maxError: 0.12 } },
            2: { name: 'Avant Bâbord', points: [], results: { slope: 2.851, offset: 1.198, r2: 0.9982, maxError: 0.15 } },
            3: { name: 'Arrière Tribord', points: [], results: { slope: 2.839, offset: 1.267, r2: 0.9991, maxError: 0.09 } },
            4: { name: 'Arrière Bâbord', points: [], results: { slope: 2.843, offset: 1.221, r2: 0.9985, maxError: 0.11 } }
        }
    }
};

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeCalibrationInterface();
    setupEventListeners();
    generateSimulatedPoints();
    updateDisplay();
});

function initializeCalibrationInterface() {
    console.log('🌊 CHNeoWave Calibration Interface Initialized');
    
    // Initialize progress
    updateProgress();
    
    // Initialize table
    populateCalibrationTable();
    
    // Initialize chart
    initializeLinearityChart();
    
    // Update results display
    updateCalibrationResults();
}

// =============================================================================
// EVENT LISTENERS SETUP
// =============================================================================

function setupEventListeners() {
    // Probe selection
    const probeSelect = document.getElementById('probeSelect');
    if (probeSelect) {
        probeSelect.addEventListener('change', handleProbeChange);
    }
    
    // Points count
    const pointsCount = document.getElementById('pointsCount');
    if (pointsCount) {
        pointsCount.addEventListener('change', handlePointsCountChange);
    }
    
    // Measurement type
    const measurementType = document.getElementById('measurementType');
    if (measurementType) {
        measurementType.addEventListener('change', handleMeasurementTypeChange);
    }
    
    // Control buttons
    setupControlButtons();
    
    // Navigation buttons
    setupNavigationButtons();
    
    // Chart controls
    setupChartControls();
}

function setupControlButtons() {
    const resetBtn = document.getElementById('resetCalibration');
    if (resetBtn) {
        resetBtn.addEventListener('click', handleResetCalibration);
    }
    
    const startBtn = document.getElementById('startMeasurement');
    if (startBtn) {
        startBtn.addEventListener('click', handleStartMeasurement);
    }
    
    const exportBtn = document.getElementById('exportPoints');
    if (exportBtn) {
        exportBtn.addEventListener('click', handleExportPoints);
    }
    
    const importBtn = document.getElementById('importPoints');
    if (importBtn) {
        importBtn.addEventListener('click', handleImportPoints);
    }
}

function setupNavigationButtons() {
    const prevBtn = document.getElementById('previousProbe');
    if (prevBtn) {
        prevBtn.addEventListener('click', handlePreviousProbe);
    }
    
    const nextBtn = document.getElementById('nextProbe');
    if (nextBtn) {
        nextBtn.addEventListener('click', handleNextProbe);
    }
    
    const saveBtn = document.getElementById('saveCalibration');
    if (saveBtn) {
        saveBtn.addEventListener('click', handleSaveCalibration);
    }
    
    const finishBtn = document.getElementById('finishCalibration');
    if (finishBtn) {
        finishBtn.addEventListener('click', handleFinishCalibration);
    }
}

function setupChartControls() {
    const toggleBtn = document.getElementById('togglePoints');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', handleTogglePoints);
    }
    
    const fullscreenBtn = document.getElementById('fullscreenChart');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', handleFullscreenChart);
    }
}

// =============================================================================
// PROBE NAVIGATION
// =============================================================================

function handleProbeChange(event) {
    const newProbe = parseInt(event.target.value);
    switchToProbe(newProbe);
}

function handlePreviousProbe() {
    if (UIState.currentProbe > 1) {
        switchToProbe(UIState.currentProbe - 1);
    }
}

function handleNextProbe() {
    if (UIState.currentProbe < UIState.totalProbes) {
        switchToProbe(UIState.currentProbe + 1);
    }
}

function switchToProbe(probeNumber) {
    console.log(`🔄 Switching to probe ${probeNumber}`);
    
    UIState.currentProbe = probeNumber;
    
    // Update UI elements
    updateProgress();
    updateProbeSelector();
    populateCalibrationTable();
    updateCalibrationResults();
    updateLinearityChart();
    updateNavigationButtons();
    
    // Visual feedback
    showNotification(`Sonde ${probeNumber} sélectionnée`, 'info');
}

// =============================================================================
// DISPLAY UPDATES
// =============================================================================

function updateDisplay() {
    updateProgress();
    updateProbeSelector();
    updateNavigationButtons();
}

function updateProgress() {
    const progressPercentage = (UIState.currentProbe / UIState.totalProbes) * 100;
    
    const currentProbeEl = document.getElementById('currentProbeNumber');
    const totalProbesEl = document.getElementById('totalProbes');
    const progressFillEl = document.getElementById('progressFill');
    const progressPercentageEl = document.getElementById('progressPercentage');
    
    if (currentProbeEl) currentProbeEl.textContent = UIState.currentProbe;
    if (totalProbesEl) totalProbesEl.textContent = UIState.totalProbes;
    if (progressFillEl) progressFillEl.style.width = `${progressPercentage}%`;
    if (progressPercentageEl) progressPercentageEl.textContent = `${Math.round(progressPercentage)}%`;
}

function updateProbeSelector() {
    const probeSelect = document.getElementById('probeSelect');
    if (probeSelect) {
        probeSelect.value = UIState.currentProbe;
    }
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('previousProbe');
    const nextBtn = document.getElementById('nextProbe');
    const finishBtn = document.getElementById('finishCalibration');
    
    if (prevBtn) {
        prevBtn.disabled = UIState.currentProbe <= 1;
    }
    
    if (nextBtn && finishBtn) {
        if (UIState.currentProbe >= UIState.totalProbes) {
            nextBtn.style.display = 'none';
            finishBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            finishBtn.style.display = 'none';
        }
    }
}

// =============================================================================
// CALIBRATION TABLE MANAGEMENT
// =============================================================================

function populateCalibrationTable() {
    const tableBody = document.getElementById('calibrationTableBody');
    if (!tableBody) return;
    
    const pointsCount = parseInt(document.getElementById('pointsCount')?.value || 10);
    const currentProbeData = UIState.simulatedData.probes[UIState.currentProbe];
    
    tableBody.innerHTML = '';
    
    for (let i = 1; i <= pointsCount; i++) {
        const row = createCalibrationTableRow(i, currentProbeData.points[i-1]);
        tableBody.appendChild(row);
    }
}

function createCalibrationTableRow(pointNumber, pointData) {
    const row = document.createElement('tr');
    
    // Default values for simulation
    const height = pointData?.height || (pointNumber * 10);
    const voltage = pointData?.voltage || (1.2 + (pointNumber * 0.285));
    const direction = pointData?.direction || (pointNumber % 2 === 0 ? 'down' : 'up');
    const status = pointData?.status || (pointNumber <= 3 ? 'completed' : 'pending');
    
    row.innerHTML = `
        <td><strong>${pointNumber}</strong></td>
        <td>${height.toFixed(1)}</td>
        <td>${voltage.toFixed(3)}</td>
        <td>
            <i class="fas fa-arrow-${direction === 'up' ? 'up' : 'down'} direction-${direction}"></i>
            ${direction === 'up' ? 'Montée' : 'Descente'}
        </td>
        <td><span class="point-status status-${status}">${getStatusText(status)}</span></td>
        <td>
            <button class="btn-outline btn-sm" onclick="measurePoint(${pointNumber})">
                <i class="fas fa-play"></i>
            </button>
        </td>
    `;
    
    return row;
}

function getStatusText(status) {
    const statusMap = {
        'pending': 'En attente',
        'measuring': 'Mesure...',
        'completed': 'Terminé',
        'error': 'Erreur'
    };
    return statusMap[status] || status;
}

// =============================================================================
// CALIBRATION RESULTS
// =============================================================================

function updateCalibrationResults() {
    const currentProbeData = UIState.simulatedData.probes[UIState.currentProbe];
    const results = currentProbeData.results;
    
    // Update result values
    const slopeEl = document.getElementById('slopeValue');
    const offsetEl = document.getElementById('offsetValue');
    const r2El = document.getElementById('r2Value');
    const errorEl = document.getElementById('errorValue');
    const r2StatusEl = document.getElementById('r2Status');
    
    if (slopeEl) slopeEl.textContent = results.slope.toFixed(3);
    if (offsetEl) offsetEl.textContent = results.offset.toFixed(3);
    if (r2El) {
        r2El.textContent = results.r2.toFixed(4);
        r2El.className = `result-value ${getR2QualityClass(results.r2)}`;
    }
    if (errorEl) errorEl.textContent = results.maxError.toFixed(2);
    if (r2StatusEl) {
        r2StatusEl.textContent = getR2QualityText(results.r2);
        r2StatusEl.className = `result-status ${getR2QualityClass(results.r2)}`;
    }
}

function getR2QualityClass(r2Value) {
    if (r2Value >= 0.995) return 'r2-excellent';
    if (r2Value >= 0.99) return 'r2-good';
    if (r2Value >= 0.98) return 'r2-acceptable';
    return 'r2-poor';
}

function getR2QualityText(r2Value) {
    if (r2Value >= 0.995) return 'Excellente';
    if (r2Value >= 0.99) return 'Bonne';
    if (r2Value >= 0.98) return 'Acceptable';
    return 'Insuffisante';
}

// =============================================================================
// LINEARITY CHART
// =============================================================================

function initializeLinearityChart() {
    const ctx = document.getElementById('linearityChart');
    if (!ctx) return;
    
    const config = {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Points Montée',
                    data: generateChartData('up'),
                    backgroundColor: 'rgba(76, 175, 80, 0.6)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Points Descente',
                    data: generateChartData('down'),
                    backgroundColor: 'rgba(46, 134, 171, 0.6)',
                    borderColor: 'rgba(46, 134, 171, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Régression Linéaire',
                    data: generateRegressionLine(),
                    type: 'line',
                    borderColor: 'rgba(231, 76, 60, 0.8)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Calibration Sonde ${UIState.currentProbe}`,
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Hauteur (mm)'
                    },
                    grid: {
                        color: 'rgba(46, 134, 171, 0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Tension (V)'
                    },
                    grid: {
                        color: 'rgba(46, 134, 171, 0.1)'
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'point'
            }
        }
    };
    
    UIState.chartInstance = new Chart(ctx, config);
}

function updateLinearityChart() {
    if (!UIState.chartInstance) return;
    
    // Update chart data
    UIState.chartInstance.data.datasets[0].data = generateChartData('up');
    UIState.chartInstance.data.datasets[1].data = generateChartData('down');
    UIState.chartInstance.data.datasets[2].data = generateRegressionLine();
    
    // Update title
    UIState.chartInstance.options.plugins.title.text = `Calibration Sonde ${UIState.currentProbe}`;
    
    UIState.chartInstance.update();
}

function generateChartData(direction) {
    const data = [];
    const pointsCount = parseInt(document.getElementById('pointsCount')?.value || 10);
    const currentProbeData = UIState.simulatedData.probes[UIState.currentProbe];
    
    for (let i = 1; i <= pointsCount; i++) {
        if ((direction === 'up' && i % 2 === 1) || (direction === 'down' && i % 2 === 0)) {
            const height = i * 10;
            const voltage = 1.2 + (i * 0.285) + (Math.random() - 0.5) * 0.02; // Small random variation
            data.push({ x: height, y: voltage });
        }
    }
    
    return data;
}

function generateRegressionLine() {
    const currentProbeData = UIState.simulatedData.probes[UIState.currentProbe];
    const slope = currentProbeData.results.slope / 1000; // Convert mV/mm to V/mm
    const offset = currentProbeData.results.offset;
    
    return [
        { x: 0, y: offset },
        { x: 100, y: offset + (slope * 100) }
    ];
}

// =============================================================================
// EVENT HANDLERS
// =============================================================================

function handlePointsCountChange(event) {
    const newCount = parseInt(event.target.value);
    console.log(`📊 Points count changed to ${newCount}`);
    populateCalibrationTable();
    updateLinearityChart();
}

function handleMeasurementTypeChange(event) {
    const newType = event.target.value;
    console.log(`🔧 Measurement type changed to ${newType}`);
    showNotification(`Type de mesure: ${newType}`, 'info');
}

function handleResetCalibration() {
    console.log('🔄 Resetting calibration');
    showNotification('Calibration réinitialisée', 'warning');
    populateCalibrationTable();
    updateLinearityChart();
}

function handleStartMeasurement() {
    console.log('▶️ Starting measurement');
    UIState.isCalibrating = true;
    showNotification('Mesure démarrée', 'success');
    
    // Simulate measurement process
    simulateMeasurementProcess();
}

function handleExportPoints() {
    console.log('📤 Exporting calibration points');
    showNotification('Points exportés', 'success');
}

function handleImportPoints() {
    console.log('📥 Importing calibration points');
    showNotification('Points importés', 'success');
}

function handleSaveCalibration() {
    console.log('💾 Saving calibration');
    showNotification('Calibration sauvegardée', 'success');
}

function handleFinishCalibration() {
    console.log('✅ Finishing calibration');
    showNotification('Calibration terminée avec succès!', 'success');
    
    // Simulate redirect to dashboard
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 2000);
}

function handleTogglePoints() {
    if (!UIState.chartInstance) return;
    
    const dataset1 = UIState.chartInstance.data.datasets[0];
    const dataset2 = UIState.chartInstance.data.datasets[1];
    const isVisible = dataset1.hidden !== true;
    
    dataset1.hidden = isVisible;
    dataset2.hidden = isVisible;
    
    const toggleBtn = document.getElementById('togglePoints');
    if (toggleBtn) {
        toggleBtn.innerHTML = isVisible ? 
            '<i class="fas fa-eye"></i> Afficher Points' : 
            '<i class="fas fa-eye-slash"></i> Masquer Points';
    }
    
    UIState.chartInstance.update();
}

function handleFullscreenChart() {
    const chartContainer = document.querySelector('.chart-container');
    if (chartContainer) {
        if (chartContainer.requestFullscreen) {
            chartContainer.requestFullscreen();
        }
    }
}

// =============================================================================
// SIMULATION FUNCTIONS
// =============================================================================

function generateSimulatedPoints() {
    Object.keys(UIState.simulatedData.probes).forEach(probeId => {
        const probe = UIState.simulatedData.probes[probeId];
        probe.points = [];
        
        for (let i = 1; i <= 10; i++) {
            probe.points.push({
                height: i * 10,
                voltage: 1.2 + (i * 0.285) + (Math.random() - 0.5) * 0.01,
                direction: i % 2 === 0 ? 'down' : 'up',
                status: i <= 3 ? 'completed' : 'pending'
            });
        }
    });
}

function simulateMeasurementProcess() {
    let currentPoint = 1;
    const totalPoints = parseInt(document.getElementById('pointsCount')?.value || 10);
    
    const measureInterval = setInterval(() => {
        if (currentPoint > totalPoints) {
            clearInterval(measureInterval);
            UIState.isCalibrating = false;
            showNotification('Mesure terminée', 'success');
            return;
        }
        
        // Update point status to measuring
        updatePointStatus(currentPoint, 'measuring');
        
        setTimeout(() => {
            // Update point status to completed
            updatePointStatus(currentPoint, 'completed');
            currentPoint++;
        }, 1000);
        
    }, 2000);
}

function updatePointStatus(pointNumber, status) {
    const tableBody = document.getElementById('calibrationTableBody');
    if (tableBody) {
        const row = tableBody.children[pointNumber - 1];
        if (row) {
            const statusCell = row.children[4];
            const statusSpan = statusCell.querySelector('.point-status');
            if (statusSpan) {
                statusSpan.className = `point-status status-${status}`;
                statusSpan.textContent = getStatusText(status);
            }
        }
    }
}

function measurePoint(pointNumber) {
    console.log(`📏 Measuring point ${pointNumber}`);
    updatePointStatus(pointNumber, 'measuring');
    
    setTimeout(() => {
        updatePointStatus(pointNumber, 'completed');
        showNotification(`Point ${pointNumber} mesuré`, 'success');
    }, 1500);
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        'info': 'info-circle',
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'error': 'times-circle'
    };
    return icons[type] || 'info-circle';
}

// =============================================================================
// GLOBAL NAVIGATION FUNCTIONS
// =============================================================================

function createProject() {
    console.log('🆕 Creating new project');
    showNotification('Redirection vers la création de projet...', 'info');
    setTimeout(() => {
        window.location.href = 'project-create.html';
    }, 1000);
}

function goToDashboard() {
    console.log('🏠 Going to dashboard');
    showNotification('Retour au tableau de bord...', 'info');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// Export functions for global access
window.UIInteractions = {
    switchToProbe,
    measurePoint,
    createProject,
    goToDashboard,
    showNotification
};