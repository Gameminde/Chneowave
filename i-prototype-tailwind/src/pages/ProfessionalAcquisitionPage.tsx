import React, { useState, useEffect, useRef } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';
import { 
  PlayIcon, 
  PauseIcon,
  StopIcon,
  DocumentArrowDownIcon,
  Cog6ToothIcon,
  SignalIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  WifiIcon,
  ChartBarIcon,
  ClockIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';

interface SondeData {
  id: number;
  name: string;
  status: 'active' | 'inactive' | 'error';
  snr: number;
  saturation: number;
  gaps: number;
  lastValue: number;
  frequency: number;
}

interface WaveData {
  timestamp: number;
  height: number;
  period: number;
  direction?: number;
}

const ProfessionalAcquisitionPage: React.FC = () => {
  // 🔄 INTÉGRATION UNIFIÉE : Utilisation du contexte unifié selon prompt ultra-précis
  const { 
    currentTheme, 
    acquisitionData, 
    isAcquiring,
    acquisitionConfig,
    sondes,
    sensorStatuses,
    isConnectedToBackend,
    startAcquisition,
    stopAcquisition,
    pauseAcquisition,
    resumeAcquisition,
    updateAcquisitionConfig,
    toggleSensor,
    addNotification
  } = useUnifiedApp();

  // État local UI uniquement (pas de duplication avec le contexte global)
  const [duration, setDuration] = useState(0);
  const [samplingRate, setSamplingRate] = useState(acquisitionConfig?.samplingRate || 1000); // Hz
  const [selectedChannels, setSelectedChannels] = useState<number[]>([0, 1]);
  const [realTimeData, setRealTimeData] = useState<WaveData[]>([]);

  const intervalRef = useRef<number | null>(null);
  const startTimeRef = useRef<number | null>(null);

  // 🔄 CATÉGORIE C : Connecter vraies données backend au lieu de simulation
  useEffect(() => {
    // Utiliser les vraies données d'acquisition du contexte unifié
    if (acquisitionData && isAcquiring) {
      const now = Date.now();
      
      // Convertir les données backend en format UI
      const channels = Object.keys(acquisitionData.channel_data);
      if (channels.length > 0) {
        const primaryChannel = channels[0];
        const channelData = acquisitionData.channel_data[primaryChannel];
        
        if (channelData && channelData.length > 0) {
          const lastValue = channelData[channelData.length - 1];
          
          const newData: WaveData = {
            timestamp: acquisitionData.timestamp,
            height: lastValue, // Vraie valeur du sonde
            period: 8.5, // À calculer depuis l'analyse spectrale backend
            direction: 240 // À obtenir depuis les sondes directionnels
          };
          
          setRealTimeData(prev => {
            const updated = [...prev, newData];
            return updated.slice(-100); // Garder seulement les 100 derniers points
          });
        }
      }
      
      // Mettre à jour la durée depuis les données backend
      setDuration(acquisitionData.duration_elapsed);
    }

    // Fallback : simulation pour développement si pas de données backend
    if (isAcquiring && !acquisitionData) {
      intervalRef.current = setInterval(() => {
        const now = Date.now();
        const newData: WaveData = {
          timestamp: now,
          height: Math.sin(now * 0.001) * 2.5 + Math.random() * 0.3,
          period: 8 + Math.sin(now * 0.0005) * 2 + Math.random() * 0.5,
          direction: 238 + Math.random() * 10 - 5
        };
        
        setRealTimeData(prev => {
          const updated = [...prev, newData];
          return updated.slice(-100);
        });

        if (startTimeRef.current) {
          setDuration(Math.floor((now - startTimeRef.current) / 1000));
        }
      }, 1000 / 2); // 2 Hz pour simulation UI
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [acquisitionData, isAcquiring, samplingRate]);

  // 🔄 FONCTIONS DE CONTRÔLE INTÉGRÉES : Utilisation des actions du contexte unifié
  const handleStart = async () => {
    try {
      const config = {
        samplingRate: samplingRate,
        duration: 3600, // 1 heure par défaut
        channels: selectedChannels,
        voltageRange: '±5V' as const,
        bufferSize: 10000,
        triggerMode: 'software' as const,
        preTriggerSamples: 0
      };

      await startAcquisition(config);
      
      startTimeRef.current = Date.now();
      setDuration(0);
      setRealTimeData([]);
      
      addNotification({
        level: 'info',
        message: 'Acquisition démarrée avec succès',
        timestamp: Date.now(),
        source: 'acquisition_ui'
      });
      
    } catch (error) {
      console.error('Erreur démarrage acquisition:', error);
    }
  };

  const handlePause = async () => {
    try {
      if (isAcquiring) {
        await pauseAcquisition();
      } else {
        await resumeAcquisition();
      }
    } catch (error) {
      console.error('Erreur pause/resume acquisition:', error);
    }
  };

  const handleStop = async () => {
    try {
      await stopAcquisition();
      startTimeRef.current = null;
      setDuration(0);
      
      addNotification({
        level: 'info',
        message: 'Acquisition arrêtée',
        timestamp: Date.now(),
        source: 'acquisition_ui'
      });
      
    } catch (error) {
      console.error('Erreur arrêt acquisition:', error);
    }
  };

  const handleSave = async () => {
    try {
      const sessionData = {
        timestamp: new Date().toISOString(),
        duration: duration,
        samplingRate: samplingRate,
        channels: selectedChannels,
        data: realTimeData,
        totalSamples: realTimeData.length,
        sondes: sondes.filter(s => selectedChannels.includes(s.channel))
      };

      const dataStr = JSON.stringify(sessionData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `acquisition_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      addNotification({
        level: 'info',
        message: 'Données sauvegardées avec succès',
        timestamp: Date.now(),
        source: 'acquisition_ui'
      });
      
    } catch (error) {
      console.error('Erreur sauvegarde:', error);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircleIcon className="w-4 h-4 text-green-500" />;
      case 'error': return <ExclamationTriangleIcon className="w-4 h-4 text-red-500" />;
      default: return <div className="w-4 h-4 rounded-full bg-gray-400" />;
    }
  };

  const currentHeight = realTimeData.length > 0 ? realTimeData[realTimeData.length - 1].height : 0;
  const currentPeriod = realTimeData.length > 0 ? realTimeData[realTimeData.length - 1].period : 0;

  return (
    <div className="h-full flex flex-col" style={{ backgroundColor: 'var(--bg-primary)' }}>
      {/* Header Professional */}
      <div className="h-16 flex items-center justify-between px-6 border-b" style={{
        backgroundColor: 'var(--bg-elevated)',
        borderColor: 'var(--border-primary)'
      }}>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <SignalIcon className="w-6 h-6" style={{ color: 'var(--accent-primary)' }} />
            <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
              Acquisition Temps Réel
            </h1>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            acquisitionState === 'running' ? 'bg-green-100 text-green-800' :
            acquisitionState === 'paused' ? 'bg-yellow-100 text-yellow-800' :
            'bg-gray-100 text-gray-800'
          }`}>
            {acquisitionState === 'running' ? 'EN COURS' :
             acquisitionState === 'paused' ? 'PAUSE' : 'ARRÊTÉ'}
              </div>
            </div>

        {/* Contrôles principaux */}
            <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-sm" style={{ color: 'var(--text-secondary)' }}>
            <ClockIcon className="w-4 h-4" />
            <span>{formatTime(duration)}</span>
          </div>
          
          {/* 🔄 CONTRÔLES INTÉGRÉS : Utilisation de l'état unifié */}
          <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
              <button
              onClick={handleStart}
              disabled={isAcquiring || !isConnectedToBackend}
              className={`p-2 rounded-md transition-colors ${
                isAcquiring || !isConnectedToBackend
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-green-500 text-white hover:bg-green-600'
              }`}
              title={!isConnectedToBackend ? 'Backend non connecté' : ''}
            >
              <PlayIcon className="w-4 h-4" />
              </button>
              
              <button
              onClick={handlePause}
              disabled={!isAcquiring}
              className={`p-2 rounded-md transition-colors ${
                !isAcquiring
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-yellow-500 text-white hover:bg-yellow-600'
              }`}
            >
              <PauseIcon className="w-4 h-4" />
              </button>
              
              <button
              onClick={handleStop}
              disabled={!isAcquiring}
              className={`p-2 rounded-md transition-colors ${
                !isAcquiring
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-red-500 text-white hover:bg-red-600'
              }`}
            >
              <StopIcon className="w-4 h-4" />
            </button>
          </div>

          <button
            onClick={handleSave}
            disabled={realTimeData.length === 0}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
              realTimeData.length === 0
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            <DocumentArrowDownIcon className="w-4 h-4" />
            <span>Sauvegarder</span>
              </button>
            </div>
          </div>

      {/* Corps principal */}
      <div className="flex-1 flex overflow-hidden">
        {/* Panneau de contrôle gauche */}
        <div className="w-80 border-r flex flex-col" style={{
          backgroundColor: 'var(--bg-secondary)',
          borderColor: 'var(--border-primary)'
        }}>
          {/* Configuration */}
          <div className="p-4 border-b" style={{ borderColor: 'var(--border-primary)' }}>
            <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
              Configuration
            </h3>
            
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                  Fréquence d'échantillonnage (Hz)
                </label>
                <select
                  value={samplingRate}
                  onChange={(e) => setSamplingRate(Number(e.target.value))}
                  disabled={acquisitionState === 'running'}
                  className="w-full px-3 py-2 rounded-md border text-sm"
                  style={{
                    backgroundColor: 'var(--bg-primary)',
                    borderColor: 'var(--border-secondary)',
                    color: 'var(--text-primary)'
                  }}
                >
                  <option value={0.5}>0.5 Hz</option>
                  <option value={1}>1 Hz</option>
                  <option value={2}>2 Hz</option>
                  <option value={4}>4 Hz</option>
                  <option value={8}>8 Hz</option>
                </select>
              </div>
            </div>
          </div>

          {/* État des sondes */}
          <div className="flex-1 p-4">
            <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
              État des Sondes
            </h3>
            
            <div className="space-y-2">
              {/* 🔄 SONDES INTÉGRÉS : Utilisation des sondes du contexte unifié */}
              {sondes.map((sonde) => {
                const sensorStatus = sensorStatuses.get(sonde.id);
                const isSelected = selectedChannels.includes(sonde.channel);
                
                return (
                  <div
                    key={sonde.id}
                    className={`p-3 rounded-lg border ${
                      isSelected ? 'ring-2 ring-blue-500' : ''
                    }`}
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: isSelected ? 'var(--accent-primary)' : 'var(--border-primary)'
                    }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        {sonde.isActive ? (
                          <CheckCircleIcon className="w-4 h-4 text-green-500" />
                        ) : (
                          <ExclamationTriangleIcon className="w-4 h-4 text-red-500" />
                        )}
                        <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                          {sonde.id} (Ch{sonde.channel})
                        </span>
                      </div>
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedChannels([...selectedChannels, sonde.channel]);
                          } else {
                            setSelectedChannels(selectedChannels.filter(ch => ch !== sonde.channel));
                          }
                          toggleSensor(sonde.id, e.target.checked);
                        }}
                        disabled={isAcquiring || !sonde.isActive}
                        className="rounded"
                      />
                    </div>
                    
                    {sonde.isActive && (
                      <div className="grid grid-cols-2 gap-2 text-xs" style={{ color: 'var(--text-secondary)' }}>
                        <div>
                          <span className="block">SNR</span>
                          <span className="font-mono">{sonde.snr?.toFixed(1) || '0.0'} dB</span>
                        </div>
                        <div>
                          <span className="block">Valeur</span>
                          <span className="font-mono">{sonde.lastValue?.toFixed(2) || '0.00'} {sonde.unit}</span>
                        </div>
                        <div>
                          <span className="block">Sat.</span>
                          <span className="font-mono">{(sonde.saturation * 100).toFixed(1)}%</span>
                        </div>
                        <div>
                          <span className="block">Lacunes</span>
                          <span className="font-mono">{sonde.gaps}</span>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Zone graphiques principale */}
        <div className="flex-1 flex flex-col">
          {/* Métriques temps réel */}
          <div className="h-20 border-b flex items-center justify-around px-6" style={{
            backgroundColor: 'var(--bg-secondary)',
            borderColor: 'var(--border-primary)'
          }}>
            <div className="text-center">
              <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Hauteur Actuelle</div>
              <div className="text-xl font-bold" style={{ color: 'var(--accent-primary)' }}>
                {currentHeight.toFixed(2)} m
          </div>
        </div>
            <div className="text-center">
              <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Période</div>
              <div className="text-xl font-bold" style={{ color: 'var(--accent-secondary)' }}>
                {currentPeriod.toFixed(1)} s
          </div>
            </div>
            <div className="text-center">
              <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Points Acquis</div>
              <div className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
                {realTimeData.length}
              </div>
            </div>
            <div className="text-center">
              <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Sondes Actifs</div>
              <div className="text-xl font-bold" style={{ color: 'var(--status-success)' }}>
                {sondes.filter(s => s.status === 'active' && selectedSensors.includes(s.id)).length}
          </div>
        </div>
      </div>

          {/* Graphiques */}
          <div className="flex-1 p-4">
            <div className="grid grid-cols-2 gap-4 h-full">
              {/* Graphique 1: Série temporelle */}
              <div className="rounded-lg border p-4" style={{
                backgroundColor: 'var(--bg-primary)',
                borderColor: 'var(--border-primary)'
              }}>
          <div className="flex items-center justify-between mb-4">
                  <h4 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                    Élévation Temps Réel
                  </h4>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs px-2 py-1 rounded-full" style={{
                      backgroundColor: 'var(--status-info-bg)',
                      color: 'var(--status-info)'
                    }}>
                      {samplingRate} Hz
                    </span>
                  </div>
          </div>
          
                {/* Simuler un graphique */}
                <div className="h-64 flex items-end justify-center space-x-1" style={{
                  backgroundColor: 'var(--bg-secondary)',
                  borderRadius: '4px'
                }}>
                  {realTimeData.slice(-50).map((data, index) => (
                    <div
                      key={index}
                      className="bg-blue-500 w-2 transition-all duration-300"
                      style={{
                        height: `${Math.max(5, (data.height + 3) * 20)}px`,
                        backgroundColor: 'var(--accent-primary)'
                      }}
                    />
                  ))}
                  {realTimeData.length === 0 && (
                    <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                <ChartBarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p className="text-sm">Démarrer l'acquisition pour voir les données</p>
              </div>
            )}
          </div>
        </div>

              {/* Graphique 2: Spectre */}
              <div className="rounded-lg border p-4" style={{
                backgroundColor: 'var(--bg-primary)',
                borderColor: 'var(--border-primary)'
              }}>
          <div className="flex items-center justify-between mb-4">
                  <h4 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                    Analyse Spectrale
                  </h4>
                  <AdjustmentsHorizontalIcon className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
          </div>
          
                <div className="h-64 flex items-end justify-center" style={{
                  backgroundColor: 'var(--bg-secondary)',
                  borderRadius: '4px'
                }}>
                  <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                    <WifiIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">Spectre de fréquence</p>
                    <p className="text-xs">Analyse FFT en temps réel</p>
          </div>
        </div>
      </div>

              {/* Graphique 3: Vue combinée */}
              <div className="col-span-2 rounded-lg border p-4" style={{
                backgroundColor: 'var(--bg-primary)',
                borderColor: 'var(--border-primary)'
              }}>
        <div className="flex items-center justify-between mb-4">
                  <h4 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                    Vue Multi-Sondes Synchronisée
                  </h4>
                  <div className="flex items-center space-x-2">
                    {selectedSensors.map(sondeId => {
                      const sonde = sondes.find(s => s.id === sondeId);
                      return sonde ? (
                        <span
                          key={sondeId}
                          className="text-xs px-2 py-1 rounded-full"
                          style={{
                            backgroundColor: `hsl(${sondeId * 60}, 70%, 90%)`,
                            color: `hsl(${sondeId * 60}, 70%, 30%)`
                          }}
                        >
                          {sonde.name}
                        </span>
                      ) : null;
                    })}
          </div>
        </div>
        
                <div className="h-32 flex items-center justify-center" style={{
                  backgroundColor: 'var(--bg-secondary)',
                  borderRadius: '4px'
                }}>
                  <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                    <SignalIcon className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">Superposition des signaux</p>
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

export default ProfessionalAcquisitionPage;