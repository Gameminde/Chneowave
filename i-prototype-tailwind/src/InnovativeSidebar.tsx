import React, { useState } from 'react';
import { 
  HomeIcon,
  CogIcon,
  PlayIcon,
  ChartBarIcon,
  DocumentArrowDownIcon,
  ChevronRightIcon,
  ChevronLeftIcon,
  BeakerIcon
} from '@heroicons/react/24/outline';

interface InnovativeSidebarProps {
  currentPage: string;
  onPageChange: (page: 'dashboard' | 'calibration' | 'acquisition' | 'analysis' | 'advanced-analysis' | 'export') => void;
  projectName: string;
}

const InnovativeSidebar: React.FC<InnovativeSidebarProps> = ({
  currentPage,
  onPageChange,
  projectName
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Tableau de Bord',
      icon: HomeIcon,
      color: 'from-blue-600 to-cyan-600',
      description: 'Vue d\'ensemble du projet'
    },
    {
      id: 'calibration',
      label: 'Calibration',
      icon: CogIcon,
      color: 'from-purple-600 to-pink-600',
      description: 'Étalonnage des sondes'
    },
    {
      id: 'acquisition',
      label: 'Acquisition',
      icon: PlayIcon,
      color: 'from-emerald-600 to-teal-600',
      description: 'Mesure temps réel'
    },
    {
      id: 'analysis',
      label: 'Analyse',
      icon: ChartBarIcon,
      color: 'from-orange-600 to-red-600',
      description: 'Statistiques de base'
    },
    {
      id: 'advanced-analysis',
      label: 'Analyse Avancée',
      icon: BeakerIcon,
      color: 'from-pink-600 to-rose-600',
      description: 'Analyses complexes'
    },
    {
      id: 'export',
      label: 'Export',
      icon: DocumentArrowDownIcon,
      color: 'from-indigo-600 to-purple-600',
      description: 'Exportation des résultats'
    }
  ];

  return (
    <div className={`h-full bg-gradient-to-b from-slate-800 to-slate-900 border-r border-slate-700 transition-all duration-300 ${
      isCollapsed ? 'w-16' : 'w-80'
    }`}>
      
      {/* Header */}
      <div className="h-20 bg-gradient-to-r from-slate-700 to-slate-800 flex items-center px-4 border-b border-slate-600">
        {!isCollapsed && (
          <div className="flex items-center space-x-3 flex-1">
            <div className="w-10 h-10">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <polygon
                  points="50,10 80,30 80,70 50,90 20,70 20,30"
                  fill="url(#sidebarGradient)"
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
                  <linearGradient id="sidebarGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#1e40af" />
                    <stop offset="100%" stopColor="#3b82f6" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div>
              <h2 className="text-white font-bold text-lg">CHNeoWave</h2>
              <p className="text-slate-400 text-xs">v2.1.0</p>
            </div>
          </div>
        )}
        
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-2 text-slate-400 hover:text-white transition-colors"
        >
          {isCollapsed ? (
            <ChevronRightIcon className="w-5 h-5" />
          ) : (
            <ChevronLeftIcon className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Project Info */}
      {!isCollapsed && (
        <div className="p-4 border-b border-slate-700">
          <div className="bg-slate-700/50 rounded-lg p-3">
            <p className="text-slate-400 text-xs mb-1">Projet Actuel</p>
            <p className="text-white font-medium text-sm leading-tight">{projectName}</p>
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="flex-1 p-4 space-y-2">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id as any)}
              className={`w-full group relative overflow-hidden rounded-xl transition-all duration-300 ${
                isActive 
                  ? `bg-gradient-to-r ${item.color} shadow-lg transform scale-105` 
                  : 'bg-slate-700/30 hover:bg-slate-700/50 hover:scale-102'
              }`}
            >
              <div className={`flex items-center p-4 ${isCollapsed ? 'justify-center' : 'space-x-4'}`}>
                <div className={`flex-shrink-0 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-white'}`}>
                  <Icon className="w-6 h-6" />
                </div>
                
                {!isCollapsed && (
                  <div className="flex-1 text-left">
                    <p className={`font-medium ${isActive ? 'text-white' : 'text-slate-300 group-hover:text-white'}`}>
                      {item.label}
                    </p>
                    <p className={`text-xs ${isActive ? 'text-white/80' : 'text-slate-500 group-hover:text-slate-400'}`}>
                      {item.description}
                    </p>
                  </div>
                )}
              </div>
              
              {/* Active indicator */}
              {isActive && !isCollapsed && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Footer */}
      {!isCollapsed && (
        <div className="p-4 border-t border-slate-700">
          <div className="text-center">
            <p className="text-slate-500 text-xs">
              Système d'Acquisition Maritime
            </p>
            <p className="text-slate-600 text-xs mt-1">
              © 2024 CHNeoWave Systems
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default InnovativeSidebar;
