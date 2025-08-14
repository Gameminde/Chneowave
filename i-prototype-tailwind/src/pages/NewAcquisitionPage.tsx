import React, { useState, useEffect } from 'react';
import { 
  PlayIcon, 
  StopIcon, 
  PauseIcon,
  ChartBarIcon,
  SignalIcon
} from '@heroicons/react/24/outline';

interface AcquisitionStats {
  hMax: number;
  hMin: number;
  h13: number;
  hSignificant: number;
  period: number;
  frequency: number;
}

interface SondeData {
  sondeId: number;
  values: number[];
  timestamps: number[];
  isActive: boolean;
}

const NewAcquisitionPage: React.FC = () => {
  const [samplingRate, setSamplingRate] = useState(100);
  const [testDuration, setTestDuration] = useState(300); // seconds
  const [isAcquiring, setIsAcquiring] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [selectedSensors, setSelectedSensors] = useState([1, 2, 3, 4, 5, 6, 7, 8]);
  const [displaySensor1, setDisplaySensor1] = useState(1);
  const [displaySensor2, setDisplaySensor2] = useState(2);
  const [multiSensorView, setMultiSensorView] = useState([1, 2, 3, 4]);
  
  // Real-time statistics
  const [stats, setStats] = useState<AcquisitionStats>({
    hMax: 0,
    hMin: 0,
    h13: 0,
    hSignificant: 0,
    period: 0,
    frequency: 0
  });

  // Simulated sonde data
  const [, setSensorData] = useState<SondeData[]>(() => 
    Array.from({ length: 16 }, (_, i) => ({
      sondeId: i + 1,
      values: [],
      timestamps: [],
      isActive: selectedSensors.includes(i + 1)
    }))
  );

  // Timer for acquisition
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (isAcquiring && !isPaused) {
      interval = setInterval(() => {
        setElapsedTime(prev => {
          const newTime = prev + 0.1;
          if (newTime >= testDuration) {
            setIsAcquiring(false);
            return testDuration;
          }
          return newTime;
        });
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isAcquiring, isPaused, testDuration]);

  // Simulate data acquisition
  useEffect(() => {
    let dataInterval: ReturnType<typeof setInterval>;
    if (isAcquiring && !isPaused) {
      dataInterval = setInterval(() => {
        const now = Date.now();
        setSensorData(prev => prev.map(sonde => {
          if (sonde.isActive) {
            // Simulate wave data with some realistic patterns
            const time = now / 1000;
            const baseWave = Math.sin(time * 0.5) * 2;
            const noise = (Math.random() - 0.5) * 0.2;
            const newValue = baseWave + noise + (Math.random() - 0.5) * 0.5;
            
            return {
              ...sonde,
              values: [...sonde.values.slice(-500), newValue], // Keep last 500 points
              timestamps: [...sonde.timestamps.slice(-500), now]
            };
          }
          return sonde;
        }));

        // Update statistics
        setStats({
          hMax: 3.2 + Math.random() * 0.5,
          hMin: -2.8 + Math.random() * 0.3,
          h13: 2.1 + Math.random() * 0.3,
          hSignificant: 2.4 + Math.random() * 0.2,
          period: 8.2 + Math.random() * 0.5,
          frequency: samplingRate
        });
      }, 1000 / samplingRate);
    }
    return () => clearInterval(dataInterval);
  }, [isAcquiring, isPaused, samplingRate]);

  const startAcquisition = () => {
    setIsAcquiring(true);
    setIsPaused(false);
    setElapsedTime(0);
    // Reset sonde data
    setSensorData(prev => prev.map(sonde => ({
      ...sonde,
      values: [],
      timestamps: [],
      isActive: selectedSensors.includes(sonde.sondeId)
    })));
  };

  const pauseAcquisition = () => {
    setIsPaused(!isPaused);
  };

  const stopAcquisition = () => {
    setIsAcquiring(false);
    setIsPaused(false);
  };

  const toggleSensor = (sondeId: number) => {
    if (!isAcquiring) {
      setSelectedSensors(prev => 
        prev.includes(sondeId) 
          ? prev.filter(id => id !== sondeId)
          : [...prev, sondeId]
      );
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const progress = (elapsedTime / testDuration) * 100;

  return (
    <div className="h-full overflow-hidden" style={{backgroundColor: 'var(--bg-primary)'}}>
      
      {/* Fixed Header */}
      <div className="h-20 flex items-center px-8 shadow-lg themed-nav" style={{background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))'}}>
        <div className="flex items-center space-x-4">
          <SignalIcon className="w-8 h-8" style={{ color: 'var(--text-inverse)' }} />
          <div>
            <h1 className="text-2xl font-bold" style={{ color: 'var(--text-inverse)' }}>Acquisition de Données</h1>
            <p className="text-sm" style={{ color: 'var(--text-inverse)' }}>Mesure en temps réel des élévations de surface</p>
          </div>
        </div>
        
        <div className="ml-auto flex items-center space-x-6">
          <div className="text-right">
            <p className="text-sm" style={{ color: 'var(--text-inverse)' }}>Temps Écoulé</p>
            <p className="font-mono text-xl" style={{ color: 'var(--text-inverse)' }}>{formatTime(elapsedTime)}</p>
          </div>
          <div className="text-right">
            <p className="text-sm" style={{ color: 'var(--text-inverse)' }}>Progression</p>
            <p className="font-bold text-xl" style={{ color: 'var(--text-inverse)' }}>{progress.toFixed(1)}%</p>
          </div>
        </div>
      </div>

      {/* Main Content - Fixed Height, No Scroll */}
      <div className="h-[calc(100vh-5rem)] p-6 grid grid-rows-3 gap-6">
        
        {/* Top Row - Configuration & Control */}
        <div className="grid grid-cols-12 gap-6">
          
          {/* Configuration Panel */}
          <div className="col-span-4 themed-card rounded-2xl p-6">
            <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Configuration d'Acquisition</h3>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                  Fréquence (Hz)
                </label>
                <select
                  value={samplingRate}
                  onChange={(e) => setSamplingRate(Number(e.target.value))}
                  disabled={isAcquiring}
                  className="themed-input w-full px-3 py-2 rounded-lg"
                >
                  <option value={32}>32 Hz</option>
                  <option value={50}>50 Hz</option>
                  <option value={100}>100 Hz</option>
                  <option value={200}>200 Hz</option>
                  <option value={500}>500 Hz</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                  Durée (s)
                </label>
                <select
                  value={testDuration}
                  onChange={(e) => setTestDuration(Number(e.target.value))}
                  disabled={isAcquiring}
                  className="themed-input w-full px-3 py-2 rounded-lg"
                >
                  <option value={60}>1 minute</option>
                  <option value={300}>5 minutes</option>
                  <option value={600}>10 minutes</option>
                  <option value={1800}>30 minutes</option>
                  <option value={3600}>1 heure</option>
                </select>
              </div>
            </div>

            {/* Control Buttons */}
            <div className="flex space-x-3">
              {!isAcquiring ? (
                <button
                  onClick={startAcquisition}
                  disabled={selectedSensors.length === 0}
                  className="themed-btn themed-btn-primary flex-1 px-4 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2"
                >
                  <PlayIcon className="w-5 h-5" />
                  <span>Commencer</span>
                </button>
              ) : (
                <>
                  <button
                    onClick={pauseAcquisition}
                    className="flex-1 px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
                    style={{ backgroundColor: 'var(--status-warning)', color: 'var(--text-inverse)' }}
                  >
                    <PauseIcon className="w-5 h-5" />
                    <span>{isPaused ? 'Reprendre' : 'Pause'}</span>
                  </button>
                  
                  <button
                    onClick={stopAcquisition}
                    className="flex-1 px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
                    style={{ backgroundColor: 'var(--status-error)', color: 'var(--text-inverse)' }}
                  >
                    <StopIcon className="w-5 h-5" />
                    <span>Arrêter</span>
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Sonde Selection */}
          <div className="col-span-4 themed-card rounded-2xl p-6">
            <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Sélection des Sondes</h3>
            
            <div className="grid grid-cols-4 gap-2 mb-4">
              {Array.from({ length: 16 }, (_, i) => {
                const sondeId = i + 1;
                const isSelected = selectedSensors.includes(sondeId);
                
                return (
                  <button
                    key={sondeId}
                    onClick={() => toggleSensor(sondeId)}
                    disabled={isAcquiring}
                    className={`p-2 rounded-lg text-xs font-medium transition-all`}
                    style={{
                      border: `1px solid ${isSelected ? 'var(--status-success)' : 'var(--border-primary)'}`,
                      backgroundColor: isSelected ? 'var(--status-success-bg)' : 'var(--bg-secondary)',
                      color: isSelected ? 'var(--status-success)' : 'var(--text-secondary)'
                    }}
                  >
                    #{sondeId}
                  </button>
                );
              })}
            </div>
            
            <div className="text-center text-sm" style={{ color: 'var(--text-secondary)' }}>
              {selectedSensors.length} sondes sélectionnées
            </div>
          </div>

          {/* Real-time Statistics */}
          <div className="col-span-4 themed-card rounded-2xl p-6">
            <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Statistiques Temps Réel</h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-lg p-3 text-center" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                <p className="text-xs mb-1" style={{ color: 'var(--text-secondary)' }}>H max</p>
                <p className="font-mono text-lg" style={{ color: 'var(--text-primary)' }}>{stats.hMax.toFixed(2)} m</p>
              </div>
              
              <div className="rounded-lg p-3 text-center" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                <p className="text-xs mb-1" style={{ color: 'var(--text-secondary)' }}>H min</p>
                <p className="font-mono text-lg" style={{ color: 'var(--text-primary)' }}>{stats.hMin.toFixed(2)} m</p>
              </div>
              
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <p className="text-slate-400 text-xs mb-1">H 1/3</p>
                <p className="text-white font-mono text-lg">{stats.h13.toFixed(2)} m</p>
              </div>
              
              <div className="bg-slate-700/50 rounded-lg p-3 text-center">
                <p className="text-slate-400 text-xs mb-1">H significative</p>
                <p className="text-white font-mono text-lg">{stats.hSignificant.toFixed(2)} m</p>
              </div>
            </div>
          </div>
        </div>

        {/* Middle Row - Individual Sonde Graphs */}
        <div className="grid grid-cols-2 gap-6">
          
          {/* Sonde 1 Graph */}
          <div className="themed-card rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Sonde Individuelle A</h3>
              <select
                value={displaySensor1}
                onChange={(e) => setDisplaySensor1(Number(e.target.value))}
                className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-white text-sm"
              >
                {selectedSensors.map(id => (
                  <option key={id} value={id}>Sonde #{id}</option>
                ))}
              </select>
            </div>
            
            <div className="h-40 bg-slate-900/50 rounded-lg border border-slate-600 flex items-center justify-center relative overflow-hidden">
              {isAcquiring ? (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-full h-full relative">
                    {/* Simulated waveform */}
                    <svg className="w-full h-full" viewBox="0 0 400 160">
                      <defs>
                        <linearGradient id="waveGradient1" x1="0%" y1="0%" x2="0%" y2="100%">
                          <stop offset="0%" stopColor="#10b981" stopOpacity="0.8"/>
                          <stop offset="100%" stopColor="#10b981" stopOpacity="0.1"/>
                        </linearGradient>
                      </defs>
                      <path
                        d={`M 0 80 ${Array.from({ length: 50 }, (_, i) => {
                          const x = i * 8;
                          const y = 80 + Math.sin((i + elapsedTime * 10) * 0.3) * 20 + Math.sin((i + elapsedTime * 5) * 0.1) * 10;
                          return `L ${x} ${y}`;
                        }).join(' ')} L 400 80 L 400 160 L 0 160 Z`}
                        fill="url(#waveGradient1)"
                        stroke="#10b981"
                        strokeWidth="2"
                      />
                    </svg>
                  </div>
                </div>
              ) : (
                <div className="text-center text-slate-400">
                  <ChartBarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">Graphique Sonde #{displaySensor1}</p>
                  <p className="text-xs">En attente d'acquisition</p>
                </div>
              )}
            </div>
          </div>

          {/* Sonde 2 Graph */}
          <div className="themed-card rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Sonde Individuelle B</h3>
              <select
                value={displaySensor2}
                onChange={(e) => setDisplaySensor2(Number(e.target.value))}
                className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-white text-sm"
              >
                {selectedSensors.map(id => (
                  <option key={id} value={id}>Sonde #{id}</option>
                ))}
              </select>
            </div>
            
            <div className="h-40 bg-slate-900/50 rounded-lg border border-slate-600 flex items-center justify-center relative overflow-hidden">
              {isAcquiring ? (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-full h-full relative">
                    <svg className="w-full h-full" viewBox="0 0 400 160">
                      <defs>
                        <linearGradient id="waveGradient2" x1="0%" y1="0%" x2="0%" y2="100%">
                          <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.8"/>
                          <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.1"/>
                        </linearGradient>
                      </defs>
                      <path
                        d={`M 0 80 ${Array.from({ length: 50 }, (_, i) => {
                          const x = i * 8;
                          const y = 80 + Math.sin((i + elapsedTime * 8) * 0.4) * 25 + Math.sin((i + elapsedTime * 3) * 0.15) * 8;
                          return `L ${x} ${y}`;
                        }).join(' ')} L 400 80 L 400 160 L 0 160 Z`}
                        fill="url(#waveGradient2)"
                        stroke="#3b82f6"
                        strokeWidth="2"
                      />
                    </svg>
                  </div>
                </div>
              ) : (
                <div className="text-center text-slate-400">
                  <ChartBarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">Graphique Sonde #{displaySensor2}</p>
                  <p className="text-xs">En attente d'acquisition</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Bottom Row - Multi-Sonde Graph */}
        <div className="themed-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Vue Multi-Sondes</h3>
            <div className="flex items-center space-x-4">
              <span className="text-slate-400 text-sm">Sondes affichées:</span>
              <div className="flex space-x-2">
                {multiSensorView.map((sondeId, index) => (
                  <select
                    key={index}
                    value={sondeId}
                    onChange={(e) => {
                      const newView = [...multiSensorView];
                      newView[index] = Number(e.target.value);
                      setMultiSensorView(newView);
                    }}
                    className="px-2 py-1 bg-slate-700 border border-slate-600 rounded text-white text-xs"
                  >
                    {selectedSensors.map(id => (
                      <option key={id} value={id}>#{id}</option>
                    ))}
                  </select>
                ))}
              </div>
            </div>
          </div>
          
          <div className="h-48 bg-slate-900/50 rounded-lg border border-slate-600 flex items-center justify-center relative overflow-hidden">
            {isAcquiring ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-full h-full relative">
                  <svg className="w-full h-full" viewBox="0 0 400 192">
                    <defs>
                      {multiSensorView.map((_, index) => (
                        <linearGradient key={index} id={`multiGradient${index}`} x1="0%" y1="0%" x2="0%" y2="100%">
                          <stop offset="0%" stopColor={['#ef4444', '#f59e0b', '#10b981', '#3b82f6'][index]} stopOpacity="0.6"/>
                          <stop offset="100%" stopColor={['#ef4444', '#f59e0b', '#10b981', '#3b82f6'][index]} stopOpacity="0.1"/>
                        </linearGradient>
                      ))}
                    </defs>
                    {multiSensorView.map((sondeId, index) => (
                      <path
                        key={sondeId}
                        d={`M 0 96 ${Array.from({ length: 50 }, (_, i) => {
                          const x = i * 8;
                          const y = 96 + Math.sin((i + elapsedTime * (7 + index)) * (0.3 + index * 0.1)) * (15 + index * 5);
                          return `L ${x} ${y}`;
                        }).join(' ')}`}
                        fill="none"
                        stroke={['#ef4444', '#f59e0b', '#10b981', '#3b82f6'][index]}
                        strokeWidth="2"
                        opacity="0.8"
                      />
                    ))}
                  </svg>
                </div>
              </div>
            ) : (
              <div className="text-center text-slate-400">
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

export default NewAcquisitionPage;
