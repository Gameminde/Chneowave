import React from 'react';
import { 
  PlayIcon, 
  StopIcon, 
  PauseIcon,
  ArrowPathIcon,
  CogIcon
} from '@heroicons/react/24/outline';

interface AcquisitionControlsProps {
  status: 'STOPPED' | 'RUNNING' | 'PAUSED' | 'ERROR';
  elapsedTime: number;
  progress: number;
  onStart: () => void;
  onPause: () => void;
  onStop: () => void;
  onReset: () => void;
  onConfigure: () => void;
  testDuration: number;
}

const AcquisitionControls: React.FC<AcquisitionControlsProps> = ({
  status,
  elapsedTime,
  progress,
  onStart,
  onPause,
  onStop,
  onReset,
  onConfigure,
  testDuration
}) => {
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getStatusColor = () => {
    switch (status) {
      case 'RUNNING': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'PAUSED': return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'ERROR': return 'text-red-400 bg-red-500/10 border-red-500/20';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'RUNNING': return 'Acquisition en cours';
      case 'PAUSED': return 'En pause';
      case 'ERROR': return 'Erreur détectée';
      default: return 'Arrêté';
    }
  };

  return (
    <div className="h-full bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 space-y-6">
      {/* En-tête et Statut */}
      <div className="text-center">
        <h3 className="text-xl font-semibold text-white mb-2">Contrôles d'Acquisition</h3>
        <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-full border text-sm font-medium ${getStatusColor()}`}>
          <div className={`w-3 h-3 rounded-full ${
            status === 'RUNNING' ? 'bg-emerald-400 animate-pulse' :
            status === 'PAUSED' ? 'bg-amber-400' :
            status === 'ERROR' ? 'bg-red-400' : 'bg-slate-400'
          }`}></div>
          <span>{getStatusText()}</span>
        </div>
      </div>

      {/* Contrôles Principaux */}
      <div className="flex justify-center space-x-4">
        {/* Bouton Start */}
        <button
          onClick={onStart}
          disabled={status === 'RUNNING'}
          className={`
            flex flex-col items-center justify-center w-20 h-20 rounded-2xl font-bold text-lg
            transition-all duration-200 ease-out transform
            ${status === 'RUNNING' 
              ? 'bg-slate-600 text-slate-400 cursor-not-allowed' 
              : 'bg-emerald-600 text-white hover:bg-emerald-700 hover:scale-105 shadow-lg shadow-emerald-600/25'
            }
          `}
        >
          <PlayIcon className="w-8 h-8 mb-1" />
          <span className="text-xs">START</span>
        </button>

        {/* Bouton Pause */}
        <button
          onClick={onPause}
          disabled={status !== 'RUNNING'}
          className={`
            flex flex-col items-center justify-center w-20 h-20 rounded-2xl font-bold text-lg
            transition-all duration-200 ease-out transform
            ${status !== 'RUNNING' 
              ? 'bg-slate-600 text-slate-400 cursor-not-allowed' 
              : 'bg-amber-600 text-white hover:bg-amber-700 hover:scale-105 shadow-lg shadow-amber-600/25'
            }
          `}
        >
          <PauseIcon className="w-8 h-8 mb-1" />
          <span className="text-xs">PAUSE</span>
        </button>

        {/* Bouton Stop */}
        <button
          onClick={onStop}
          disabled={status === 'STOPPED'}
          className={`
            flex flex-col items-center justify-center w-20 h-20 rounded-2xl font-bold text-lg
            transition-all duration-200 ease-out transform
            ${status === 'STOPPED' 
              ? 'bg-slate-600 text-slate-400 cursor-not-allowed' 
              : 'bg-red-600 text-white hover:bg-red-700 hover:scale-105 shadow-lg shadow-red-600/25'
            }
          `}
        >
          <StopIcon className="w-8 h-8 mb-1" />
          <span className="text-xs">STOP</span>
        </button>
      </div>

      {/* Contrôles Secondaires */}
      <div className="flex justify-center space-x-3">
        {/* Bouton Reset */}
        <button
          onClick={onReset}
          className="flex items-center space-x-2 px-4 py-2.5 bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white rounded-lg transition-all duration-200"
        >
          <ArrowPathIcon className="w-4 h-4" />
          <span className="text-sm font-medium">Reset</span>
        </button>

        {/* Bouton Configuration */}
        <button
          onClick={onConfigure}
          className="flex items-center space-x-2 px-4 py-2.5 bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white rounded-lg transition-all duration-200"
        >
          <CogIcon className="w-4 h-4" />
          <span className="text-sm font-medium">Config</span>
        </button>
      </div>

      {/* Timer et Progression */}
      <div className="space-y-4">
        {/* Timer Principal */}
        <div className="text-center">
          <div className="text-3xl font-bold text-white font-mono">
            {formatTime(elapsedTime)}
          </div>
          <div className="text-sm text-slate-400">
            Durée totale: {formatTime(testDuration)}
          </div>
        </div>

        {/* Barre de Progression */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-slate-400">Progression</span>
            <span className="text-white font-medium">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Indicateurs de Performance */}
      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-600/30">
        <div className="text-center">
          <div className="text-lg font-semibold text-emerald-400">
            {status === 'RUNNING' ? '60' : '0'} FPS
          </div>
          <div className="text-xs text-slate-400">Performance</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-semibold text-blue-400">
            {status === 'RUNNING' ? '8' : '0'}
          </div>
          <div className="text-xs text-slate-400">Sondes Actifs</div>
        </div>
      </div>
    </div>
  );
};

export default AcquisitionControls;
