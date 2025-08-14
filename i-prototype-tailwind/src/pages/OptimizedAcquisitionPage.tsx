import React, { useState, useEffect } from 'react';
import { 
  PlayIcon, 
  StopIcon, 
  PauseIcon,
  SignalIcon,
  CpuChipIcon,
  Battery0Icon,
  WifiIcon
} from '@heroicons/react/24/outline';

// Types pour les données scientifiques
interface WaveMetrics {
  Hs: number;           // Hauteur significative (m)
  Hmax: number;         // Hauteur maximale (m)
  H13: number;          // Hauteur 1/3 supérieur (m)
  Hmean: number;        // Hauteur moyenne (m)
  Tp: number;           // Période pic (s)
  Tz: number;           // Période zéro-crossing (s)
  T13: number;          // Période 1/3 (s)
  meanDirection: number; // Direction moyenne (°)
  directionalSpread: number; // Étalement directionnel (°)
  snr: number;          // Signal-to-noise ratio (dB)
  coherence: number;    // Cohérence inter-sondes
}

interface EnvironmentalData {
  waterTemp: number;    // Température eau (°C)
  airTemp: number;      // Température air (°C)
  pressure: number;     // Pression atmosphérique (hPa)
  windSpeed: number;    // Vitesse vent (m/s)
  windDirection: number; // Direction vent (°)
  tideLevel: number;    // Niveau marée (m)
  currentSpeed: number; // Vitesse courant (m/s)
  currentDirection: number; // Direction courant (°)
}

interface SystemStatus {
  cpu: number;          // % utilisation CPU
  memory: number;       // % utilisation RAM
  diskSpace: number;    // GB libres
  temperature: number;  // °C système
  batteryLevel: number; // % batterie
  networkLatency: number; // ms
}

interface CriticalAlert {
  id: string;
  level: 'CRITICAL' | 'WARNING' | 'INFO';
  message: string;
  timestamp: Date;
  acknowledged: boolean;
}

