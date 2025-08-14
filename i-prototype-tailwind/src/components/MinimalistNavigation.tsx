import React from 'react';
import {
  HomeIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  PlayIcon,
  ChartBarIcon,
  BeakerIcon,
  ArrowDownTrayIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';
import ThemeSelector from './ThemeSelector';

interface MinimalistNavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
  projectName: string;
}

const MinimalistNavigation: React.FC<MinimalistNavigationProps> = ({
  currentPage,
  onPageChange,
  projectName
}) => {
  const navigationItems = [
    { id: 'dashboard', label: 'Tableau de Bord', icon: HomeIcon },
    { id: 'project', label: 'Projet', icon: DocumentTextIcon },
    { id: 'calibration', label: 'Calibration', icon: Cog6ToothIcon },
    { id: 'acquisition', label: 'Acquisition', icon: PlayIcon },
    { id: 'analysis', label: 'Analyse', icon: ChartBarIcon },
    { id: 'advanced-analysis', label: 'Analyse Avancée', icon: BeakerIcon },
    { id: 'export', label: 'Export', icon: ArrowDownTrayIcon },
    { id: 'settings', label: 'Paramètres', icon: AdjustmentsHorizontalIcon }
  ];

  return (
    <nav className="themed-nav" style={{
      backgroundColor: 'var(--bg-elevated)',
      borderBottom: '1px solid var(--border-primary)',
      backdropFilter: 'blur(10px)'
    }}>
      <div className="golden-container">
        <div className="flex items-center justify-between py-4">
          
          {/* Logo & Project */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center shadow-lg" style={{
                background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))'
              }}>
                <span className="text-white font-bold text-sm">CHN</span>
              </div>
              <div>
                <div className="text-body font-semibold" style={{color: 'var(--text-primary)'}}>CHNeoWave</div>
                <div className="text-meta truncate max-w-xs" style={{color: 'var(--text-muted)'}}>
                  {projectName}
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center gap-1 overflow-x-auto scrollbar-hide">
            {navigationItems.map((item) => {
              const IconComponent = item.icon;
              const isActive = currentPage === item.id;
              
              return (
                <button
                  key={item.id}
                  onClick={() => onPageChange(item.id)}
                  className={`px-3 py-2 rounded-lg flex items-center gap-2 transition-all duration-200 whitespace-nowrap flex-shrink-0 ${isActive ? 'active' : ''}`}
                  style={{
                    color: isActive ? 'var(--accent-primary)' : 'var(--text-secondary)',
                    backgroundColor: isActive ? 'var(--status-info-bg)' : 'transparent'
                  }}
                  onMouseEnter={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.color = 'var(--text-primary)';
                      e.currentTarget.style.backgroundColor = 'var(--bg-secondary)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.color = 'var(--text-secondary)';
                      e.currentTarget.style.backgroundColor = 'transparent';
                    }
                  }}
                  title={item.label}
                >
                  <IconComponent className="w-4 h-4" />
                  <span className="hidden sm:inline text-sm font-medium">{item.label}</span>
                </button>
              );
            })}
          </div>

          {/* Status & Theme Selector */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full animate-pulse" style={{backgroundColor: 'var(--status-success)'}}></div>
              <span className="text-small hidden sm:inline" style={{color: 'var(--text-secondary)'}}>
                Système actif
              </span>
            </div>
            <div className="text-meta font-mono" style={{color: 'var(--text-muted)'}}>
              {new Date().toLocaleTimeString('fr-FR', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
            <ThemeSelector />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default MinimalistNavigation;
