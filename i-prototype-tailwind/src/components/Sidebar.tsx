import React, { useState, useEffect } from 'react';
import logo from '../assets/logo-chneowave.svg';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  FolderIcon, 
  Cog6ToothIcon, 
  PlayIcon, 
  ChartBarIcon, 
  TableCellsIcon,
  ArrowDownTrayIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline';

const Sidebar: React.FC = () => {
  const location = useLocation();
  const [isExpanded, setIsExpanded] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  // Check if mobile on mount and resize
  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 1024);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  const navItems = [
    { name: 'Tableau de Bord', path: '/', icon: HomeIcon },
    { name: 'Projet', path: '/project', icon: FolderIcon },
    { name: 'Calibration', path: '/calibration', icon: Cog6ToothIcon },
    { name: 'Acquisition', path: '/acquisition', icon: PlayIcon },
    { name: 'Analyse', path: '/analysis', icon: ChartBarIcon },
    { name: 'Statistiques', path: '/statistics', icon: TableCellsIcon },
    { name: 'Export', path: '/export', icon: ArrowDownTrayIcon },
    { name: 'Paramètres', path: '/settings', icon: Cog6ToothIcon },
  ];

  const toggleSidebar = () => setIsExpanded(!isExpanded);

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobile && isExpanded && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsExpanded(false)}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        ${isMobile ? 'fixed' : 'relative'} 
        ${isMobile && !isExpanded ? '-translate-x-full' : 'translate-x-0'}
        ${isExpanded ? 'w-64' : 'w-16'} 
        flex flex-col h-full shadow-lg 
        transition-all duration-200 ease-in-out
        ${isMobile ? 'z-50' : 'z-10'}
      `} style={{
        backgroundColor: 'var(--bg-elevated)',
        color: 'var(--text-primary)',
        borderRight: '1px solid var(--border-primary)'
      }}>
        {/* Header */}
        <div className={`
          px-3 py-4 flex items-center ${isExpanded ? 'gap-3' : 'justify-center'}
        `} style={{ borderBottom: '1px solid var(--border-primary)' }}>
          {/* Toggle Button */}
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-lg transition-colors duration-150"
            style={{ color: 'var(--text-secondary)' }}
            aria-label={isExpanded ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {isExpanded ? (
              <XMarkIcon className="h-5 w-5 text-slate-400" />
            ) : (
              <Bars3Icon className="h-5 w-5 text-slate-400" />
            )}
          </button>
          
          {/* Logo and Brand */}
          {isExpanded && (
            <div className="flex items-center gap-3 overflow-hidden">
              <img src={logo} alt="Logo CHNeoWave" className="h-6 w-auto drop-shadow flex-shrink-0" />
              <div className="min-w-0">
                <div className="text-lg font-semibold leading-tight truncate" style={{ color: 'var(--text-primary)' }}>CHNeoWave</div>
                <div className="text-xs truncate" style={{ color: 'var(--text-secondary)' }}>Suite maritime</div>
              </div>
            </div>
          )}
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 p-2">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const IconComponent = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`
                      group flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-150 relative
                      ${!isExpanded ? 'justify-center' : ''}
                    `}
                    style={{
                      backgroundColor: isActive ? 'var(--status-info-bg)' : 'transparent',
                      color: isActive ? 'var(--accent-primary)' : 'var(--text-secondary)',
                      borderLeft: isActive ? '4px solid var(--accent-primary)' : '4px solid transparent'
                    }}
                    title={!isExpanded ? item.name : undefined}
                  >
                    <IconComponent className={`
                      h-5 w-5 flex-shrink-0
                    `} style={{ color: isActive ? 'var(--accent-primary)' : 'var(--text-secondary)' }} />
                    
                    {isExpanded && (
                      <span className="font-medium text-sm truncate" style={{ color: isActive ? 'var(--accent-primary)' : 'var(--text-secondary)' }}>{item.name}</span>
                    )}
                    
                    {/* Tooltip for collapsed state */}
                    {!isExpanded && (
                      <div className="
                        absolute left-full ml-2 px-2 py-1 
                        bg-slate-800 text-white text-sm rounded 
                        opacity-0 group-hover:opacity-100 
                        transition-opacity duration-150 
                        pointer-events-none z-50
                        whitespace-nowrap
                      ">
                        {item.name}
                      </div>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
        
        {/* Footer */}
        <div className={`${isExpanded ? 'text-left' : 'text-center'}`} style={{
          padding: '1rem .75rem',
          borderTop: '1px solid var(--border-primary)',
          color: 'var(--text-secondary)'
        }}>
          {isExpanded ? (
            <div>
              <div className="font-medium mb-1" style={{ color: 'var(--status-success)' }}>● Connecté</div>
              <div>© {new Date().getFullYear()} CHNeoWave</div>
            </div>
          ) : (
            <div className="w-3 h-3 rounded-full mx-auto" title="Connecté" style={{ backgroundColor: 'var(--status-success)' }} />
          )}
        </div>
      </div>
    </>
  );
};

export default Sidebar;
