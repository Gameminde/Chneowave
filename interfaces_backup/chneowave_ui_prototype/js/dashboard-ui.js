/**
 * DASHBOARD UI - Enhanced Interface Logic for Main Dashboard
 * Logique d'interface améliorée pour le tableau de bord principal
 * Version: Interface Visuelle Seulement
 */

// =============================================================================
// DASHBOARD SPECIFIC STATE
// =============================================================================

const DashboardUI = {
    isInitialized: false,
    refreshInterval: null,
    kpiAnimations: new Map(),
    chartUpdateQueue: [],
    
    // Real-time simulation settings
    simulationSettings: {
        updateInterval: 2000,
        waveVariation: 0.3,
        periodVariation: 0.2,
        acquisitionJitter: 0.1
    },
    
    // Performance monitoring
    performance: {
        lastUpdate: Date.now(),
        updateCount: 0,
        averageUpdateTime: 0
    }
};

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    if (DashboardUI.isInitialized) return;
    
    initializeDashboardUI();
    setupDashboardAnimations();
    setupRealTimeUpdates();
    setupInteractiveElements();
    
    DashboardUI.isInitialized = true;
    console.log('📊 Dashboard UI Initialized');
});

function initializeDashboardUI() {
    // Add custom CSS for dashboard enhancements
    addDashboardStyles();
    
    // Initialize tooltips for KPI cards
    initializeKPITooltips();
    
    // Setup keyboard shortcuts
    setupDashboardKeyboardShortcuts();
    
    // Initialize responsive behavior
    setupResponsiveBehavior();
}

function setupDashboardAnimations() {
    // Animate KPI cards on load
    animateKPICards();
    
    // Setup sparkline animations
    setupSparklineAnimations();
    
    // Animate action cards
    animateActionCards();
}

function setupRealTimeUpdates() {
    // Start real-time data simulation
    startRealTimeSimulation();
    
    // Setup chart auto-refresh
    setupChartAutoRefresh();
    
    // Monitor system performance
    startPerformanceMonitoring();
}

function setupInteractiveElements() {
    // Enhanced refresh button
    setupEnhancedRefresh();
    
    // Interactive KPI cards
    setupInteractiveKPICards();
    
    // Action card interactions
    setupActionCardInteractions();
}

// =============================================================================
// ENHANCED KPI ANIMATIONS
// =============================================================================

function animateKPICards() {
    const kpiCards = document.querySelectorAll('.kpi-card');
    
    kpiCards.forEach((card, index) => {
        // Initial state
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px) scale(0.95)';
        
        // Animate in
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
            
            // Add hover effects
            setupKPICardHover(card);
        }, 100 + (index * 150));
    });
}

function setupKPICardHover(card) {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-4px) scale(1.02)';
        card.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = '';
    });
}

function animateKPIValue(cardId, newValue, trend = 'stable') {
    const card = document.getElementById(cardId);
    if (!card) return;
    
    const valueElement = card.querySelector('.kpi-value');
    const trendElement = card.querySelector('.kpi-trend');
    
    if (valueElement) {
        // Animate value change
        valueElement.style.transform = 'scale(1.1)';
        valueElement.style.color = getTrendColor(trend);
        
        setTimeout(() => {
            valueElement.textContent = newValue;
            valueElement.style.transform = 'scale(1)';
            valueElement.style.color = '';
        }, 200);
    }
    
    if (trendElement) {
        // Update trend indicator
        updateTrendIndicator(trendElement, trend);
    }
    
    // Add pulse effect
    card.classList.add('kpi-pulse');
    setTimeout(() => card.classList.remove('kpi-pulse'), 600);
}

function getTrendColor(trend) {
    switch (trend) {
        case 'up': return 'var(--emerald-success)';
        case 'down': return '#e74c3c';
        default: return 'var(--harbor-blue)';
    }
}

function updateTrendIndicator(element, trend) {
    element.className = `kpi-trend trend-${trend}`;
    
    const icons = {
        up: 'fas fa-arrow-up',
        down: 'fas fa-arrow-down',
        stable: 'fas fa-minus'
    };
    
    element.innerHTML = `<i class="${icons[trend]}"></i>`;
}

// =============================================================================
// SPARKLINE ENHANCEMENTS
// =============================================================================

