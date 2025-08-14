import React, { useState } from 'react';
import { 
  ChartBarIcon,
  CpuChipIcon,
  DocumentChartBarIcon,
  BeakerIcon,
  CalculatorIcon,
  CogIcon
} from '@heroicons/react/24/outline';

const AdvancedAnalysisPage: React.FC = () => {
  const [selectedAnalysis, setSelectedAnalysis] = useState<string>('spectral');
  const [isProcessing, setIsProcessing] = useState(false);

  const analysisTypes = [
    {
      id: 'spectral',
      name: 'Analyse Spectrale',
      icon: ChartBarIcon,
      description: 'Analyse FFT et densité spectrale de puissance',
      color: 'from-blue-600 to-cyan-600'
    },
    {
      id: 'directional',
      name: 'Analyse Directionnelle',
      icon: CpuChipIcon,
      description: 'Distribution directionnelle des vagues',
      color: 'from-purple-600 to-pink-600'
    },
    {
      id: 'nonlinear',
      name: 'Analyse Non-Linéaire',
      icon: BeakerIcon,
      description: 'Bispectrum et interactions non-linéaires',
      color: 'from-emerald-600 to-teal-600'
    },
    {
      id: 'extreme',
      name: 'Analyse des Extrêmes',
      icon: CalculatorIcon,
      description: 'Distribution de Weibull et valeurs extrêmes',
      color: 'from-orange-600 to-red-600'
    },
    {
      id: 'coherence',
      name: 'Cohérence Spatiale',
      icon: DocumentChartBarIcon,
      description: 'Corrélation entre sondes multiples',
      color: 'from-indigo-600 to-purple-600'
    },
    {
      id: 'custom',
      name: 'Analyse Personnalisée',
      icon: CogIcon,
      description: 'Algorithmes définis par l\'utilisateur',
      color: 'from-slate-600 to-gray-600'
    }
  ];

  const handleStartAnalysis = () => {
    setIsProcessing(true);
    // Simulate processing
    setTimeout(() => {
      setIsProcessing(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen p-6 overflow-hidden" style={{ backgroundColor: 'var(--bg-primary)' }}>
      <div className="h-full max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>Analyse Avancée</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Outils d'analyse complexe pour données maritimes</p>
        </div>

        <div className="grid grid-cols-12 gap-6 h-[calc(100%-120px)]">
          
          {/* Analysis Selection - Left Panel */}
          <div className="col-span-4 space-y-4">
            <div className="themed-card golden-card h-full">
              <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Types d'Analyse</h3>
              
              <div className="space-y-3">
                {analysisTypes.map((analysis) => {
                  const Icon = analysis.icon;
                  const isSelected = selectedAnalysis === analysis.id;
                  
                  return (
                    <button
                      key={analysis.id}
                      onClick={() => setSelectedAnalysis(analysis.id)}
                      className={`w-full p-4 rounded-xl transition-all duration-300 text-left`}
                      style={{
                        background: isSelected ? 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))' : 'var(--bg-secondary)',
                        color: isSelected ? 'var(--text-inverse)' : 'var(--text-primary)',
                        border: `1px solid ${isSelected ? 'var(--accent-primary)' : 'var(--border-primary)'}`,
                        transform: isSelected ? 'scale(1.02)' : 'none'
                      }}
                    >
                      <div className="flex items-start space-x-3">
                        <div className={`flex-shrink-0`} style={{ color: isSelected ? 'var(--text-inverse)' : 'var(--text-secondary)' }}>
                          <Icon className="w-6 h-6" />
                        </div>
                        <div className="flex-1">
                          <h4 className={`font-medium`} style={{ color: isSelected ? 'var(--text-inverse)' : 'var(--text-primary)' }}>
                            {analysis.name}
                          </h4>
                          <p className={`text-xs mt-1`} style={{ color: isSelected ? 'var(--text-inverse)' : 'var(--text-secondary)' }}>
                            {analysis.description}
                          </p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Analysis Configuration & Results - Right Panel */}
          <div className="col-span-8 space-y-6">
            
            {/* Configuration Panel */}
              <div className="themed-card golden-card">
                <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                Configuration - {analysisTypes.find(a => a.id === selectedAnalysis)?.name}
              </h3>
              
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                      Fenêtre d'Analyse
                    </label>
                    <select className="w-full px-3 py-2 rounded-lg" style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)', color: 'var(--text-primary)' }}>
                      <option>Hanning</option>
                      <option>Hamming</option>
                      <option>Blackman</option>
                      <option>Kaiser</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                      Résolution Fréquentielle
                    </label>
                    <input 
                      type="number" 
                      defaultValue="0.01"
                      step="0.001"
                      className="w-full px-3 py-2 rounded-lg"
                      style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)', color: 'var(--text-primary)' }}
                    />
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                      Bande de Fréquence
                    </label>
                    <div className="flex space-x-2">
                      <input 
                        type="number" 
                        placeholder="Min (Hz)"
                        defaultValue="0.05"
                        step="0.01"
                        className="flex-1 px-3 py-2 rounded-lg"
                        style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)', color: 'var(--text-primary)' }}
                      />
                      <input 
                        type="number" 
                        placeholder="Max (Hz)"
                        defaultValue="2.0"
                        step="0.01"
                        className="flex-1 px-3 py-2 rounded-lg"
                        style={{ backgroundColor: 'var(--bg-elevated)', border: '1px solid var(--border-primary)', color: 'var(--text-primary)' }}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                      Overlap (%)
                    </label>
                    <input 
                      type="range" 
                      min="0" 
                      max="75" 
                      defaultValue="50"
                      className="w-full"
                    />
                    <div className="flex justify-between text-xs mt-1" style={{ color: 'var(--text-muted)' }}>
                      <span>0%</span>
                      <span>50%</span>
                      <span>75%</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 flex space-x-4">
                <button
                  onClick={handleStartAnalysis}
                  disabled={isProcessing}
                  className={`px-6 py-3 rounded-lg font-medium transition-all duration-200`}
                  style={{
                    backgroundColor: isProcessing ? 'var(--bg-tertiary)' : 'var(--accent-primary)',
                    color: isProcessing ? 'var(--text-secondary)' : 'var(--text-inverse)',
                    cursor: isProcessing ? 'not-allowed' : 'pointer'
                  }}
                >
                  {isProcessing ? 'Traitement en cours...' : 'Démarrer Analyse'}
                </button>
                
                <button className="px-6 py-3 rounded-lg font-medium transition-colors" style={{ backgroundColor: 'var(--bg-surface)', color: 'var(--text-primary)', border: '1px solid var(--border-primary)' }}>
                  Exporter Configuration
                </button>
              </div>
            </div>

            {/* Results Panel */}
            <div className="themed-card golden-card flex-1">
              <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Résultats d'Analyse</h3>
              
              {isProcessing ? (
                <div className="flex items-center justify-center h-48">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-slate-400">Traitement en cours...</p>
                    <p className="text-slate-500 text-sm mt-2">Analyse spectrale avancée</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Mock Results Graph */}
                  <div className="rounded-lg p-4" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                    <h4 className="font-medium mb-3" style={{ color: 'var(--text-primary)' }}>Densité Spectrale de Puissance</h4>
                    <div className="h-48 rounded-lg p-4" style={{ backgroundColor: 'var(--bg-tertiary)' }}>
                      <svg width="100%" height="100%" viewBox="0 0 400 160">
                        {/* Grid */}
                        <defs>
                          <pattern id="advancedGrid" width="40" height="32" patternUnits="userSpaceOnUse">
                            <path d="M 40 0 L 0 0 0 32" fill="none" stroke="#334155" strokeWidth="0.5"/>
                          </pattern>
                        </defs>
                        <rect width="400" height="160" fill="url(#advancedGrid)" />
                        
                        {/* Axes */}
                        <line x1="40" y1="140" x2="360" y2="140" stroke="#64748b" strokeWidth="2"/>
                        <line x1="40" y1="140" x2="40" y2="20" stroke="#64748b" strokeWidth="2"/>
                        
                        {/* Mock spectrum curve */}
                          <path d="M 40 120 Q 80 100 120 80 T 200 60 T 280 90 T 360 130" stroke="var(--accent-primary)" strokeWidth="2" fill="none" />
                        
                        {/* Peak marker */}
                        <circle cx="200" cy="60" r="4" fill="#ef4444" stroke="#ffffff" strokeWidth="2"/>
                        <text x="200" y="50" textAnchor="middle" fill="#ef4444" fontSize="12">Peak</text>
                        
                        {/* Labels */}
                          <text x="200" y="155" textAnchor="middle" fill="var(--text-muted)" fontSize="12">Fréquence (Hz)</text>
                          <text x="25" y="80" textAnchor="middle" fill="var(--text-muted)" fontSize="12" transform="rotate(-90 25 80)">PSD (m²/Hz)</text>
                      </svg>
                    </div>
                  </div>

                  {/* Results Summary */}
                  <div className="grid grid-cols-3 gap-4">
                    <div className="rounded-lg p-4 text-center" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                      <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Fréquence Pic</p>
                      <p className="font-mono text-lg" style={{ color: 'var(--text-primary)' }}>0.125 Hz</p>
                    </div>
                    <div className="rounded-lg p-4 text-center" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                      <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Énergie Totale</p>
                      <p className="font-mono text-lg" style={{ color: 'var(--text-primary)' }}>2.34 m²</p>
                    </div>
                    <div className="rounded-lg p-4 text-center" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                      <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Largeur Spectrale</p>
                      <p className="font-mono text-lg" style={{ color: 'var(--text-primary)' }}>0.089</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedAnalysisPage;
