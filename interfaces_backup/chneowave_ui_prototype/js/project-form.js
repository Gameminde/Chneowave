/**
 * CHNeoWave - Gestion Formulaire Projet
 * Logique pour le formulaire de création de projet en plusieurs étapes
 */

// Fonction pour passer à l'étape suivante avec validation
function nextStepWithValidation() {
    if (window.projectFormManager && window.projectFormManager.validateCurrentStep()) {
        window.projectFormManager.nextStep();
        updateSummary();
    }
}

// Mise à jour du résumé dans l'étape de validation
function updateSummary() {
    if (window.projectFormManager && window.projectFormManager.currentStep === 3) {
        const formData = window.projectFormManager.collectFormData();
        
        // Mettre à jour les éléments du résumé
        const summaryElements = {
            'summary-name': formData.projectName || '-',
            'summary-code': formData.projectCode || '-',
            'summary-leader': formData.projectLeader || '-',
            'summary-location': getLocationLabel(formData.projectLocation) || '-',
            'summary-sondes': formData.nbSondes || '-',
            'summary-freq': formData.freqAcquisition ? `${formData.freqAcquisition} Hz` : '-'
        };
        
        Object.entries(summaryElements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }
}

// Obtenir le libellé de la localisation
function getLocationLabel(value) {
    const locations = {
        'ifremer-brest': 'IFREMER Brest',
        'ecn-nantes': 'École Centrale Nantes',
        'ensta-bretagne': 'ENSTA Bretagne',
        'mediterranee': 'Mer Méditerranée',
        'autre': 'Autre site'
    };
    return locations[value] || value;
}

// Validation personnalisée pour le code projet
function validateProjectCode(input) {
    const pattern = /^CHN-\d{4}-\d{3}$/;
    const value = input.value.trim();
    
    if (value && !pattern.test(value)) {
        window.projectFormManager.showFieldError(input, 'Format requis: CHN-YYYY-XXX (ex: CHN-2024-016)');
        return false;
    }
    return true;
}

// Auto-génération du code projet
function generateProjectCode() {
    const currentYear = new Date().getFullYear();
    const randomNum = Math.floor(Math.random() * 900) + 100; // 100-999
    return `CHN-${currentYear}-${randomNum.toString().padStart(3, '0')}`;
}

// Gestion des événements du formulaire
class ProjectFormHandler {
    constructor() {
        this.initEventListeners();
        this.initFormValidation();
    }
    
    initEventListeners() {
        // Auto-génération du code projet si vide
        const projectNameInput = document.getElementById('project-name');
        const projectCodeInput = document.getElementById('project-code');
        
        if (projectNameInput && projectCodeInput) {
            projectNameInput.addEventListener('blur', () => {
                if (projectNameInput.value.trim() && !projectCodeInput.value.trim()) {
                    projectCodeInput.value = generateProjectCode();
                }
            });
        }
        
        // Validation en temps réel du code projet
        if (projectCodeInput) {
            projectCodeInput.addEventListener('input', (e) => {
                // Forcer le format en majuscules
                e.target.value = e.target.value.toUpperCase();
            });
            
            projectCodeInput.addEventListener('blur', (e) => {
                validateProjectCode(e.target);
            });
        }
        
        // Gestion du changement de localisation
        const locationSelect = document.getElementById('project-location');
        if (locationSelect) {
            locationSelect.addEventListener('change', (e) => {
                if (e.target.value === 'autre') {
                    this.showCustomLocationInput();
                }
            });
        }
        
        // Gestion du nombre de sondes
        const nbSondesInput = document.getElementById('nb-sondes');
        if (nbSondesInput) {
            nbSondesInput.addEventListener('change', (e) => {
                const value = parseInt(e.target.value);
                if (value > 16) {
                    window.projectFormManager.showFieldError(e.target, 'Maximum 16 sondes supportées');
                    e.target.value = 16;
                } else if (value < 1) {
                    window.projectFormManager.showFieldError(e.target, 'Minimum 1 sonde requise');
                    e.target.value = 1;
                }
            });
        }
    }
    
    initFormValidation() {
        // Validation personnalisée pour tous les champs requis
        const requiredFields = document.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => {
                this.validateField(field);
            });
            
            field.addEventListener('input', () => {
                // Supprimer les erreurs lors de la saisie
                this.clearFieldError(field);
            });
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        
        if (field.hasAttribute('required') && !value) {
            window.projectFormManager.showFieldError(field, 'Ce champ est obligatoire');
            return false;
        }
        
        // Validations spécifiques
        switch (field.id) {
            case 'project-code':
                return validateProjectCode(field);
            case 'project-name':
                if (value.length < 3) {
                    window.projectFormManager.showFieldError(field, 'Le nom doit contenir au moins 3 caractères');
                    return false;
                }
                break;
            case 'project-leader':
                if (value.length < 2) {
                    window.projectFormManager.showFieldError(field, 'Le nom du chef de projet doit contenir au moins 2 caractères');
                    return false;
                }
                break;
        }
        
        return true;
    }
    
    clearFieldError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
            field.style.borderColor = '';
        }
    }
    
    showCustomLocationInput() {
        const locationGroup = document.getElementById('project-location').parentNode;
        
        // Vérifier si l'input personnalisé existe déjà
        if (locationGroup.querySelector('#custom-location')) {
            return;
        }
        
        const customInput = document.createElement('input');
        customInput.type = 'text';
        customInput.id = 'custom-location';
        customInput.name = 'customLocation';
        customInput.placeholder = 'Spécifiez la localisation';
        customInput.style.marginTop = '8px';
        customInput.required = true;
        
        locationGroup.appendChild(customInput);
        customInput.focus();
    }
}