function setupSparklineAnimations() {
    const sparklines = document.querySelectorAll('.sparkline');
    
    sparklines.forEach(sparkline => {
        // Add interactive hover effects
        sparkline.addEventListener('mouseenter', () => {
            sparkline.style.transform = 'scaleY(1.1)';
            sparkline.style.filter = 'brightness(1.2)';
        });
        
        sparkline.addEventListener('mouseleave', () => {
            sparkline.style.transform = 'scaleY(1)';
            sparkline.style.filter = 'brightness(1)';
        });
        
        // Add click to expand functionality
        sparkline.addEventListener('click', () => {
            expandSparkline(sparkline);
        });
    });
}

function expandSparkline(sparklineElement) {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'sparkline-modal';
    modal.innerHTML = `
        <div class="sparkline-modal-content">
            <div class="sparkline-modal-header">
                <h3>Évolution Détaillée</h3>
                <button class="close-modal" onclick="this.closest('.sparkline-modal').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="sparkline-modal-body">
                <canvas id="expandedSparkline" width="600" height="300"></canvas>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Animate modal in
    setTimeout(() => modal.classList.add('show'), 10);
    
    // Create expanded chart
    createExpandedSparklineChart('expandedSparkline');
}

function createExpandedSparklineChart(canvasId) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;
    
    // Generate sample data
    const data = Array.from({ length: 50 }, (_, i) => ({
        x: i,
        y: Math.sin(i * 0.2) * 20 + 50 + Math.random() * 10
    }));
    
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Évolution',
                data: data,
                borderColor: 'var(--harbor-blue)',
                backgroundColor: 'rgba(46, 134, 171, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { display: false },
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0,0,0,0.1)' }
                }
            }
        }
    });
}

// =============================================================================
// REAL-TIME DATA SIMULATION
// =============================================================================

function startRealTimeSimulation() {
    DashboardUI.refreshInterval = setInterval(() => {
        updateRealTimeData();
    }, DashboardUI.simulationSettings.updateInterval);
    
    console.log('🔄 Real-time simulation started');
}

function updateRealTimeData() {
    const startTime = performance.now();
    
    // Update wave height
    const currentWaveHeight = parseFloat(document.getElementById('waveHeightValue')?.textContent || '2.3');
    const newWaveHeight = generateRealisticWaveHeight(currentWaveHeight);
    const waveTrend = newWaveHeight > currentWaveHeight ? 'up' : newWaveHeight < currentWaveHeight ? 'down' : 'stable';
    animateKPIValue('waveHeightCard', newWaveHeight.toFixed(1) + 'm', waveTrend);
    
    // Update average period
    const currentPeriod = parseFloat(document.getElementById('avgPeriodValue')?.textContent || '8.2');
    const newPeriod = generateRealisticPeriod(currentPeriod);
    const periodTrend = newPeriod > currentPeriod ? 'up' : newPeriod < currentPeriod ? 'down' : 'stable';
    animateKPIValue('avgPeriodCard', newPeriod.toFixed(1) + 's', periodTrend);
    
    // Update acquisition rate
    const baseRate = 98.5;
    const newRate = baseRate + (Math.random() - 0.5) * DashboardUI.simulationSettings.acquisitionJitter;
    const rateTrend = newRate > 98 ? 'up' : newRate < 97 ? 'down' : 'stable';
    animateKPIValue('acquisitionRateCard', newRate.toFixed(1) + '%', rateTrend);
    
    // Update acquisition frequency
    const frequencies = ['50 Hz', '100 Hz', '200 Hz'];
    const currentFreq = document.getElementById('acquisitionFreqValue')?.textContent || '100 Hz';
    // Keep frequency stable most of the time
    if (Math.random() < 0.05) {
        const newFreq = frequencies[Math.floor(Math.random() * frequencies.length)];
        animateKPIValue('acquisitionFreqCard', newFreq, 'stable');
    }
    
    // Update system health
    const healthValues = ['Excellent', 'Bon', 'Moyen'];
    const healthColors = ['var(--emerald-success)', 'var(--harbor-blue)', '#f39c12'];
    const currentHealth = document.getElementById('systemHealthValue')?.textContent || 'Excellent';
    // Keep health stable most of the time
    if (Math.random() < 0.02) {
        const newHealth = healthValues[Math.floor(Math.random() * healthValues.length)];
        animateKPIValue('systemHealthCard', newHealth, 'stable');
    }
    
    // Update chart if it exists
    if (window.waveChart) {
        updateWaveChart();
    }
    
    // Update performance metrics
    const endTime = performance.now();
    updatePerformanceMetrics(endTime - startTime);
}

function generateRealisticWaveHeight(current) {
    const variation = DashboardUI.simulationSettings.waveVariation;
    const change = (Math.random() - 0.5) * variation;
    const newValue = current + change;
    return Math.max(0.1, Math.min(5.0, newValue)); // Clamp between 0.1m and 5.0m
}

function generateRealisticPeriod(current) {
    const variation = DashboardUI.simulationSettings.periodVariation;
    const change = (Math.random() - 0.5) * variation;
    const newValue = current + change;
    return Math.max(3.0, Math.min(15.0, newValue)); // Clamp between 3s and 15s
}

function updateWaveChart() {
    if (!window.waveChart) return;
    
    const now = new Date();
    const newDataPoint = {
        x: now,
        y: Math.sin(now.getTime() / 1000) * 2 + 2.5 + (Math.random() - 0.5) * 0.5
    };
    
    // Add new point
    window.waveChart.data.datasets[0].data.push(newDataPoint);
    
    // Remove old points (keep last 50)
    if (window.waveChart.data.datasets[0].data.length > 50) {
        window.waveChart.data.datasets[0].data.shift();
    }
    
    // Update chart
    window.waveChart.update('none');
}

// =============================================================================
// ENHANCED REFRESH FUNCTIONALITY
// =============================================================================

function setupEnhancedRefresh() {
    const refreshBtn = document.getElementById('refreshData');
    if (!refreshBtn) return;
    
    refreshBtn.addEventListener('click', () => {
        performEnhancedRefresh();
    });
}

function performEnhancedRefresh() {
    const refreshBtn = document.getElementById('refreshData');
    if (!refreshBtn) return;
    
    // Add loading state
    refreshBtn.classList.add('loading');
    refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Actualisation...';
    
    // Simulate refresh process
    setTimeout(() => {
        // Force update all KPIs
        updateRealTimeData();
        
        // Show success feedback
        refreshBtn.classList.remove('loading');
        refreshBtn.classList.add('success');
        refreshBtn.innerHTML = '<i class="fas fa-check"></i> Actualisé';
        
        // Reset button after delay
        setTimeout(() => {
            refreshBtn.classList.remove('success');
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Actualiser';
        }, 2000);
        
        showNotification('Données actualisées', 'success');
    }, 1500);
}

// =============================================================================
// INTERACTIVE KPI CARDS
// =============================================================================

function setupInteractiveKPICards() {
    const kpiCards = document.querySelectorAll('.kpi-card');
    
    kpiCards.forEach(card => {
        card.addEventListener('click', () => {
            showKPIDetails(card);
        });
        
        // Add context menu
        card.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            showKPIContextMenu(e, card);
        });
    });
}

function showKPIDetails(card) {
    const cardId = card.id;
    const title = card.querySelector('.kpi-label')?.textContent || 'Détails KPI';
    
    const modal = document.createElement('div');
    modal.className = 'kpi-details-modal';
    modal.innerHTML = `
        <div class="kpi-details-content">
            <div class="kpi-details-header">
                <h3>${title}</h3>
                <button class="close-modal" onclick="this.closest('.kpi-details-modal').remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="kpi-details-body">
                <div class="kpi-stats-grid">
                    <div class="stat-item">
                        <span class="stat-label">Valeur Actuelle</span>
                        <span class="stat-value">${card.querySelector('.kpi-value')?.textContent || 'N/A'}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Tendance</span>
                        <span class="stat-value">${getTrendText(card)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Dernière Mise à Jour</span>
                        <span class="stat-value">${new Date().toLocaleTimeString()}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Statut</span>
                        <span class="stat-value status-good">Normal</span>
                    </div>
                </div>
                <div class="kpi-chart-container">
                    <canvas id="kpiDetailChart" width="400" height="200"></canvas>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('show'), 10);
    
    // Create detail chart
    createKPIDetailChart('kpiDetailChart', cardId);
}

