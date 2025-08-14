import React, { useState, useEffect, useRef } from 'react';
import { 
  ChartBarIcon, 
  MagnifyingGlassIcon,
  ArrowDownTrayIcon,
  CogIcon
} from '@heroicons/react/24/outline';

interface SondeData {
  id: number;
  name: string;
  values: number[];
  timestamps: number[];
  isActive: boolean;
  color: string;
}

interface ScientificChartContainerProps {
  sondes: SondeData[];
  isAcquiring: boolean;
  onExport: () => void;
  onConfigure: () => void;
}

const ScientificChartContainer: React.FC<ScientificChartContainerProps> = ({
  sondes,
  isAcquiring,
  onExport,
  onConfigure
}) => {
  const [selectedView, setSelectedView] = useState<'time' | 'spectrum' | 'correlation'>('time');
  const [timeRange, setTimeRange] = useState(300); // 5 minutes par défaut
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Génération de données simulées pour le graphique
  useEffect(() => {
    if (!canvasRef.current || !isAcquiring) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Configuration du canvas
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    // Nettoyage du canvas
    ctx.clearRect(0, 0, rect.width, rect.height);

    // Dessin du graphique temps réel
    drawTimeSeriesChart(ctx, rect.width, rect.height);
  }, [sondes, isAcquiring, timeRange]);

  const drawTimeSeriesChart = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    // Configuration du style
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    ctx.fillStyle = 'rgba(59, 130, 246, 0.1)';

    // Grille de fond
    drawGrid(ctx, width, height);

    // Dessin des données des sondes actifs
    sondes.filter(s => s.isActive).forEach((sonde, index) => {
      if (sonde.values.length < 2) return;

      ctx.strokeStyle = sonde.color;
      ctx.fillStyle = `${sonde.color}20`;

      ctx.beginPath();
      sonde.values.forEach((value, i) => {
        const x = (i / (sonde.values.length - 1)) * width;
        const y = height - ((value + 3) / 6) * height; // Normalisation -3 à +3

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();

      // Remplissage sous la courbe
      ctx.lineTo(width, height);
      ctx.lineTo(0, height);
      ctx.closePath();
      ctx.fill();
    });

    // Axes et labels
    drawAxes(ctx, width, height);
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.2)';
    ctx.lineWidth = 1;

    // Lignes verticales
    for (let i = 0; i <= 10; i++) {
      const x = (i / 10) * width;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }

    // Lignes horizontales
    for (let i = 0; i <= 6; i++) {
      const y = (i / 6) * height;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
  };

  const drawAxes = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2;
    ctx.fillStyle = '#64748b';
    ctx.font = '12px Inter';

    // Axe X
    ctx.beginPath();
    ctx.moveTo(0, height - 20);
    ctx.lineTo(width, height - 20);
    ctx.stroke();

    // Axe Y
    ctx.beginPath();
    ctx.moveTo(20, 0);
    ctx.lineTo(20, height - 20);
    ctx.stroke();

    // Labels axe X (temps)
    for (let i = 0; i <= 5; i++) {
      const x = 20 + (i / 5) * (width - 40);
      const time = (i / 5) * timeRange;
      ctx.fillText(`${time}s`, x - 15, height - 5);
    }

    // Labels axe Y (amplitude)
    for (let i = 0; i <= 6; i++) {
      const y = 20 + (i / 6) * (height - 40);
      const amplitude = 3 - (i / 6) * 6;
      ctx.fillText(`${amplitude.toFixed(1)}m`, 5, y + 4);
    }
  };

  const getViewLabel = (view: string) => {
    const labels = {
      time: 'Série Temporelle',
      spectrum: 'Spectre Fréquentiel',
      correlation: 'Corrélation Croisée'
    };
    return labels[view as keyof typeof labels] || view;
  };

  return (
    <div className="h-full bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 space-y-4">
      {/* En-tête avec contrôles */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h3 className="text-xl font-semibold text-white flex items-center space-x-2">
            <ChartBarIcon className="w-6 h-6 text-blue-400" />
            <span>Visualisation Scientifique</span>
          </h3>
          
          {/* Sélecteur de vue */}
          <div className="flex bg-slate-700/50 rounded-lg p-1">
            {(['time', 'spectrum', 'correlation'] as const).map((view) => (
              <button
                key={view}
                onClick={() => setSelectedView(view)}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200 ${
                  selectedView === view
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-slate-400 hover:text-white hover:bg-slate-600'
                }`}
              >
                {getViewLabel(view)}
              </button>
            ))}
          </div>
        </div>

        {/* Contrôles de graphique */}
        <div className="flex items-center space-x-3">
          {/* Sélecteur de plage temporelle */}
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(Number(e.target.value))}
            className="px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={60}>1 minute</option>
            <option value={300}>5 minutes</option>
            <option value={600}>10 minutes</option>
            <option value={1800}>30 minutes</option>
          </select>

          {/* Bouton Export */}
          <button
            onClick={onExport}
            className="flex items-center space-x-2 px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-all duration-200"
          >
            <ArrowDownTrayIcon className="w-4 h-4" />
            <span className="text-sm font-medium">Export</span>
          </button>

          {/* Bouton Configuration */}
          <button
            onClick={onConfigure}
            className="flex items-center space-x-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white rounded-lg transition-all duration-200"
          >
            <CogIcon className="w-4 h-4" />
            <span className="text-sm font-medium">Config</span>
          </button>
        </div>
      </div>

      {/* Zone de graphique */}
      <div className="flex-1 bg-slate-900/50 rounded-lg border border-slate-600/30 p-4 relative">
        <canvas
          ref={canvasRef}
          className="w-full h-full"
          style={{ minHeight: '400px' }}
        />
        
        {/* Indicateur d'acquisition */}
        {isAcquiring && (
          <div className="absolute top-4 right-4 flex items-center space-x-2 px-3 py-2 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
            <span className="text-sm font-medium text-blue-400">Acquisition en cours</span>
          </div>
        )}

        {/* Légende des sondes */}
        <div className="absolute bottom-4 left-4 bg-slate-800/80 backdrop-blur-sm rounded-lg p-3 border border-slate-600/30">
          <div className="text-sm font-medium text-white mb-2">Sondes Actifs</div>
          <div className="space-y-1">
            {sondes.filter(s => s.isActive).map((sonde) => (
              <div key={sonde.id} className="flex items-center space-x-2">
                <div 
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: sonde.color }}
                ></div>
                <span className="text-xs text-slate-300">{sonde.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Métriques du graphique */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30 text-center">
          <div className="text-lg font-semibold text-blue-400">
            {sondes.filter(s => s.isActive).length}
          </div>
          <div className="text-xs text-slate-400">Sondes</div>
        </div>
        <div className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30 text-center">
          <div className="text-lg font-semibold text-emerald-400">
            {timeRange}s
          </div>
          <div className="text-xs text-slate-400">Plage</div>
        </div>
        <div className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30 text-center">
          <div className="text-lg font-semibold text-violet-400">
            {sondes.filter(s => s.isActive).reduce((acc, s) => acc + s.values.length, 0).toLocaleString()}
          </div>
          <div className="text-xs text-slate-400">Points</div>
        </div>
        <div className="bg-slate-700/30 rounded-lg p-3 border border-slate-600/30 text-center">
          <div className="text-lg font-semibold text-amber-400">
            {isAcquiring ? '60' : '0'}
          </div>
          <div className="text-xs text-slate-400">FPS</div>
        </div>
      </div>
    </div>
  );
};

export default ScientificChartContainer;
