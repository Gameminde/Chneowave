import React from 'react';
import { 
  ChartBarIcon, 
  ClockIcon, 
  ArrowTrendingUpIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface WaveMetrics {
  Hs: number;           // Hauteur significative (m)
  Tp: number;           // Période pic (s)
  frequency: number;    // Fréquence d'échantillonnage (Hz)
  samples: number;      // Nombre d'échantillons
  direction: number;    // Direction des vagues (degrés)
  quality: 'excellent' | 'good' | 'fair' | 'poor';
}

interface WaveMetricsPanelProps {
  metrics: WaveMetrics;
  isAcquiring: boolean;
}

const WaveMetricsPanel: React.FC<WaveMetricsPanelProps> = ({ metrics, isAcquiring }) => {
  const getQualityColor = (quality: string) => {
    const colorMap = {
      excellent: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
      good: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
      fair: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
      poor: 'text-red-400 bg-red-500/10 border-red-500/20'
    };
    return colorMap[quality as keyof typeof colorMap] || colorMap.fair;
  };

  const getQualityIcon = (quality: string) => {
    if (quality === 'poor') return <ExclamationTriangleIcon className="w-4 h-4" />;
    return <ChartBarIcon className="w-4 h-4" />;
  };

  return (
    <div className="h-full bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-4 space-y-4">
      {/* En-tête du Panel */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white flex items-center space-x-2">
          <ChartBarIcon className="w-5 h-5 text-blue-400" />
          <span>Métriques de Houle</span>
        </h3>
        <div className={`px-2 py-1 rounded-full text-xs font-medium border ${getQualityColor(metrics.quality)}`}>
          <div className="flex items-center space-x-1">
            {getQualityIcon(metrics.quality)}
            <span className="capitalize">{metrics.quality}</span>
          </div>
        </div>
      </div>

      {/* Métriques Principales */}
      <div className="grid grid-cols-2 gap-4">
        {/* Hauteur Significative */}
        <div className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium">Hauteur Significative</span>
            <ChartBarIcon className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {metrics.Hs.toFixed(2)} m
          </div>
          <div className="text-xs text-slate-400">Hs - ITTC Standard</div>
        </div>

        {/* Période Pic */}
        <div className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium">Période Pic</span>
            <ClockIcon className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white mb-1">
            {metrics.Tp.toFixed(1)} s
          </div>
          <div className="text-xs text-slate-400">Tp - Fréquence dominante</div>
        </div>
      </div>

      {/* Métriques Secondaires */}
      <div className="space-y-3">
        {/* Fréquence d'Échantillonnage */}
        <div className="flex items-center justify-between p-3 bg-slate-700/20 rounded-lg border border-slate-600/20">
          <div className="flex items-center space-x-2">
            <ArrowTrendingUpIcon className="w-4 h-4 text-violet-400" />
            <span className="text-sm text-slate-300">Fréquence</span>
          </div>
          <span className="text-sm font-semibold text-white">{metrics.frequency} Hz</span>
        </div>

        {/* Direction des Vagues */}
        <div className="flex items-center justify-between p-3 bg-slate-700/20 rounded-lg border border-slate-600/20">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 text-amber-400">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9L8.91 8.26L12 2Z" />
              </svg>
            </div>
            <span className="text-sm text-slate-300">Direction</span>
          </div>
          <span className="text-sm font-semibold text-white">{metrics.direction}°</span>
        </div>

        {/* Nombre d'Échantillons */}
        <div className="flex items-center justify-between p-3 bg-slate-700/20 rounded-lg border border-slate-600/20">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 text-rose-400">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 11H7C5.9 11 5 11.9 5 13V17C5 18.1 5.9 19 7 19H9C10.1 19 11 18.1 11 17V13C11 11.9 10.1 11 9 11ZM15 7H13C11.9 7 11 7.9 11 9V17C11 18.1 11.9 19 13 19H15C16.1 19 17 18.1 17 17V9C17 7.9 16.1 7 15 7Z" />
              </svg>
            </div>
            <span className="text-sm text-slate-300">Échantillons</span>
          </div>
          <span className="text-sm font-semibold text-white">{metrics.samples.toLocaleString()}</span>
        </div>
      </div>

      {/* Indicateur d'Acquisition */}
      {isAcquiring && (
        <div className="mt-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
            <span className="text-sm font-medium text-blue-400">Acquisition en cours...</span>
          </div>
        </div>
      )}

      {/* Barre de Progression Qualité */}
      <div className="mt-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-400">Qualité du Signal</span>
          <span className="text-xs text-slate-400">{(metrics.quality === 'excellent' ? 95 : metrics.quality === 'good' ? 80 : metrics.quality === 'fair' ? 65 : 45)}%</span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-500 ${
              metrics.quality === 'excellent' ? 'bg-emerald-500' :
              metrics.quality === 'good' ? 'bg-blue-500' :
              metrics.quality === 'fair' ? 'bg-amber-500' : 'bg-red-500'
            }`}
            style={{ 
              width: `${metrics.quality === 'excellent' ? 95 : metrics.quality === 'good' ? 80 : metrics.quality === 'fair' ? 65 : 45}%` 
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default WaveMetricsPanel;