// Fonctions utilitaires pour l'interface
function showFormTip(message, type = 'info') {
    const tipContainer = document.createElement('div');
    tipContainer.className = `form-tip form-tip-${type}`;
    tipContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--emerald-success)' : 'var(--harbor-blue)'};
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    
    tipContainer.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
            <i class="fas fa-${type === 'success' ? 'check' : 'info'}-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(tipContainer);
    
    // Supprimer après 3 secondes
    setTimeout(() => {
        if (tipContainer.parentNode) {
            tipContainer.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                tipContainer.remove();
            }, 300);
        }
    }, 3000);
}

// Ajouter les animations CSS
function addFormAnimations() {
    if (!document.getElementById('form-animations')) {
        const style = document.createElement('style');
        style.id = 'form-animations';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Sauvegarde automatique du formulaire
class FormAutoSave {
    constructor() {
        this.saveKey = 'chneowave-project-draft';
        this.saveInterval = 30000; // 30 secondes
        this.initAutoSave();
    }
    
    initAutoSave() {
        // Charger les données sauvegardées
        this.loadDraft();
        
        // Sauvegarder automatiquement
        setInterval(() => {
            this.saveDraft();
        }, this.saveInterval);
        
        // Sauvegarder avant de quitter
        window.addEventListener('beforeunload', () => {
            this.saveDraft();
        });
    }
    
    saveDraft() {
        if (window.projectFormManager) {
            const formData = window.projectFormManager.collectFormData();
            const draftData = {
                ...formData,
                currentStep: window.projectFormManager.currentStep,
                timestamp: Date.now()
            };
            
            try {
                localStorage.setItem(this.saveKey, JSON.stringify(draftData));
                console.log('Brouillon sauvegardé automatiquement');
            } catch (error) {
                console.warn('Erreur lors de la sauvegarde du brouillon:', error);
            }
        }
    }
    
    loadDraft() {
        try {
            const draftData = localStorage.getItem(this.saveKey);
            if (draftData) {
                const data = JSON.parse(draftData);
                
                // Vérifier si le brouillon n'est pas trop ancien (24h)
                const maxAge = 24 * 60 * 60 * 1000;
                if (Date.now() - data.timestamp < maxAge) {
                    this.restoreFormData(data);
                    showFormTip('Brouillon restauré automatiquement', 'info');
                } else {
                    this.clearDraft();
                }
            }
        } catch (error) {
            console.warn('Erreur lors du chargement du brouillon:', error);
            this.clearDraft();
        }
    }
    
    restoreFormData(data) {
        Object.entries(data).forEach(([key, value]) => {
            if (key !== 'currentStep' && key !== 'timestamp') {
                const field = document.querySelector(`[name="${key}"]`);
                if (field) {
                    if (field.type === 'checkbox') {
                        field.checked = value;
                    } else {
                        field.value = value;
                    }
                }
            }
        });
    }
    
    clearDraft() {
        localStorage.removeItem(this.saveKey);
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('CHNeoWave Project Form initialisé');
    
    // Ajouter les animations
    addFormAnimations();
    
    // Initialiser le gestionnaire de formulaire
    if (document.getElementById('project-form')) {
        window.projectFormHandler = new ProjectFormHandler();
        window.formAutoSave = new FormAutoSave();
        
        // Message de bienvenue
        setTimeout(() => {
            showFormTip('Remplissez le formulaire étape par étape. Vos données sont sauvegardées automatiquement.', 'info');
        }, 1000);
    }
});

// Export des fonctions pour utilisation globale
window.nextStepWithValidation = nextStepWithValidation;
window.updateSummary = updateSummary;
window.showFormTip = showFormTip;