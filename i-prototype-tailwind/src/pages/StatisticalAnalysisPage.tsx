import React, { useState, useEffect } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';
import { api } from '../api/CHNeoWaveAPI';
import { 
  ChartBarIcon, 
  TableCellsIcon,
  ArrowDownTrayIcon,
  CalendarDaysIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface StatisticalData {
  timestamp: Date;
  hMax: number;
  hMin: number;
  h13: number;
  hSignificant: number;
  period: number;
  frequency: number;
  snr: number;
  sondeId: number;
  duration: number;
  samplingRate: number;
}

const StatisticalAnalysisPage: React.FC = () => {
  // 🔄 CATÉGORIE C : Étendre calculs backend au lieu de simulation
  const { 
    sessions,
    currentSession,
    sondes,
    acquisitionData,
    isConnectedToBackend,
    addNotification,
    addError
  } = useUnifiedApp();
  
  const [statisticalData, setStatisticalData] = useState<StatisticalData[]>([]);
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
  const [selectedSensors, setSelectedSensors] = useState<number[]>([0, 1]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedSession, setSelectedSession] = useState(currentSession?.id || '');

  // Générer des données statistiques simulées
  useEffect(() => {
    const generateData = () => {
      const data: StatisticalData[] = [];
      const now = new Date();
      
      for (let i = 0; i < 50; i++) {
        for (const sondeId of selectedSensors) {
          const timestamp = new Date(now.getTime() - i * 30 * 60 * 1000); // Toutes les 30 minutes
          
          data.push({
            timestamp,
            hMax: 2.5 + Math.random() * 1.5,
            hMin: -2.0 - Math.random() * 1.0,
            h13: 1.8 + Math.random() * 0.8,
            hSignificant: 2.1 + Math.random() * 0.6,
            period: 7.5 + Math.random() * 2.0,
            frequency: 0.11 + Math.random() * 0.04,
            snr: 20 + Math.random() * 15,
            sondeId,
            duration: 300 + Math.random() * 600,
            samplingRate: [32, 50, 100, 200][Math.floor(Math.random() * 4)]
          });
        }
      }
      
      return data.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    };

    setIsLoading(true);
    setTimeout(() => {
      setStatisticalData(generateData());
      setIsLoading(false);
    }, 500);
  }, [selectedTimeRange, selectedSensors]);

  // Calculer les statistiques globales
  const globalStats = React.useMemo(() => {
    if (statisticalData.length === 0) return null;

    return {
      totalMeasurements: statisticalData.length,
      avgHMax: statisticalData.reduce((sum, d) => sum + d.hMax, 0) / statisticalData.length,
      avgHMin: statisticalData.reduce((sum, d) => sum + d.hMin, 0) / statisticalData.length,
      avgH13: statisticalData.reduce((sum, d) => sum + d.h13, 0) / statisticalData.length,
      avgHSignificant: statisticalData.reduce((sum, d) => sum + d.hSignificant, 0) / statisticalData.length,
      avgPeriod: statisticalData.reduce((sum, d) => sum + d.period, 0) / statisticalData.length,
      avgSNR: statisticalData.reduce((sum, d) => sum + d.snr, 0) / statisticalData.length,
      maxHMax: Math.max(...statisticalData.map(d => d.hMax)),
      minHMin: Math.min(...statisticalData.map(d => d.hMin))
    };
  }, [statisticalData]);

  const exportData = () => {
    const csvContent = [
      'Timestamp,Sonde ID,H Max (m),H Min (m),H 1/3 (m),H Sig (m),Period (s),Frequency (Hz),SNR (dB),Duration (s),Sampling Rate (Hz)',
      ...statisticalData.map(d => 
        `${d.timestamp.toISOString()},${d.sondeId},${d.hMax.toFixed(3)},${d.hMin.toFixed(3)},${d.h13.toFixed(3)},${d.hSignificant.toFixed(3)},${d.period.toFixed(2)},${d.frequency.toFixed(3)},${d.snr.toFixed(1)},${d.duration},${d.samplingRate}`
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `statistical_analysis_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-full" style={{ backgroundColor: 'var(--bg-primary)' }}>
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="p-3 rounded-xl" style={{ backgroundColor: 'var(--accent-primary)', color: 'var(--text-inverse)' }}>
              <TableCellsIcon className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-3xl font-bold" style={{ color: 'var(--text-primary)' }}>
                Analyse Statistique
              </h1>
              <p className="text-lg" style={{ color: 'var(--text-secondary)' }}>
                Tableau des résultats et métriques détaillées
              </p>
            </div>
          </div>
          
          <button
            onClick={exportData}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg transition-all"
            style={{ 
              backgroundColor: 'var(--accent-secondary)', 
              color: 'var(--text-inverse)' 
            }}
          >
            <ArrowDownTrayIcon className="w-5 h-5" />
            <span>Exporter CSV</span>
          </button>
        </div>

        {/* Filtres */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              Période d'analyse
            </label>
            <select
              value={selectedTimeRange}
              onChange={(e) => setSelectedTimeRange(e.target.value)}
              className="w-full px-3 py-2 rounded-lg themed-input"
            >
              <option value="1h">Dernière heure</option>
              <option value="6h">6 dernières heures</option>
              <option value="24h">24 dernières heures</option>
              <option value="7d">7 derniers jours</option>
              <option value="30d">30 derniers jours</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              Sondes sélectionnés
            </label>
            <div className="flex flex-wrap gap-2">
              {[1, 2, 3, 4, 5, 6, 7, 8].map(sondeId => (
                <button
                  key={sondeId}
                  onClick={() => {
                    setSelectedSensors(prev => 
                      prev.includes(sondeId)
                        ? prev.filter(id => id !== sondeId)
                        : [...prev, sondeId]
                    );
                  }}
                  className={`px-3 py-1 text-sm rounded-lg transition-all`}
                  style={{
                    backgroundColor: selectedSensors.includes(sondeId) ? 'var(--accent-primary)' : 'var(--bg-secondary)',
                    color: selectedSensors.includes(sondeId) ? 'var(--text-inverse)' : 'var(--text-secondary)',
                    border: `1px solid ${selectedSensors.includes(sondeId) ? 'var(--accent-primary)' : 'var(--border-primary)'}`
                  }}
                >
                  #{sondeId}
                </button>
              ))}
            </div>
          </div>
          
          <div className="flex items-end">
            <div className="text-sm" style={{ color: 'var(--text-muted)' }}>
              <div className="flex items-center space-x-2 mb-1">
                <CalendarDaysIcon className="w-4 h-4" />
                <span>Dernière mise à jour</span>
              </div>
              <div className="flex items-center space-x-2">
                <ClockIcon className="w-4 h-4" />
                <span>{new Date().toLocaleTimeString('fr-FR')}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Statistiques Globales */}
      {globalStats && (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <div className="p-4 rounded-xl text-center" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
            <div className="text-2xl font-bold mb-1" style={{ color: 'var(--accent-primary)' }}>
              {globalStats.totalMeasurements}
            </div>
            <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>Mesures</div>
          </div>
          
          <div className="p-4 rounded-xl text-center" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
            <div className="text-2xl font-bold mb-1" style={{ color: 'var(--status-success)' }}>
              {globalStats.maxHMax.toFixed(2)}m
            </div>
            <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>H Max Global</div>
          </div>
          
          <div className="p-4 rounded-xl text-center" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
            <div className="text-2xl font-bold mb-1" style={{ color: 'var(--status-error)' }}>
              {globalStats.minHMin.toFixed(2)}m
            </div>
            <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>H Min Global</div>
          </div>
          
          <div className="p-4 rounded-xl text-center" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
            <div className="text-2xl font-bold mb-1" style={{ color: 'var(--accent-secondary)' }}>
              {globalStats.avgH13.toFixed(2)}m
            </div>
            <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>H 1/3 Moyen</div>
          </div>
          
          <div className="p-4 rounded-xl text-center" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
            <div className="text-2xl font-bold mb-1" style={{ color: 'var(--accent-tertiary)' }}>
              {globalStats.avgPeriod.toFixed(1)}s
            </div>
            <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>Période Moy.</div>
          </div>
          
          <div className="p-4 rounded-xl text-center" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
            <div className="text-2xl font-bold mb-1" style={{ color: 'var(--status-info)' }}>
              {globalStats.avgSNR.toFixed(1)}dB
            </div>
            <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>SNR Moyen</div>
          </div>
        </div>
      )}

      {/* Tableau des Données */}
      <div className="rounded-xl overflow-hidden" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)' }}>
        <div className="p-6 border-b" style={{ borderColor: 'var(--border-primary)' }}>
          <h2 className="text-xl font-semibold flex items-center space-x-2" style={{ color: 'var(--text-primary)' }}>
            <ChartBarIcon className="w-6 h-6" />
            <span>Données Statistiques Détaillées</span>
          </h2>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead style={{ backgroundColor: 'var(--bg-secondary)' }}>
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  Horodatage
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  Sonde
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  H Max (m)
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  H Min (m)
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  H 1/3 (m)
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  H Sig (m)
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  Période (s)
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  Fréquence (Hz)
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                  SNR (dB)
                </th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <tr>
                  <td colSpan={9} className="px-6 py-8 text-center" style={{ color: 'var(--text-secondary)' }}>
                    <div className="flex items-center justify-center space-x-2">
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2" style={{ borderColor: 'var(--accent-primary)' }}></div>
                      <span>Chargement des données...</span>
                    </div>
                  </td>
                </tr>
              ) : (
                statisticalData.slice(0, 100).map((data, index) => (
                  <tr key={index} className={index % 2 === 0 ? '' : ''} style={{ backgroundColor: index % 2 === 0 ? 'var(--bg-elevated)' : 'var(--bg-primary)' }}>
                    <td className="px-6 py-4 text-sm" style={{ color: 'var(--text-primary)' }}>
                      {data.timestamp.toLocaleString('fr-FR')}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span className="px-2 py-1 rounded text-xs font-medium" style={{ 
                        backgroundColor: 'var(--accent-primary)', 
                        color: 'var(--text-inverse)' 
                      }}>
                        #{data.sondeId}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ color: 'var(--status-success)' }}>
                      {data.hMax.toFixed(3)}
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ color: 'var(--status-error)' }}>
                      {data.hMin.toFixed(3)}
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ color: 'var(--text-primary)' }}>
                      {data.h13.toFixed(3)}
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ color: 'var(--text-primary)' }}>
                      {data.hSignificant.toFixed(3)}
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ color: 'var(--accent-tertiary)' }}>
                      {data.period.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ color: 'var(--text-secondary)' }}>
                      {data.frequency.toFixed(3)}
                    </td>
                    <td className="px-6 py-4 text-sm text-right font-mono" style={{ 
                      color: data.snr > 25 ? 'var(--status-success)' : data.snr > 15 ? 'var(--status-warning)' : 'var(--status-error)' 
                    }}>
                      {data.snr.toFixed(1)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        
        {statisticalData.length > 100 && (
          <div className="p-4 text-center border-t" style={{ borderColor: 'var(--border-primary)', color: 'var(--text-secondary)' }}>
            Affichage des 100 premières entrées sur {statisticalData.length} au total
          </div>
        )}
      </div>
    </div>
  );
};

export default StatisticalAnalysisPage;
