import React, { useState, useEffect } from 'react';
import ModernNavigation from './ModernNavigation';
import WaveMetricsPanel from './components/WaveMetricsPanel';
import AcquisitionControls from './AcquisitionControls';
import ScientificChartContainer from './ScientificChartContainer';

interface SondeData {
  id: number;
  name: string;
  values: number[];
  timestamps: number[];
  isActive: boolean;
  color: string;
}

interface WaveMetrics {
  Hs: number;
  Tp: number;
  frequency: number;
  samples: number;
  direction: number;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
}

const ModernAcquisitionPage: React.FC = () => {
  const [currentPage, setCurrentPage] = useState('acquisition');
  const [acquisitionStatus, setAcquisitionStatus] = useState<'STOPPED' | 'RUNNING' | 'PAUSED' | 'ERROR'>('STOPPED');
  const [elapsedTime, setElapsedTime] = useState(0);
  const [progress, setProgress] = useState(0);
  const [testDuration] = useState(1800); // 30 minutes
  const [projectName] = useState('Projet Test Océan Atlantique');

  // Données simulées des sondes
  const [sondes] = useState<SondeData[]>([
    {
      id: 1,
      name: 'Sonde 1 - Profondeur 10m',
      values: [],
      timestamps: [],
      isActive: true,
      color: '#3b82f6'
    },
    {
      id: 2,
      name: 'Sonde 2 - Profondeur 20m',
      values: [],
      timestamps: [],
      isActive: true,
      color: '#10b981'
    },
    {
      id: 3,
      name: 'Sonde 3 - Profondeur 30m',
      values: [],
      timestamps: [],
      isActive: true,
      color: '#8b5cf6'
    },
    {
      id: 4,
      name: 'Sonde 4 - Profondeur 40m',
      values: [],
      timestamps: [],
      isActive: true,
      color: '#f59e0b'
    }
  ]);

  // Métriques de houle simulées
  const [waveMetrics] = useState<WaveMetrics>({
    Hs: 2.45,
    Tp: 8.7,
    frequency: 64,
    samples: 0,
    direction: 245,
    quality: 'excellent'
  });

  // Timer pour l'acquisition
  useEffect(() => {
    let interval: number | undefined;
    
    if (acquisitionStatus === 'RUNNING') {
      interval = window.setInterval(() => {
        setElapsedTime(prev => {
          const newTime = prev + 1;
          const newProgress = Math.min((newTime / testDuration) * 100, 100);
          setProgress(newProgress);
          
          // Générer de nouvelles données simulées
          sondes.forEach(sonde => {
            if (sonde.isActive) {
              const newValue = Math.sin(newTime * 0.1 + sonde.id) * 2 + Math.random() * 0.5;
              sonde.values.push(newValue);
              sonde.timestamps.push(newTime);
              
              // Garder seulement les 1000 derniers points
              if (sonde.values.length > 1000) {
                sonde.values.shift();
                sonde.timestamps.shift();
              }
            }
          });
          
          return newTime;
        });
      }, 1000);
    }
    
    return () => {
      if (interval !== undefined) window.clearInterval(interval);
    };
  }, [acquisitionStatus, testDuration, sondes]);

  // Handlers pour les contrôles
  const handleStart = () => {
    setAcquisitionStatus('RUNNING');
    setElapsedTime(0);
    setProgress(0);
  };

  const handlePause = () => {
    setAcquisitionStatus('PAUSED');
  };

  const handleStop = () => {
    setAcquisitionStatus('STOPPED');
    setElapsedTime(0);
    setProgress(0);
  };

  const handleReset = () => {
    setAcquisitionStatus('STOPPED');
    setElapsedTime(0);
    setProgress(0);
    sondes.forEach(sonde => {
      sonde.values = [];
      sonde.timestamps = [];
    });
  };

  const handleConfigure = () => {
    // TODO: Ouvrir modal de configuration
    console.log('Configuration ouverte');
  };

  const handleExport = () => {
    // TODO: Logique d'export
    console.log('Export des données');
  };

  const handlePageChange = (page: string) => {
    setCurrentPage(page);
    // TODO: Navigation entre pages
    console.log('Navigation vers:', page);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation Moderne */}
      <ModernNavigation
        currentPage={currentPage}
        onPageChange={handlePageChange}
        projectName={projectName}
      />

      {/* Contenu Principal */}
      <div className="p-6 space-y-6">
        {/* En-tête de la page */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-white">Acquisition de Données</h1>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Interface moderne pour l'acquisition et la visualisation en temps réel des données de houle
          </p>
        </div>

        {/* Grille principale */}
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-200px)]">
          {/* Colonne gauche - Contrôles et Métriques */}
          <div className="col-span-3 space-y-6">
            {/* Contrôles d'Acquisition */}
            <div className="h-1/2">
              <AcquisitionControls
                status={acquisitionStatus}
                elapsedTime={elapsedTime}
                progress={progress}
                onStart={handleStart}
                onPause={handlePause}
                onStop={handleStop}
                onReset={handleReset}
                onConfigure={handleConfigure}
                testDuration={testDuration}
              />
            </div>

            {/* Métriques de Houle */}
            <div className="h-1/2">
              <WaveMetricsPanel
                metrics={{
                  ...waveMetrics,
                  samples: sondes.reduce((acc, s) => acc + s.values.length, 0)
                }}
                isAcquiring={acquisitionStatus === 'RUNNING'}
              />
            </div>
          </div>

          {/* Colonne centrale - Graphique Principal */}
          <div className="col-span-6">
            <ScientificChartContainer
              sondes={sondes}
              isAcquiring={acquisitionStatus === 'RUNNING'}
              onExport={handleExport}
              onConfigure={handleConfigure}
            />
          </div>

          {/* Colonne droite - Informations et Statuts */}
          <div className="col-span-3 space-y-6">
            {/* Statut des Sondes */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
                <span>Statut des Sondes</span>
              </h3>
              <div className="space-y-3">
                {sondes.map((sonde) => (
                  <div key={sonde.id} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                    <div className="flex items-center space-x-2">
                      <div 
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: sonde.color }}
                      ></div>
                      <span className="text-sm text-slate-300">{sonde.name}</span>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                      sonde.isActive 
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-slate-500/10 text-slate-400 border border-slate-500/20'
                    }`}>
                      {sonde.isActive ? 'Actif' : 'Inactif'}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Informations du Projet */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Informations Projet</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Nom:</span>
                  <span className="text-white font-medium">{projectName}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Date:</span>
                  <span className="text-white font-medium">{new Date().toLocaleDateString('fr-FR')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Heure:</span>
                  <span className="text-white font-medium">{new Date().toLocaleTimeString('fr-FR')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Durée:</span>
                  <span className="text-white font-medium">{Math.floor(testDuration / 60)} min</span>
                </div>
              </div>
            </div>

            {/* Indicateurs Système */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Système</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">CPU</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-slate-700 rounded-full h-2">
                      <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                    </div>
                    <span className="text-sm text-white">45%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">Mémoire</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-slate-700 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: '62%' }}></div>
                    </div>
                    <span className="text-sm text-white">62%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-400">Stockage</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-slate-700 rounded-full h-2">
                      <div className="bg-violet-500 h-2 rounded-full" style={{ width: '28%' }}></div>
                    </div>
                    <span className="text-sm text-white">28%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernAcquisitionPage;
