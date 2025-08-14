import React from 'react';
import { 
  ClockIcon, 
  UserIcon, 
  MapPinIcon, 
  CalendarIcon,
  DocumentTextIcon,
  ScaleIcon
} from '@heroicons/react/24/outline';

interface ProjectInfo {
  name: string;
  engineer: string;
  location: string;
  date: string;
  description: string;
  modelScale: string;
  waveType: string;
  status: 'active' | 'completed' | 'paused';
  progress: number;
}

const NewDashboardPage: React.FC = () => {
  // Mock project data - in real app this would come from props/context
  const projectInfo: ProjectInfo = {
    name: "Essai de Houle Irrégulière - Phase 2",
    engineer: "Dr. Marine Dupont",
    location: "Bassin de Houle - Laboratoire Maritime IFREMER",
    date: "2024-08-09",
    description: "Analyse des caractéristiques hydrodynamiques d'un modèle de navire à l'échelle 1:75 en conditions de houle irrégulière JONSWAP. Étude de la résistance à l'avancement et des mouvements du navire.",
    modelScale: "1:75",
    waveType: "Spectre JONSWAP",
    status: 'active',
    progress: 65
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 bg-green-400/10 border-green-400/20';
      case 'completed': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'paused': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Projet Actif';
      case 'completed': return 'Terminé';
      case 'paused': return 'En Pause';
      default: return 'Inconnu';
    }
  };

  return (
    <div className="h-full overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Fixed Header */}
      <div className="h-20 bg-gradient-to-r from-blue-600 to-cyan-600 flex items-center px-8 shadow-lg">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12">
            <svg viewBox="0 0 100 100" className="w-full h-full">
              <polygon
                points="50,10 80,30 80,70 50,90 20,70 20,30"
                fill="rgba(255,255,255,0.2)"
                stroke="white"
                strokeWidth="2"
              />
              <path
                d="M30 45 Q40 40 50 45 T70 45"
                stroke="white"
                strokeWidth="2"
                fill="none"
              />
              <circle cx="50" cy="50" r="2" fill="white" />
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Tableau de Bord</h1>
            <p className="text-blue-100 text-sm">Aperçu du projet en cours</p>
          </div>
        </div>
        
        <div className="ml-auto flex items-center space-x-4">
          <div className={`px-4 py-2 rounded-full border text-sm font-medium ${getStatusColor(projectInfo.status)}`}>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-current animate-pulse" />
              <span>{getStatusText(projectInfo.status)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Fixed Height, No Scroll */}
      <div className="h-[calc(100vh-5rem)] p-8 grid grid-cols-12 gap-6">
        
        {/* Project Information Panel - Left Side */}
        <div className="col-span-8 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700 p-6">
          <div className="h-full flex flex-col">
            
            {/* Project Header */}
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-white mb-2">{projectInfo.name}</h2>
              <div className="w-full bg-slate-700 rounded-full h-2 mb-4">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${projectInfo.progress}%` }}
                />
              </div>
              <p className="text-slate-400 text-sm">Progression: {projectInfo.progress}% complété</p>
            </div>

            {/* Project Details Grid */}
            <div className="flex-1 grid grid-cols-2 gap-6">
              
              {/* Left Column */}
              <div className="space-y-6">
                <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-600">
                  <div className="flex items-center space-x-3 mb-3">
                    <UserIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-300">Ingénieur Responsable</span>
                  </div>
                  <p className="text-white font-semibold">{projectInfo.engineer}</p>
                </div>

                <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-600">
                  <div className="flex items-center space-x-3 mb-3">
                    <MapPinIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-300">Lieu d'Essai</span>
                  </div>
                  <p className="text-white font-semibold">{projectInfo.location}</p>
                </div>

                <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-600">
                  <div className="flex items-center space-x-3 mb-3">
                    <CalendarIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-300">Date d'Essai</span>
                  </div>
                  <p className="text-white font-semibold">
                    {new Date(projectInfo.date).toLocaleDateString('fr-FR', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-600">
                  <div className="flex items-center space-x-3 mb-3">
                    <ScaleIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-300">Échelle du Modèle</span>
                  </div>
                  <p className="text-white font-semibold">{projectInfo.modelScale}</p>
                </div>

                <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-600">
                  <div className="flex items-center space-x-3 mb-3">
                    <ClockIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-300">Type de Houle</span>
                  </div>
                  <p className="text-white font-semibold">{projectInfo.waveType}</p>
                </div>

                <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-600 flex-1">
                  <div className="flex items-center space-x-3 mb-3">
                    <DocumentTextIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-300">Description</span>
                  </div>
                  <p className="text-slate-300 text-sm leading-relaxed">{projectInfo.description}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* System Status & Activity - Right Side */}
        <div className="col-span-4 space-y-6">
          
          {/* System Status */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700 p-6">
            <h3 className="text-lg font-semibold text-white mb-4">État du Système</h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
                <span className="text-green-400 font-medium">Acquisition</span>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-green-400 text-sm">Prêt</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                <span className="text-blue-400 font-medium">Calibration</span>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
                  <span className="text-blue-400 text-sm">Configuré</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                <span className="text-yellow-400 font-medium">Sondes</span>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" />
                  <span className="text-yellow-400 text-sm">8/16 Actives</span>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700 p-6 flex-1">
            <h3 className="text-lg font-semibold text-white mb-4">Activité Récente</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex items-center space-x-3 p-2 bg-slate-700/50 rounded-lg">
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span className="text-slate-300">Calibration sonde 8 terminée</span>
                <span className="text-slate-500 ml-auto">14:32</span>
              </div>
              
              <div className="flex items-center space-x-3 p-2 bg-slate-700/50 rounded-lg">
                <div className="w-2 h-2 bg-blue-400 rounded-full" />
                <span className="text-slate-300">Configuration sauvegardée</span>
                <span className="text-slate-500 ml-auto">14:28</span>
              </div>
              
              <div className="flex items-center space-x-3 p-2 bg-slate-700/50 rounded-lg">
                <div className="w-2 h-2 bg-yellow-400 rounded-full" />
                <span className="text-slate-300">Projet créé</span>
                <span className="text-slate-500 ml-auto">14:15</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewDashboardPage;
