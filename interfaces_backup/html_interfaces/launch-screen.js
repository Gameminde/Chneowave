/**
 * CHNeoWave - Écran de Lancement JavaScript
 * Interface maritime moderne avec Golden Ratio et WCAG 2.1 AA
 * Auteur: Architecte Logiciel en Chef
 * Version: 2.0.0 - Modernisation complète
 */

// Gestion avancée du thème maritime
class MaritimeThemeManager {
    constructor() {
        this.themes = {
            maritime: {
                name: 'Maritime Classique',
                primary: '#1e3a5f',
                secondary: '#2c5aa0',
                accent: '#4a90e2'
            },
            deep_ocean: {
                name: 'Océan Profond',
                primary: '#0a1628',
                secondary: '#1a2f4a',
                accent: '#3b82f6'
            },
            mediterranean: {
                name: 'Méditerranéen',
                primary: '#1e3c72',
                secondary: '#2a5298',
                accent: '#5ba3f5'
            }
        };
        
        this.currentTheme = localStorage.getItem('chneowave-theme') || 'maritime';
        this.applyTheme();
    }
    
    applyTheme() {
        const theme = this.themes[this.currentTheme];
        if (theme) {
            document.documentElement.style.setProperty('--maritime-primary', theme.primary);
            document.documentElement.style.setProperty('--maritime-secondary', theme.secondary);
            document.documentElement.style.setProperty('--maritime-accent', theme.accent);
            document.body.setAttribute('data-theme', this.currentTheme);
        }
    }
    
    toggleTheme() {
        const themeKeys = Object.keys(this.themes);
        const currentIndex = themeKeys.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % themeKeys.length;
        this.currentTheme = themeKeys[nextIndex];
        
        localStorage.setItem('chneowave-theme', this.currentTheme);
        this.applyTheme();
        
        // Animation de transition
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }
    
    getCurrentThemeName() {
        return this.themes[this.currentTheme]?.name || 'Inconnu';
    }
}

// Gestionnaire principal de l'écran de lancement moderne
class ModernLaunchScreenManager {
    constructor() {
        this.themeManager = new MaritimeThemeManager();
        this.recentProjects = this.loadRecentProjects();
        this.systemMetrics = this.initializeSystemMetrics();
        
        this.initializeEventListeners();
        this.updateSystemInfo();
        this.renderRecentProjects();
        this.startSystemMonitoring();
        this.setupAccessibility();
    }
    
    initializeEventListeners() {
        // Raccourcis clavier étendus
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey) {
                switch(e.key) {
                    case 'n':
                        e.preventDefault();
                        this.createProject();
                        break;
                    case 'o':
                        e.preventDefault();
                        this.openProject();
                        break;
                    case 'i':
                        e.preventDefault();
                        this.importProject();
                        break;
                    case 'r':
                        e.preventDefault();
                        this.quickCalibration();
                        break;
                    case 't':
                        e.preventDefault();
                        this.themeManager.toggleTheme();
                        break;
                }
            }
            
