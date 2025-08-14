import React, { useState, useEffect } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';
import {
  PlayIcon,
  PauseIcon,
  StopIcon,
  DocumentArrowDownIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  AdjustmentsHorizontalIcon,
  BeakerIcon,
  ChartBarIcon,
  ClockIcon,
  CogIcon,
  ArrowRightIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline';

interface CalibrationPoint {
  reference: number;
  measured: number;
  timestamp: number;
}

interface CalibrationResult {
  slope: number;
  offset: number;
  r2: number;
  rmse: number;
  points: CalibrationPoint[];
}

interface SensorCalibration {
  id: number;
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  progress: number;
  result?: CalibrationResult;
}

const CALIBRATION_STEPS = [
  { id: 1, name: 'Préparation', description: 'Configuration et vérification du système' },
  { id: 2, name: 'Acquisition Points', description: 'Collecte des points de calibration' },
  { id: 3, name: 'Modélisation', description: 'Calcul de la fonction de transfert' },
  { id: 4, name: 'Validation', description: 'Vérification de la qualité' },
  { id: 5, name: 'Certification', description: 'Génération du certificat' }
];

const ProfessionalCalibrationPage: React.FC = () => {
  const { theme } = useUnifiedApp();
  const [currentStep, setCurrentStep] = useState(1);
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [activeSensor, setActiveSensor] = useState(1);
  const [calibrationTime, setCalibrationTime] = useState(0);
  const [targetPoints, setTargetPoints] = useState(10);
  const [currentPoints, setCurrentPoints] = useState(0);
  const [referenceValue, setReferenceValue] = useState(0.0);
  
  const [sondes, setSensors] = useState<SensorCalibration[]>([
    { id: 1, name: 'HF-1', status: 'pending', progress: 0 },
    { id: 2, name: 'HF-2', status: 'pending', progress: 0 },
    { id: 3, name: 'HF-3', status: 'pending', progress: 0 },
    { id: 4, name: 'HF-4', status: 'pending', progress: 0 },
  ]);

  const currentSensor = sondes.find(s => s.id === activeSensor)!;

  // Simulation du processus de calibration
  useEffect(() => {
    let interval: number | null = null;
    
    if (isCalibrating && currentStep === 2) {
      interval = setInterval(() => {
        setCalibrationTime(prev => prev + 1);
        
        // Simuler l'acquisition de points
        if (Math.random() > 0.7 && currentPoints < targetPoints) {
          setCurrentPoints(prev => prev + 1);
          
          // Mettre à jour le progrès du sonde
          setSensors(prev => prev.map(sonde => 
            sonde.id === activeSensor 
              ? { 
                  ...sonde, 
                  progress: ((currentPoints + 1) / targetPoints) * 100,
                  status: 'in_progress'
                }
              : sonde
          ));
        }
        
        // Passer à l'étape suivante si tous les points sont acquis
        if (currentPoints >= targetPoints) {
          setCurrentStep(3);
          setIsCalibrating(false);
        }
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isCalibrating, currentStep, currentPoints, targetPoints, activeSensor]);

  const handleStartCalibration = () => {
    if (currentStep === 1) {
      setCurrentStep(2);
    }
    setIsCalibrating(true);
    setCalibrationTime(0);
    setCurrentPoints(0);
  };

  const handleStopCalibration = () => {
    setIsCalibrating(false);
  };

  const handleNextStep = () => {
    if (currentStep < 5) {
      setCurrentStep(currentStep + 1);
      
      if (currentStep === 3) {
        // Simuler le calcul de la régression
        setTimeout(() => {
          const mockResult: CalibrationResult = {
            slope: 0.985 + (Math.random() - 0.5) * 0.1,
            offset: 0.012 + (Math.random() - 0.5) * 0.02,
            r2: 0.995 + Math.random() * 0.004,
            rmse: 0.005 + Math.random() * 0.003,
            points: Array.from({ length: targetPoints }, (_, i) => ({
              reference: i * 0.5,
              measured: (i * 0.5) * 0.985 + 0.012 + (Math.random() - 0.5) * 0.01,
              timestamp: Date.now() - (targetPoints - i) * 1000
            }))
          };
          
          setSensors(prev => prev.map(sonde =>
            sonde.id === activeSensor
              ? { ...sonde, status: 'completed', result: mockResult }
              : sonde
          ));
        }, 2000);
      }
    }
  };

  const handlePrevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const getStepStatus = (stepId: number) => {
    if (stepId < currentStep) return 'completed';
    if (stepId === currentStep) return 'current';
    return 'pending';
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="h-full flex flex-col" style={{ backgroundColor: 'var(--bg-primary)' }}>
      {/* Header Professional */}
      <div className="h-16 flex items-center justify-between px-6 border-b" style={{
        backgroundColor: 'var(--bg-elevated)',
        borderColor: 'var(--border-primary)'
      }}>
        <div className="flex items-center space-x-4">
          <BeakerIcon className="w-6 h-6" style={{ color: 'var(--accent-primary)' }} />
          <div>
            <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
              Calibration Professionnelle
            </h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Assistant de calibration multi-sondes
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm" style={{ color: 'var(--text-secondary)' }}>
            <ClockIcon className="w-4 h-4" />
            <span>{formatTime(calibrationTime)}</span>
          </div>
          
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            isCalibrating ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
          }`}>
            {isCalibrating ? 'EN COURS' : 'PRÊT'}
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Panneau étapes gauche */}
        <div className="w-80 border-r flex flex-col" style={{
          backgroundColor: 'var(--bg-secondary)',
          borderColor: 'var(--border-primary)'
        }}>
          {/* Assistant d'étapes */}
          <div className="p-4 border-b" style={{ borderColor: 'var(--border-primary)' }}>
            <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
              Assistant de Calibration
            </h3>
            
            <div className="space-y-3">
              {CALIBRATION_STEPS.map(step => {
                const status = getStepStatus(step.id);
                return (
                  <div
                    key={step.id}
                    className={`p-3 rounded-lg border ${
                      status === 'current' ? 'ring-2 ring-blue-500' : ''
                    }`}
                    style={{
                      backgroundColor: status === 'completed' ? 'var(--status-success-bg)' :
                                     status === 'current' ? 'var(--accent-primary)' + '20' :
                                     'var(--bg-primary)',
                      borderColor: status === 'completed' ? 'var(--status-success)' :
                                  status === 'current' ? 'var(--accent-primary)' :
                                  'var(--border-primary)'
                    }}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                        status === 'completed' ? 'bg-green-500 text-white' :
                        status === 'current' ? 'bg-blue-500 text-white' :
                        'bg-gray-300 text-gray-600'
                      }`}>
                        {status === 'completed' ? '✓' : step.id}
                      </div>
                      
                      <div className="flex-1">
                        <div className="text-sm font-medium" style={{
                          color: status === 'current' ? 'var(--accent-primary)' : 'var(--text-primary)'
                        }}>
                          {step.name}
                        </div>
                        <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                          {step.description}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Contrôles de navigation */}
            <div className="flex justify-between mt-4">
              <button
                onClick={handlePrevStep}
                disabled={currentStep === 1}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm ${
                  currentStep === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                <ArrowLeftIcon className="w-4 h-4" />
                <span>Précédent</span>
              </button>
              
              <button
                onClick={handleNextStep}
                disabled={currentStep === 5 || (currentStep === 2 && currentPoints < targetPoints)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm ${
                  currentStep === 5 || (currentStep === 2 && currentPoints < targetPoints)
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-blue-500 text-white hover:bg-blue-600'
                }`}
              >
                <span>Suivant</span>
                <ArrowRightIcon className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Sélection sondes */}
          <div className="flex-1 p-4">
            <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
              Sondes à Calibrer
            </h3>
            
            <div className="grid grid-cols-2 gap-2">
              {sondes.map(sonde => (
                <button
                  key={sonde.id}
                  onClick={() => !isCalibrating && setActiveSensor(sonde.id)}
                  disabled={isCalibrating && sonde.id !== activeSensor}
                  className={`p-3 rounded-lg border-2 transition-all text-sm font-medium`}
                  style={{
                    borderColor: sonde.id === activeSensor ? 'var(--accent-primary)' :
                                sonde.status === 'completed' ? 'var(--status-success)' :
                                'var(--border-primary)',
                    backgroundColor: sonde.id === activeSensor ? 'var(--accent-primary)' + '20' :
                                    sonde.status === 'completed' ? 'var(--status-success-bg)' :
                                    'var(--bg-primary)',
                    color: sonde.id === activeSensor ? 'var(--accent-primary)' :
                          sonde.status === 'completed' ? 'var(--status-success)' :
                          'var(--text-secondary)'
                  }}
                >
                  <div className="flex flex-col items-center">
                    <span>{sonde.name}</span>
                    {sonde.status === 'completed' && <CheckCircleIcon className="w-4 h-4 mt-1" />}
                    {sonde.status === 'in_progress' && (
                      <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                        <div
                          className="bg-blue-600 h-1.5 rounded-full transition-all"
                          style={{ width: `${sonde.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                </button>
              ))}
            </div>

            {/* Status sonde actuel */}
            <div className="mt-4 p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-primary)' }}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                  Sonde {currentSensor.name}
                </span>
                <span className={`text-xs px-2 py-1 rounded-full`}
                      style={{
                        backgroundColor: currentSensor.status === 'completed' ? 'var(--status-success-bg)' :
                                       currentSensor.status === 'in_progress' ? 'var(--accent-primary)' + '20' :
                                       'var(--bg-tertiary)',
                        color: currentSensor.status === 'completed' ? 'var(--status-success)' :
                               currentSensor.status === 'in_progress' ? 'var(--accent-primary)' :
                               'var(--text-muted)'
                      }}>
                  {currentSensor.status === 'completed' ? 'Terminé' :
                   currentSensor.status === 'in_progress' ? 'En cours' :
                   'Prêt'}
                </span>
              </div>
              
              {currentSensor.result && (
                <div className="text-xs space-y-1" style={{ color: 'var(--text-muted)' }}>
                  <div>R² = {currentSensor.result.r2.toFixed(4)}</div>
                  <div>Pente = {currentSensor.result.slope.toFixed(4)}</div>
                  <div>Offset = {currentSensor.result.offset.toFixed(4)} m</div>
                  <div>RMSE = {currentSensor.result.rmse.toFixed(4)} m</div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Zone principale */}
        <div className="flex-1 flex flex-col">
          {/* Contrôles de calibration */}
          {currentStep === 2 && (
            <div className="h-20 border-b flex items-center justify-between px-6" style={{
              backgroundColor: 'var(--bg-secondary)',
              borderColor: 'var(--border-primary)'
            }}>
              <div className="flex items-center space-x-6">
                <div>
                  <label className="block text-xs" style={{ color: 'var(--text-secondary)' }}>
                    Valeur de Référence (m)
                  </label>
                  <input
                    type="number"
                    value={referenceValue}
                    onChange={(e) => setReferenceValue(Number(e.target.value))}
                    step="0.001"
                    className="mt-1 px-3 py-1 rounded border text-sm w-24"
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: 'var(--border-secondary)',
                      color: 'var(--text-primary)'
                    }}
                  />
                </div>
                
                <div>
                  <label className="block text-xs" style={{ color: 'var(--text-secondary)' }}>
                    Points Cibles
                  </label>
                  <select
                    value={targetPoints}
                    onChange={(e) => setTargetPoints(Number(e.target.value))}
                    disabled={isCalibrating}
                    className="mt-1 px-3 py-1 rounded border text-sm"
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: 'var(--border-secondary)',
                      color: 'var(--text-primary)'
                    }}
                  >
                    <option value={5}>5 points</option>
                    <option value={10}>10 points</option>
                    <option value={15}>15 points</option>
                    <option value={20}>20 points</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Progression</div>
                  <div className="text-lg font-bold" style={{ color: 'var(--accent-primary)' }}>
                    {currentPoints}/{targetPoints}
                  </div>
                </div>

                <div className="flex space-x-2">
                  {!isCalibrating ? (
                    <button
                      onClick={handleStartCalibration}
                      className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                    >
                      <PlayIcon className="w-4 h-4" />
                      <span>Démarrer</span>
                    </button>
                  ) : (
                    <button
                      onClick={handleStopCalibration}
                      className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    >
                      <StopIcon className="w-4 h-4" />
                      <span>Arrêter</span>
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Contenu principal selon l'étape */}
          <div className="flex-1 p-6">
            {currentStep === 1 && (
              <div className="h-full flex items-center justify-center">
                <div className="text-center max-w-md">
                  <CogIcon className="w-16 h-16 mx-auto mb-4 opacity-50" style={{ color: 'var(--text-secondary)' }} />
                  <h3 className="text-xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
                    Préparation du Système
                  </h3>
                  <p className="text-sm mb-6" style={{ color: 'var(--text-secondary)' }}>
                    Vérifiez que tous les sondes sont connectés et fonctionnels.
                    Préparez les étalons de référence pour la calibration.
                  </p>
                  <button
                    onClick={handleNextStep}
                    className="flex items-center space-x-2 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors mx-auto"
                  >
                    <span>Commencer la Calibration</span>
                    <ArrowRightIcon className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="h-full">
                <div className="grid grid-cols-2 gap-6 h-full">
                  <div className="rounded-lg border p-4" style={{
                    backgroundColor: 'var(--bg-primary)',
                    borderColor: 'var(--border-primary)'
                  }}>
                    <h4 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                      Acquisition en Temps Réel
                    </h4>
                    <div className="h-64 flex items-center justify-center" style={{
                      backgroundColor: 'var(--bg-secondary)',
                      borderRadius: '4px'
                    }}>
                      <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                        <ChartBarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <p className="text-sm">Signal du sonde {currentSensor.name}</p>
                        <p className="text-xs">Valeur actuelle: {(2.5 + Math.sin(Date.now() * 0.001) * 0.5).toFixed(3)} m</p>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-lg border p-4" style={{
                    backgroundColor: 'var(--bg-primary)',
                    borderColor: 'var(--border-primary)'
                  }}>
                    <h4 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                      Points de Calibration
                    </h4>
                    <div className="h-64 overflow-y-auto">
                      <div className="space-y-2">
                        {Array.from({ length: currentPoints }, (_, i) => (
                          <div key={i} className="flex justify-between items-center p-2 rounded" style={{
                            backgroundColor: 'var(--bg-secondary)'
                          }}>
                            <span className="text-sm" style={{ color: 'var(--text-primary)' }}>
                              Point {i + 1}
                            </span>
                            <div className="text-xs space-x-4" style={{ color: 'var(--text-secondary)' }}>
                              <span>Ref: {(i * 0.5).toFixed(2)}m</span>
                              <span>Mes: {((i * 0.5) * 0.985 + 0.012).toFixed(3)}m</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {currentStep === 3 && (
              <div className="h-full flex items-center justify-center">
                <div className="text-center">
                  <AdjustmentsHorizontalIcon className="w-16 h-16 mx-auto mb-4 opacity-50" style={{ color: 'var(--accent-primary)' }} />
                  <h3 className="text-xl font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
                    Calcul en Cours...
                  </h3>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    Modélisation de la fonction de transfert par régression linéaire
                  </p>
                  <div className="mt-4">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 mx-auto" style={{ borderColor: 'var(--accent-primary)' }}></div>
                  </div>
                </div>
              </div>
            )}

            {currentStep >= 4 && currentSensor.result && (
              <div className="h-full">
                <div className="grid grid-cols-2 gap-6 h-full">
                  <div className="rounded-lg border p-4" style={{
                    backgroundColor: 'var(--bg-primary)',
                    borderColor: 'var(--border-primary)'
                  }}>
                    <h4 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                      Résultats de Calibration
                    </h4>
                    
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                          <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Coefficient R²</div>
                          <div className="text-lg font-bold" style={{ color: 'var(--status-success)' }}>
                            {currentSensor.result.r2.toFixed(4)}
                          </div>
                        </div>
                        
                        <div className="p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                          <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>RMSE (m)</div>
                          <div className="text-lg font-bold" style={{ color: 'var(--accent-primary)' }}>
                            {currentSensor.result.rmse.toFixed(4)}
                          </div>
                        </div>
                        
                        <div className="p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                          <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Pente</div>
                          <div className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
                            {currentSensor.result.slope.toFixed(4)}
                          </div>
                        </div>
                        
                        <div className="p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                          <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>Offset (m)</div>
                          <div className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
                            {currentSensor.result.offset.toFixed(4)}
                          </div>
                        </div>
                      </div>

                      <div className="mt-6">
                        <h5 className="text-sm font-medium mb-2" style={{ color: 'var(--text-primary)' }}>
                          Équation de Calibration
                        </h5>
                        <div className="p-3 rounded-lg font-mono text-sm" style={{
                          backgroundColor: 'var(--bg-tertiary)',
                          color: 'var(--accent-primary)'
                        }}>
                          y = {currentSensor.result.slope.toFixed(4)}x + {currentSensor.result.offset.toFixed(4)}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-lg border p-4" style={{
                    backgroundColor: 'var(--bg-primary)',
                    borderColor: 'var(--border-primary)'
                  }}>
                    <h4 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                      Graphique de Régression
                    </h4>
                    <div className="h-64 flex items-center justify-center" style={{
                      backgroundColor: 'var(--bg-secondary)',
                      borderRadius: '4px'
                    }}>
                      <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                        <ChartBarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <p className="text-sm">Régression Linéaire</p>
                        <p className="text-xs">Référence vs Mesure</p>
                      </div>
                    </div>
                  </div>
                </div>

                {currentStep === 5 && (
                  <div className="mt-6 flex justify-center">
                    <button
                      onClick={() => {/* Génerer certificat */}}
                      className="flex items-center space-x-2 px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                    >
                      <DocumentArrowDownIcon className="w-5 h-5" />
                      <span>Générer le Certificat de Calibration</span>
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalCalibrationPage;
