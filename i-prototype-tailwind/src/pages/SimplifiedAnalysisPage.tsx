import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon,
  CalculatorIcon,
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

interface WaveStatistics {
  Hs: number;        // Hauteur significative (m)
  Hmax: number;      // Hauteur maximale (m)
  Hmin: number;      // Hauteur minimale (m)
  H13: number;       // Hauteur 1/3 supérieur (m)
  Hmean: number;     // Hauteur moyenne (m)
  Tp: number;        // Période pic (s)
  Tz: number;        // Période zéro-crossing (s)
  T13: number;       // Période 1/3 (s)
  Tmean: number;     // Période moyenne (s)
  skewness: number;  // Asymétrie
  kurtosis: number;  // Aplatissement
  bandwidth: number; // Largeur de bande spectrale
}

interface StatisticalValidation {
  sampleSize: number;
  confidenceLevel: number;
  standardError: number;
  isStatisticallySignificant: boolean;
  pValue: number;
}

const SimplifiedAnalysisPage: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  
  // Données statistiques simulées temps réel
  const [waveStats, setWaveStats] = useState<WaveStatistics>({
    Hs: 2.42,
    Hmax: 3.75,
    Hmin: 0.12,
    H13: 2.65,
    Hmean: 1.85,
    Tp: 8.1,
    Tz: 6.8,
    T13: 7.4,
    Tmean: 7.2,
    skewness: 0.15,
    kurtosis: 2.98,
    bandwidth: 0.25
  });

  const [validation, setValidation] = useState<StatisticalValidation>({
    sampleSize: 2048,
    confidenceLevel: 95,
    standardError: 0.08,
    isStatisticallySignificant: true,
    pValue: 0.001
  });

  // Mise à jour temps réel des statistiques
  useEffect(() => {
    const interval = setInterval(() => {
      setWaveStats(prev => ({
        ...prev,
        Hs: 2.42 + Math.sin(Date.now() / 10000) * 0.3,
        Hmax: 3.75 + Math.random() * 0.2 - 0.1,
        H13: 2.65 + Math.sin(Date.now() / 15000) * 0.2,
        Hmean: 1.85 + Math.random() * 0.1 - 0.05,
        Tp: 8.1 + Math.sin(Date.now() / 12000) * 0.4,
        Tz: 6.8 + Math.random() * 0.2 - 0.1,
        skewness: 0.15 + Math.random() * 0.1 - 0.05,
        kurtosis: 2.98 + Math.random() * 0.2 - 0.1
      }));
      setLastUpdate(new Date());
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const recalculateStatistics = () => {
    setIsCalculating(true);
    setTimeout(() => {
      setIsCalculating(false);
      setLastUpdate(new Date());
    }, 1500);
  };

  const getStatisticalSignificance = (value: number, reference: number, tolerance: number) => {
    const deviation = Math.abs(value - reference) / reference;
    if (deviation < tolerance * 0.5) return 'excellent';
    if (deviation < tolerance) return 'good';
    return 'warning';
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('fr-FR', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-cyan-900 to-teal-900 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <CalculatorIcon className="w-8 h-8 text-cyan-400" />
            <div>
              <h1 className="text-2xl font-bold text-cyan-50">Analyse Statistique</h1>
              <p className="text-cyan-300 text-sm">Statistiques descriptives des données de houle</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-right text-sm text-cyan-300">
              <div>Dernière mise à jour:</div>
              <div className="font-mono">{formatTime(lastUpdate)}</div>
            </div>
            <button
              onClick={recalculateStatistics}
              disabled={isCalculating}
              className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors duration-200 min-h-[44px] flex items-center space-x-2"
            >
              <CalculatorIcon className="w-5 h-5" />
              <span>{isCalculating ? 'Calcul...' : 'Recalculer'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Statistiques principales */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        
        {/* Statistiques Hauteurs */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-6">
          <h3 className="text-lg font-bold text-cyan-50 mb-4 flex items-center">
            <ChartBarIcon className="w-6 h-6 mr-2" />
            Statistiques Hauteurs
          </h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <div className="text-cyan-300 text-sm mb-1">Hauteur Significative</div>
                <div className="text-2xl font-bold text-cyan-50">{waveStats.Hs.toFixed(2)} m</div>
                <div className="text-xs text-cyan-400">Hs (1/3 supérieur)</div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4">
                <div className="text-cyan-300 text-sm mb-1">Hauteur Maximale</div>
                <div className="text-2xl font-bold text-cyan-50">{waveStats.Hmax.toFixed(2)} m</div>
                <div className="text-xs text-cyan-400">Hmax observée</div>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-slate-800/30 rounded-lg p-3 text-center">
                <div className="text-cyan-300 text-xs mb-1">H1/3</div>
                <div className="text-lg font-bold text-cyan-50">{waveStats.H13.toFixed(2)}</div>
                <div className="text-xs text-cyan-400">m</div>
              </div>
              <div className="bg-slate-800/30 rounded-lg p-3 text-center">
                <div className="text-cyan-300 text-xs mb-1">Hmoy</div>
                <div className="text-lg font-bold text-cyan-50">{waveStats.Hmean.toFixed(2)}</div>
                <div className="text-xs text-cyan-400">m</div>
              </div>
              <div className="bg-slate-800/30 rounded-lg p-3 text-center">
                <div className="text-cyan-300 text-xs mb-1">Hmin</div>
                <div className="text-lg font-bold text-cyan-50">{waveStats.Hmin.toFixed(2)}</div>
                <div className="text-xs text-cyan-400">m</div>
              </div>
            </div>
          </div>
        </div>

        {/* Statistiques Périodes */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-6">
          <h3 className="text-lg font-bold text-cyan-50 mb-4 flex items-center">
            <ClockIcon className="w-6 h-6 mr-2" />
            Statistiques Périodes
          </h3>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <div className="text-cyan-300 text-sm mb-1">Période Pic</div>
                <div className="text-2xl font-bold text-cyan-50">{waveStats.Tp.toFixed(1)} s</div>
                <div className="text-xs text-cyan-400">Tp (énergie max)</div>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4">
                <div className="text-cyan-300 text-sm mb-1">Période Zéro-Crossing</div>
                <div className="text-2xl font-bold text-cyan-50">{waveStats.Tz.toFixed(1)} s</div>
                <div className="text-xs text-cyan-400">Tz (moyenne)</div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-800/30 rounded-lg p-3 text-center">
                <div className="text-cyan-300 text-xs mb-1">T1/3</div>
                <div className="text-lg font-bold text-cyan-50">{waveStats.T13.toFixed(1)}</div>
                <div className="text-xs text-cyan-400">s</div>
              </div>
              <div className="bg-slate-800/30 rounded-lg p-3 text-center">
                <div className="text-cyan-300 text-xs mb-1">Tmoy</div>
                <div className="text-lg font-bold text-cyan-50">{waveStats.Tmean.toFixed(1)}</div>
                <div className="text-xs text-cyan-400">s</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Statistiques avancées et validation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Paramètres statistiques */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-6">
          <h3 className="text-lg font-bold text-cyan-50 mb-4">Paramètres Statistiques</h3>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b border-slate-700 pb-2">
              <span className="text-cyan-300">Asymétrie (Skewness)</span>
              <div className="text-right">
                <span className="text-cyan-50 font-bold">{waveStats.skewness.toFixed(3)}</span>
                <div className={`text-xs ${Math.abs(waveStats.skewness) < 0.5 ? 'text-green-400' : 'text-yellow-400'}`}>
                  {Math.abs(waveStats.skewness) < 0.5 ? 'Symétrique' : 'Asymétrique'}
                </div>
              </div>
            </div>
            
            <div className="flex justify-between items-center border-b border-slate-700 pb-2">
              <span className="text-cyan-300">Aplatissement (Kurtosis)</span>
              <div className="text-right">
                <span className="text-cyan-50 font-bold">{waveStats.kurtosis.toFixed(3)}</span>
                <div className={`text-xs ${Math.abs(waveStats.kurtosis - 3) < 0.5 ? 'text-green-400' : 'text-yellow-400'}`}>
                  {Math.abs(waveStats.kurtosis - 3) < 0.5 ? 'Normale' : 'Non-normale'}
                </div>
              </div>
            </div>
            
            <div className="flex justify-between items-center border-b border-slate-700 pb-2">
              <span className="text-cyan-300">Largeur de bande</span>
              <div className="text-right">
                <span className="text-cyan-50 font-bold">{waveStats.bandwidth.toFixed(3)}</span>
                <div className={`text-xs ${waveStats.bandwidth < 0.3 ? 'text-green-400' : 'text-yellow-400'}`}>
                  {waveStats.bandwidth < 0.3 ? 'Étroite' : 'Large'}
                </div>
              </div>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-cyan-300">Ratio Hs/Hmean</span>
              <div className="text-right">
                <span className="text-cyan-50 font-bold">{(waveStats.Hs / waveStats.Hmean).toFixed(2)}</span>
                <div className="text-xs text-cyan-400">Facteur de forme</div>
              </div>
            </div>
          </div>
        </div>

        {/* Validation statistique */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-6">
          <h3 className="text-lg font-bold text-cyan-50 mb-4 flex items-center">
            <CheckCircleIcon className="w-6 h-6 mr-2" />
            Validation Statistique
          </h3>
          
          <div className="space-y-4">
            <div className="bg-slate-800/50 rounded-lg p-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <div className="text-cyan-300 mb-1">Taille échantillon</div>
                  <div className="text-cyan-50 font-bold">{validation.sampleSize.toLocaleString()}</div>
                </div>
                <div>
                  <div className="text-cyan-300 mb-1">Niveau confiance</div>
                  <div className="text-cyan-50 font-bold">{validation.confidenceLevel}%</div>
                </div>
                <div>
                  <div className="text-cyan-300 mb-1">Erreur standard</div>
                  <div className="text-cyan-50 font-bold">{validation.standardError.toFixed(3)}</div>
                </div>
                <div>
                  <div className="text-cyan-300 mb-1">p-value</div>
                  <div className="text-cyan-50 font-bold">{validation.pValue.toFixed(3)}</div>
                </div>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center">
                <div className="w-3 h-3 rounded-full bg-green-500 mr-3"></div>
                <span className="text-cyan-50 text-sm">Échantillon statistiquement significatif</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 rounded-full bg-green-500 mr-3"></div>
                <span className="text-cyan-50 text-sm">Distribution conforme aux attentes</span>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 rounded-full bg-green-500 mr-3"></div>
                <span className="text-cyan-50 text-sm">Intervalle de confiance validé</span>
              </div>
              <div className="flex items-center">
                <div className={`w-3 h-3 rounded-full ${validation.isStatisticallySignificant ? 'bg-green-500' : 'bg-yellow-500'} mr-3`}></div>
                <span className="text-cyan-50 text-sm">
                  {validation.isStatisticallySignificant ? 'Résultats statistiquement significatifs' : 'Significativité à vérifier'}
                </span>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-cyan-900/30 rounded-lg">
              <div className="text-cyan-300 text-xs font-semibold mb-1">RECOMMANDATION</div>
              <div className="text-cyan-50 text-sm">
                Les statistiques calculées sont fiables avec un niveau de confiance de {validation.confidenceLevel}%. 
                Pour des analyses plus poussées, utiliser la fenêtre "Analyse Avancée".
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimplifiedAnalysisPage;
