import React, { useState, useEffect } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';
import {
  ChartBarIcon,
  AdjustmentsHorizontalIcon,
  DocumentArrowDownIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  PlayIcon,
  StopIcon,
  Cog6ToothIcon,
  ClockIcon,
  SignalIcon,
  CalculatorIcon,
  TableCellsIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  WifiIcon
} from '@heroicons/react/24/outline';

interface AnalysisResult {
  parameter: string;
  value: number;
  unit: string;
  confidence: number;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
}

interface SpectralPeak {
  frequency: number;
  amplitude: number;
  period: number;
  confidence: number;
}

interface WaveStatistics {
  hMax: number;
  hMin: number;
  hMean: number;
  h13: number;
  hSignificant: number;
  tMean: number;
  tPeak: number;
  direction: number;
  spread: number;
}

const ProfessionalAnalysisPage: React.FC = () => {
  const { theme } = useUnifiedApp();
  const [selectedDataset, setSelectedDataset] = useState('current');
  const [analysisType, setAnalysisType] = useState('spectral');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [expandedSection, setExpandedSection] = useState<string | null>('parameters');
  
  const [filterSettings, setFilterSettings] = useState({
    lowPass: 0.5,
    highPass: 0.05,
    windowType: 'hanning',
    windowSize: 1024,
    overlap: 50
  });

  const [results, setResults] = useState<AnalysisResult[]>([
    { parameter: 'H_max', value: 5.23, unit: 'm', confidence: 0.95, quality: 'excellent' },
    { parameter: 'H_1/3', value: 3.12, unit: 'm', confidence: 0.92, quality: 'excellent' },
    { parameter: 'H_sig', value: 3.45, unit: 'm', confidence: 0.94, quality: 'excellent' },
    { parameter: 'T_peak', value: 8.2, unit: 's', confidence: 0.88, quality: 'good' },
    { parameter: 'T_mean', value: 7.8, unit: 's', confidence: 0.91, quality: 'excellent' },
    { parameter: 'Direction', value: 238, unit: '°', confidence: 0.85, quality: 'good' },
    { parameter: 'Spread', value: 15.2, unit: '°', confidence: 0.79, quality: 'fair' },
  ]);

  const [spectralPeaks, setSpectralPeaks] = useState<SpectralPeak[]>([
    { frequency: 0.122, amplitude: 2.45, period: 8.2, confidence: 0.95 },
    { frequency: 0.244, amplitude: 0.87, period: 4.1, confidence: 0.78 },
    { frequency: 0.156, amplitude: 1.23, period: 6.4, confidence: 0.82 },
  ]);

  // Simulation du traitement
  useEffect(() => {
    let interval: number | null = null;
    
    if (isProcessing) {
      interval = setInterval(() => {
        setProcessingProgress(prev => {
          if (prev >= 100) {
            setIsProcessing(false);
            return 100;
          }
          return prev + Math.random() * 10;
        });
      }, 200);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isProcessing]);

  const handleStartAnalysis = () => {
    setIsProcessing(true);
    setProcessingProgress(0);
  };

  const handleStopAnalysis = () => {
    setIsProcessing(false);
    setProcessingProgress(0);
  };

  const handleExportResults = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      dataset: selectedDataset,
      analysisType: analysisType,
      filterSettings: filterSettings,
      results: results,
      spectralPeaks: spectralPeaks
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent': return 'text-green-600';
      case 'good': return 'text-blue-600';
      case 'fair': return 'text-yellow-600';
      case 'poor': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getQualityBg = (quality: string) => {
    switch (quality) {
      case 'excellent': return 'bg-green-100';
      case 'good': return 'bg-blue-100';
      case 'fair': return 'bg-yellow-100';
      case 'poor': return 'bg-red-100';
      default: return 'bg-gray-100';
    }
  };

  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="h-full flex flex-col" style={{ backgroundColor: 'var(--bg-primary)' }}>
      {/* Header Professional */}
      <div className="h-16 flex items-center justify-between px-6 border-b" style={{
        backgroundColor: 'var(--bg-elevated)',
        borderColor: 'var(--border-primary)'
      }}>
        <div className="flex items-center space-x-4">
          <CalculatorIcon className="w-6 h-6" style={{ color: 'var(--accent-primary)' }} />
          <div>
            <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
              Analyse Avancée des Données
            </h1>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Traitement du signal et analyse statistique
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            isProcessing ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
          }`}>
            {isProcessing ? `TRAITEMENT ${processingProgress.toFixed(0)}%` : 'PRÊT'}
          </div>
          
          <div className="flex space-x-2">
            {!isProcessing ? (
              <button
                onClick={handleStartAnalysis}
                className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                <PlayIcon className="w-4 h-4" />
                <span>Analyser</span>
              </button>
            ) : (
              <button
                onClick={handleStopAnalysis}
                className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                <StopIcon className="w-4 h-4" />
                <span>Arrêter</span>
              </button>
            )}
            
            <button
              onClick={handleExportResults}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              <DocumentArrowDownIcon className="w-4 h-4" />
              <span>Export</span>
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Panneau de contrôle gauche */}
        <div className="w-80 border-r flex flex-col" style={{
          backgroundColor: 'var(--bg-secondary)',
          borderColor: 'var(--border-primary)'
        }}>
          {/* Sélection des données */}
          <div className="p-4 border-b" style={{ borderColor: 'var(--border-primary)' }}>
            <button
              onClick={() => toggleSection('dataset')}
              className="w-full flex items-center justify-between text-left"
            >
              <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                Source des Données
              </h3>
              {expandedSection === 'dataset' ? 
                <ChevronDownIcon className="w-4 h-4" /> : 
                <ChevronRightIcon className="w-4 h-4" />
              }
            </button>
            
            {expandedSection === 'dataset' && (
              <div className="mt-3 space-y-2">
                <select
                  value={selectedDataset}
                  onChange={(e) => setSelectedDataset(e.target.value)}
                  disabled={isProcessing}
                  className="w-full px-3 py-2 rounded-md border text-sm"
                  style={{
                    backgroundColor: 'var(--bg-primary)',
                    borderColor: 'var(--border-secondary)',
                    color: 'var(--text-primary)'
                  }}
                >
                  <option value="current">Session Actuelle</option>
                  <option value="archive_001">Archive_001.dat</option>
                  <option value="archive_002">Archive_002.dat</option>
                  <option value="archive_003">Archive_003.dat</option>
                </select>
                
                <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                  <div>Durée: 2h 34min</div>
                  <div>Points: 18,432</div>
                  <div>Fréq.: 2 Hz</div>
                </div>
              </div>
            )}
          </div>

          {/* Type d'analyse */}
          <div className="p-4 border-b" style={{ borderColor: 'var(--border-primary)' }}>
            <button
              onClick={() => toggleSection('analysis')}
              className="w-full flex items-center justify-between text-left"
            >
              <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                Type d'Analyse
              </h3>
              {expandedSection === 'analysis' ? 
                <ChevronDownIcon className="w-4 h-4" /> : 
                <ChevronRightIcon className="w-4 h-4" />
              }
            </button>
            
            {expandedSection === 'analysis' && (
              <div className="mt-3 space-y-2">
                <div className="space-y-2">
                  {[
                    { value: 'spectral', label: 'Analyse Spectrale', icon: WifiIcon },
                    { value: 'statistical', label: 'Statistiques', icon: TableCellsIcon },
                    { value: 'directional', label: 'Directionnelle', icon: SignalIcon },
                    { value: 'extreme', label: 'Valeurs Extrêmes', icon: ChartBarIcon }
                  ].map(type => (
                    <label key={type.value} className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="radio"
                        value={type.value}
                        checked={analysisType === type.value}
                        onChange={(e) => setAnalysisType(e.target.value)}
                        disabled={isProcessing}
                        className="rounded"
                      />
                      <type.icon className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                      <span className="text-sm" style={{ color: 'var(--text-primary)' }}>
                        {type.label}
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Paramètres de filtrage */}
          <div className="p-4 border-b" style={{ borderColor: 'var(--border-primary)' }}>
            <button
              onClick={() => toggleSection('parameters')}
              className="w-full flex items-center justify-between text-left"
            >
              <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                Paramètres de Traitement
              </h3>
              {expandedSection === 'parameters' ? 
                <ChevronDownIcon className="w-4 h-4" /> : 
                <ChevronRightIcon className="w-4 h-4" />
              }
            </button>
            
            {expandedSection === 'parameters' && (
              <div className="mt-3 space-y-3">
                <div>
                  <label className="block text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                    Passe-Bas (Hz)
                  </label>
                  <input
                    type="number"
                    value={filterSettings.lowPass}
                    onChange={(e) => setFilterSettings({...filterSettings, lowPass: Number(e.target.value)})}
                    step="0.01"
                    min="0.01"
                    max="1"
                    disabled={isProcessing}
                    className="w-full px-2 py-1 rounded border text-sm"
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: 'var(--border-secondary)',
                      color: 'var(--text-primary)'
                    }}
                  />
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                    Passe-Haut (Hz)
                  </label>
                  <input
                    type="number"
                    value={filterSettings.highPass}
                    onChange={(e) => setFilterSettings({...filterSettings, highPass: Number(e.target.value)})}
                    step="0.001"
                    min="0.001"
                    max="0.1"
                    disabled={isProcessing}
                    className="w-full px-2 py-1 rounded border text-sm"
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: 'var(--border-secondary)',
                      color: 'var(--text-primary)'
                    }}
                  />
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                    Fenêtre FFT
                  </label>
                  <select
                    value={filterSettings.windowType}
                    onChange={(e) => setFilterSettings({...filterSettings, windowType: e.target.value})}
                    disabled={isProcessing}
                    className="w-full px-2 py-1 rounded border text-sm"
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: 'var(--border-secondary)',
                      color: 'var(--text-primary)'
                    }}
                  >
                    <option value="hanning">Hanning</option>
                    <option value="hamming">Hamming</option>
                    <option value="blackman">Blackman</option>
                    <option value="rectangular">Rectangulaire</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                    Taille Fenêtre
                  </label>
                  <select
                    value={filterSettings.windowSize}
                    onChange={(e) => setFilterSettings({...filterSettings, windowSize: Number(e.target.value)})}
                    disabled={isProcessing}
                    className="w-full px-2 py-1 rounded border text-sm"
                    style={{
                      backgroundColor: 'var(--bg-primary)',
                      borderColor: 'var(--border-secondary)',
                      color: 'var(--text-primary)'
                    }}
                  >
                    <option value={256}>256</option>
                    <option value={512}>512</option>
                    <option value={1024}>1024</option>
                    <option value={2048}>2048</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-xs font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>
                    Recouvrement (%)
                  </label>
                  <input
                    type="range"
                    value={filterSettings.overlap}
                    onChange={(e) => setFilterSettings({...filterSettings, overlap: Number(e.target.value)})}
                    min="0"
                    max="75"
                    step="5"
                    disabled={isProcessing}
                    className="w-full"
                  />
                  <div className="text-xs text-center" style={{ color: 'var(--text-muted)' }}>
                    {filterSettings.overlap}%
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Progrès du traitement */}
          {isProcessing && (
            <div className="p-4">
              <h3 className="text-sm font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
                Traitement en Cours
              </h3>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${processingProgress}%` }}
                />
              </div>
              <div className="text-xs mt-1 text-center" style={{ color: 'var(--text-secondary)' }}>
                {processingProgress.toFixed(0)}%
              </div>
            </div>
          )}
        </div>

        {/* Zone principale des résultats */}
        <div className="flex-1 flex flex-col">
          {/* Onglets de résultats */}
          <div className="h-12 border-b flex items-center px-4" style={{
            backgroundColor: 'var(--bg-secondary)',
            borderColor: 'var(--border-primary)'
          }}>
            <div className="flex space-x-4">
              {[
                { id: 'parameters', name: 'Paramètres', icon: TableCellsIcon },
                { id: 'spectral', name: 'Spectre', icon: WifiIcon },
                { id: 'statistics', name: 'Statistiques', icon: ChartBarIcon },
                { id: 'quality', name: 'Qualité', icon: AdjustmentsHorizontalIcon }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setAnalysisType(tab.id)}
                  className={`flex items-center space-x-2 px-3 py-1 rounded-lg text-sm transition-colors ${
                    analysisType === tab.id
                      ? 'bg-blue-500 text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Contenu des résultats */}
          <div className="flex-1 p-6 overflow-auto">
            {analysisType === 'parameters' && (
              <div className="grid grid-cols-2 gap-6">
                {/* Tableau des paramètres */}
                <div className="rounded-lg border p-4" style={{
                  backgroundColor: 'var(--bg-primary)',
                  borderColor: 'var(--border-primary)'
                }}>
                  <h4 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                    Paramètres de Houle
                  </h4>
                  
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead style={{ backgroundColor: 'var(--bg-tertiary)' }}>
                        <tr>
                          <th className="text-left p-3" style={{ color: 'var(--text-secondary)' }}>Paramètre</th>
                          <th className="text-right p-3" style={{ color: 'var(--text-secondary)' }}>Valeur</th>
                          <th className="text-center p-3" style={{ color: 'var(--text-secondary)' }}>Qualité</th>
                        </tr>
                      </thead>
                      <tbody>
                        {results.map((result, index) => (
                          <tr key={index} className={index % 2 === 0 ? '' : 'bg-gray-50'} style={{
                            backgroundColor: index % 2 === 0 ? 'transparent' : 'var(--bg-secondary)'
                          }}>
                            <td className="p-3 font-medium" style={{ color: 'var(--text-primary)' }}>
                              {result.parameter}
                            </td>
                            <td className="p-3 text-right font-mono" style={{ color: 'var(--text-primary)' }}>
                              {result.value.toFixed(2)} {result.unit}
                            </td>
                            <td className="p-3 text-center">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getQualityBg(result.quality)} ${getQualityColor(result.quality)}`}>
                                {result.quality}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Graphique des paramètres */}
                <div className="rounded-lg border p-4" style={{
                  backgroundColor: 'var(--bg-primary)',
                  borderColor: 'var(--border-primary)'
                }}>
                  <h4 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                    Évolution Temporelle
                  </h4>
                  
                  <div className="h-64 flex items-center justify-center" style={{
                    backgroundColor: 'var(--bg-secondary)',
                    borderRadius: '4px'
                  }}>
                    <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                      <ChartBarIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p className="text-sm">Graphique des paramètres</p>
                      <p className="text-xs">Evolution temporelle H_sig, T_peak</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {analysisType === 'spectral' && (
              <div className="grid grid-cols-2 gap-6">
                {/* Spectre de densité */}
                <div className="rounded-lg border p-4" style={{
                  backgroundColor: 'var(--bg-primary)',
                  borderColor: 'var(--border-primary)'
                }}>
                  <h4 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                    Spectre de Densité d'Énergie
                  </h4>
                  
                  <div className="h-64 flex items-center justify-center" style={{
                    backgroundColor: 'var(--bg-secondary)',
                    borderRadius: '4px'
                  }}>
                    <div className="text-center" style={{ color: 'var(--text-muted)' }}>
                      <WifiIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p className="text-sm">Spectre S(f)</p>
                      <p className="text-xs">Densité spectrale d'énergie</p>
                    </div>
                  </div>
                </div>

                {/* Pics spectraux */}
                <div className="rounded-lg border p-4" style={{
                  backgroundColor: 'var(--bg-primary)',
                  borderColor: 'var(--border-primary)'
                }}>
                  <h4 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                    Pics Spectraux Détectés
                  </h4>
                  
                  <div className="space-y-3">
                    {spectralPeaks.map((peak, index) => (
                      <div key={index} className="p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-medium" style={{ color: 'var(--text-primary)' }}>
                            Pic #{index + 1}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs ${
                            peak.confidence > 0.9 ? 'bg-green-100 text-green-800' :
                            peak.confidence > 0.8 ? 'bg-blue-100 text-blue-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}>
                            {(peak.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-2 text-xs" style={{ color: 'var(--text-secondary)' }}>
                          <div>
                            <span className="block">Fréquence</span>
                            <span className="font-mono">{peak.frequency.toFixed(3)} Hz</span>
                          </div>
                          <div>
                            <span className="block">Période</span>
                            <span className="font-mono">{peak.period.toFixed(1)} s</span>
                          </div>
                          <div>
                            <span className="block">Amplitude</span>
                            <span className="font-mono">{peak.amplitude.toFixed(2)} m²/Hz</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Autres onglets similaires... */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalAnalysisPage;
