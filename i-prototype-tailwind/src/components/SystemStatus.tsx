import React, { useState, useEffect } from 'react';
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  ExclamationTriangleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

interface SystemCheck {
  name: string;
  status: 'success' | 'error' | 'warning' | 'info';
  message: string;
  details?: string;
}

const SystemStatus: React.FC = () => {
  const [checks, setChecks] = useState<SystemCheck[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const performSystemChecks = () => {
      const systemChecks: SystemCheck[] = [];

      // Vérification de CHNeoWave
      if (typeof window !== 'undefined' && window.CHNeoWave) {
        systemChecks.push({
          name: 'CHNeoWave System',
          status: window.CHNeoWave.initialized ? 'success' : 'warning',
          message: window.CHNeoWave.initialized ? 'Système initialisé' : 'Initialisation en cours...',
          details: `Version: ${window.CHNeoWave.version}`
        });
      } else {
        systemChecks.push({
          name: 'CHNeoWave System',
          status: 'error',
          message: 'Système non disponible',
          details: 'Le système global CHNeoWave n\'a pas pu être initialisé'
        });
      }

      // Vérification des thèmes
      const themeElement = document.documentElement;
      const currentTheme = themeElement.getAttribute('data-theme');
      systemChecks.push({
        name: 'Système de Thème',
        status: currentTheme ? 'success' : 'warning',
        message: currentTheme ? `Thème "${currentTheme}" actif` : 'Aucun thème détecté',
        details: currentTheme ? `Variables CSS appliquées` : 'Vérifier la configuration des thèmes'
      });

      // Vérification du localStorage
      try {
        localStorage.setItem('test', 'test');
        localStorage.removeItem('test');
        systemChecks.push({
          name: 'Local Storage',
          status: 'success',
          message: 'Stockage local disponible',
          details: 'Persistance des préférences activée'
        });
      } catch (error) {
        systemChecks.push({
          name: 'Local Storage',
          status: 'error',
          message: 'Stockage local indisponible',
          details: 'Les préférences ne seront pas sauvegardées'
        });
      }

      // Vérification des Event Listeners
      try {
        const testEvent = new CustomEvent('test');
        systemChecks.push({
          name: 'Event System',
          status: 'success',
          message: 'Système d\'événements fonctionnel',
          details: 'Communication inter-composants activée'
        });
      } catch (error) {
        systemChecks.push({
          name: 'Event System',
          status: 'error',
          message: 'Système d\'événements défaillant',
          details: 'Synchronisation des thèmes compromise'
        });
      }

      // Vérification des variables CSS
      const computedStyle = getComputedStyle(document.documentElement);
      const primaryBg = computedStyle.getPropertyValue('--bg-primary').trim();
      systemChecks.push({
        name: 'Variables CSS',
        status: primaryBg ? 'success' : 'warning',
        message: primaryBg ? 'Variables CSS chargées' : 'Variables CSS partielles',
        details: primaryBg ? `--bg-primary: ${primaryBg}` : 'Certaines variables peuvent être manquantes'
      });

      setChecks(systemChecks);
    };

    // Effectuer les vérifications après un délai pour laisser le système s'initialiser
    const timer = setTimeout(performSystemChecks, 1000);
    
    return () => clearTimeout(timer);
  }, []);

  const getStatusIcon = (status: SystemCheck['status']) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon className="w-5 h-5" style={{ color: 'var(--status-success)' }} />;
      case 'error':
        return <XCircleIcon className="w-5 h-5" style={{ color: 'var(--status-error)' }} />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5" style={{ color: 'var(--status-warning)' }} />;
      case 'info':
        return <InformationCircleIcon className="w-5 h-5" style={{ color: 'var(--status-info)' }} />;
    }
  };

  const getStatusColor = (status: SystemCheck['status']) => {
    switch (status) {
      case 'success': return 'var(--status-success)';
      case 'error': return 'var(--status-error)';
      case 'warning': return 'var(--status-warning)';
      case 'info': return 'var(--status-info)';
    }
  };

  if (!isVisible) {
    return (
      <button
        onClick={() => setIsVisible(true)}
        className="fixed bottom-4 right-4 p-2 rounded-lg shadow-lg transition-all z-50"
        style={{
          backgroundColor: 'var(--bg-elevated)',
          border: '1px solid var(--border-primary)',
          color: 'var(--text-secondary)'
        }}
        title="Afficher le statut système"
      >
        <InformationCircleIcon className="w-6 h-6" />
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 w-96 rounded-xl shadow-lg z-50 animate-slide-up"
         style={{
           backgroundColor: 'var(--bg-elevated)',
           border: '1px solid var(--border-primary)'
         }}>
      <div className="p-4 border-b flex items-center justify-between" 
           style={{ borderColor: 'var(--border-primary)' }}>
        <h3 className="font-semibold" style={{ color: 'var(--text-primary)' }}>
          Statut Système
        </h3>
        <button
          onClick={() => setIsVisible(false)}
          className="p-1 rounded transition-colors"
          style={{ color: 'var(--text-secondary)' }}
        >
          ✕
        </button>
      </div>
      
      <div className="p-4 max-h-80 overflow-y-auto">
        {checks.map((check, index) => (
          <div key={index} className="flex items-start space-x-3 mb-3 last:mb-0">
            {getStatusIcon(check.status)}
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <span className="font-medium text-sm" style={{ color: 'var(--text-primary)' }}>
                  {check.name}
                </span>
                <span className="text-xs px-2 py-1 rounded-full" style={{
                  backgroundColor: getStatusColor(check.status) + '20',
                  color: getStatusColor(check.status)
                }}>
                  {check.status.toUpperCase()}
                </span>
              </div>
              <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
                {check.message}
              </p>
              {check.details && (
                <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>
                  {check.details}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-3 border-t text-center" style={{ borderColor: 'var(--border-primary)' }}>
        <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
          Dernière vérification: {new Date().toLocaleTimeString('fr-FR')}
        </span>
      </div>
    </div>
  );
};

export default SystemStatus;