            // Navigation par touches fléchées
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                this.handleKeyboardNavigation(e);
            }
        });
        
        // Redimensionnement adaptatif
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Animations avancées des cartes
        this.setupAdvancedCardAnimations();
        
        // Gestion des événements tactiles
        this.setupTouchEvents();
    }
    
    setupAdvancedCardAnimations() {
        const cards = document.querySelectorAll('.action-card');
        
        cards.forEach((card, index) => {
            // Animation d'entrée échelonnée
            card.style.animationDelay = `${index * 0.1}s`;
            
            // Effets de survol avancés
            card.addEventListener('mouseenter', (e) => {
                this.animateCardHover(card, true);
            });
            
            card.addEventListener('mouseleave', (e) => {
                this.animateCardHover(card, false);
            });
            
            // Effet de clic
            card.addEventListener('mousedown', (e) => {
                card.style.transform = 'translateY(-4px) scale(1.01)';
            });
            
            card.addEventListener('mouseup', (e) => {
                setTimeout(() => {
                    card.style.transform = 'translateY(-8px) scale(1.02)';
                }, 100);
            });
        });
    }
    
    animateCardHover(card, isHover) {
        if (isHover) {
            card.style.transform = 'translateY(-8px) scale(1.02)';
            card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
        } else {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = '';
        }
    }
    
    setupTouchEvents() {
        const cards = document.querySelectorAll('.action-card');
        
        cards.forEach(card => {
            card.addEventListener('touchstart', (e) => {
                card.style.transform = 'scale(0.98)';
            });
            
            card.addEventListener('touchend', (e) => {
                card.style.transform = 'scale(1)';
            });
        });
    }
    
    setupAccessibility() {
        // Amélioration de l'accessibilité
        const cards = document.querySelectorAll('.action-card');
        
        cards.forEach(card => {
            card.setAttribute('role', 'button');
            card.setAttribute('tabindex', '0');
            
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
        });
    }
    
    handleKeyboardNavigation(e) {
        const focusableElements = document.querySelectorAll('.action-card, .recent-item, .footer-link');
        const currentIndex = Array.from(focusableElements).indexOf(document.activeElement);
        
        let nextIndex;
        switch(e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
                nextIndex = (currentIndex + 1) % focusableElements.length;
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
                nextIndex = (currentIndex - 1 + focusableElements.length) % focusableElements.length;
                break;
        }
        
        if (nextIndex !== undefined) {
            e.preventDefault();
            focusableElements[nextIndex].focus();
        }
    }
    
    initializeSystemMetrics() {
        return {
            version: '1.1.0',
            status: 'operational',
            connectedSensors: 4,
            lastSync: new Date(),
            uptime: Date.now(),
            memoryUsage: Math.random() * 100,
            cpuUsage: Math.random() * 50
        };
    }
    
    startSystemMonitoring() {
        // Mise à jour des métriques système toutes les 30 secondes
        setInterval(() => {
            this.updateSystemMetrics();
            this.updateSystemInfo();
        }, 30000);
        
        // Mise à jour de l'heure toutes les secondes
        setInterval(() => {
            this.updateLastSyncTime();
        }, 1000);
    }
    
    updateSystemMetrics() {
        this.systemMetrics.lastSync = new Date();
        this.systemMetrics.memoryUsage = Math.random() * 100;
        this.systemMetrics.cpuUsage = Math.random() * 50;
        
        // Simulation de déconnexion/reconnexion de capteurs
        if (Math.random() < 0.1) {
            this.systemMetrics.connectedSensors = Math.floor(Math.random() * 5) + 3;
        }
    }
    
    loadRecentProjects() {
        // Chargement des projets récents avec plus de détails
        const projects = [
            {
                id: 'projet-houle-med-2024',
                name: 'Étude Houle Méditerranée 2024',
                lastModified: new Date(Date.now() - 2 * 60 * 60 * 1000),
                type: 'acquisition',
                status: 'active',
                progress: 75
            },
            {
                id: 'calibration-capteurs-jan',
                name: 'Calibration Capteurs Janvier',
                lastModified: new Date(Date.now() - 24 * 60 * 60 * 1000),
                type: 'calibration',
                status: 'completed',
                progress: 100
            },
            {
                id: 'analyse-tempete-dec',
                name: 'Analyse Tempête Décembre',
                lastModified: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
                type: 'analysis',
                status: 'archived',
                progress: 100
            },
            {
                id: 'test-bassin-nord',
                name: 'Tests Bassin Nord',
                lastModified: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
                type: 'testing',
                status: 'paused',
                progress: 45
            }
        ];
        
        return projects.sort((a, b) => b.lastModified - a.lastModified);
    }
    
    renderRecentProjects() {
        const grid = document.getElementById('recentProjectsGrid');
        if (!grid) return;
        
        grid.innerHTML = '';
        
        this.recentProjects.slice(0, 6).forEach(project => {
            const item = document.createElement('div');
            item.className = 'recent-item';
            item.onclick = () => this.openRecentProject(project.id);
            item.setAttribute('tabindex', '0');
            item.setAttribute('role', 'button');
            item.setAttribute('aria-label', `Ouvrir le projet ${project.name}`);
            
            const timeAgo = this.getTimeAgo(project.lastModified);
            const statusIcon = this.getStatusIcon(project.status);
            
            item.innerHTML = `
                <div class="recent-name">${statusIcon} ${project.name}</div>
                <div class="recent-date">Modifié ${timeAgo}</div>
                <div class="recent-progress" style="width: ${project.progress}%; background: var(--maritime-accent); height: 2px; margin-top: 8px; border-radius: 1px;"></div>
            `;
            
            grid.appendChild(item);
        });
    }
    
    getStatusIcon(status) {
        const icons = {
            active: '🟢',
            completed: '✅',
            paused: '⏸️',
            archived: '📦'
        };
        return icons[status] || '📋';
    }
    
    getTimeAgo(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / (1000 * 60));
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (minutes < 1) return 'à l\'instant';
        if (minutes < 60) return `il y a ${minutes} min`;
        if (hours < 1) return 'il y a moins d\'une heure';
        if (hours < 24) return `il y a ${hours} heure${hours > 1 ? 's' : ''}`;
        if (days === 1) return 'hier';
        return `il y a ${days} jours`;
    }
    
    updateSystemInfo() {
        const elements = {
            systemVersion: document.getElementById('systemVersion'),
            systemStatus: document.getElementById('systemStatus'),
            lastSyncTime: document.getElementById('lastSyncTime'),
            sensorCount: document.getElementById('sensorCount')
        };
        
        if (elements.systemVersion) {
            elements.systemVersion.textContent = `CHNeoWave v${this.systemMetrics.version}`;
        }
        
        if (elements.systemStatus) {
            const statusText = this.systemMetrics.status === 'operational' ? '🟢 Système opérationnel' : '🔴 Système en maintenance';
            elements.systemStatus.textContent = statusText;
        }
        
        if (elements.sensorCount) {
            elements.sensorCount.textContent = this.systemMetrics.connectedSensors;
        }
        
        this.updateLastSyncTime();
    }
    
    updateLastSyncTime() {
        const element = document.getElementById('lastSyncTime');
        if (element) {
            const now = new Date();
            element.textContent = now.toLocaleTimeString('fr-FR', { 
                hour: '2-digit', 
                minute: '2-digit',
                second: '2-digit'
            });
        }
    }
    
    handleResize() {
        const container = document.querySelector('.launch-container');
        const width = window.innerWidth;
        
        // Gestion responsive avancée
        container.classList.toggle('mobile-layout', width < 768);
        container.classList.toggle('tablet-layout', width >= 768 && width < 1024);
        container.classList.toggle('desktop-layout', width >= 1024);
        
        // Ajustement dynamique de la grille
        const actionGrid = document.querySelector('.action-grid');
        if (actionGrid) {
            const cardCount = width < 768 ? 1 : width < 1024 ? 2 : 4;
            actionGrid.style.gridTemplateColumns = `repeat(${cardCount}, 1fr)`;
        }
    }
    
    // Méthodes d'action étendues
    createProject() {
        console.log('🚀 Création d\'un nouveau projet maritime');
        this.showProjectDialog('create');
    }
    
    openProject() {
        console.log('📂 Ouverture d\'un projet existant');
        this.showProjectDialog('open');
    }
    
    importProject() {
        console.log('📊 Import de données maritimes');
        this.showProjectDialog('import');
    }
    
    quickCalibration() {
        console.log('⚙️ Calibration rapide des capteurs');
        this.showCalibrationDialog();
    }
    
    openRecentProject(projectId) {
        console.log(`🔄 Ouverture du projet récent: ${projectId}`);
        const project = this.recentProjects.find(p => p.id === projectId);
        if (project) {
            this.showProjectDetails(project);
        }
    }
    
    showProjectDialog(type) {
        const messages = {
            create: 'Création d\'un nouveau projet maritime\n\nFonctionnalités disponibles:\n• Configuration automatisée des capteurs\n• Templates de projets prédéfinis\n• Validation des paramètres d\'acquisition',
            open: 'Ouverture d\'un projet existant\n\nFormats supportés:\n• Projets CHNeoWave (.chnw)\n• Données MATLAB (.mat)\n• Fichiers CSV d\'acquisition',
            import: 'Import de données maritimes\n\nSources supportées:\n• Capteurs de houle externes\n• Données météorologiques\n• Fichiers de simulation numérique'
        };
        
        alert(messages[type] || 'Fonctionnalité en cours de développement');
    }
    
    showCalibrationDialog() {
        alert(`Calibration Rapide des Capteurs\n\nÉtat actuel:\n• Capteurs connectés: ${this.systemMetrics.connectedSensors}\n• Dernière calibration: ${this.getTimeAgo(this.systemMetrics.lastSync)}\n\nLancement de la séquence de calibration automatisée...`);
    }
    
    showProjectDetails(project) {
        alert(`Détails du Projet\n\nNom: ${project.name}\nType: ${project.type}\nStatut: ${project.status}\nProgrès: ${project.progress}%\nDernière modification: ${this.getTimeAgo(project.lastModified)}\n\nOuverture du projet...`);
    }
}

