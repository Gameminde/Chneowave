import React, { useState, useEffect } from 'react';
import { 
  PlayIcon, 
  StopIcon, 
  PauseIcon,
  SignalIcon,
  ChartBarIcon,
  EyeSlashIcon,
  EyeIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';

// Types pour statistiques temps réel
interface WaveStatistics {
  variance: number;        // Variance d'élévation (m²)
  SHmax: number;          // Hauteur maximale instantanée (m)
  Hmin: number;           // Hauteur minimale (m)
  H13: number;            // H1/3 - Hauteur significative (m)
  periodeMoyenne: number; // Période moyenne (s)
  Tp: number;             // Période pic (s)
  samples: number;        // Nombre d'échantillons
}

interface AcquisitionState {
  status: 'STOPPED' | 'RUNNING' | 'PAUSED';
  elapsedTime: number;
  progress: number;
}

const GoldenRatioAcquisitionPage: React.FC = () => {
  // États principaux
  const [acquisitionState, setAcquisitionState] = useState<AcquisitionState>({
    status: 'STOPPED',
    elapsedTime: 0,
    progress: 0
  });

  const [showAdvancedStats, setShowAdvancedStats] = useState(true);
  const [testDuration, setTestDuration] = useState(300);
  const [samplingRate, setSamplingRate] = useState(100);

  // Données sondes simulées
  const [sensorData, setSensorData] = useState<number[]>([]);
  const [timestamps, setTimestamps] = useState<number[]>([]);

  // Statistiques temps réel
  const [waveStats, setWaveStats] = useState<WaveStatistics>({
    variance: 0,
    SHmax: 0,
    Hmin: 0,
    H13: 0,
    periodeMoyenne: 0,
    Tp: 0,
    samples: 0
  });

  // Simulation acquisition temps réel
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (acquisitionState.status === 'RUNNING') {
      interval = setInterval(() => {
        const now = Date.now();
        const time = now / 1000;
        
        // Génération signal réaliste
        const baseWave = Math.sin(time * 0.4) * 2.5;
        const harmonics = Math.sin(time * 0.8) * 0.8 + Math.sin(time * 1.2) * 0.4;
        const noise = (Math.random() - 0.5) * 0.3;
        const newValue = baseWave + harmonics + noise;

        // Mise à jour données
        setSensorData(prev => [...prev.slice(-200), newValue]);
        setTimestamps(prev => [...prev.slice(-200), now]);

        // Calcul statistiques en temps réel
        setSensorData(currentData => {
          if (currentData.length > 10) {
            const variance = currentData.reduce((sum, val) => {
              const mean = currentData.reduce((s, v) => s + v, 0) / currentData.length;
              return sum + Math.pow(val - mean, 2);
            }, 0) / currentData.length;

            const SHmax = Math.max(...currentData);
            const Hmin = Math.min(...currentData);
            
            // H1/3 - Hauteur significative (1/3 des plus hautes)
            const sortedHeights = [...currentData].sort((a, b) => b - a);
            const H13 = sortedHeights.slice(0, Math.max(1, Math.floor(sortedHeights.length / 3)))
              .reduce((sum, h) => sum + h, 0) / Math.max(1, Math.floor(sortedHeights.length / 3));

            // Période moyenne (estimation zero-crossing)
            let zeroCrossings = 0;
            for (let i = 1; i < currentData.length; i++) {
              if ((currentData[i-1] >= 0 && currentData[i] < 0) || 
                  (currentData[i-1] < 0 && currentData[i] >= 0)) {
                zeroCrossings++;
              }
            }
            const periodeMoyenne = zeroCrossings > 0 ? (currentData.length * 2) / (zeroCrossings * samplingRate) : 0;

            setWaveStats({
              variance: variance,
              SHmax: SHmax,
              Hmin: Hmin,
              H13: H13,
              periodeMoyenne: periodeMoyenne,
              Tp: 8.2 + Math.sin(time * 0.1) * 0.6, // Simulation Tp
              samples: currentData.length
            });
          }
          return currentData;
        });

        // Mise à jour progression
        setAcquisitionState(prev => {
          const newElapsed = prev.elapsedTime + 0.1;
          const newProgress = Math.min((newElapsed / testDuration) * 100, 100);
          
          if (newProgress >= 100) {
            return { ...prev, status: 'STOPPED', elapsedTime: testDuration, progress: 100 };
          }
          
          return { ...prev, elapsedTime: newElapsed, progress: newProgress };
        });
      }, 100);
    }
    return () => clearInterval(interval);
  }, [acquisitionState.status, testDuration, samplingRate]);

  // Contrôles acquisition
  const startAcquisition = () => {
    setAcquisitionState({ status: 'RUNNING', elapsedTime: 0, progress: 0 });
    setSensorData([]);
    setTimestamps([]);
  };

  const pauseAcquisition = () => {
    setAcquisitionState(prev => ({ 
      ...prev, 
      status: prev.status === 'PAUSED' ? 'RUNNING' : 'PAUSED' 
    }));
  };

  const stopAcquisition = () => {
    setAcquisitionState(prev => ({ ...prev, status: 'STOPPED' }));
  };

  // Export des données
  const exportCSV = () => {
    const csvContent = [
      'Timestamp,Elevation,Variance,SHmax,Hmin,H13,PeriodeMoyenne,Tp',
      ...sensorData.map((value, index) => 
        `${timestamps[index] || 0},${value},${waveStats.variance},${waveStats.SHmax},${waveStats.Hmin},${waveStats.H13},${waveStats.periodeMoyenne},${waveStats.Tp}`
      )
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `acquisition_${Date.now()}.csv`;
    a.click();
  };

  const exportJSON = () => {
    const jsonData = {
      metadata: {
        samplingRate,
        testDuration,
        timestamp: new Date().toISOString()
      },
      statistics: waveStats,
      data: sensorData.map((value, index) => ({
        timestamp: timestamps[index] || 0,
        elevation: value
      }))
    };
    
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `acquisition_${Date.now()}.json`;
    a.click();
  };

  // Génération SVG pour graphiques
  const generateWaveform = (data: number[], width: number, height: number) => {
    if (data.length < 2) return '';
    const points = data.slice(-100).map((value, index) => {
      const x = (index / 99) * width;
      const y = height / 2 + (value * height / 8);
      return `${x},${y}`;
    });
    return `M ${points.join(' L ')}`;
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-cyan-900 to-teal-900 p-4">
      {/* Header Contrôles - Golden Ratio φ⁻³ = 0.236 */}
      <div className="mb-4 bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4" 
           style={{ height: '12vh' }}>
        <div className="flex items-center justify-between h-full">
          <div className="flex items-center space-x-4">
            <button
              onClick={startAcquisition}
              disabled={acquisitionState.status === 'RUNNING'}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 min-h-[44px] flex items-center space-x-2"
            >
              <PlayIcon className="w-5 h-5" />
              <span>START</span>
            </button>
            
            <button
              onClick={pauseAcquisition}
              disabled={acquisitionState.status === 'STOPPED'}
              className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 min-h-[44px] flex items-center space-x-2"
            >
              <PauseIcon className="w-5 h-5" />
              <span>{acquisitionState.status === 'PAUSED' ? 'REPRENDRE' : 'PAUSE'}</span>
            </button>
            
            <button
              onClick={stopAcquisition}
              disabled={acquisitionState.status === 'STOPPED'}
              className="bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 min-h-[44px] flex items-center space-x-2"
            >
              <StopIcon className="w-5 h-5" />
              <span>STOP</span>
            </button>
          </div>

          <div className="flex items-center space-x-6">
            <div className="text-cyan-50">
              <span className="text-sm text-cyan-300">Temps: </span>
              <span className="font-mono text-lg font-bold">{formatTime(acquisitionState.elapsedTime)}</span>
            </div>
            
            <div className="w-64">
              <div className="bg-slate-700 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-cyan-500 to-blue-500 h-3 rounded-full transition-all duration-300"
                  style={{ width: `${acquisitionState.progress}%` }}
                ></div>
              </div>
              <div className="text-xs text-cyan-300 mt-1 text-center">
                {acquisitionState.progress.toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Barre Statistiques Compacte */}
      <div className="mb-4 bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2">
              <span className="text-cyan-300 text-sm">Variance:</span>
              <span className="text-cyan-50 font-bold">{waveStats.variance.toFixed(4)} m²</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-cyan-300 text-sm">SHmax:</span>
              <span className="text-cyan-50 font-bold">{waveStats.SHmax.toFixed(2)} m</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-cyan-300 text-sm">Hmin:</span>
              <span className="text-cyan-50 font-bold">{waveStats.Hmin.toFixed(2)} m</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-cyan-300 text-sm">H1/3:</span>
              <span className="text-cyan-50 font-bold">{waveStats.H13.toFixed(2)} m</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-cyan-300 text-sm">Tp:</span>
              <span className="text-cyan-50 font-bold">{waveStats.Tp.toFixed(1)} s</span>
            </div>
          </div>
          
          <button
            onClick={exportCSV}
            disabled={sensorData.length === 0}
            className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 text-white px-6 py-2 rounded-lg font-medium transition-colors duration-200 min-h-[44px] flex items-center space-x-2"
          >
            <ArrowDownTrayIcon className="w-4 h-4" />
            <span>Sauvegarder</span>
          </button>
        </div>
      </div>

      {/* Layout Principal - 3 Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4" style={{ height: '76vh' }}>
        
        {/* Graphique 1 - Sonde Principal */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-cyan-50 flex items-center">
              <SignalIcon className="w-5 h-5 mr-2" />
              Sonde Principal
            </h3>
            <select
              value={1}
              className="bg-slate-700 border border-slate-600 rounded px-3 py-2 text-cyan-50 text-sm min-h-[44px]"
            >
              <option value={1}>Sonde 1</option>
              <option value={2}>Sonde 2</option>
              <option value={3}>Sonde 3</option>
              <option value={4}>Sonde 4</option>
            </select>
          </div>
          
          <div className="h-full bg-slate-800/50 rounded-lg border border-slate-600 flex items-center justify-center" style={{ height: 'calc(100% - 60px)' }}>
            {acquisitionState.status === 'RUNNING' && sensorData.length > 0 ? (
              <svg className="w-full h-full" viewBox="0 0 400 300">
                <path
                  d={generateWaveform(sensorData, 400, 300)}
                  fill="none"
                  stroke="#06b6d4"
                  strokeWidth="2"
                />
              </svg>
            ) : (
              <div className="text-center text-cyan-400">
                <SignalIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Sonde 1</p>
                <p className="text-xs">En attente d'acquisition</p>
              </div>
            )}
          </div>
        </div>

        {/* Graphique 2 - Sonde Secondaire */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-cyan-50 flex items-center">
              <SignalIcon className="w-5 h-5 mr-2" />
              Sonde Secondaire
            </h3>
            <select
              value={2}
              className="bg-slate-700 border border-slate-600 rounded px-3 py-2 text-cyan-50 text-sm min-h-[44px]"
            >
              <option value={1}>Sonde 1</option>
              <option value={2}>Sonde 2</option>
              <option value={3}>Sonde 3</option>
              <option value={4}>Sonde 4</option>
            </select>
          </div>
          
          <div className="h-full bg-slate-800/50 rounded-lg border border-slate-600 flex items-center justify-center" style={{ height: 'calc(100% - 60px)' }}>
            {acquisitionState.status === 'RUNNING' && sensorData.length > 0 ? (
              <svg className="w-full h-full" viewBox="0 0 400 300">
                <path
                  d={generateWaveform(sensorData.map(v => v * 0.8 + Math.sin(Date.now() / 2000) * 0.3), 400, 300)}
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="2"
                />
              </svg>
            ) : (
              <div className="text-center text-cyan-400">
                <SignalIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Sonde 2</p>
                <p className="text-xs">En attente d'acquisition</p>
              </div>
            )}
          </div>
        </div>

        {/* Graphique 3 - Multi-Sondes */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-cyan-50 flex items-center">
              <ChartBarIcon className="w-5 h-5 mr-2" />
              Vue Multi-Sondes Combinée
            </h3>
            
            <div className="flex items-center space-x-4">
              <span className="text-cyan-300 text-sm">Sondes actifs:</span>
              <div className="flex space-x-2">
                {[1, 2, 3, 4].map(id => (
                  <div key={id} className="flex items-center space-x-1">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: ['#06b6d4', '#10b981', '#f59e0b', '#ef4444'][id-1] }}
                    ></div>
                    <span className="text-cyan-50 text-xs">C{id}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="h-full bg-slate-800/50 rounded-lg border border-slate-600 flex items-center justify-center" style={{ height: 'calc(100% - 60px)' }}>
            {acquisitionState.status === 'RUNNING' && sensorData.length > 0 ? (
              <svg className="w-full h-full" viewBox="0 0 800 200">
                {/* Sonde 1 */}
                <path
                  d={generateWaveform(sensorData, 800, 200)}
                  fill="none"
                  stroke="#06b6d4"
                  strokeWidth="2"
                  opacity="0.8"
                />
                {/* Sonde 2 */}
                <path
                  d={generateWaveform(sensorData.map(v => v * 0.8 + Math.sin(Date.now() / 2000) * 0.3), 800, 200)}
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="2"
                  opacity="0.8"
                />
                {/* Sonde 3 */}
                <path
                  d={generateWaveform(sensorData.map(v => v * 1.2 + Math.cos(Date.now() / 1500) * 0.4), 800, 200)}
                  fill="none"
                  stroke="#f59e0b"
                  strokeWidth="2"
                  opacity="0.8"
                />
                {/* Sonde 4 */}
                <path
                  d={generateWaveform(sensorData.map(v => v * 0.9 + Math.sin(Date.now() / 2500) * 0.2), 800, 200)}
                  fill="none"
                  stroke="#ef4444"
                  strokeWidth="2"
                  opacity="0.8"
                />
              </svg>
            ) : (
              <div className="text-center text-cyan-400">
                <ChartBarIcon className="w-16 h-16 mx-auto mb-3 opacity-50" />
                <p className="text-lg font-medium">Visualisation Multi-Sondes</p>
                <p className="text-sm">Comparaison simultanée des signaux</p>
                <p className="text-xs mt-2">En attente d'acquisition</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GoldenRatioAcquisitionPage;