function getTrendText(card) {
    const trendElement = card.querySelector('.kpi-trend');
    if (!trendElement) return 'Stable';
    
    if (trendElement.classList.contains('trend-up')) return 'En hausse';
    if (trendElement.classList.contains('trend-down')) return 'En baisse';
    return 'Stable';
}

function createKPIDetailChart(canvasId, kpiType) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;
    
    // Generate historical data based on KPI type
    const data = generateKPIHistoricalData(kpiType);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Évolution',
                data: data.values,
                borderColor: 'var(--harbor-blue)',
                backgroundColor: 'rgba(46, 134, 171, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0,0,0,0.1)' }
                },
                x: {
                    grid: { color: 'rgba(0,0,0,0.1)' }
                }
            }
        }
    });
}

function generateKPIHistoricalData(kpiType) {
    const now = new Date();
    const labels = [];
    const values = [];
    
    for (let i = 23; i >= 0; i--) {
        const time = new Date(now.getTime() - i * 60 * 60 * 1000);
        labels.push(time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        
        switch (kpiType) {
            case 'waveHeightCard':
                values.push(2.0 + Math.sin(i * 0.3) * 0.8 + Math.random() * 0.4);
                break;
            case 'avgPeriodCard':
                values.push(8.0 + Math.cos(i * 0.2) * 1.5 + Math.random() * 0.6);
                break;
            case 'acquisitionRateCard':
                values.push(98 + Math.random() * 2);
                break;
            default:
                values.push(Math.random() * 100);
        }
    }
    
    return { labels, values };
}

// =============================================================================
// ACTION CARD INTERACTIONS
// =============================================================================

function setupActionCardInteractions() {
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px)';
            card.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.2)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '';
        });
        
        // Add click animations
        card.addEventListener('click', () => {
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = 'translateY(-8px)';
            }, 150);
        });
    });
}

