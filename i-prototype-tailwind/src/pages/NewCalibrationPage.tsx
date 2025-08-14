import React, { useState, useEffect } from 'react';
import { 
  CheckIcon, 
  PlayIcon, 
  StopIcon,
  ChartBarIcon,
  CogIcon
} from '@heroicons/react/24/outline';

interface CalibrationPoint {
  height: number; // in cm
  voltage: number; // measured voltage
  confirmed: boolean;
  timestamp?: Date;
}

interface SensorCalibration {
  sondeId: number;
  points: CalibrationPoint[];
  linearFit?: {
    slope: number;
    offset: number;
    r2: number;
  };
  status: 'idle' | 'calibrating' | 'completed';
}

const NewCalibrationPage: React.FC = () => {
  const [selectedSensorCount, setSelectedSensorCount] = useState(8);
  const [selectedPointCount, setSelectedPointCount] = useState(3);
  const [activeSensor, setActiveSensor] = useState(1);
  const [currentPointIndex, setCurrentPointIndex] = useState(0);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [currentVoltage, setCurrentVoltage] = useState(0);
  
  // Initialize calibration data
  const [calibrations, setCalibrations] = useState<SensorCalibration[]>(() => {
    return Array.from({ length: 16 }, (_, i) => ({
      sondeId: i + 1,
      points: [],
      status: 'idle'
    }));
  });

  // Predefined calibration heights based on point count
  const getCalibrationHeights = (pointCount: number): number[] => {
    switch (pointCount) {
      case 3: return [0, 5, -5];
      case 5: return [0, 5, 10, -5, -10];
      case 7: return [0, 5, 10, 15, -5, -10, -15];
      default: return [0, 5, -5];
    }
  };

  // Simulate voltage reading
  useEffect(() => {
    if (isCalibrating) {
      const interval = setInterval(() => {
        // Simulate realistic voltage reading with some noise
        const baseVoltage = 2.5 + (Math.random() - 0.5) * 0.1;
        setCurrentVoltage(baseVoltage);
      }, 100);
      return () => clearInterval(interval);
    }
  }, [isCalibrating]);

  // Calculate linear fit for sonde
  const calculateLinearFit = (points: CalibrationPoint[]) => {
    if (points.length < 2) return null;
    
    const n = points.length;
    const sumX = points.reduce((sum, p) => sum + p.height, 0);
    const sumY = points.reduce((sum, p) => sum + p.voltage, 0);
    const sumXY = points.reduce((sum, p) => sum + p.height * p.voltage, 0);
    const sumXX = points.reduce((sum, p) => sum + p.height * p.height, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const offset = (sumY - slope * sumX) / n;
    
    // Calculate R²
    const yMean = sumY / n;
    const ssRes = points.reduce((sum, p) => {
      const predicted = slope * p.height + offset;
      return sum + Math.pow(p.voltage - predicted, 2);
    }, 0);
    const ssTot = points.reduce((sum, p) => sum + Math.pow(p.voltage - yMean, 2), 0);
    const r2 = 1 - (ssRes / ssTot);
    
    return { slope, offset, r2 };
  };

  const startCalibration = () => {
    setIsCalibrating(true);
    setCurrentPointIndex(0);
    
    // Initialize points for active sonde
    const heights = getCalibrationHeights(selectedPointCount);
    const newCalibrations = [...calibrations];
    newCalibrations[activeSensor - 1] = {
      ...newCalibrations[activeSensor - 1],
      points: heights.map(height => ({
        height,
        voltage: 0,
        confirmed: false
      })),
      status: 'calibrating'
    };
    setCalibrations(newCalibrations);
  };

  const confirmPoint = () => {
    const newCalibrations = [...calibrations];
    const sensorCalib = newCalibrations[activeSensor - 1];
    
    if (sensorCalib.points[currentPointIndex]) {
      sensorCalib.points[currentPointIndex] = {
        ...sensorCalib.points[currentPointIndex],
        voltage: currentVoltage,
        confirmed: true,
        timestamp: new Date()
      };
      
      if (currentPointIndex < sensorCalib.points.length - 1) {
        setCurrentPointIndex(currentPointIndex + 1);
      } else {
        // Calibration complete for this sonde
        const linearFit = calculateLinearFit(sensorCalib.points);
        sensorCalib.linearFit = linearFit || undefined;
        sensorCalib.status = 'completed';
        setIsCalibrating(false);
      }
      
      setCalibrations(newCalibrations);
    }
  };

  const stopCalibration = () => {
    setIsCalibrating(false);
    const newCalibrations = [...calibrations];
    newCalibrations[activeSensor - 1].status = 'idle';
    setCalibrations(newCalibrations);
  };

  const currentSensorCalib = calibrations[activeSensor - 1];
  const currentPoint = currentSensorCalib.points[currentPointIndex];

  return (
    <div className="h-full overflow-hidden" style={{backgroundColor: 'var(--bg-primary)'}}>
      
      {/* Fixed Header */}
      <div className="h-20 flex items-center px-8 shadow-lg themed-nav" style={{background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))'}}>
        <div className="flex items-center space-x-4">
          <CogIcon className="w-8 h-8 text-white" />
          <div>
            <h1 className="text-2xl font-bold text-white">Calibration des Sondes</h1>
            <p className="text-purple-100 text-sm">Configuration et étalonnage précis</p>
          </div>
        </div>
        
        <div className="ml-auto flex items-center space-x-4">
          <div className="text-right">
            <p className="text-purple-100 text-sm">Sonde Active</p>
            <p className="text-white font-bold text-lg">#{activeSensor}</p>
          </div>
        </div>
      </div>

      {/* Main Content - Fixed Height, No Scroll */}
      <div className="h-[calc(100vh-5rem)] p-6 grid grid-cols-12 gap-6">
        
        {/* Left Panel - Configuration & Control */}
        <div className="col-span-4 space-y-6">
          
          {/* Configuration */}
          <div className="themed-card rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Configuration</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Nombre de Sondes
                </label>
                <select
                  value={selectedSensorCount}
                  onChange={(e) => setSelectedSensorCount(Number(e.target.value))}
                  disabled={isCalibrating}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                >
                  {[4, 8, 12, 16].map(count => (
                    <option key={count} value={count}>{count} sondes</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Points de Calibration
                </label>
                <select
                  value={selectedPointCount}
                  onChange={(e) => setSelectedPointCount(Number(e.target.value))}
                  disabled={isCalibrating}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
                >
                  <option value={3}>3 points</option>
                  <option value={5}>5 points</option>
                  <option value={7}>7 points</option>
                </select>
              </div>
            </div>
          </div>

          {/* Sonde Selection */}
          <div className="themed-card rounded-2xl p-6 flex-1">
            <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Sélection de Sonde</h3>
            
            <div className="grid grid-cols-4 gap-2 mb-4">
              {Array.from({ length: selectedSensorCount }, (_, i) => {
                const sondeId = i + 1;
                const calibration = calibrations[i];
                const isActive = activeSensor === sondeId;
                const isCompleted = calibration.status === 'completed';
                
                return (
                  <button
                    key={sondeId}
                    onClick={() => !isCalibrating && setActiveSensor(sondeId)}
                    disabled={isCalibrating && !isActive}
                    className={`p-3 rounded-lg border-2 transition-all text-sm font-medium`}
                    style={{
                      borderColor: isActive ? 'var(--accent-primary)' : isCompleted ? 'var(--status-success)' : 'var(--border-primary)',
                      backgroundColor: isActive ? 'var(--accent-primary)' + '20' : isCompleted ? 'var(--status-success-bg)' : 'var(--bg-secondary)',
                      color: isActive ? 'var(--accent-primary)' : isCompleted ? 'var(--status-success)' : 'var(--text-secondary)'
                    }}
                  >
                    <div className="flex flex-col items-center">
                      <span>#{sondeId}</span>
                      {isCompleted && <CheckIcon className="w-3 h-3 mt-1" />}
                    </div>
                  </button>
                );
              })}
            </div>
            
            {/* Current Sonde Status */}
            <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--bg-secondary)' }}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>Sonde #{activeSensor}</span>
                <span className={`text-xs px-2 py-1 rounded-full`}
                      style={{
                        backgroundColor: currentSensorCalib.status === 'completed' ? 'var(--status-success-bg)' :
                                       currentSensorCalib.status === 'calibrating' ? 'var(--accent-primary)' + '20' : 'var(--bg-tertiary)',
                        color: currentSensorCalib.status === 'completed' ? 'var(--status-success)' :
                               currentSensorCalib.status === 'calibrating' ? 'var(--accent-primary)' : 'var(--text-muted)'
                      }}>
                  {currentSensorCalib.status === 'completed' ? 'Terminé' :
                   currentSensorCalib.status === 'calibrating' ? 'En cours' : 'Prêt'}
                </span>
              </div>
              
              {currentSensorCalib.linearFit && (
                <div className="text-xs space-y-1" style={{ color: 'var(--text-muted)' }}>
                  <div>R² = {currentSensorCalib.linearFit.r2.toFixed(3)}</div>
                  <div>Pente = {currentSensorCalib.linearFit.slope.toFixed(3)}</div>
                  <div>Ordonnée = {currentSensorCalib.linearFit.offset.toFixed(3)}</div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Center Panel - Live Calibration */}
        <div className="col-span-4 themed-card rounded-2xl p-6">
          <div className="h-full flex flex-col">
            
            <h3 className="text-lg font-semibold text-white mb-4">Calibration en Temps Réel</h3>
            
            {!isCalibrating ? (
              <div className="flex-1 flex flex-col items-center justify-center space-y-6">
                <div className="text-center">
                  <div className="w-20 h-20 mx-auto mb-4 bg-purple-500/20 rounded-full flex items-center justify-center">
                    <PlayIcon className="w-10 h-10 text-purple-400" />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-2">Prêt à Calibrer</h4>
                  <p className="text-slate-400 text-sm mb-6">
                    Sonde #{activeSensor} • {selectedPointCount} points
                  </p>
                </div>
                
                <button
                  onClick={startCalibration}
                  className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-xl text-white font-medium transition-all duration-200 transform hover:scale-105"
                >
                  Démarrer la Calibration
                </button>
              </div>
            ) : (
              <div className="flex-1 flex flex-col">
                
                {/* Current Point Info */}
                <div className="bg-slate-700/50 rounded-lg p-4 mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-slate-300">Point {currentPointIndex + 1}/{selectedPointCount}</span>
                    <span className="text-purple-400 font-mono text-sm">
                      {currentPoint?.height > 0 ? '+' : ''}{currentPoint?.height} cm
                    </span>
                  </div>
                  <div className="w-full bg-slate-600 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${((currentPointIndex + 1) / selectedPointCount) * 100}%` }}
                    />
                  </div>
                </div>

                {/* Live Voltage Display */}
                <div className="flex-1 flex flex-col items-center justify-center space-y-6">
                  <div className="text-center">
                    <p className="text-slate-400 text-sm mb-2">Tension Mesurée</p>
                    <div className="text-6xl font-mono font-bold text-white mb-2">
                      {currentVoltage.toFixed(3)}
                    </div>
                    <p className="text-slate-400 text-lg">Volts</p>
                  </div>
                  
                  <div className="text-center text-slate-400 text-sm">
                    <p>Positionnez la sonde à {currentPoint?.height > 0 ? '+' : ''}{currentPoint?.height} cm</p>
                    <p>puis confirmez la mesure</p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-4">
                  <button
                    onClick={stopCalibration}
                    className="flex-1 px-4 py-3 bg-red-600 hover:bg-red-700 rounded-lg text-white font-medium transition-colors flex items-center justify-center space-x-2"
                  >
                    <StopIcon className="w-4 h-4" />
                    <span>Arrêter</span>
                  </button>
                  
                  <button
                    onClick={confirmPoint}
                    className="flex-1 px-4 py-3 bg-green-600 hover:bg-green-700 rounded-lg text-white font-medium transition-colors flex items-center justify-center space-x-2"
                  >
                    <CheckIcon className="w-4 h-4" />
                    <span>Confirmer</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Data Table & Graph */}
        <div className="col-span-4 space-y-6">
          
          {/* Calibration Points Table */}
          <div className="themed-card rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <ChartBarIcon className="w-5 h-5 mr-2" />
              Points de Calibration
            </h3>
            
            <div className="space-y-2">
              <div className="grid grid-cols-3 gap-4 text-xs font-medium text-slate-400 pb-2 border-b border-slate-600">
                <span>Hauteur (cm)</span>
                <span>Tension (V)</span>
                <span>État</span>
              </div>
              
              {currentSensorCalib.points.map((point, index) => (
                <div key={index} className={`grid grid-cols-3 gap-4 text-sm py-2 px-2 rounded ${
                  index === currentPointIndex && isCalibrating ? 'bg-purple-500/20' : ''
                }`}>
                  <span className="text-white font-mono">
                    {point.height > 0 ? '+' : ''}{point.height}
                  </span>
                  <span className="text-white font-mono">
                    {point.confirmed ? point.voltage.toFixed(3) : '---'}
                  </span>
                  <span>
                    {point.confirmed ? (
                      <CheckIcon className="w-4 h-4 text-green-400" />
                    ) : index === currentPointIndex && isCalibrating ? (
                      <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <div className="w-4 h-4 border border-slate-600 rounded" />
                    )}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Calibration Results & Graph */}
          <div className="themed-card rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Résultats de Calibration</h3>
            
            {currentSensorCalib.linearFit ? (
              <div className="space-y-6">
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                    <p className="text-slate-400 text-sm">Pente</p>
                    <p className="text-white font-mono text-lg">
                      {currentSensorCalib.linearFit.slope.toFixed(4)}
                    </p>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                    <p className="text-slate-400 text-sm">Offset</p>
                    <p className="text-white font-mono text-lg">
                      {currentSensorCalib.linearFit.offset.toFixed(4)}
                    </p>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                    <p className="text-slate-400 text-sm">R²</p>
                    <p className="text-white font-mono text-lg">
                      {currentSensorCalib.linearFit.r2.toFixed(4)}
                    </p>
                  </div>
                </div>

                {/* Linearity Graph */}
                <div className="bg-slate-700/30 rounded-lg p-4">
                  <h4 className="text-white font-medium mb-3">Graphique de Linéarité</h4>
                  <div className="relative h-48 bg-slate-900/50 rounded-lg p-4">
                    <svg width="100%" height="100%" viewBox="0 0 400 160" className="overflow-visible">
                      {/* Grid */}
                      <defs>
                        <pattern id="grid" width="40" height="32" patternUnits="userSpaceOnUse">
                          <path d="M 40 0 L 0 0 0 32" fill="none" stroke="#334155" strokeWidth="0.5"/>
                        </pattern>
                      </defs>
                      <rect width="400" height="160" fill="url(#grid)" />
                      
                      {/* Axes */}
                      <line x1="40" y1="140" x2="360" y2="140" stroke="#64748b" strokeWidth="2"/>
                      <line x1="40" y1="140" x2="40" y2="20" stroke="#64748b" strokeWidth="2"/>
                      
                      {/* Axis labels */}
                      <text x="200" y="155" textAnchor="middle" fill="#94a3b8" fontSize="12">Tension (V)</text>
                      <text x="25" y="80" textAnchor="middle" fill="#94a3b8" fontSize="12" transform="rotate(-90 25 80)">Hauteur (m)</text>
                      
                      {/* Data points */}
                      {currentSensorCalib.points.map((point, index) => {
                        const x = 40 + (point.voltage / 5) * 320;
                        const y = 140 - (point.height / 2) * 120;
                        return (
                          <circle
                            key={index}
                            cx={x}
                            cy={y}
                            r="4"
                            fill="#3b82f6"
                            stroke="#60a5fa"
                            strokeWidth="2"
                          />
                        );
                      })}
                      
                      {/* Linear fit line */}
                      {(() => {
                        const fit = currentSensorCalib.linearFit!;
                        const x1 = 40;
                        const y1 = 140 - ((fit.slope * 0 + fit.offset) / 2) * 120;
                        const x2 = 360;
                        const y2 = 140 - ((fit.slope * 5 + fit.offset) / 2) * 120;
                        return (
                          <line
                            x1={x1}
                            y1={Math.max(20, Math.min(140, y1))}
                            x2={x2}
                            y2={Math.max(20, Math.min(140, y2))}
                            stroke="#10b981"
                            strokeWidth="2"
                            strokeDasharray="5,5"
                          />
                        );
                      })()}
                      
                      {/* Scale markers */}
                      {[0, 1, 2, 3, 4, 5].map(v => (
                        <g key={v}>
                          <line x1={40 + (v/5) * 320} y1="140" x2={40 + (v/5) * 320} y2="145" stroke="#64748b"/>
                          <text x={40 + (v/5) * 320} y="155" textAnchor="middle" fill="#94a3b8" fontSize="10">{v}</text>
                        </g>
                      ))}
                      {[0, 0.5, 1, 1.5, 2].map(h => (
                        <g key={h}>
                          <line x1="35" y1={140 - (h/2) * 120} x2="40" y2={140 - (h/2) * 120} stroke="#64748b"/>
                          <text x="30" y={140 - (h/2) * 120 + 3} textAnchor="end" fill="#94a3b8" fontSize="10">{h}</text>
                        </g>
                      ))}
                    </svg>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-400 text-center py-8">
                Aucune calibration effectuée pour cette sonde
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewCalibrationPage;
