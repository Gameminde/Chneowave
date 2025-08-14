import React, { useState } from 'react';
import { FolderPlusIcon, FolderOpenIcon, InformationCircleIcon } from '@heroicons/react/24/outline';

interface ProjectSelectionModalProps {
  onCreateProject: () => void;
  onImportProject: () => void;
}

const ProjectSelectionModal: React.FC<ProjectSelectionModalProps> = ({
  onCreateProject,
  onImportProject
}) => {
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
         style={{
           background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)'
         }}>
      
      {/* Background Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-30 backdrop-blur-sm" />
      
      {/* Modal Content */}
      <div className="relative z-10 w-full max-w-4xl">
        
        {/* Header Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <div className="w-16 h-16">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <polygon
                  points="50,10 80,30 80,70 50,90 20,70 20,30"
                  fill="url(#headerGradient)"
                  stroke="#3b82f6"
                  strokeWidth="2"
                />
                <path
                  d="M30 45 Q40 40 50 45 T70 45"
                  stroke="#60a5fa"
                  strokeWidth="2"
                  fill="none"
                />
                <circle cx="50" cy="50" r="2" fill="#ffffff" />
                <defs>
                  <linearGradient id="headerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#1e40af" />
                    <stop offset="100%" stopColor="#3b82f6" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-white mb-4">
            CHNeoWave
          </h1>
          <p className="text-xl text-blue-200 mb-2">
            Système d'Acquisition Maritime Professionnel
          </p>
          <p className="text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Logiciel scientifique de haute précision pour l'acquisition et l'analyse 
            de données hydrodynamiques en laboratoire maritime
          </p>
        </div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          
          {/* Create New Project Card */}
          <div
            className="relative group cursor-pointer transform transition-all duration-300 hover:scale-105"
            onMouseEnter={() => setHoveredCard('create')}
            onMouseLeave={() => setHoveredCard(null)}
            onClick={onCreateProject}
          >
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700 hover:border-blue-500 transition-all duration-300 h-full">
              <div className="flex flex-col items-center text-center">
                <div className={`w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center mb-6 transition-all duration-300 ${hoveredCard === 'create' ? 'shadow-lg shadow-blue-500/25' : ''}`}>
                  <FolderPlusIcon className="w-10 h-10 text-white" />
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-4">
                  Créer un Nouveau Projet
                </h3>
                
                <p className="text-slate-400 mb-6 leading-relaxed">
                  Démarrez une nouvelle campagne d'essais maritimes avec configuration 
                  complète des paramètres d'acquisition et calibration des sondes
                </p>
                
                <div className="space-y-2 text-sm text-slate-500">
                  <div className="flex items-center justify-center">
                    <span className="w-2 h-2 bg-blue-400 rounded-full mr-2" />
                    Configuration des sondes
                  </div>
                  <div className="flex items-center justify-center">
                    <span className="w-2 h-2 bg-blue-400 rounded-full mr-2" />
                    Paramètres d'acquisition
                  </div>
                  <div className="flex items-center justify-center">
                    <span className="w-2 h-2 bg-blue-400 rounded-full mr-2" />
                    Métadonnées du projet
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Import Existing Project Card */}
          <div
            className="relative group cursor-pointer transform transition-all duration-300 hover:scale-105"
            onMouseEnter={() => setHoveredCard('import')}
            onMouseLeave={() => setHoveredCard(null)}
            onClick={onImportProject}
          >
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700 hover:border-emerald-500 transition-all duration-300 h-full">
              <div className="flex flex-col items-center text-center">
                <div className={`w-20 h-20 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mb-6 transition-all duration-300 ${hoveredCard === 'import' ? 'shadow-lg shadow-emerald-500/25' : ''}`}>
                  <FolderOpenIcon className="w-10 h-10 text-white" />
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-4">
                  Importer un Projet
                </h3>
                
                <p className="text-slate-400 mb-6 leading-relaxed">
                  Ouvrez un projet existant pour continuer l'analyse ou 
                  consulter les résultats d'essais précédents
                </p>
                
                <div className="space-y-2 text-sm text-slate-500">
                  <div className="flex items-center justify-center">
                    <span className="w-2 h-2 bg-emerald-400 rounded-full mr-2" />
                    Fichiers .chnw
                  </div>
                  <div className="flex items-center justify-center">
                    <span className="w-2 h-2 bg-emerald-400 rounded-full mr-2" />
                    Données d'acquisition
                  </div>
                  <div className="flex items-center justify-center">
                    <span className="w-2 h-2 bg-emerald-400 rounded-full mr-2" />
                    Résultats d'analyse
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Software Information */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
          <div className="flex items-start space-x-4">
            <InformationCircleIcon className="w-6 h-6 text-blue-400 flex-shrink-0 mt-1" />
            <div>
              <h4 className="text-lg font-semibold text-white mb-2">
                À propos de CHNeoWave
              </h4>
              <p className="text-slate-400 text-sm leading-relaxed mb-4">
                CHNeoWave est un système d'acquisition de données maritimes de haute précision, 
                conçu pour les laboratoires de recherche hydrodynamique. Il permet l'acquisition 
                simultanée multi-sondes, l'analyse spectrale avancée et la génération de rapports 
                conformes aux standards ITTC et ISO 9001.
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs text-slate-500">
                <div>
                  <span className="font-medium text-slate-400">Fréquence max:</span><br />
                  1000 Hz
                </div>
                <div>
                  <span className="font-medium text-slate-400">Sondes max:</span><br />
                  16 sondes
                </div>
                <div>
                  <span className="font-medium text-slate-400">Précision:</span><br />
                  ±0.1 mm
                </div>
                <div>
                  <span className="font-medium text-slate-400">Standards:</span><br />
                  ITTC/ISO 9001
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-xs text-slate-500">
            CHNeoWave v2.1.0 | Développé pour les laboratoires maritimes professionnels
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProjectSelectionModal;
