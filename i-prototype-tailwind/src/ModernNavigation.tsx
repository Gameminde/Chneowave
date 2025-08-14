import React from 'react';
import { useUnifiedApp } from './contexts/UnifiedAppContext';
import { 
  HomeIcon, 
  CogIcon, 
  ChartBarIcon, 
  PlayIcon, 
  DocumentTextIcon,
  ArrowUpTrayIcon
} from '@heroicons/react/24/outline';

interface NavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
  projectName?: string;
}

const ModernNavigation: React.FC<NavigationProps> = ({ 
  currentPage, 
  onPageChange, 
  projectName = 'Projet Sans Nom' 
}) => {
  const { theme } = useUnifiedApp();
  const navigationItems = [
    { id: 'dashboard', label: 'Tableau de Bord', icon: HomeIcon, color: 'blue' },
    { id: 'calibration', label: 'Calibration', icon: CogIcon, color: 'emerald' },
    { id: 'acquisition', label: 'Acquisition', icon: PlayIcon, color: 'violet' },
    { id: 'analysis', label: 'Analyse', icon: ChartBarIcon, color: 'amber' },
    { id: 'export', label: 'Export', icon: ArrowUpTrayIcon, color: 'rose' }
  ];

  const getColorClasses = (color: string, isActive: boolean) => {
    if (isActive) {
      const colorMap: { [key: string]: string } = {
        blue: 'bg-blue-600 text-white shadow-lg shadow-blue-600/25',
        emerald: 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/25',
        violet: 'bg-violet-600 text-white shadow-lg shadow-violet-600/25',
        amber: 'bg-amber-600 text-white shadow-lg shadow-amber-600/25',
        rose: 'bg-rose-600 text-white shadow-lg shadow-rose-600/25'
      };
      return colorMap[color] || 'bg-blue-600 text-white';
    }
    return 'text-slate-400 hover:text-white hover:bg-slate-700/50 transition-all duration-200';
  };

  return (
    <div className="h-16 backdrop-blur-md border-b flex items-center justify-between px-6" style={{
      backgroundColor: 'var(--bg-elevated)',
      borderColor: 'var(--border-primary)'
    }}>
      {/* Logo et Nom du Projet */}
      <div className="flex items-center space-x-4">
        <div className="w-10 h-10 flex-shrink-0">
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
        <div className="flex flex-col">
          <h1 className="font-bold text-lg leading-tight" style={{color: 'var(--text-primary)'}}>CHNeoWave</h1>
          <p className="text-xs leading-tight max-w-48 truncate" style={{color: 'var(--text-secondary)'}}>
            {projectName}
          </p>
        </div>
      </div>
      
      {/* Navigation Principale */}
      <nav className="flex items-center space-x-2">
        {navigationItems.map((item) => {
          const IconComponent = item.icon;
          const isActive = currentPage === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`
                flex items-center space-x-2 px-4 py-2.5 rounded-lg font-medium text-sm
                transition-all duration-200 ease-out
                ${getColorClasses(item.color, isActive)}
                ${!isActive ? 'hover:scale-105' : ''}
              `}
            >
              <IconComponent className="w-4 h-4" />
              <span className="hidden sm:inline">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Indicateur de Statut Système */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="text-xs font-medium text-emerald-400">Système OK</span>
        </div>
      </div>
    </div>
  );
};

export default ModernNavigation;
