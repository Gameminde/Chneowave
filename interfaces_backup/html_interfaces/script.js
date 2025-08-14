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
        document.getElementById(`${moduleName}-module`).classList.add('active');

        // Update header
        this.updateHeader(moduleName);
        
        this.currentModule = moduleName;
        
        // Initialize module-specific features
        this.initializeModule(moduleName);
    }

    updateHeader(moduleName) {
        const titles = {
            'dashboard': { title: 'Tableau de Bord Principal', subtitle: 'Système d\'acquisition et d\'analyse de houle maritime' },
            'project': { title: 'Gestion de Projet', subtitle: 'Créer ou importer un projet existant' },
            'calibration': { title: 'Calibration des Sondes', subtitle: 'Établir la relation linéaire tension/hauteur d\'eau' },
            'acquisition': { title: 'Acquisition Temps Réel', subtitle: 'Configuration et visualisation des données' },
            'analysis': { title: 'Analyse des Données', subtitle: 'Traitement du signal et calculs statistiques maritimes' },
            'export': { title: 'Export et Rapports', subtitle: 'Génération de rapports et export des données' },
            'system': { title: 'Configuration Système', subtitle: 'Paramètres et configuration du système' },
            'about': { title: 'À Propos de CHNeoWave', subtitle: 'Système d\'analyse maritime professionnel' }
        };

        const header = titles[moduleName] || titles['dashboard'];
        document.getElementById('page-title').textContent = header.title;
        document.getElementById('page-subtitle').textContent = header.subtitle;
    }

    initializeModule(moduleName) {
        switch(moduleName) {
            case 'calibration':
                this.initializeCalibration();
                break;
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
        // Sidebar slide behavior
        this.setupSidebarSlide();
        
        // Project management
        document.getElementById('new-project-btn')?.addEventListener('click', () => {
            this.showProjectForm();
        });

        document.getElementById('save-project')?.addEventListener('click', () => {
            this.saveProject();
        });

        document.getElementById('cancel-project')?.addEventListener('click', () => {
            this.hideProjectForm();
        });

        // Acquisition controls
        document.getElementById('start-acquisition')?.addEventListener('click', () => {
            this.startAcquisition();
        });

        document.getElementById('stop-acquisition')?.addEventListener('click', () => {
            this.stopAcquisition();
        });

        document.getElementById('save-acquisition')?.addEventListener('click', () => {
            this.saveAcquisition();
        });

        // Calibration
        document.getElementById('active-sensor')?.addEventListener('change', (e) => {
            this.switchCalibrationSensor(e.target.value);
        });

        document.getElementById('calibration-points')?.addEventListener('change', (e) => {
            this.updateCalibrationTable(e.target.value);
        });

        // Export
        document.getElementById('generate-report')?.addEventListener('click', () => {
            this.generateReport();
        });

        document.getElementById('export-data')?.addEventListener('click', () => {
            this.exportData();
        });

        // Theme toggle
        document.querySelector('.theme-toggle')?.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Sensor selection for charts
        document.getElementById('sensor-a-select')?.addEventListener('change', (e) => {
            this.updateSensorChart('sensor-a-chart', e.target.value);
        });

        document.getElementById('sensor-b-select')?.addEventListener('change', (e) => {
            this.updateSensorChart('sensor-b-chart', e.target.value);
        });

        // Analysis method buttons
        document.querySelectorAll('.method-btn')?.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchAnalysisMethod(e.target.getAttribute('data-method'));
            });
        });
    }

    showProjectForm() {
        document.getElementById('project-form').style.display = 'block';
        document.querySelector('.project-actions').style.display = 'none';
    }

    hideProjectForm() {
        document.getElementById('project-form').style.display = 'none';
        document.querySelector('.project-actions').style.display = 'flex';
    }

    saveProject() {
        const projectData = {
            name: document.getElementById('project-name').value,
            code: document.getElementById('project-code').value,
            leader: document.getElementById('project-leader').value,
            engineer: document.getElementById('project-engineer').value,
            location: document.getElementById('test-location').value,
            date: document.getElementById('test-date').value,
            sensors: parseInt(document.getElementById('sensor-count').value),
            frequency: parseInt(document.getElementById('sampling-freq').value),
            createdAt: new Date().toISOString()
        };

        if (!projectData.name || !projectData.code) {
            this.showNotification('Veuillez remplir les champs obligatoires', 'warning');
            return;
        }

        this.currentProject = projectData;
        this.updateProjectInfo();
        this.hideProjectForm();
        this.switchModule('dashboard');
        
        // Update project stats
        document.getElementById('active-projects').textContent = '1';
        
        this.showNotification('Projet créé avec succès', 'success');
        console.log('Projet créé:', projectData);
    }

    updateProjectInfo() {
        if (this.currentProject) {
            document.querySelector('.project-name').textContent = this.currentProject.name;
            
            // Afficher les détails du projet dans le dashboard
            this.displayProjectDetails();
        } else {
            document.querySelector('.project-name').textContent = 'Aucun projet actif';
            document.getElementById('project-info-section').style.display = 'none';
        }
    }

    displayProjectDetails() {
        const projectInfoSection = document.getElementById('project-info-section');
        if (!this.currentProject) return;

        // Mettre à jour tous les champs d'affichage
        document.getElementById('project-name-display').textContent = this.currentProject.name;
        document.getElementById('project-code-display').textContent = this.currentProject.code;
        document.getElementById('project-leader-display').textContent = this.currentProject.leader;
        document.getElementById('project-engineer-display').textContent = this.currentProject.engineer;
        document.getElementById('project-location-display').textContent = this.currentProject.location;
        document.getElementById('project-date-display').textContent = this.currentProject.date;
        document.getElementById('project-sensors-display').textContent = this.currentProject.sensors + ' sondes';
        document.getElementById('project-freq-display').textContent = this.currentProject.frequency + ' Hz';

        // Afficher la section
        projectInfoSection.style.display = 'block';
    }

    startAcquisition() {
        if (!this.currentProject) {
            this.showNotification('Veuillez créer un projet avant de démarrer l\'acquisition', 'warning');
            return;
        }

        this.isAcquiring = true;
        document.getElementById('start-acquisition').disabled = true;
        document.getElementById('stop-acquisition').disabled = false;
        document.getElementById('save-acquisition').disabled = true;

        // Start data simulation
        this.startDataSimulation();
        
        this.showNotification('Acquisition démarrée', 'success');
        console.log('Acquisition démarrée');
    }

    stopAcquisition() {
        this.isAcquiring = false;
        document.getElementById('start-acquisition').disabled = false;
        document.getElementById('stop-acquisition').disabled = true;
        document.getElementById('save-acquisition').disabled = false;

        // Stop data simulation
        this.stopDataSimulation();
        
        this.showNotification('Acquisition arrêtée', 'info');
        console.log('Acquisition arrêtée');
    }

    saveAcquisition() {
        if (this.sensorData && Object.keys(this.sensorData).length > 0) {
            // Simulate saving data
            const saveButton = document.getElementById('save-acquisition');
            const originalText = saveButton.innerHTML;
            saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sauvegarde...';
            saveButton.disabled = true;

            setTimeout(() => {
                saveButton.innerHTML = '<i class="fas fa-check"></i> Sauvegardé';
                this.showNotification('Données sauvegardées avec succès', 'success');
                
                setTimeout(() => {
                    saveButton.innerHTML = originalText;
                    saveButton.disabled = false;
                    this.switchModule('analysis');
                }, 1000);
            }, 2000);

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
        const sensor1Data = this.sensorData['1'].map(d => d.value);
        if (sensor1Data.length === 0) return;

        const values = sensor1Data.slice(-100); // Last 100 points
        const max = Math.max(...values);
        const min = Math.min(...values);
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        
        // Calculate Hs (Significant Wave Height)
        const sortedValues = [...values].sort((a, b) => b - a);
        const hs = sortedValues.slice(0, Math.floor(values.length / 3))
                              .reduce((a, b) => a + b, 0) / Math.floor(values.length / 3);

        // Update display
        document.getElementById('hs-value').textContent = hs.toFixed(1);
        document.getElementById('hmax-value').textContent = max.toFixed(1);
        document.getElementById('hmin-value').textContent = min.toFixed(1);
        document.getElementById('h13-value').textContent = hs.toFixed(1);
        document.getElementById('tm-value').textContent = (2.5 + Math.random() * 1).toFixed(1);
        document.getElementById('tp-value').textContent = (3.0 + Math.random() * 1.5).toFixed(1);
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
            const x = (index / data.length) * canvas.width;
            const y = canvas.height / 2 + (point.value / 50) * canvas.height / 2;
            
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
            ctx.lineWidth = 1.5;
            ctx.beginPath();

            data.forEach((point, pointIndex) => {
                const x = (pointIndex / data.length) * canvas.width;
                const y = canvas.height / 2 + (point.value / 50) * canvas.height / 2;
                
                if (pointIndex === 0) {
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
                this.chartContexts[id] = canvas.getContext('2d');
            }
        });
    }

    initializeCalibration() {
        const activeSensor = document.getElementById('active-sensor');
        const calibrationPoints = document.getElementById('calibration-points');
        const totalSensors = document.getElementById('total-sensors-to-calibrate');
        
        if (activeSensor) {
            activeSensor.addEventListener('change', () => {
                this.switchCalibrationSensor(activeSensor.value);
                document.getElementById('current-sensor-number').textContent = activeSensor.value;
            });
        }
        
        if (calibrationPoints) {
            calibrationPoints.addEventListener('input', () => {
                const points = parseInt(calibrationPoints.value) || 3;
                this.updateCalibrationTable(points);
            });
        }

        if (totalSensors) {
            totalSensors.addEventListener('input', () => {
                const sensors = parseInt(totalSensors.value) || 1;
                this.updateSensorOptions(sensors);
            });
        }
        
        // Initialize buttons
        this.initializeCalibrationButtons();
        
        // Initialize with default values
        this.updateCalibrationTable(5);
        this.updateSensorOptions(1);
    }

    updateSensorOptions(totalSensors) {
        const activeSensorSelect = document.getElementById('active-sensor');
        activeSensorSelect.innerHTML = '';
        
        for (let i = 1; i <= totalSensors; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `Sonde ${i}`;
            activeSensorSelect.appendChild(option);
        }
        
        // Update current sensor number display
        document.getElementById('current-sensor-number').textContent = '1';
    }

    initializeCalibrationButtons() {
        // Reset button
        document.getElementById('reset-calibration').addEventListener('click', () => {
            this.resetCalibration();
        });

        // Validate button
        document.getElementById('validate-calibration').addEventListener('click', () => {
            this.validateCalibration();
        });

        // Save button
        document.getElementById('save-calibration').addEventListener('click', () => {
            this.saveCalibration();
        });
    }

    resetCalibration() {
        const tbody = document.getElementById('calibration-tbody');
        tbody.querySelectorAll('input').forEach(input => {
            input.value = '';
        });
        
        tbody.querySelectorAll('.status-pending, .status-calculated, .status-validated').forEach(status => {
            status.textContent = 'En attente';
            status.className = 'status-pending';
            status.style.color = 'var(--warning)';
        });

        this.updateCalibrationChart();
        this.showNotification('Calibration réinitialisée', 'info');
    }

    validateCalibration() {
        const tbody = document.getElementById('calibration-tbody');
        const rows = tbody.querySelectorAll('tr');
        let validPoints = 0;
        let totalPoints = rows.length;

        // Vérifier que tous les points ont été calculés
        rows.forEach((row, index) => {
            const heightInput = row.querySelector('.height-input');
            const voltageInput = row.querySelector('.voltage-input');
            
            if (heightInput.value && voltageInput.value) {
                validPoints++;
                this.updateRowStatus(index, 'validated');
            }
        });

        if (validPoints === totalPoints) {
            // Calculer la linéarité
            const linearityResult = this.calculateLinearity();
            
            // Mettre à jour le graphique avec les données de linéarité
            this.updateCalibrationChart();
            
            // Mettre à jour les statistiques affichées
            document.getElementById('r-squared').textContent = linearityResult.r2.toFixed(4);
            document.getElementById('slope').textContent = linearityResult.slope.toFixed(4);
            document.getElementById('offset').textContent = linearityResult.intercept.toFixed(4);
            
            if (linearityResult.r2 > 0.99) {
                this.showNotification(`Calibration validée ! R² = ${linearityResult.r2.toFixed(4)} - Excellente linéarité`, 'success');
            } else if (linearityResult.r2 > 0.95) {
                this.showNotification(`Calibration acceptée. R² = ${linearityResult.r2.toFixed(4)} - Bonne linéarité`, 'warning');
            } else {
                this.showNotification(`Calibration rejetée. R² = ${linearityResult.r2.toFixed(4)} - Linéarité insuffisante`, 'error');
            }
        } else {
            this.showNotification(`Calibration incomplète. ${validPoints}/${totalPoints} points calculés`, 'warning');
        }
    }

    calculateLinearity() {
        const tbody = document.getElementById('calibration-tbody');
        const data = [];
        
        tbody.querySelectorAll('tr').forEach(row => {
            const heightInput = row.querySelector('.height-input');
            const voltageInput = row.querySelector('.voltage-input');
            
            if (heightInput.value && voltageInput.value) {
                data.push({
                    x: parseFloat(heightInput.value),
                    y: parseFloat(voltageInput.value)
                });
            }
        });

        if (data.length < 2) {
            return { r2: 0, slope: 0, intercept: 0 };
        }

        return this.calculateLinearRegression(data);
    }

    saveCalibration() {
        const activeSensor = document.getElementById('active-sensor').value;
        const calibrationData = this.collectCalibrationData();
        
        if (calibrationData.length === 0) {
            this.showNotification('Aucune donnée de calibration à sauvegarder', 'warning');
            return;
        }

        // Simuler la sauvegarde
        const calibrationRecord = {
            sensorId: activeSensor,
            timestamp: new Date().toISOString(),
            points: calibrationData,
            linearity: this.calculateLinearity()
        };

        // Stocker dans le localStorage pour la démonstration
        const savedCalibrations = JSON.parse(localStorage.getItem('chneowave_calibrations') || '[]');
        savedCalibrations.push(calibrationRecord);
        localStorage.setItem('chneowave_calibrations', JSON.stringify(savedCalibrations));

        this.showNotification(`Calibration de la sonde ${activeSensor} sauvegardée avec succès`, 'success');
    }

    collectCalibrationData() {
        const tbody = document.getElementById('calibration-tbody');
        const data = [];
        
        tbody.querySelectorAll('tr').forEach(row => {
            const heightInput = row.querySelector('.height-input');
            const voltageInput = row.querySelector('.voltage-input');
            
            if (heightInput.value && voltageInput.value) {
                data.push({
                    height: parseFloat(heightInput.value),
                    voltage: parseFloat(voltageInput.value)
                });
            }
        });

        return data;
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
                <td><input type="number" class="height-input" placeholder="cm" step="0.1" min="0" max="100"></td>
                <td><input type="number" class="voltage-input" placeholder="V" step="0.001" min="0" max="10" readonly></td>
                <td>↑↓</td>
                <td><span class="status-pending">En attente</span></td>
                <td>
                    <button class="btn btn-sm btn-primary calculate-btn" data-row="${i}">
                        <i class="fas fa-calculator"></i>
                        Calculer
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        }

        // Add event listeners to inputs
        tbody.querySelectorAll('.height-input').forEach((input, index) => {
            input.addEventListener('input', () => {
                this.updateCalibrationChart();
                this.updateRowStatus(index, 'pending');
            });
        });

        // Add event listeners to calculate buttons
        tbody.querySelectorAll('.calculate-btn').forEach((btn, index) => {
            btn.addEventListener('click', () => {
                this.calculateVoltageForRow(index);
            });
        });
    }

    calculateVoltageForRow(rowIndex) {
        const tbody = document.getElementById('calibration-tbody');
        const row = tbody.children[rowIndex];
        const heightInput = row.querySelector('.height-input');
        const voltageInput = row.querySelector('.voltage-input');
        const statusSpan = row.querySelector('.status-pending');

        if (!heightInput.value) {
            this.showNotification('Veuillez saisir une hauteur', 'warning');
            return;
        }

        const height = parseFloat(heightInput.value);
        
        // Simulation d'un calcul de tension basé sur la hauteur
        // En réalité, ce serait basé sur les caractéristiques du capteur
        const voltage = this.simulateVoltageCalculation(height);
        
        voltageInput.value = voltage.toFixed(3);
        statusSpan.textContent = 'Calculé';
        statusSpan.className = 'status-calculated';
        statusSpan.style.color = 'var(--success)';

        this.updateCalibrationChart();
        this.showNotification(`Tension calculée: ${voltage.toFixed(3)}V pour ${height}cm`, 'success');
    }

    simulateVoltageCalculation(height) {
        // Simulation d'un capteur avec une relation linéaire
        // Pente: ~0.05 V/cm, Offset: ~0.5V
        const slope = 0.05;
        const offset = 0.5;
        const noise = (Math.random() - 0.5) * 0.01; // Bruit de ±0.005V
        
        return offset + slope * height + noise;
    }

    updateRowStatus(rowIndex, status) {
        const tbody = document.getElementById('calibration-tbody');
        const row = tbody.children[rowIndex];
        const statusSpan = row.querySelector('.status-pending, .status-calculated, .status-validated');
        
        if (status === 'pending') {
            statusSpan.textContent = 'En attente';
            statusSpan.className = 'status-pending';
            statusSpan.style.color = 'var(--warning)';
        } else if (status === 'calculated') {
            statusSpan.textContent = 'Calculé';
            statusSpan.className = 'status-calculated';
            statusSpan.style.color = 'var(--success)';
        } else if (status === 'validated') {
            statusSpan.textContent = 'Validé';
            statusSpan.className = 'status-validated';
            statusSpan.style.color = 'var(--success)';
        }
    }

    updateCalibrationChart(sensorId = null) {
        const canvas = document.getElementById('calibration-chart');
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
            
            if (heightInput.value && voltageInput.value) {
                data.push({
                    height: parseFloat(heightInput.value),
                    voltage: parseFloat(voltageInput.value)
                });
            }
        });

        if (data.length > 0) {
            // Draw calibration points
            ctx.fillStyle = '#3b82f6';
            data.forEach(point => {
                const x = (point.voltage / 10) * canvas.width; // Assuming 0-10V range
                const y = canvas.height - (point.height / 50) * canvas.height; // Assuming 0-50cm range
                
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
                document.getElementById('r-squared').textContent = regression.r2.toFixed(4);
                document.getElementById('slope').textContent = regression.slope.toFixed(4);
                document.getElementById('offset').textContent = regression.intercept.toFixed(4);
            }
        }
    }

    calculateLinearRegression(data) {
        const n = data.length;
        const sumX = data.reduce((sum, point) => sum + point.voltage, 0);
        const sumY = data.reduce((sum, point) => sum + point.height, 0);
        const sumXY = data.reduce((sum, point) => sum + point.voltage * point.height, 0);
        const sumX2 = data.reduce((sum, point) => sum + point.voltage * point.voltage, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        // Calculate R-squared
        const meanY = sumY / n;
        const ssRes = data.reduce((sum, point) => {
            const predicted = slope * point.voltage + intercept;
            return sum + Math.pow(point.height - predicted, 2);
        }, 0);
        const ssTot = data.reduce((sum, point) => {
            return sum + Math.pow(point.height - meanY, 2);
        }, 0);
        const r2 = 1 - (ssRes / ssTot);

        return { slope, intercept, r2 };
    }

    switchAnalysisMethod(method) {
        // Update active method button
        document.querySelectorAll('.method-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-method="${method}"]`).classList.add('active');

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
            const values = [result.hs + ' cm', result.tp + ' s', result.tm + ' s', '0.85'];
            if (values[index]) {
                stat.textContent = values[index];
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
        const originalText = reportButton.innerHTML;
        reportButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Génération...';
        reportButton.disabled = true;

        setTimeout(() => {
            reportButton.innerHTML = '<i class="fas fa-check"></i> Rapport Généré';
            
            // Update preview
            const preview = document.getElementById('report-preview');
            preview.innerHTML = `
                <div class="report-content">
                    <h4>Rapport d'Analyse Maritime</h4>
                    <p><strong>Projet:</strong> ${this.currentProject?.name || 'N/A'}</p>
                    <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
                    <p><strong>Hauteur Significative (Hs):</strong> 15.2 cm</p>
                    <p><strong>Période de Pic (Tp):</strong> 3.4 s</p>
                    <p><strong>Période Moyenne (Tm):</strong> 2.8 s</p>
                    <p><strong>Conformité ITTC:</strong> Validée</p>
                </div>
            `;

            this.showNotification('Rapport généré avec succès', 'success');

            setTimeout(() => {
                reportButton.innerHTML = originalText;
                reportButton.disabled = false;
            }, 2000);
        }, 3000);
    }

    exportData() {
        const exportButton = document.getElementById('export-data');
        const originalText = exportButton.innerHTML;
        exportButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Export...';
        exportButton.disabled = true;

        setTimeout(() => {
            exportButton.innerHTML = '<i class="fas fa-check"></i> Exporté';
            this.showNotification('Données exportées avec succès', 'success');
            
            setTimeout(() => {
                exportButton.innerHTML = originalText;
                exportButton.disabled = false;
            }, 2000);
        }, 2000);
    }

    toggleTheme() {
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        body.setAttribute('data-theme', newTheme);
        
        const themeToggle = document.querySelector('.theme-toggle');
        if (newTheme === 'light') {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i><span>Mode Sombre</span>';
        } else {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i><span>Mode Clair</span>';
        }
    }

    updateMetrics() {
        // Simulate real-time system metrics
        setInterval(() => {
            const metricValues = document.querySelectorAll('.metric-value');
            if (metricValues.length >= 4) {
                metricValues[0].textContent = Math.floor(Math.random() * 100) + '%';
                metricValues[1].textContent = Math.floor(Math.random() * 80) + '%';
                metricValues[2].textContent = Math.floor(Math.random() * 50) + '%';
                metricValues[3].textContent = this.isAcquiring ? Math.floor(Math.random() * 4) + 1 : '0';
            }
        }, 3000);
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
                document.body.removeChild(notification);
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
        this.setupCharts();
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

    setupSidebarSlide() {
        const sidebar = document.querySelector('.sidebar');
        let slideTimeout;

        // Mouse enter - expand sidebar
        sidebar.addEventListener('mouseenter', () => {
            clearTimeout(slideTimeout);
            sidebar.classList.remove('collapsed');
        });

        // Mouse leave - collapse sidebar after delay
        sidebar.addEventListener('mouseleave', () => {
            slideTimeout = setTimeout(() => {
                sidebar.classList.add('collapsed');
            }, 500); // 500ms delay before collapsing
        });

        // Prevent collapse when clicking inside sidebar
        sidebar.addEventListener('click', (e) => {
            clearTimeout(slideTimeout);
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chneowave = new CHNeoWave();
});

// Handle window resize for responsive charts
window.addEventListener('resize', () => {
    if (window.chneowave) {
        window.chneowave.setupCharts();
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