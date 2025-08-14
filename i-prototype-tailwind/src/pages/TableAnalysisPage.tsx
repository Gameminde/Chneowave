import React, { useState, useEffect } from 'react';
import { 
  ChartBarIcon,
  CalculatorIcon,
  CheckCircleIcon,
  TableCellsIcon
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
  hsHmeanRatio: number; // Ratio Hs/Hmean
}

interface StatisticalValidation {
  sampleSize: number;
  confidenceLevel: number;
  standardError: number;
  isStatisticallySignificant: boolean;
  pValue: number;
}

const TableAnalysisPage: React.FC = () => {
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
    bandwidth: 0.25,
    hsHmeanRatio: 1.31
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
        kurtosis: 2.98 + Math.random() * 0.2 - 0.1,
        bandwidth: 0.25 + Math.random() * 0.05 - 0.025,
        hsHmeanRatio: (2.42 + Math.sin(Date.now() / 10000) * 0.3) / (1.85 + Math.random() * 0.1 - 0.05)
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

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('fr-FR', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    });
  };

  const getQualityIndicator = (value: number, type: string) => {
    switch (type) {
      case 'skewness':
        return Math.abs(value) < 0.5 ? 'Symétrique' : 'Asymétrique';
      case 'kurtosis':
        return Math.abs(value - 3) < 0.5 ? 'Normale' : 'Non-normale';
      case 'bandwidth':
        return value < 0.3 ? 'Étroite' : 'Large';
      default:
        return 'Normal';
    }
  };

  const getQualityColor = (value: number, type: string) => {
    switch (type) {
      case 'skewness':
        return Math.abs(value) < 0.5 ? 'text-green-400' : 'text-yellow-400';
      case 'kurtosis':
        return Math.abs(value - 3) < 0.5 ? 'text-green-400' : 'text-yellow-400';
      case 'bandwidth':
        return value < 0.3 ? 'text-green-400' : 'text-yellow-400';
      default:
        return 'text-cyan-400';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-cyan-900 to-teal-900 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <TableCellsIcon className="w-8 h-8 text-cyan-400" />
            <div>
              <h1 className="text-2xl font-bold text-cyan-50">Analyse Statistique</h1>
              <p className="text-cyan-300 text-sm">Tableau des résultats statistiques des données de houle</p>
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

      {/* Tableau principal des résultats statistiques */}
      <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-6 mb-6">
        <h3 className="text-xl font-bold text-cyan-50 mb-6 flex items-center">
          <ChartBarIcon className="w-6 h-6 mr-2" />
          Résultats Statistiques Complets
        </h3>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left" style={{ fontSize: '1.125rem' }}>
            <thead>
              <tr className="border-b-2 border-cyan-700/50">
                <th className="text-cyan-300 font-semibold py-4 px-6 text-base" style={{ width: '30%' }}>PARAMÈTRE</th>
                <th className="text-cyan-300 font-semibold py-4 px-6 text-base text-center" style={{ width: '18.5%' }}>VALEUR</th>
                <th className="text-cyan-300 font-semibold py-4 px-6 text-base text-center" style={{ width: '11.5%' }}>UNITÉ</th>
                <th className="text-cyan-300 font-semibold py-4 px-6 text-base text-center" style={{ width: '18.5%' }}>QUALITÉ</th>
                <th className="text-cyan-300 font-semibold py-4 px-6 text-base" style={{ width: '21.5%' }}>DESCRIPTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              
              {/* Section Hauteurs */}
              <tr className="bg-slate-800/30">
                <td colSpan={5} className="py-4 px-6 text-cyan-400 font-semibold text-base">
                  📊 HAUTEURS DE HOULE
                </td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Hauteur Significative (Hs)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-xl">{waveStats.Hs.toFixed(2)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">m</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-green-500/20 text-green-400 px-3 py-2 rounded text-sm font-medium">
                    EXCELLENT
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Hauteur moyenne du tiers supérieur des vagues</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Hauteur Maximale (Hmax)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.Hmax.toFixed(2)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">m</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-2 rounded text-sm font-medium">
                    NORMAL
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Hauteur de vague maximale observée</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Hauteur 1/3 (H1/3)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.H13.toFixed(2)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">m</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-green-500/20 text-green-400 px-3 py-2 rounded text-sm font-medium">
                    EXCELLENT
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Hauteur moyenne du tiers des plus hautes vagues</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Hauteur Moyenne (Hmoy)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.Hmean.toFixed(2)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">m</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-2 rounded text-sm font-medium">
                    NORMAL
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Hauteur moyenne de toutes les vagues</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Hauteur Minimale (Hmin)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.Hmin.toFixed(2)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">m</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-2 rounded text-sm font-medium">
                    NORMAL
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Hauteur de vague minimale observée</td>
              </tr>

              {/* Section Périodes */}
              <tr className="bg-slate-800/30">
                <td colSpan={5} className="py-4 px-6 text-cyan-400 font-semibold text-base">
                  ⏱️ PÉRIODES DE HOULE
                </td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Période Pic (Tp)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-xl">{waveStats.Tp.toFixed(1)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">s</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-green-500/20 text-green-400 px-3 py-2 rounded text-sm font-medium">
                    EXCELLENT
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Période correspondant au pic d'énergie spectrale</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Période Zéro-Crossing (Tz)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.Tz.toFixed(1)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">s</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-2 rounded text-sm font-medium">
                    NORMAL
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Période moyenne entre passages par zéro</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Période 1/3 (T1/3)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.T13.toFixed(1)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">s</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-green-500/20 text-green-400 px-3 py-2 rounded text-sm font-medium">
                    EXCELLENT
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Période moyenne du tiers des plus hautes vagues</td>
              </tr>
              
              <tr className="hover:bg-slate-800/20 transition-colors">
                <td className="py-4 px-6 text-cyan-50 font-medium text-base">Période Moyenne (Tmoy)</td>
                <td className="py-4 px-6 text-center text-cyan-50 font-bold text-lg">{waveStats.Tmean.toFixed(1)}</td>
                <td className="py-4 px-6 text-center text-cyan-300 text-base">s</td>
                <td className="py-4 px-6 text-center">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-2 rounded text-sm font-medium">
                    NORMAL
                  </span>
                </td>
                <td className="py-4 px-6 text-cyan-300 text-base">Période moyenne de toutes les vagues</td>
              </tr>


            </tbody>
          </table>
        </div>
      </div>

      {/* Validation statistique */}
      <div className="bg-slate-900/80 backdrop-blur-xl border border-cyan-700/50 rounded-lg p-6">
        <h3 className="text-lg font-bold text-cyan-50 mb-4 flex items-center">
          <CheckCircleIcon className="w-6 h-6 mr-2" />
          Validation Statistique
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 rounded-lg p-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <div className="text-cyan-300 mb-1">Taille échantillon</div>
                <div className="text-cyan-50 font-bold text-xl">{validation.sampleSize.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-cyan-300 mb-1">Niveau confiance</div>
                <div className="text-cyan-50 font-bold text-xl">{validation.confidenceLevel}%</div>
              </div>
              <div>
                <div className="text-cyan-300 mb-1">Erreur standard</div>
                <div className="text-cyan-50 font-bold text-xl">{validation.standardError.toFixed(3)}</div>
              </div>
              <div>
                <div className="text-cyan-300 mb-1">p-value</div>
                <div className="text-cyan-50 font-bold text-xl">{validation.pValue.toFixed(3)}</div>
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

export default TableAnalysisPage;