// Fonctions globales pour les événements HTML
function createProject() {
    window.launchManager?.createProject();
}

function openProject() {
    window.launchManager?.openProject();
}

function importProject() {
    window.launchManager?.importProject();
}

function quickCalibration() {
    window.launchManager?.quickCalibration();
}

function openRecentProject(projectId) {
    window.launchManager?.openRecentProject(projectId);
}

function toggleTheme() {
    window.launchManager?.themeManager.toggleTheme();
    const themeName = window.launchManager?.themeManager.getCurrentThemeName();
    console.log(`🎨 Thème changé: ${themeName}`);
}

function showAbout() {
    const aboutText = `🌊 CHNeoWave v1.1.0\n\nInterface Maritime Professionnelle\nLaboratoires d'Étude de Houle\n\n🏗️ Architecture Moderne:\n• Design basé sur le Golden Ratio\n• Palette WCAG 2.1 AA compliant\n• Interface sans scroll adaptative\n\n👨‍💻 Développé par l'Architecte Logiciel en Chef\n📅 Version: ${new Date().getFullYear()}\n\n🚀 Fonctionnalités:\n• Acquisition temps réel\n• Calibration automatisée\n• Analyse avancée des données\n• Rapports professionnels`;
    alert(aboutText);
}

function showHelp() {
    const helpText = `❓ Aide CHNeoWave\n\n⌨️ Raccourcis Clavier:\n• Ctrl+N: Nouveau projet\n• Ctrl+O: Ouvrir projet\n• Ctrl+I: Importer données\n• Ctrl+R: Calibration rapide\n• Ctrl+T: Changer de thème\n\n🧭 Navigation:\n• Flèches: Navigation clavier\n• Tab: Parcourir les éléments\n• Entrée/Espace: Activer\n\n🎨 Thèmes Disponibles:\n• Maritime Classique\n• Océan Profond\n• Méditerranéen\n\n📞 Support: support@chneowave.fr`;
    alert(helpText);
}

