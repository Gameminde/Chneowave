import React, { useEffect, useState } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';

interface SyncStatus {
  component: string;
  status: 'synced' | 'desynced' | 'unknown';
  lastCheck: Date;
  details?: string;
}

const ThemeSyncValidator: React.FC = () => {
  const { theme } = useUnifiedApp();
  const [syncStatus, setSyncStatus] = useState<SyncStatus[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  // Liste des composants à vérifier
  const componentsToCheck = [
    'ThemeSelector',
    'MinimalistNavigation',
    'MinimalistDashboard',
    'SettingsPage',
    'ModernNavigation',
    'ModernDashboard',
    'App'
  ];

  const checkComponentSync = (componentName: string): SyncStatus => {
    const status: SyncStatus = {
      component: componentName,
      status: 'unknown',
      lastCheck: new Date()
    };

    try {
      // Vérifier si le thème DOM correspond au thème global
      const domTheme = document.documentElement.getAttribute('data-theme');
      const bodyThemeClass = document.body.className.includes(`theme-${theme}`);
      
      if (domTheme === theme && bodyThemeClass) {
        status.status = 'synced';
        status.details = `DOM: ${domTheme}, Body: theme-${theme}`;
      } else {
        status.status = 'desynced';
        status.details = `Attendu: ${theme}, DOM: ${domTheme}, Body: ${bodyThemeClass}`;
      }
    } catch (error) {
      status.status = 'unknown';
      status.details = `Erreur: ${error}`;
    }

    return status;
  };

  useEffect(() => {
    const newStatus = componentsToCheck.map(checkComponentSync);
    setSyncStatus(newStatus);
  }, [theme]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'synced': return 'text-green-600 bg-green-100';
      case 'desynced': return 'text-red-600 bg-red-100';
      default: return 'text-yellow-600 bg-yellow-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'synced': return '✅';
      case 'desynced': return '❌';
      default: return '⚠️';
    }
  };

  if (isThemeLoading) {
    return null;
  }

  return (
    <>
      {/* Bouton de toggle */}
      <button
        onClick={() => setIsVisible(!isVisible)}
        className="fixed bottom-4 right-4 z-50 bg-blue-600 text-white p-2 rounded-full shadow-lg hover:bg-blue-700 transition-colors"
        title="Valider la synchronisation du thème"
      >
        🎨
      </button>

      {/* Panel de validation */}
      {isVisible && (
        <div className="fixed bottom-16 right-4 z-50 bg-white border border-gray-200 rounded-lg shadow-xl p-4 max-w-sm">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-gray-800">Validation Synchronisation</h3>
            <button
              onClick={() => setIsVisible(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <div className="mb-3">
            <div className="text-sm text-gray-600">
              Thème actuel: <span className="font-mono">{theme}</span>
            </div>
            <div className="text-xs text-gray-500">
              DOM: <span className="font-mono">{document.documentElement.getAttribute('data-theme') || 'none'}</span>
            </div>
          </div>

          <div className="space-y-2 max-h-64 overflow-y-auto">
            {syncStatus.map((status, index) => (
              <div
                key={index}
                className={`flex items-center justify-between p-2 rounded text-sm ${getStatusColor(status.status)}`}
              >
                <div className="flex items-center space-x-2">
                  <span>{getStatusIcon(status.status)}</span>
                  <span className="font-medium">{status.component}</span>
                </div>
                <span className="text-xs">
                  {status.status === 'synced' ? 'OK' : status.status === 'desynced' ? 'ERREUR' : 'INCONNU'}
                </span>
              </div>
            ))}
          </div>

          <div className="mt-3 pt-3 border-t border-gray-200">
            <div className="text-xs text-gray-500">
              Synchronisés: {syncStatus.filter(s => s.status === 'synced').length}/{syncStatus.length}
            </div>
            <div className="text-xs text-gray-500">
              Dernière vérification: {new Date().toLocaleTimeString()}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ThemeSyncValidator;
