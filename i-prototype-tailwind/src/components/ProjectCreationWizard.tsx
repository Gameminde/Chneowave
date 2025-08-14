import React, { useState } from 'react';
import { ChevronRightIcon, ChevronLeftIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface ProjectData {
  name: string;
  description: string;
  engineer: string;
  location: string;
  date: string;
  modelScale: string;
  waveType: string;
  testDuration: string;
  notes: string;
}

interface ProjectCreationWizardProps {
  onComplete: (data: ProjectData) => void;
  onCancel: () => void;
}

const ProjectCreationWizard: React.FC<ProjectCreationWizardProps> = ({
  onComplete,
  onCancel
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [projectData, setProjectData] = useState<ProjectData>({
    name: '',
    description: '',
    engineer: '',
    location: '',
    date: '',
    modelScale: '',
    waveType: '',
    testDuration: '',
    notes: ''
  });

  const steps = [
    {
      title: 'Informations Générales',
      subtitle: 'Définissez les paramètres de base du projet'
    },
    {
      title: 'Configuration d\'Essai',
      subtitle: 'Spécifiez les conditions expérimentales'
    },
    {
      title: 'Validation',
      subtitle: 'Vérifiez et confirmez les paramètres'
    }
  ];

  const handleInputChange = (field: keyof ProjectData, value: string) => {
    setProjectData(prev => ({ ...prev, [field]: value }));
  };

  const isStepValid = (step: number) => {
    switch (step) {
      case 0:
        return projectData.name && projectData.engineer && projectData.location;
      case 1:
        return projectData.date && projectData.modelScale && projectData.waveType;
      case 2:
        return true;
      default:
        return false;
    }
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    onComplete(projectData);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Nom du Projet *
                </label>
                <input
                  type="text"
                  value={projectData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="Essai de houle irrégulière"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Ingénieur Responsable *
                </label>
                <input
                  type="text"
                  value={projectData.engineer}
                  onChange={(e) => handleInputChange('engineer', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="Dr. Marine Dupont"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Lieu d'Essai *
                </label>
                <input
                  type="text"
                  value={projectData.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="Bassin de houle - Laboratoire Maritime"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Description du Projet
              </label>
              <textarea
                value={projectData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                rows={4}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                placeholder="Description détaillée des objectifs et conditions d'essai..."
              />
            </div>
          </div>
        );
        
      case 1:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Date d'Essai *
                </label>
                <input
                  type="date"
                  value={projectData.date}
                  onChange={(e) => handleInputChange('date', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Échelle du Modèle *
                </label>
                <select
                  value={projectData.modelScale}
                  onChange={(e) => handleInputChange('modelScale', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                >
                  <option value="">Sélectionner l'échelle</option>
                  <option value="1:50">1:50</option>
                  <option value="1:75">1:75</option>
                  <option value="1:100">1:100</option>
                  <option value="1:150">1:150</option>
                  <option value="custom">Personnalisée</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Type de Houle *
                </label>
                <select
                  value={projectData.waveType}
                  onChange={(e) => handleInputChange('waveType', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                >
                  <option value="">Sélectionner le type</option>
                  <option value="regular">Houle régulière</option>
                  <option value="irregular">Houle irrégulière</option>
                  <option value="jonswap">Spectre JONSWAP</option>
                  <option value="pierson-moskowitz">Pierson-Moskowitz</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Durée d'Essai
                </label>
                <select
                  value={projectData.testDuration}
                  onChange={(e) => handleInputChange('testDuration', e.target.value)}
                  className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                >
                  <option value="">Durée estimée</option>
                  <option value="30min">30 minutes</option>
                  <option value="1h">1 heure</option>
                  <option value="2h">2 heures</option>
                  <option value="4h">4 heures</option>
                  <option value="full-day">Journée complète</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Notes Techniques
              </label>
              <textarea
                value={projectData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                rows={4}
                className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                placeholder="Conditions météorologiques, paramètres spéciaux, observations..."
              />
            </div>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-6">
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-600">
              <h3 className="text-lg font-semibold text-white mb-4">Récapitulatif du Projet</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <span className="text-sm text-slate-400">Nom du projet:</span>
                    <p className="text-white font-medium">{projectData.name || 'Non défini'}</p>
                  </div>
                  <div>
                    <span className="text-sm text-slate-400">Ingénieur:</span>
                    <p className="text-white font-medium">{projectData.engineer || 'Non défini'}</p>
                  </div>
                  <div>
                    <span className="text-sm text-slate-400">Lieu:</span>
                    <p className="text-white font-medium">{projectData.location || 'Non défini'}</p>
                  </div>
                  <div>
                    <span className="text-sm text-slate-400">Date:</span>
                    <p className="text-white font-medium">{projectData.date || 'Non définie'}</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <span className="text-sm text-slate-400">Échelle:</span>
                    <p className="text-white font-medium">{projectData.modelScale || 'Non définie'}</p>
                  </div>
                  <div>
                    <span className="text-sm text-slate-400">Type de houle:</span>
                    <p className="text-white font-medium">{projectData.waveType || 'Non défini'}</p>
                  </div>
                  <div>
                    <span className="text-sm text-slate-400">Durée:</span>
                    <p className="text-white font-medium">{projectData.testDuration || 'Non définie'}</p>
                  </div>
                </div>
              </div>
              
              {projectData.description && (
                <div className="mt-4 pt-4 border-t border-slate-600">
                  <span className="text-sm text-slate-400">Description:</span>
                  <p className="text-white mt-1">{projectData.description}</p>
                </div>
              )}
              
              {projectData.notes && (
                <div className="mt-4 pt-4 border-t border-slate-600">
                  <span className="text-sm text-slate-400">Notes:</span>
                  <p className="text-white mt-1">{projectData.notes}</p>
                </div>
              )}
            </div>
            
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-blue-200 font-medium">Prêt à créer le projet</p>
                  <p className="text-blue-300 text-sm mt-1">
                    Le projet sera créé avec les paramètres spécifiés. Vous pourrez ensuite 
                    procéder à la calibration des sondes et à la configuration d'acquisition.
                  </p>
                </div>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
         style={{
           background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)'
         }}>
      
      <div className="bg-slate-900 rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden border border-slate-700">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white">Nouveau Projet</h2>
              <p className="text-blue-100">{steps[currentStep].subtitle}</p>
            </div>
            <button
              onClick={onCancel}
              className="text-blue-100 hover:text-white transition-colors p-2"
            >
              <XMarkIcon className="w-6 h-6" />
            </button>
          </div>
          
          {/* Progress Steps */}
          <div className="flex items-center mt-6 space-x-4">
            {steps.map((step, index) => (
              <div key={index} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all ${
                  index < currentStep 
                    ? 'bg-white text-blue-600' 
                    : index === currentStep 
                      ? 'bg-blue-200 text-blue-800' 
                      : 'bg-blue-400 text-blue-100'
                }`}>
                  {index < currentStep ? <CheckIcon className="w-4 h-4" /> : index + 1}
                </div>
                <span className={`ml-2 text-sm ${
                  index <= currentStep ? 'text-white' : 'text-blue-200'
                }`}>
                  {step.title}
                </span>
                {index < steps.length - 1 && (
                  <ChevronRightIcon className="w-4 h-4 text-blue-200 mx-4" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-8 overflow-y-auto max-h-[60vh]">
          {renderStepContent()}
        </div>

        {/* Footer */}
        <div className="bg-slate-800 px-8 py-4 flex items-center justify-between border-t border-slate-700">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
              currentStep === 0
                ? 'text-slate-500 cursor-not-allowed'
                : 'text-slate-300 hover:text-white hover:bg-slate-700'
            }`}
          >
            <ChevronLeftIcon className="w-4 h-4 mr-2" />
            Précédent
          </button>

          <div className="flex space-x-3">
            <button
              onClick={onCancel}
              className="px-6 py-2 text-slate-300 hover:text-white transition-colors"
            >
              Annuler
            </button>
            
            {currentStep < steps.length - 1 ? (
              <button
                onClick={nextStep}
                disabled={!isStepValid(currentStep)}
                className={`flex items-center px-6 py-2 rounded-lg transition-colors ${
                  isStepValid(currentStep)
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-slate-600 text-slate-400 cursor-not-allowed'
                }`}
              >
                Suivant
                <ChevronRightIcon className="w-4 h-4 ml-2" />
              </button>
            ) : (
              <button
                onClick={handleComplete}
                className="flex items-center px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
              >
                <CheckIcon className="w-4 h-4 mr-2" />
                Créer le Projet
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectCreationWizard;
