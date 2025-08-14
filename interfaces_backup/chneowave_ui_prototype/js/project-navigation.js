/**
 * CHNeoWave - Navigation Projet
 * Gestion de la navigation entre les pages de projet
 */

// Fonctions de navigation globale
function showCreateProject() {
    console.log('Navigation vers création de projet');
    window.location.href = 'project-create.html';
}

function showImportProject() {
    console.log('Ouverture dialogue import projet');
    // Simulation d'un dialogue d'import
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.chn,.json';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            console.log('Fichier sélectionné:', file.name);
            // Simulation du chargement
            showLoadingDialog('Import du projet en cours...');
            setTimeout(() => {
                hideLoadingDialog();
                alert(`Projet "${file.name}" importé avec succès!`);
                window.location.href = 'index.html';
            }, 2000);
        }
    };
    input.click();
}

function openRecentProject(projectCode) {
    console.log('Ouverture projet récent:', projectCode);
    showLoadingDialog('Chargement du projet...');
    setTimeout(() => {
        hideLoadingDialog();
        window.location.href = 'index.html';
    }, 1500);
}

function createProjectDemo() {
    console.log('Création projet démo');
    showLoadingDialog('Création du projet en cours...');
    setTimeout(() => {
        hideLoadingDialog();
        alert('Projet créé avec succès! Redirection vers le dashboard...');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
    }, 2000);
}

// Fonctions utilitaires
function showLoadingDialog(message) {
    // Créer un overlay de chargement
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        backdrop-filter: blur(5px);
    `;
    
    const dialog = document.createElement('div');
    dialog.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        max-width: 300px;
    `;
    
    dialog.innerHTML = `
        <div style="margin-bottom: 1rem;">
            <div style="
                width: 40px;
                height: 40px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid var(--harbor-blue);
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            "></div>
        </div>
        <p style="margin: 0; color: var(--ocean-deep); font-weight: 500;">${message}</p>
    `;
    
    // Ajouter l'animation CSS
    if (!document.getElementById('loading-styles')) {
        const style = document.createElement('style');
        style.id = 'loading-styles';
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
    
    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
}

function hideLoadingDialog() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Gestion des formulaires de projet
class ProjectFormManager {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 3;
        this.projectData = {};
    }
    
    nextStep() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.updateStepDisplay();
            this.showStep(this.currentStep);
        }
    }
    
    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStepDisplay();
            this.showStep(this.currentStep);
        }
    }
    
    updateStepDisplay() {
        const progressBar = document.querySelector('.progress-fill');
        const stepIndicators = document.querySelectorAll('.step-indicator');
        
        if (progressBar) {
            const progress = (this.currentStep / this.totalSteps) * 100;
            progressBar.style.width = `${progress}%`;
        }
        
        stepIndicators.forEach((indicator, index) => {
            const stepNumber = index + 1;
            indicator.classList.toggle('active', stepNumber === this.currentStep);
            indicator.classList.toggle('completed', stepNumber < this.currentStep);
        });
    }
    
    showStep(stepNumber) {
        const steps = document.querySelectorAll('.form-step');
        steps.forEach((step, index) => {
            step.style.display = (index + 1) === stepNumber ? 'block' : 'none';
        });
        
        // Mettre à jour les boutons
        const prevBtn = document.getElementById('prev-step');
        const nextBtn = document.getElementById('next-step');
        const submitBtn = document.getElementById('submit-project');
        
        if (prevBtn) prevBtn.style.display = stepNumber === 1 ? 'none' : 'inline-flex';
        if (nextBtn) nextBtn.style.display = stepNumber === this.totalSteps ? 'none' : 'inline-flex';
        if (submitBtn) submitBtn.style.display = stepNumber === this.totalSteps ? 'inline-flex' : 'none';
    }
    
    collectFormData() {
        const formData = new FormData(document.getElementById('project-form'));
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
    
    validateCurrentStep() {
        const currentStepElement = document.querySelector(`.form-step:nth-child(${this.currentStep})`);
        const requiredFields = currentStepElement.querySelectorAll('[required]');
        
        for (let field of requiredFields) {
            if (!field.value.trim()) {
                field.focus();
                this.showFieldError(field, 'Ce champ est obligatoire');
                return false;
            }
        }
        
        return true;
    }
    
    showFieldError(field, message) {
        // Supprimer les erreurs existantes
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Ajouter la nouvelle erreur
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.style.cssText = `
            color: var(--coral-warning);
            font-size: 0.8rem;
            margin-top: 4px;
        `;
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
        field.style.borderColor = 'var(--coral-warning)';
        
        // Supprimer l'erreur après 3 secondes
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
                field.style.borderColor = '';
            }
        }, 3000);
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('CHNeoWave Project Navigation initialisé');
    
    // Initialiser le gestionnaire de formulaire si on est sur la page de création
    if (document.getElementById('project-form')) {
        window.projectFormManager = new ProjectFormManager();
        window.projectFormManager.showStep(1);
    }
});

// Export des fonctions pour utilisation globale
window.showCreateProject = showCreateProject;
window.showImportProject = showImportProject;
window.openRecentProject = openRecentProject;
window.createProjectDemo = createProjectDemo;