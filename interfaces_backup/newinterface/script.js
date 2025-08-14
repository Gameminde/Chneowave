// CHNeoWave - Maritime Analysis System
// Professional scientific software for oceanographic data acquisition and analysis

class CHNeoWave {
    constructor() {
        this.currentModule = 'dashboard';
        this.currentProject = null;
        this.isAcquiring = false;
        this.calibrationData = {};
        this.sensorData = {};
        this.dataInterval = null;
        this.chartContexts = {};
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.updateMetrics();
        this.setupCharts();
        this.loadProjectData();
        this.initializeCalibration();
    }

    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const module = item.getAttribute('data-module');
                this.switchModule(module);
            });
        });
    }

    switchModule(moduleName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-module="${moduleName}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.module-content').forEach(content => {
            content.classList.remove('active');
        });
        
        const targetModule = document.getElementById(`${moduleName}-module`);
        if (targetModule) {
            targetModule.classList.add('active');
        }
        
        // Update page title
        this.updatePageTitle(moduleName);
        
        // Initialize module-specific features
        this.initializeModule(moduleName);
    }

    updatePageTitle(moduleName) {
        const titles = {
            'dashboard': 'Tableau de Bord Principal',
            'project': 'Gestion de Projet',
            'calibration': 'Calibration des Capteurs',
            'acquisition': 'Acquisition de Données',
            'analysis': 'Analyse des Données',
            'export': 'Export et Rapports',
            'system': 'Configuration Système',
            'about': 'À propos'
        };
        
        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = titles[moduleName] || 'CHNeoWave';
        }
    }

    initializeModule(moduleName) {
        switch(moduleName) {
            case 'acquisition':
                this.initializeAcquisition();
                break;
            case 'analysis':
                this.initializeAnalysis();
                break;
            case 'export':
                this.initializeExport();
                break;
        }
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }

        // Project initialization
        const initButton = document.getElementById('init-session');
        if (initButton) {
            initButton.addEventListener('click', () => {
                this.initializeSession();
            });
        }

        // Acquisition controls
        const startBtn = document.getElementById('start-acquisition');
        const stopBtn = document.getElementById('stop-acquisition');
        const saveBtn = document.getElementById('save-acquisition');
        
        if (startBtn) startBtn.addEventListener('click', () => this.startAcquisition());
        if (stopBtn) stopBtn.addEventListener('click', () => this.stopAcquisition());
        if (saveBtn) saveBtn.addEventListener('click', () => this.saveAcquisition());

        // Analysis controls
        document.querySelectorAll('.method-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const method = e.target.getAttribute('data-method');
                this.switchAnalysisMethod(method);
            });
        });

        // Export controls
        const reportBtn = document.getElementById('generate-report');
        const exportBtn = document.getElementById('export-data');
        
        if (reportBtn) reportBtn.addEventListener('click', () => this.generateReport());
        if (exportBtn) exportBtn.addEventListener('click', () => this.exportData());

        // Calibration controls
        const activeSensor = document.getElementById('active-sensor');
        const calibrationPoints = document.getElementById('calibration-points');
        
        if (activeSensor) {
            activeSensor.addEventListener('change', (e) => {
                this.switchCalibrationSensor(e.target.value);
            });
        }
        
        if (calibrationPoints) {
            calibrationPoints.addEventListener('change', (e) => {
                this.updateCalibrationTable(parseInt(e.target.value));
            });
        }
    }

    initializeSession() {
        this.showNotification('Session initialisée avec succès', 'success');
        
        // Create a new project
        this.currentProject = {
            name: `Projet_${new Date().toISOString().split('T')[0]}`,
            created: new Date().toISOString(),
            sensors: 4,
            frequency: 1000
        };
        
        // Save to localStorage
        localStorage.setItem('chneowave_project', JSON.stringify(this.currentProject));
        
        this.updateProjectInfo();
    }

    updateProjectInfo() {
        const projectName = document.querySelector('.project-name');
        if (this.currentProject && projectName) {
            projectName.textContent = this.currentProject.name;
        } else if (projectName) {
            projectName.textContent = 'Aucun projet actif';
        }
    }

    startAcquisition() {
        if (!this.currentProject) {
            this.showNotification('Veuillez créer un projet avant de démarrer l\'acquisition', 'warning');
            return;
        }

        this.isAcquiring = true;
        const startBtn = document.getElementById('start-acquisition');
        const stopBtn = document.getElementById('stop-acquisition');
        const saveBtn = document.getElementById('save-acquisition');
        
        if (startBtn) startBtn.disabled = true;
        if (stopBtn) stopBtn.disabled = false;
        if (saveBtn) saveBtn.disabled = true;

        // Start data simulation
        this.startDataSimulation();
        
        this.showNotification('Acquisition démarrée', 'success');
        console.log('Acquisition démarrée');
    }

    stopAcquisition() {
        this.isAcquiring = false;
        const startBtn = document.getElementById('start-acquisition');
        const stopBtn = document.getElementById('stop-acquisition');
        const saveBtn = document.getElementById('save-acquisition');
        
        if (startBtn) startBtn.disabled = false;
        if (stopBtn) stopBtn.disabled = true;
        if (saveBtn) saveBtn.disabled = false;

        // Stop data simulation
        this.stopDataSimulation();
        
        this.showNotification('Acquisition arrêtée', 'info');
        console.log('Acquisition arrêtée');
    }

    saveAcquisition() {
        if (this.sensorData && Object.keys(this.sensorData).length > 0) {
            // Simulate saving data
            const saveButton = document.getElementById('save-acquisition');
            if (saveButton) {
                const originalText = saveButton.innerHTML;
                saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sauvegarde...';
                saveButton.disabled = true;

                setTimeout(() => {
                    saveButton.innerHTML = originalText;
                    saveButton.disabled = false;
                    this.showNotification('Données sauvegardées avec succès', 'success');
                }, 2000);
            }

            console.log('Données sauvegardées:', this.sensorData);
        }
    }

    startDataSimulation() {
        this.dataInterval = setInterval(() => {
            this.updateSensorData();
            this.updateStatistics();
            this.updateCharts();
        }, 100);
    }

    stopDataSimulation() {
        if (this.dataInterval) {
            clearInterval(this.dataInterval);
            this.dataInterval = null;
        }
    }

    updateSensorData() {
        const sensors = ['1', '2', '3', '4'];
        sensors.forEach(sensorId => {
            if (!this.sensorData[sensorId]) {
                this.sensorData[sensorId] = [];
            }

            // Generate realistic wave data
            const time = Date.now() / 1000;
            const amplitude = 15 + Math.random() * 10;
            const frequency = 0.5 + Math.random() * 0.5;
            const phase = Math.random() * Math.PI * 2;
            
            const value = amplitude * Math.sin(2 * Math.PI * frequency * time + phase) + 
                         (Math.random() - 0.5) * 2; // Add noise

            this.sensorData[sensorId].push({
                time: time,
                value: value,
                timestamp: new Date().toISOString()
            });

            // Keep only last 1000 points
            if (this.sensorData[sensorId].length > 1000) {
                this.sensorData[sensorId].shift();
            }
        });
    }

    updateStatistics() {
        if (Object.keys(this.sensorData).length === 0) return;

        // Calculate statistics for the first sensor
        const sensor1Data = this.sensorData['1']?.map(point => point.value) || [];
        if (sensor1Data.length === 0) return;

        const values = sensor1Data.slice(-100); // Last 100 points
        const max = Math.max(...values);
        const min = Math.min(...values);
        const sortedValues = [...values].sort((a, b) => b - a);
        
        // Calculate Hs (Significant Wave Height)
        const hs = sortedValues.slice(0, Math.floor(values.length / 3))
                              .reduce((sum, val) => sum + val, 0) / Math.floor(values.length / 3);

        // Update display
        const hsValue = document.getElementById('hs-value');
        const hmaxValue = document.getElementById('hmax-value');
        const hminValue = document.getElementById('hmin-value');
        const h13Value = document.getElementById('h13-value');
        const tmValue = document.getElementById('tm-value');
        const tpValue = document.getElementById('tp-value');
        
        if (hsValue) hsValue.textContent = hs.toFixed(1);
        if (hmaxValue) hmaxValue.textContent = max.toFixed(1);
        if (hminValue) hminValue.textContent = min.toFixed(1);
        if (h13Value) h13Value.textContent = hs.toFixed(1);
        if (tmValue) tmValue.textContent = (2.5 + Math.random() * 1).toFixed(1);
        if (tpValue) tpValue.textContent = (3.0 + Math.random() * 1.5).toFixed(1);
    }

    updateCharts() {
        // Update sensor charts if they exist
        this.updateSensorChart('sensor-a-chart', document.getElementById('sensor-a-select')?.value || '1');
        this.updateSensorChart('sensor-b-chart', document.getElementById('sensor-b-select')?.value || '2');
        this.updateMultiSensorChart();
    }

    updateSensorChart(canvasId, sensorId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas || !this.sensorData[sensorId]) return;

        const ctx = canvas.getContext('2d');
        const data = this.sensorData[sensorId].slice(-100);

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw grid
        this.drawChartGrid(ctx, canvas.width, canvas.height);

        // Draw wave
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2;
        ctx.beginPath();

        data.forEach((point, index) => {
            const x = (index / (data.length - 1)) * canvas.width;
            const y = canvas.height / 2 - (point.value / 50) * canvas.height / 2;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();
    }

    updateMultiSensorChart() {
        const canvas = document.getElementById('multi-sensor-chart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw grid
        this.drawChartGrid(ctx, canvas.width, canvas.height);

        const colors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b'];
        const sensors = ['1', '2', '3', '4'];

        sensors.forEach((sensorId, index) => {
            if (!this.sensorData[sensorId]) return;

            const data = this.sensorData[sensorId].slice(-100);
            ctx.strokeStyle = colors[index];
            ctx.lineWidth = 2;
            ctx.beginPath();

            data.forEach((point, dataIndex) => {
                const x = (dataIndex / (data.length - 1)) * canvas.width;
                const y = canvas.height / 2 - (point.value / 50) * canvas.height / 2;
                
                if (dataIndex === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });

            ctx.stroke();
        });
    }

    drawChartGrid(ctx, width, height) {
        ctx.strokeStyle = '#374151';
        ctx.lineWidth = 1;
        ctx.globalAlpha = 0.3;

        // Vertical lines
        for (let i = 0; i <= 10; i++) {
            const x = (i / 10) * width;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }

        // Horizontal lines
        for (let i = 0; i <= 10; i++) {
            const y = (i / 10) * height;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }

        ctx.globalAlpha = 1;
    }

    setupCharts() {
        // Initialize chart canvases
        const chartIds = ['sensor-a-chart', 'sensor-b-chart', 'multi-sensor-chart', 'calibration-chart', 'spectrum-chart'];
        chartIds.forEach(id => {
            const canvas = document.getElementById(id);
            if (canvas) {
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;
            }
        });
    }

    initializeCalibration() {
        const sensorId = document.getElementById('active-sensor')?.value || '1';
        this.switchCalibrationSensor(sensorId);
    }

    switchCalibrationSensor(sensorId) {
        // Load calibration data for selected sensor
        if (!this.calibrationData[sensorId]) {
            this.calibrationData[sensorId] = [];
        }
        
        this.updateCalibrationTable(document.getElementById('calibration-points')?.value || 5);
        this.updateCalibrationChart(sensorId);
    }

    updateCalibrationTable(points) {
        const tbody = document.getElementById('calibration-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        for (let i = 0; i < points; i++) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i + 1}</td>
                <td><input type="number" class="height-input" placeholder="cm" step="0.1"></td>
                <td><input type="number" class="voltage-input" placeholder="V" step="0.001"></td>
                <td>↑↓</td>
                <td><span class="status-pending">En attente</span></td>
            `;
            tbody.appendChild(row);
        }

        // Add event listeners to inputs
        tbody.querySelectorAll('.height-input, .voltage-input').forEach(input => {
            input.addEventListener('input', () => {
                this.updateCalibrationChart();
            });
        });
    }

    updateCalibrationChart(sensorId = null) {
        const canvas = document.getElementById('calibration-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw grid
        this.drawChartGrid(ctx, canvas.width, canvas.height);

        // Get calibration data from table
        const tbody = document.getElementById('calibration-tbody');
        if (!tbody) return;

        const data = [];
        tbody.querySelectorAll('tr').forEach(row => {
            const heightInput = row.querySelector('.height-input');
            const voltageInput = row.querySelector('.voltage-input');
            
            if (heightInput && voltageInput && heightInput.value && voltageInput.value) {
                data.push({
                    x: parseFloat(voltageInput.value),
                    y: parseFloat(heightInput.value)
                });
            }
        });

        if (data.length > 0) {
            // Draw calibration points
            ctx.fillStyle = '#3b82f6';
            data.forEach(point => {
                const x = (point.x / 10) * canvas.width;
                const y = canvas.height - (point.y / 50) * canvas.height;
                
                ctx.beginPath();
                ctx.arc(x, y, 4, 0, 2 * Math.PI);
                ctx.fill();
            });

            // Draw regression line if we have enough points
            if (data.length >= 2) {
                const regression = this.calculateLinearRegression(data);
                
                ctx.strokeStyle = '#06b6d4';
                ctx.lineWidth = 2;
                ctx.beginPath();
                
                const x1 = 0;
                const y1 = canvas.height - (regression.slope * 0 + regression.intercept) / 50 * canvas.height;
                const x2 = canvas.width;
                const y2 = canvas.height - (regression.slope * 10 + regression.intercept) / 50 * canvas.height;
                
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.stroke();

                // Update stats
                const rSquared = document.getElementById('r-squared');
                const slope = document.getElementById('slope');
                const offset = document.getElementById('offset');
                
                if (rSquared) rSquared.textContent = regression.rSquared.toFixed(3);
                if (slope) slope.textContent = regression.slope.toFixed(2) + ' cm/V';
                if (offset) offset.textContent = regression.intercept.toFixed(2) + ' cm';
            }
        }
    }

    calculateLinearRegression(data) {
        const n = data.length;
        const sumX = data.reduce((sum, point) => sum + point.x, 0);
        const sumY = data.reduce((sum, point) => sum + point.y, 0);
        const sumXY = data.reduce((sum, point) => sum + point.x * point.y, 0);
        const sumX2 = data.reduce((sum, point) => sum + point.x * point.x, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        // Calculate R-squared
        const meanY = sumY / n;
        const ssRes = data.reduce((sum, point) => {
            const predicted = slope * point.x + intercept;
            return sum + Math.pow(point.y - predicted, 2);
        }, 0);
        const ssTot = data.reduce((sum, point) => {
            return sum + Math.pow(point.y - meanY, 2);
        }, 0);
        const rSquared = 1 - (ssRes / ssTot);

        return { slope, intercept, rSquared };
    }

    switchAnalysisMethod(method) {
        // Update active method button
        document.querySelectorAll('.method-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-method="${method}"]`)?.classList.add('active');

        // Update analysis results based on method
        this.updateAnalysisResults(method);
    }

    updateAnalysisResults(method) {
        const methods = {
            'fft': { name: 'Analyse Spectrale FFT', hs: 15.2, tp: 3.4, tm: 2.8 },
            'jonswap': { name: 'JONSWAP', hs: 14.8, tp: 3.2, tm: 2.6 },
            'pierson': { name: 'Pierson-Moskowitz', hs: 15.5, tp: 3.6, tm: 3.0 },
            'goda': { name: 'Goda-SVD', hs: 14.9, tp: 3.3, tm: 2.7 }
        };

        const result = methods[method] || methods['fft'];
        
        // Update analysis stats
        document.querySelectorAll('.analysis-stat .stat-value').forEach((stat, index) => {
            const values = [result.hs, result.tp, result.tm];
            if (values[index] !== undefined) {
                stat.textContent = values[index].toFixed(1);
            }
        });

        // Update spectrum chart
        this.updateSpectrumChart(method);
    }

    updateSpectrumChart(method) {
        const canvas = document.getElementById('spectrum-chart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw grid
        this.drawChartGrid(ctx, canvas.width, canvas.height);

        // Generate spectrum data based on method
        const frequencies = [];
        const powers = [];

        for (let i = 0; i < 100; i++) {
            const freq = i * 0.1; // 0 to 10 Hz
            frequencies.push(freq);

            let power = 0;
            switch(method) {
                case 'fft':
                    power = Math.exp(-Math.pow(freq - 2, 2) / 2) * 10;
                    break;
                case 'jonswap':
                    power = Math.exp(-1.25 * Math.pow(freq / 2, -4)) * Math.pow(freq / 2, -5) * 8;
                    break;
                case 'pierson':
                    power = Math.exp(-0.74 * Math.pow(freq / 2, -4)) * Math.pow(freq / 2, -5) * 12;
                    break;
                case 'goda':
                    power = Math.exp(-Math.pow(freq - 1.5, 2) / 1.5) * 9;
                    break;
            }
            powers.push(power);
        }

        // Draw spectrum
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2;
        ctx.beginPath();

        frequencies.forEach((freq, index) => {
            const x = (freq / 10) * canvas.width;
            const y = canvas.height - (powers[index] / 15) * canvas.height;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();
    }

    generateReport() {
        const reportButton = document.getElementById('generate-report');
        if (!reportButton) return;
        
        const originalText = reportButton.innerHTML;
        reportButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Génération...';
        reportButton.disabled = true;

        setTimeout(() => {
            reportButton.innerHTML = originalText;
            reportButton.disabled = false;
            
            const preview = document.getElementById('report-preview');
            if (preview) {
                preview.innerHTML = `
                    <div class="report-content">
                        <h3>Rapport d'Analyse Maritime</h3>
                        <p><strong>Projet:</strong> ${this.currentProject?.name || 'Non défini'}</p>
                        <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
                        <p><strong>Hs:</strong> 15.2 cm</p>
                        <p><strong>Tp:</strong> 3.4 s</p>
                        <p>Rapport généré avec succès.</p>
                    </div>
                `;
            }
            
            this.showNotification('Rapport généré avec succès', 'success');
        }, 3000);
    }

    exportData() {
        const exportButton = document.getElementById('export-data');
        if (!exportButton) return;
        
        const originalText = exportButton.innerHTML;
        exportButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Export...';
        exportButton.disabled = true;

        setTimeout(() => {
            exportButton.innerHTML = originalText;
            exportButton.disabled = false;
            this.showNotification('Données exportées avec succès', 'success');
        }, 2000);
    }

    toggleTheme() {
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        body.setAttribute('data-theme', newTheme);
        
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            if (newTheme === 'light') {
                themeToggle.innerHTML = '<i class="fas fa-moon"></i><span>Mode Sombre</span>';
            } else {
                themeToggle.innerHTML = '<i class="fas fa-sun"></i><span>Mode Clair</span>';
            }
        }
    }

    updateMetrics() {
        // Simulate real-time system metrics
        setInterval(() => {
            const cpuUsage = document.getElementById('cpu-usage');
            const memoryUsage = document.getElementById('memory-usage');
            const diskUsage = document.getElementById('disk-usage');
            
            if (cpuUsage) cpuUsage.textContent = (Math.random() * 30 + 10).toFixed(1) + '%';
            if (memoryUsage) memoryUsage.textContent = (Math.random() * 40 + 30).toFixed(1) + '%';
            if (diskUsage) diskUsage.textContent = (Math.random() * 20 + 60).toFixed(1) + '%';
        }, 2000);
    }

    loadProjectData() {
        // Load any existing project data from localStorage
        const savedProject = localStorage.getItem('chneowave_project');
        if (savedProject) {
            this.currentProject = JSON.parse(savedProject);
            this.updateProjectInfo();
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: var(--space-3) var(--space-4);
            color: var(--text-primary);
            font-size: var(--text-sm);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: var(--space-2);
            box-shadow: var(--shadow-lg);
            transform: translateX(100%);
            transition: transform var(--transition-normal);
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'error': 'times-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    initializeAcquisition() {
        // Initialize acquisition-specific features
        console.log('Acquisition module initialized');
    }

    initializeAnalysis() {
        // Initialize analysis-specific features
        this.updateAnalysisResults('fft');
    }

    initializeExport() {
        // Initialize export-specific features
        const preview = document.getElementById('report-preview');
        if (preview) {
            preview.innerHTML = `
                <div class="preview-placeholder">
                    <i class="fas fa-file-alt"></i>
                    <p>Aperçu du rapport généré apparaîtra ici</p>
                </div>
            `;
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Afficher la fenêtre d’accueil au lancement
    const welcomeModal = document.getElementById('welcome-modal');
    const projectFormModal = document.getElementById('project-form-modal');
    const btnNewProject = document.getElementById('btn-new-project');
    const btnImportProject = document.getElementById('btn-import-project');
    const mainContent = document.querySelector('.main-content');
    if (welcomeModal) {
        welcomeModal.style.display = 'flex';
    }
    // Actions boutons accueil
    if (btnNewProject) {
        btnNewProject.addEventListener('click', () => {
            if (welcomeModal) welcomeModal.style.display = 'none';
            if (projectFormModal) projectFormModal.style.display = 'flex';
        });
    }
    if (btnImportProject) {
        btnImportProject.addEventListener('click', () => {
            if (welcomeModal) welcomeModal.style.display = 'none';
            // TODO: afficher import projet
            if (mainContent) mainContent.style.display = 'block';
        });
    }
    // Gestion Annuler formulaire projet
    const cancelProjectForm = document.getElementById('cancel-project-form');
    if (cancelProjectForm) {
        cancelProjectForm.addEventListener('click', () => {
            if (projectFormModal) projectFormModal.style.display = 'none';
            if (welcomeModal) welcomeModal.style.display = 'flex';
        });
    }
    // Validation formulaire projet
    const projectForm = document.getElementById('project-form');
    if (projectForm) {
        projectForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Récupérer les données
            const data = {
                name: document.getElementById('project-name').value,
                code: document.getElementById('project-code').value,
                leader: document.getElementById('project-leader').value,
                engineer: document.getElementById('project-engineer').value,
                technician: document.getElementById('project-technician').value,
                date: document.getElementById('project-date').value,
                type: document.getElementById('project-type').value
            };
            // Sauvegarder (localStorage pour démo)
            localStorage.setItem('chneowave_project', JSON.stringify(data));
            if (projectFormModal) projectFormModal.style.display = 'none';
            // Afficher dashboard
            const dashboardModal = document.getElementById('dashboard-modal');
            const dashboardProjectInfo = document.getElementById('dashboard-project-info');
            if (dashboardModal) {
                dashboardModal.style.display = 'flex';
                if (dashboardProjectInfo) {
                    dashboardProjectInfo.innerHTML = `
                        <div><strong>Nom du Projet :</strong> ${data.name}</div>
                        <div><strong>Code Projet :</strong> ${data.code}</div>
                        <div><strong>Chef de Projet :</strong> ${data.leader}</div>
                        <div><strong>Ingénieur :</strong> ${data.engineer}</div>
                        <div><strong>Technicien :</strong> ${data.technician}</div>
                        <div><strong>Date :</strong> ${data.date}</div>
                        <div><strong>Type :</strong> ${data.type === 'bassin' ? 'Bassin à Houle' : 'Canal à Houle'}</div>
                    `;
                }
            }
            // Masquer mainContent si visible
            if (mainContent) mainContent.style.display = 'none';
        });
    }
    // TODO: afficher dashboard après import projet
    // Navigation vers modules (handlers vides)
    const btnGoCalibration = document.getElementById('btn-go-calibration');
    const btnGoAcquisition = document.getElementById('btn-go-acquisition');
    const btnGoProcessing = document.getElementById('btn-go-processing');
    if (btnGoCalibration) btnGoCalibration.addEventListener('click', () => {
        // TODO: afficher module calibration
    });
    if (btnGoAcquisition) btnGoAcquisition.addEventListener('click', () => {
        // TODO: afficher module acquisition
    });
    if (btnGoProcessing) btnGoProcessing.addEventListener('click', () => {
        // TODO: afficher module traitement
    });

    const calibrationModal = document.getElementById('calibration-modal');
    const btnBackDashboard = document.getElementById('btn-back-dashboard');
    const btnSaveCalibration = document.getElementById('btn-save-calibration');
    const calibSensorCount = document.getElementById('calib-sensor-count');
    const calibPointCount = document.getElementById('calib-point-count');
    const calibActiveSensor = document.getElementById('calib-active-sensor');
    const calibrationTableBody = document.getElementById('calibration-tbody');
    const calibrationCanvas = document.getElementById('calibration-canvas');
    let calibrationData = {};
    // Afficher calibration après dashboard
    if (btnGoCalibration) btnGoCalibration.addEventListener('click', () => {
        document.getElementById('dashboard-modal').style.display = 'none';
        if (calibrationModal) calibrationModal.style.display = 'flex';
        // Initialiser sélecteurs
        initCalibrationSelectors();
        updateCalibrationTable();
        updateCalibrationChart();
    });
    // Retour dashboard
    if (btnBackDashboard) btnBackDashboard.addEventListener('click', () => {
        if (calibrationModal) calibrationModal.style.display = 'none';
        document.getElementById('dashboard-modal').style.display = 'flex';
    });
    // Initialisation des sélecteurs calibration
    function initCalibrationSelectors() {
        // Nombre de sondes
        calibSensorCount.innerHTML = '';
        for (let i = 1; i <= 16; i++) {
            const opt = document.createElement('option');
            opt.value = i; opt.textContent = i;
            calibSensorCount.appendChild(opt);
        }
        calibSensorCount.value = 4;
        // Nombre de points
        calibPointCount.innerHTML = '';
        for (let i = 3; i <= 20; i++) {
            const opt = document.createElement('option');
            opt.value = i; opt.textContent = i;
            calibPointCount.appendChild(opt);
        }
        calibPointCount.value = 5;
        // Sondes actives
        updateActiveSensorOptions();
        calibActiveSensor.value = 1;
    }
    function updateActiveSensorOptions() {
        const n = parseInt(calibSensorCount.value);
        calibActiveSensor.innerHTML = '';
        for (let i = 1; i <= n; i++) {
            const opt = document.createElement('option');
            opt.value = i; opt.textContent = 'Sonde ' + i;
            calibActiveSensor.appendChild(opt);
        }
    }
    // Générer le tableau calibration
    function updateCalibrationTable() {
        const points = parseInt(calibPointCount.value);
        const sensor = calibActiveSensor.value;
        if (!calibrationData[sensor]) calibrationData[sensor] = Array(points).fill({height: '', voltage: ''});
        calibrationTableBody.innerHTML = '';
        for (let i = 0; i < points; i++) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${i + 1}</td>
                <td><input type="number" class="height-input" value="${calibrationData[sensor][i]?.height || ''}" step="0.1"></td>
                <td><input type="number" class="voltage-input" value="${calibrationData[sensor][i]?.voltage || ''}" step="0.001"></td>
                <td><span class="status-pending">En attente</span></td>
            `;
            calibrationTableBody.appendChild(row);
        }
        // Event listeners
        calibrationTableBody.querySelectorAll('.height-input, .voltage-input').forEach((input, idx) => {
            input.addEventListener('input', () => {
                const rows = calibrationTableBody.querySelectorAll('tr');
                calibrationData[sensor] = Array.from(rows).map(row => ({
                    height: row.querySelector('.height-input').value,
                    voltage: row.querySelector('.voltage-input').value
                }));
                updateCalibrationChart();
            });
        });
    }
    // Changement sélecteurs
    if (calibSensorCount) calibSensorCount.addEventListener('change', () => {
        updateActiveSensorOptions();
        updateCalibrationTable();
        updateCalibrationChart();
    });
    if (calibPointCount) calibPointCount.addEventListener('change', () => {
        updateCalibrationTable();
        updateCalibrationChart();
    });
    if (calibActiveSensor) calibActiveSensor.addEventListener('change', () => {
        updateCalibrationTable();
        updateCalibrationChart();
    });
    // Graphe de linéarité
    function updateCalibrationChart() {
        if (!calibrationCanvas) return;
        const ctx = calibrationCanvas.getContext('2d');
        ctx.clearRect(0, 0, calibrationCanvas.width, calibrationCanvas.height);
        // Grille
        ctx.strokeStyle = '#374151';
        ctx.lineWidth = 1;
        ctx.globalAlpha = 0.3;
        for (let i = 0; i <= 10; i++) {
            const x = (i / 10) * calibrationCanvas.width;
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, calibrationCanvas.height); ctx.stroke();
        }
        for (let i = 0; i <= 10; i++) {
            const y = (i / 10) * calibrationCanvas.height;
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(calibrationCanvas.width, y); ctx.stroke();
        }
        ctx.globalAlpha = 1;
        // Points calibration
        const sensor = calibActiveSensor.value;
        const data = (calibrationData[sensor] || []).filter(pt => pt.height && pt.voltage);
        if (data.length > 0) {
            ctx.fillStyle = '#3b82f6';
            data.forEach(pt => {
                const x = (parseFloat(pt.voltage) / 10) * calibrationCanvas.width;
                const y = calibrationCanvas.height - (parseFloat(pt.height) / 50) * calibrationCanvas.height;
                ctx.beginPath(); ctx.arc(x, y, 4, 0, 2 * Math.PI); ctx.fill();
            });
            // Régression linéaire
            if (data.length >= 2) {
                const regression = calculateLinearRegression(data);
                ctx.strokeStyle = '#06b6d4';
                ctx.lineWidth = 2;
                ctx.beginPath();
                const x1 = 0;
                const y1 = calibrationCanvas.height - (regression.slope * 0 + regression.intercept) / 50 * calibrationCanvas.height;
                const x2 = calibrationCanvas.width;
                const y2 = calibrationCanvas.height - (regression.slope * 10 + regression.intercept) / 50 * calibrationCanvas.height;
                ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
                // Stats
                document.getElementById('r-squared').textContent = regression.rSquared.toFixed(4);
                document.getElementById('slope').textContent = regression.slope.toFixed(2) + ' cm/V';
                document.getElementById('offset').textContent = regression.intercept.toFixed(2) + ' cm';
            } else {
                document.getElementById('r-squared').textContent = '--';
                document.getElementById('slope').textContent = '--';
                document.getElementById('offset').textContent = '--';
            }
        } else {
            document.getElementById('r-squared').textContent = '--';
            document.getElementById('slope').textContent = '--';
            document.getElementById('offset').textContent = '--';
        }
    }
    function calculateLinearRegression(data) {
        const n = data.length;
        const sumX = data.reduce((sum, pt) => sum + parseFloat(pt.voltage), 0);
        const sumY = data.reduce((sum, pt) => sum + parseFloat(pt.height), 0);
        const sumXY = data.reduce((sum, pt) => sum + parseFloat(pt.voltage) * parseFloat(pt.height), 0);
        const sumX2 = data.reduce((sum, pt) => sum + Math.pow(parseFloat(pt.voltage), 2), 0);
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        const meanY = sumY / n;
        const ssRes = data.reduce((sum, pt) => {
            const predicted = slope * parseFloat(pt.voltage) + intercept;
            return sum + Math.pow(parseFloat(pt.height) - predicted, 2);
        }, 0);
        const ssTot = data.reduce((sum, pt) => sum + Math.pow(parseFloat(pt.height) - meanY, 2), 0);
        const rSquared = 1 - (ssRes / ssTot);
        return { slope, intercept, rSquared };
    }
    // Sauvegarder calibration
    if (btnSaveCalibration) btnSaveCalibration.addEventListener('click', () => {
        // Pour démo, sauvegarde dans localStorage
        localStorage.setItem('chneowave_calibration', JSON.stringify(calibrationData));
        alert('Calibration sauvegardée avec succès.');
    });

    const acquisitionModal = document.getElementById('acquisition-modal');
    const btnGoAcquisition = document.getElementById('btn-go-acquisition');
    const btnBackDashboardAcq = document.getElementById('btn-back-dashboard-acq');
    const btnStartAcquisition = document.getElementById('btn-start-acquisition');
    const btnStopAcquisition = document.getElementById('btn-stop-acquisition');
    const btnSaveAcquisition = document.getElementById('btn-save-acquisition');
    const acqSensorA = document.getElementById('acq-sensor-a');
    const acqSensorB = document.getElementById('acq-sensor-b');
    const acqMultiSensors = document.getElementById('acq-multi-sensors');
    const acqSensorAChart = document.getElementById('acq-sensor-a-chart');
    const acqSensorBChart = document.getElementById('acq-sensor-b-chart');
    const acqMultiSensorChart = document.getElementById('acq-multi-sensor-chart');
    let acqData = {};
    let acqInterval = null;
    // Afficher acquisition après dashboard
    if (btnGoAcquisition) btnGoAcquisition.addEventListener('click', () => {
        document.getElementById('dashboard-modal').style.display = 'none';
        if (acquisitionModal) acquisitionModal.style.display = 'flex';
        initAcquisitionSelectors();
        resetAcquisitionCharts();
        btnStartAcquisition.disabled = false;
        btnStopAcquisition.disabled = true;
        btnSaveAcquisition.disabled = true;
    });
    // Retour dashboard
    if (btnBackDashboardAcq) btnBackDashboardAcq.addEventListener('click', () => {
        if (acquisitionModal) acquisitionModal.style.display = 'none';
        document.getElementById('dashboard-modal').style.display = 'flex';
        stopAcquisition();
    });
    // Initialisation des sélecteurs acquisition
    function initAcquisitionSelectors() {
        // Nombre de sondes selon calibration
        let n = 4;
        try {
            const calib = JSON.parse(localStorage.getItem('chneowave_calibration'));
            n = Math.max(...Object.keys(calib || {}).map(Number) || [4]);
        } catch { n = 4; }
        acqSensorA.innerHTML = '';
        acqSensorB.innerHTML = '';
        acqMultiSensors.innerHTML = '';
        for (let i = 1; i <= n; i++) {
            const optA = document.createElement('option');
            optA.value = i; optA.textContent = 'Sonde ' + i;
            acqSensorA.appendChild(optA);
            const optB = document.createElement('option');
            optB.value = i; optB.textContent = 'Sonde ' + i;
            acqSensorB.appendChild(optB);
            const optM = document.createElement('option');
            optM.value = i; optM.textContent = 'Sonde ' + i;
            acqMultiSensors.appendChild(optM);
        }
        acqSensorA.value = 1;
        acqSensorB.value = 2;
        acqMultiSensors.options[0].selected = true;
        acqMultiSensors.options[1] && (acqMultiSensors.options[1].selected = true);
    }
    // Acquisition temps réel
    if (btnStartAcquisition) btnStartAcquisition.addEventListener('click', () => {
        btnStartAcquisition.disabled = true;
        btnStopAcquisition.disabled = false;
        btnSaveAcquisition.disabled = true;
        startAcquisition();
    });
    if (btnStopAcquisition) btnStopAcquisition.addEventListener('click', () => {
        btnStartAcquisition.disabled = false;
        btnStopAcquisition.disabled = true;
        btnSaveAcquisition.disabled = false;
        stopAcquisition();
    });
    if (btnSaveAcquisition) btnSaveAcquisition.addEventListener('click', () => {
        localStorage.setItem('chneowave_acquisition', JSON.stringify(acqData));
        alert('Données d’acquisition sauvegardées.');
    });
    function startAcquisition() {
        acqData = {};
        const sensors = Array.from(acqMultiSensors.selectedOptions).map(opt => opt.value);
        sensors.forEach(s => acqData[s] = []);
        acqInterval = setInterval(() => {
            const t = Date.now() / 1000;
            sensors.forEach(s => {
                if (!acqData[s]) acqData[s] = [];
                const amplitude = 15 + Math.random() * 10;
                const frequency = 0.5 + Math.random() * 0.5;
                const phase = Math.random() * Math.PI * 2;
                const value = amplitude * Math.sin(2 * Math.PI * frequency * t + phase) + (Math.random() - 0.5) * 2;
                acqData[s].push({ time: t, value });
                if (acqData[s].length > 1000) acqData[s].shift();
            });
            updateAcquisitionCharts();
        }, 100);
    }
    function stopAcquisition() {
        if (acqInterval) clearInterval(acqInterval);
        acqInterval = null;
    }
    function resetAcquisitionCharts() {
        [acqSensorAChart, acqSensorBChart, acqMultiSensorChart].forEach(canvas => {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        });
    }
    function updateAcquisitionCharts() {
        // Sonde A
        drawSensorChart(acqSensorAChart, acqData[acqSensorA.value] || []);
        // Sonde B
        drawSensorChart(acqSensorBChart, acqData[acqSensorB.value] || []);
        // Multi-sondes
        const sensors = Array.from(acqMultiSensors.selectedOptions).map(opt => opt.value);
        drawMultiSensorChart(acqMultiSensorChart, sensors.map(s => acqData[s] || []));
    }
    function drawSensorChart(canvas, data) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2;
        ctx.beginPath();
        data.slice(-100).forEach((pt, idx, arr) => {
            const x = (idx / (arr.length - 1 || 1)) * canvas.width;
            const y = canvas.height / 2 - (pt.value / 50) * canvas.height / 2;
            if (idx === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        });
        ctx.stroke();
    }
    function drawMultiSensorChart(canvas, sensorsData) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const colors = ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#a21caf', '#0ea5e9', '#eab308'];
        sensorsData.forEach((data, idx) => {
            ctx.strokeStyle = colors[idx % colors.length];
            ctx.lineWidth = 2;
            ctx.beginPath();
            data.slice(-100).forEach((pt, i, arr) => {
                const x = (i / (arr.length - 1 || 1)) * canvas.width;
                const y = canvas.height / 2 - (pt.value / 50) * canvas.height / 2;
                if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            });
            ctx.stroke();
        });
    }

    const processingModal = document.getElementById('processing-modal');
    const btnGoProcessing = document.getElementById('btn-go-processing');
    const btnBackDashboardProc = document.getElementById('btn-back-dashboard-proc');
    const btnGenerateReport = document.getElementById('btn-generate-report');
    const procMethod = document.getElementById('proc-method');
    const procSpectrumChart = document.getElementById('proc-spectrum-chart');
    // Afficher processing après dashboard
    if (btnGoProcessing) btnGoProcessing.addEventListener('click', () => {
        document.getElementById('dashboard-modal').style.display = 'none';
        if (processingModal) processingModal.style.display = 'flex';
        updateProcessingResults();
        updateProcessingSpectrum();
    });
    // Retour dashboard
    if (btnBackDashboardProc) btnBackDashboardProc.addEventListener('click', () => {
        if (processingModal) processingModal.style.display = 'none';
        document.getElementById('dashboard-modal').style.display = 'flex';
    });
    // Changement méthode
    if (procMethod) procMethod.addEventListener('change', () => {
        updateProcessingResults();
        updateProcessingSpectrum();
    });
    function updateProcessingResults() {
        // Simuler résultats selon méthode
        const method = procMethod.value;
        const stats = {
            fft:   { hs: 15.2, hmax: 18.1, hmin: 12.3, h13: 14.9, tm: 2.8, tp: 3.4 },
            jonswap: { hs: 14.8, hmax: 17.5, hmin: 11.9, h13: 14.5, tm: 2.6, tp: 3.2 },
            pierson: { hs: 15.5, hmax: 19.0, hmin: 13.0, h13: 15.1, tm: 3.0, tp: 3.6 },
            goda: { hs: 14.9, hmax: 17.8, hmin: 12.1, h13: 14.7, tm: 2.7, tp: 3.3 }
        }[method] || stats.fft;
        document.getElementById('proc-hs').textContent = stats.hs;
        document.getElementById('proc-hmax').textContent = stats.hmax;
        document.getElementById('proc-hmin').textContent = stats.hmin;
        document.getElementById('proc-h13').textContent = stats.h13;
        document.getElementById('proc-tm').textContent = stats.tm;
        document.getElementById('proc-tp').textContent = stats.tp;
    }
    function updateProcessingSpectrum() {
        if (!procSpectrumChart) return;
        const ctx = procSpectrumChart.getContext('2d');
        ctx.clearRect(0, 0, procSpectrumChart.width, procSpectrumChart.height);
        // Grille
        ctx.strokeStyle = '#374151';
        ctx.lineWidth = 1;
        ctx.globalAlpha = 0.3;
        for (let i = 0; i <= 10; i++) {
            const x = (i / 10) * procSpectrumChart.width;
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, procSpectrumChart.height); ctx.stroke();
        }
        for (let i = 0; i <= 10; i++) {
            const y = (i / 10) * procSpectrumChart.height;
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(procSpectrumChart.width, y); ctx.stroke();
        }
        ctx.globalAlpha = 1;
        // Simuler spectre selon méthode
        const method = procMethod.value;
        const frequencies = [];
        const powers = [];
        for (let i = 0; i < 100; i++) {
            const freq = i * 0.1;
            frequencies.push(freq);
            let power = 0;
            switch(method) {
                case 'fft': power = Math.exp(-Math.pow(freq - 2, 2) / 2) * 10; break;
                case 'jonswap': power = Math.exp(-1.25 * Math.pow(freq / 2, -4)) * Math.pow(freq / 2, -5) * 8; break;
                case 'pierson': power = Math.exp(-0.74 * Math.pow(freq / 2, -4)) * Math.pow(freq / 2, -5) * 12; break;
                case 'goda': power = Math.exp(-Math.pow(freq - 1.5, 2) / 1.5) * 9; break;
            }
            powers.push(power);
        }
        ctx.strokeStyle = '#06b6d4';
        ctx.lineWidth = 2;
        ctx.beginPath();
        frequencies.forEach((freq, idx) => {
            const x = (freq / 10) * procSpectrumChart.width;
            const y = procSpectrumChart.height - (powers[idx] / 15) * procSpectrumChart.height;
            if (idx === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        });
        ctx.stroke();
    }
    if (btnGenerateReport) btnGenerateReport.addEventListener('click', () => {
        alert('Rapport généré avec succès. (Simulation)');
    });
});

// Handle window resize for responsive charts
window.addEventListener('resize', () => {
    const app = window.chneowave;
    if (app) {
        app.setupCharts();
    }
});

// Add notification styles to CSS
const notificationStyles = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: var(--space-3) var(--space-4);
    color: var(--text-primary);
    font-size: var(--text-sm);
    z-index: 10000;
    display: flex;
    align-items: center;
    gap: var(--space-2);
    box-shadow: var(--shadow-lg);
    transform: translateX(100%);
    transition: transform var(--transition-normal);
}

.notification-success {
    border-color: var(--success);
    background: var(--success);
    color: white;
}

.notification-warning {
    border-color: var(--warning);
    background: var(--warning);
    color: white;
}

.notification-error {
    border-color: var(--error);
    background: var(--error);
    color: white;
}

.notification-info {
    border-color: var(--info);
    background: var(--info);
    color: white;
}
`;

// Inject notification styles
const style = document.createElement('style');
style.textContent = notificationStyles;
document.head.appendChild(style);