const OptimizedAcquisitionPage: React.FC = () => {
  // États principaux
  const [acquisitionState, setAcquisitionState] = useState<'STOPPED' | 'RUNNING' | 'PAUSED' | 'ERROR'>('STOPPED');
  const [elapsedTime, setElapsedTime] = useState(0);
  const [samplingRate, setSamplingRate] = useState(100);
  const [testDuration, setTestDuration] = useState(300);
  
  // Données scientifiques temps réel
  const [waveMetrics, setWaveMetrics] = useState<WaveMetrics>({
    Hs: 0, Hmax: 0, H13: 0, Hmean: 0,
    Tp: 0, Tz: 0, T13: 0,
    meanDirection: 0, directionalSpread: 0,
    snr: 0, coherence: 0
  });
  
  const [environmentalData, setEnvironmentalData] = useState<EnvironmentalData>({
    waterTemp: 18.5, airTemp: 22.1, pressure: 1013.2,
    windSpeed: 12.3, windDirection: 280,
    tideLevel: 1.2, currentSpeed: 0.8, currentDirection: 95
  });
  
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    cpu: 45, memory: 64, diskSpace: 847,
    temperature: 42, batteryLevel: 87, networkLatency: 12
  });
  
  const [criticalAlerts, setCriticalAlerts] = useState<CriticalAlert[]>([]);

  // Simulation données temps réel
  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (acquisitionState === 'RUNNING') {
      interval = setInterval(() => {
        setElapsedTime(prev => prev + 0.1);
        
        // Simulation métriques houle
        setWaveMetrics({
          Hs: 2.34 + Math.sin(Date.now() / 10000) * 0.5,
          Hmax: 4.12 + Math.random() * 0.3,
          H13: 2.89 + Math.random() * 0.2,
          Hmean: 1.85 + Math.random() * 0.1,
          Tp: 8.2 + Math.sin(Date.now() / 15000) * 0.8,
          Tz: 6.7 + Math.random() * 0.3,
          T13: 7.4 + Math.random() * 0.2,
          meanDirection: 245 + Math.sin(Date.now() / 20000) * 15,
          directionalSpread: 15 + Math.random() * 5,
          snr: 28.5 + Math.random() * 2,
          coherence: 0.94 + Math.random() * 0.05
        });
        
        // Simulation système
        setSystemStatus(prev => ({
          ...prev,
          cpu: Math.max(20, Math.min(80, prev.cpu + (Math.random() - 0.5) * 5)),
          memory: Math.max(40, Math.min(90, prev.memory + (Math.random() - 0.5) * 3)),
          temperature: Math.max(35, Math.min(65, prev.temperature + (Math.random() - 0.5) * 2))
        }));
      }, 100);
    }
    return () => clearInterval(interval);
  }, [acquisitionState]);

  const startAcquisition = () => {
    setAcquisitionState('RUNNING');
    setElapsedTime(0);
  };

  const pauseAcquisition = () => {
    setAcquisitionState(acquisitionState === 'PAUSED' ? 'RUNNING' : 'PAUSED');
  };

  const stopAcquisition = () => {
    setAcquisitionState('STOPPED');
    setElapsedTime(0);
  };

  const emergencyStop = () => {
    setAcquisitionState('STOPPED');
    setCriticalAlerts(prev => [...prev, {
      id: Date.now().toString(),
      level: 'CRITICAL',
      message: 'ARRÊT D\'URGENCE ACTIVÉ',
      timestamp: new Date(),
      acknowledged: false
    }]);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getStatusColor = () => {
    switch (acquisitionState) {
      case 'RUNNING': return 'bg-green-500';
      case 'PAUSED': return 'bg-yellow-500';
      case 'ERROR': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-cyan-900 to-teal-900 p-4">
      {/* ZONE 1: ALERTES CRITIQUES */}
      <div className="mb-4 bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={emergencyStop}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-bold text-sm transition-colors duration-100 min-w-[120px] min-h-[44px]"
            >
              🛑 ARRÊT URGENCE
            </button>
            <div className="flex items-center space-x-2">
              <div className={`w-4 h-4 rounded-full ${getStatusColor()} animate-pulse`}></div>
              <span className="text-cyan-50 font-semibold">
                {acquisitionState === 'RUNNING' ? 'ACQUISITION EN COURS' :
                 acquisitionState === 'PAUSED' ? 'ACQUISITION SUSPENDUE' :
                 acquisitionState === 'ERROR' ? 'ERREUR SYSTÈME' : 'SYSTÈME PRÊT'}
              </span>
            </div>
          </div>
          <div className="flex items-center space-x-4 text-cyan-300 text-sm">
            <span>SNR: {waveMetrics.snr.toFixed(1)} dB</span>
            <span>Cohérence: {waveMetrics.coherence.toFixed(2)}</span>
            <span>Qualité: {waveMetrics.snr > 20 ? '🟢 EXCELLENTE' : waveMetrics.snr > 15 ? '🟡 BONNE' : '🔴 DÉGRADÉE'}</span>
          </div>
        </div>
      </div>

      {/* ZONE 2: CONTRÔLES ACQUISITION */}
      <div className="mb-4 bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={startAcquisition}
              disabled={acquisitionState === 'RUNNING'}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-100 min-w-[100px] min-h-[44px] flex items-center space-x-2"
            >
              <PlayIcon className="w-5 h-5" />
              <span>START</span>
            </button>
            <button
              onClick={pauseAcquisition}
              disabled={acquisitionState === 'STOPPED'}
              className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-100 min-w-[100px] min-h-[44px] flex items-center space-x-2"
            >
              <PauseIcon className="w-5 h-5" />
              <span>PAUSE</span>
            </button>
            <button
              onClick={stopAcquisition}
              disabled={acquisitionState === 'STOPPED'}
              className="bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-100 min-w-[100px] min-h-[44px] flex items-center space-x-2"
            >
              <StopIcon className="w-5 h-5" />
              <span>STOP</span>
            </button>
          </div>
          
          <div className="flex items-center space-x-6 text-cyan-50">
            <div className="text-center">
              <div className="text-2xl font-bold">{formatTime(elapsedTime)}</div>
              <div className="text-xs text-cyan-300">Temps écoulé</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{Math.round((elapsedTime / testDuration) * 100)}%</div>
              <div className="text-xs text-cyan-300">Progression</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{samplingRate} Hz</div>
              <div className="text-xs text-cyan-300">Fréquence</div>
            </div>
          </div>
        </div>
      </div>

      {/* ZONE 3: LAYOUT 3 COLONNES */}
      <div className="grid grid-cols-4 gap-4 mb-4" style={{ height: '600px' }}>
        
        {/* COLONNE 1: MONITORING TEMPS RÉEL */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4 overflow-y-auto">
          <h3 className="text-lg font-bold text-cyan-50 mb-4 flex items-center">
            <SignalIcon className="w-6 h-6 mr-2" />
            Métriques Houle
          </h3>
          
          {/* Hauteurs */}
          <div className="mb-6">
            <h4 className="text-cyan-300 font-semibold mb-2">HAUTEURS (m)</h4>
            <div className="space-y-2">
              <div className="flex justify-between text-cyan-50">
                <span>Hs:</span>
                <span className="font-bold text-xl">{waveMetrics.Hs.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-cyan-50">
                <span>Hmax:</span>
                <span className="font-bold">{waveMetrics.Hmax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-cyan-50">
                <span>H1/3:</span>
                <span className="font-bold">{waveMetrics.H13.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-cyan-50">
                <span>Hmoy:</span>
                <span className="font-bold">{waveMetrics.Hmean.toFixed(2)}</span>
              </div>
            </div>
          </div>

          {/* Périodes */}
          <div className="mb-6">
            <h4 className="text-cyan-300 font-semibold mb-2">PÉRIODES (s)</h4>
            <div className="space-y-2">
              <div className="flex justify-between text-cyan-50">
                <span>Tp:</span>
                <span className="font-bold text-xl">{waveMetrics.Tp.toFixed(1)}</span>
              </div>
              <div className="flex justify-between text-cyan-50">
                <span>Tz:</span>
                <span className="font-bold">{waveMetrics.Tz.toFixed(1)}</span>
              </div>
              <div className="flex justify-between text-cyan-50">
                <span>T1/3:</span>
                <span className="font-bold">{waveMetrics.T13.toFixed(1)}</span>
              </div>
            </div>
          </div>

          {/* Direction */}
          <div className="mb-6">
            <h4 className="text-cyan-300 font-semibold mb-2">DIRECTION (°)</h4>
            <div className="space-y-2">
              <div className="flex justify-between text-cyan-50">
                <span>Moyenne:</span>
                <span className="font-bold text-xl">{Math.round(waveMetrics.meanDirection)}</span>
              </div>
              <div className="flex justify-between text-cyan-50">
                <span>Étalement:</span>
                <span className="font-bold">±{Math.round(waveMetrics.directionalSpread)}</span>
              </div>
            </div>
          </div>

          {/* Environnement */}
          <div>
            <h4 className="text-cyan-300 font-semibold mb-2">ENVIRONNEMENT</h4>
            <div className="space-y-1 text-sm text-cyan-50">
              <div>🌊 Eau: {environmentalData.waterTemp.toFixed(1)}°C</div>
              <div>🌡️ Air: {environmentalData.airTemp.toFixed(1)}°C</div>
              <div>🔽 Press: {environmentalData.pressure.toFixed(1)} hPa</div>
              <div>💨 Vent: {environmentalData.windSpeed.toFixed(1)} m/s @ {environmentalData.windDirection}°</div>
              <div>🌊 Marée: {environmentalData.tideLevel > 0 ? '+' : ''}{environmentalData.tideLevel.toFixed(1)}m</div>
              <div>➡️ Courant: {environmentalData.currentSpeed.toFixed(1)} m/s @ {environmentalData.currentDirection.toString().padStart(3, '0')}°</div>
            </div>
          </div>
        </div>

        {/* COLONNE 2-3: VISUALISATION PRINCIPALE */}
        <div className="col-span-2 bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4">
          <h3 className="text-lg font-bold text-cyan-50 mb-4">Visualisation Temps Réel</h3>
          
          <div className="h-full bg-slate-800/50 rounded-lg border border-slate-600 flex items-center justify-center relative overflow-hidden">
            {acquisitionState === 'RUNNING' ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-full h-full relative">
                  <svg className="w-full h-full" viewBox="0 0 800 400">
                    <defs>
                      <linearGradient id="waveGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.8"/>
                        <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.1"/>
                      </linearGradient>
                    </defs>
                    <path
                      d={`M 0 200 ${Array.from({ length: 100 }, (_, i) => {
                        const x = i * 8;
                        const y = 200 + Math.sin((i + elapsedTime * 10) * 0.1) * waveMetrics.Hs * 20;
                        return `L ${x} ${y}`;
                      }).join(' ')}`}
                      fill="url(#waveGradient)"
                      stroke="#06b6d4"
                      strokeWidth="2"
                    />
                  </svg>
                </div>
              </div>
            ) : (
              <div className="text-center text-cyan-400">
                <SignalIcon className="w-16 h-16 mx-auto mb-3 opacity-50" />
                <p className="text-lg font-medium">Visualisation Houle</p>
                <p className="text-sm">En attente d'acquisition</p>
              </div>
            )}
          </div>
        </div>

        {/* COLONNE 4: SYSTÈME & CONFIGURATION */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-4 overflow-y-auto">
          <h3 className="text-lg font-bold text-cyan-50 mb-4 flex items-center">
            <CpuChipIcon className="w-6 h-6 mr-2" />
            Système
          </h3>
          
          {/* Performance */}
          <div className="mb-6">
            <h4 className="text-cyan-300 font-semibold mb-2">PERFORMANCE</h4>
            <div className="space-y-2">
              <div className="flex justify-between text-cyan-50 text-sm">
                <span>CPU:</span>
                <span>{systemStatus.cpu}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-cyan-500 h-2 rounded-full transition-all duration-300" style={{ width: `${systemStatus.cpu}%` }}></div>
              </div>
              
              <div className="flex justify-between text-cyan-50 text-sm">
                <span>RAM:</span>
                <span>{systemStatus.memory}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-cyan-500 h-2 rounded-full transition-all duration-300" style={{ width: `${systemStatus.memory}%` }}></div>
              </div>
              
              <div className="flex justify-between text-cyan-50 text-sm">
                <span>Disque:</span>
                <span>{systemStatus.diskSpace} GB</span>
              </div>
              
              <div className="flex justify-between text-cyan-50 text-sm">
                <span>Temp:</span>
                <span className={systemStatus.temperature > 60 ? 'text-red-400' : systemStatus.temperature > 50 ? 'text-yellow-400' : 'text-green-400'}>
                  {systemStatus.temperature}°C
                </span>
              </div>
            </div>
          </div>

          {/* Connectivité */}
          <div className="mb-6">
            <h4 className="text-cyan-300 font-semibold mb-2">CONNECTIVITÉ</h4>
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between text-cyan-50">
                <div className="flex items-center">
                  <WifiIcon className="w-4 h-4 mr-2" />
                  <span>Réseau:</span>
                </div>
                <span className="text-green-400">{systemStatus.networkLatency}ms</span>
              </div>
              <div className="flex items-center justify-between text-cyan-50">
                <div className="flex items-center">
                  <Battery0Icon className="w-4 h-4 mr-2" />
                  <span>Batterie:</span>
                </div>
                <span className={systemStatus.batteryLevel > 50 ? 'text-green-400' : systemStatus.batteryLevel > 20 ? 'text-yellow-400' : 'text-red-400'}>
                  {systemStatus.batteryLevel}%
                </span>
              </div>
            </div>
          </div>

          {/* Configuration rapide */}
          <div>
            <h4 className="text-cyan-300 font-semibold mb-2">CONFIG RAPIDE</h4>
            <div className="space-y-3">
              <div>
                <label className="block text-cyan-50 text-sm mb-1">Fréquence (Hz)</label>
                <select 
                  value={samplingRate}
                  onChange={(e) => setSamplingRate(Number(e.target.value))}
                  className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-cyan-50 text-sm min-h-[44px]"
                  disabled={acquisitionState === 'RUNNING'}
                >
                  <option value={50}>50 Hz</option>
                  <option value={100}>100 Hz</option>
                  <option value={200}>200 Hz</option>
                </select>
              </div>
              <div>
                <label className="block text-cyan-50 text-sm mb-1">Durée (s)</label>
                <input
                  type="number"
                  value={testDuration}
                  onChange={(e) => setTestDuration(Number(e.target.value))}
                  className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-cyan-50 text-sm min-h-[44px]"
                  disabled={acquisitionState === 'RUNNING'}
                  min="60"
                  max="3600"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ZONE 4: STATUS SYSTÈME */}
      <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-3">
        <div className="flex items-center justify-between text-sm text-cyan-300">
          <div className="flex items-center space-x-6">
            <span>Acquisition: {acquisitionState}</span>
            <span>Sondes: 8/8 actifs</span>
            <span>Données: {Math.round(elapsedTime * samplingRate)} échantillons</span>
          </div>
          <div className="flex items-center space-x-6">
            <span>Dernière sauvegarde: {new Date().toLocaleTimeString()}</span>
            <span>Version: CHNeoWave v2.1.0</span>
            <span className="text-green-400">● Système opérationnel</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptimizedAcquisitionPage;