function animateActionCards() {
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(40px) rotateX(10deg)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) rotateX(0deg)';
        }, 300 + (index * 200));
    });
}

// =============================================================================
// PERFORMANCE MONITORING
// =============================================================================

function startPerformanceMonitoring() {
    setInterval(() => {
        const memoryInfo = performance.memory;
        if (memoryInfo) {
            const usedMB = Math.round(memoryInfo.usedJSHeapSize / 1048576);
            const totalMB = Math.round(memoryInfo.totalJSHeapSize / 1048576);
            
            console.log(`📊 Memory Usage: ${usedMB}MB / ${totalMB}MB`);
            
            // Update system health based on memory usage
            const memoryUsagePercent = (usedMB / totalMB) * 100;
            updateSystemHealthBasedOnPerformance(memoryUsagePercent);
        }
    }, 30000); // Check every 30 seconds
}

function updatePerformanceMetrics(updateTime) {
    DashboardUI.performance.updateCount++;
    DashboardUI.performance.averageUpdateTime = 
        (DashboardUI.performance.averageUpdateTime + updateTime) / 2;
    DashboardUI.performance.lastUpdate = Date.now();
    
    // Log performance if it's getting slow
    if (updateTime > 100) {
        console.warn(`⚠️ Slow update detected: ${updateTime.toFixed(2)}ms`);
    }
}

function updateSystemHealthBasedOnPerformance(memoryUsagePercent) {
    const healthCard = document.getElementById('systemHealthCard');
    if (!healthCard) return;
    
    let health, trend;
    
    if (memoryUsagePercent < 70) {
        health = 'Excellent';
        trend = 'up';
    } else if (memoryUsagePercent < 85) {
        health = 'Bon';
        trend = 'stable';
    } else {
        health = 'Attention';
        trend = 'down';
    }
    
    const currentHealth = document.getElementById('systemHealthValue')?.textContent;
    if (currentHealth !== health) {
        animateKPIValue('systemHealthCard', health, trend);
    }
}

// =============================================================================
// RESPONSIVE BEHAVIOR
// =============================================================================

function setupResponsiveBehavior() {
    let resizeTimeout;
    
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            handleResponsiveResize();
        }, 250);
    });
}

function handleResponsiveResize() {
    // Recalculate chart dimensions
    if (window.waveChart) {
        window.waveChart.resize();
    }
    
    // Adjust KPI card layout
    adjustKPICardLayout();
    
    console.log('📱 Responsive layout adjusted');
}