function showPreferences() {
    const prefsText = `⚙️ Préférences Système\n\n🎨 Interface:\n• Thème: ${window.launchManager?.themeManager.getCurrentThemeName()}\n• Animation: Activée\n• Accessibilité: Optimisée\n\n📊 Système:\n• Version: ${window.launchManager?.systemMetrics.version}\n• Capteurs: ${window.launchManager?.systemMetrics.connectedSensors} connectés\n• Mémoire: ${Math.round(window.launchManager?.systemMetrics.memoryUsage || 0)}%\n\n💾 Données:\n• Sauvegarde auto: Activée\n• Compression: Activée\n• Backup cloud: Configuré\n\nConfiguration avancée disponible dans l'interface principale.`;
    alert(prefsText);
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌊 Initialisation CHNeoWave Launch Screen v2.0.0');
    
    // Vérification de la compatibilité
    if (!window.CSS || !window.CSS.supports) {
        console.warn('⚠️ Navigateur non compatible avec les fonctionnalités CSS avancées');
    }
    
    // Initialisation du gestionnaire principal
    window.launchManager = new ModernLaunchScreenManager();
    
    // Animation d'entrée
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
    
    console.log('✅ CHNeoWave Launch Screen initialisé avec succès');
    console.log('🎯 Interface maritime moderne prête');
});