function adjustKPICardLayout() {
    const kpiGrid = document.querySelector('.kpi-grid');
    if (!kpiGrid) return;
    
    const containerWidth = kpiGrid.offsetWidth;
    const cardMinWidth = 250;
    const gap = 20;
    
    const columnsCount = Math.floor((containerWidth + gap) / (cardMinWidth + gap));
    kpiGrid.style.gridTemplateColumns = `repeat(${Math.max(1, columnsCount)}, 1fr)`;
}

// =============================================================================
// KEYBOARD SHORTCUTS
// =============================================================================

function setupDashboardKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
        // Ctrl/Cmd + R: Refresh data
        if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
            event.preventDefault();
            performEnhancedRefresh();
        }
        
        // Ctrl/Cmd + D: Toggle dark mode
        if ((event.ctrlKey || event.metaKey) && event.key === 'd') {
            event.preventDefault();
            toggleTheme();
        }
        
        // F11: Toggle fullscreen
        if (event.key === 'F11') {
            event.preventDefault();
            toggleFullscreen();
        }
    });
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        showNotification('Mode plein écran activé', 'info');
    } else {
        document.exitFullscreen();
        showNotification('Mode plein écran désactivé', 'info');
    }
}

// =============================================================================
// DASHBOARD STYLES
// =============================================================================

function addDashboardStyles() {
    if (document.getElementById('dashboard-ui-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'dashboard-ui-styles';
    style.textContent = `
        .kpi-pulse {
            animation: kpi-pulse 0.6s ease-out;
        }
        
        @keyframes kpi-pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .sparkline-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .sparkline-modal.show {
            opacity: 1;
        }
        
        .sparkline-modal-content {
            background: var(--foam-white);
            border-radius: 12px;
            width: 90%;
            max-width: 800px;
            max-height: 80%;
            overflow: hidden;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        }
        
        .sparkline-modal.show .sparkline-modal-content {
            transform: scale(1);
        }
        
        .sparkline-modal-header {
            padding: 20px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .sparkline-modal-body {
            padding: 20px;
            height: 350px;
        }
        
        .close-modal {
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: var(--ocean-deep);
            padding: 8px;
            border-radius: 50%;
            transition: background-color 0.2s ease;
        }
        
        .close-modal:hover {
            background-color: rgba(0, 0, 0, 0.1);
        }
        
        .kpi-details-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .kpi-details-modal.show {
            opacity: 1;
        }
        
        .kpi-details-content {
            background: var(--foam-white);
            border-radius: 12px;
            width: 90%;
            max-width: 600px;
            max-height: 80%;
            overflow: hidden;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        }
        
        .kpi-details-modal.show .kpi-details-content {
            transform: scale(1);
        }
        
        .kpi-details-header {
            padding: 20px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .kpi-details-body {
            padding: 20px;
        }
        
        .kpi-stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(46, 134, 171, 0.05);
            border-radius: 8px;
        }
        
        .stat-label {
            display: block;
            font-size: 0.8rem;
            color: var(--ocean-deep);
            margin-bottom: 5px;
        }
        
        .stat-value {
            display: block;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--harbor-blue);
        }
        
        .status-good {
            color: var(--emerald-success) !important;
        }
        
        .kpi-chart-container {
            height: 250px;
            position: relative;
        }
        
        .loading {
            opacity: 0.7;
            pointer-events: none;
        }
        
        .success {
            background-color: var(--emerald-success) !important;
            color: white !important;
        }
        
        @media (max-width: 768px) {
            .sparkline-modal-content,
            .kpi-details-content {
                width: 95%;
                margin: 20px;
            }
            
            .kpi-stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    `;
    
    document.head.appendChild(style);
}

// =============================================================================
// EXPORT FOR GLOBAL ACCESS
// =============================================================================

window.DashboardUI = {
    performEnhancedRefresh,
    toggleFullscreen,
    startRealTimeSimulation: () => {
        if (DashboardUI.refreshInterval) {
            clearInterval(DashboardUI.refreshInterval);
        }
        startRealTimeSimulation();
    },
    stopRealTimeSimulation: () => {
        if (DashboardUI.refreshInterval) {
            clearInterval(DashboardUI.refreshInterval);
            DashboardUI.refreshInterval = null;
        }
    }
};

// =============================================================================
// CLEANUP ON PAGE UNLOAD
// =============================================================================

window.addEventListener('beforeunload', () => {
    if (DashboardUI.refreshInterval) {
        clearInterval(DashboardUI.refreshInterval);
    }
});