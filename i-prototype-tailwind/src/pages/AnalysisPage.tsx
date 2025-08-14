import React, { useState } from 'react';

const AnalysisPage: React.FC = () => {
  const [analysisMethod, setAnalysisMethod] = useState('fft');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleProcess = () => {
    setIsProcessing(true);
    // Simulate processing time
    setTimeout(() => setIsProcessing(false), 2000);
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Analyse des Données</h2>
      
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Méthode d'Analyse
            </label>
            <select
              value={analysisMethod}
              onChange={(e) => setAnalysisMethod(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="fft">FFT (Transformée de Fourier Rapide)</option>
              <option value="jonswap">JONSWAP</option>
              <option value="pierson-moskowitz">Pierson-Moskowitz</option>
              <option value="goda-svd">Goda-SVD</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <button
              onClick={handleProcess}
              disabled={isProcessing}
              className={`w-full py-3 rounded-lg transition-colors font-medium ${
                isProcessing
                  ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              {isProcessing ? 'Traitement en Cours...' : 'Lancer l\'Analyse'}
            </button>
          </div>
        </div>
      </div>
      
      {/* Power Spectrum Graph */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Spectre de Puissance</h3>
        <div className="bg-blue-900 h-80 rounded-lg flex items-center justify-center">
          <div className="text-white text-center">
            <p className="text-lg mb-2">Spectre de puissance en temps réel</p>
            <p className="text-sm opacity-75">Méthode: {analysisMethod.toUpperCase()}</p>
          </div>
        </div>
      </div>
      
      {/* Maritime Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Statistiques Maritimes</h3>
          <div className="space-y-4">
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">Hauteur Significative (Hs)</span>
              <span className="font-medium">2.42 m</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">Hauteur Maximum (Hmax)</span>
              <span className="font-medium">3.75 m</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">Hauteur Minimum (Hmin)</span>
              <span className="font-medium">0.12 m</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">Hauteur 1/3 (H1/3)</span>
              <span className="font-medium">2.65 m</span>
            </div>
            <div className="flex justify-between border-b pb-2">
              <span className="text-gray-600">Période Moyenne (Tm)</span>
              <span className="font-medium">7.8 s</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Période de Pic (Tp)</span>
              <span className="font-medium">8.1 s</span>
            </div>
          </div>
        </div>
        
        {/* ITTC Validation */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Validation ITTC</h3>
          <div className="space-y-4">
            <div className="flex items-center">
              <div className="w-5 h-5 rounded-full bg-green-500 mr-3"></div>
              <span>Conformité aux procédures ITTC</span>
            </div>
            <div className="flex items-center">
              <div className="w-5 h-5 rounded-full bg-green-500 mr-3"></div>
              <span>Résolution spectrale adéquate</span>
            </div>
            <div className="flex items-center">
              <div className="w-5 h-5 rounded-full bg-green-500 mr-3"></div>
              <span>Durée d'acquisition suffisante</span>
            </div>
            <div className="flex items-center">
              <div className="w-5 h-5 rounded-full bg-green-500 mr-3"></div>
              <span>Calibration des sondes validée</span>
            </div>
            <div className="flex items-center">
              <div className="w-5 h-5 rounded-full bg-yellow-500 mr-3"></div>
              <span>Validation ISO 9001 en cours</span>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-gray-700 mb-2">Résultats de l'Analyse</h4>
            <p className="text-sm text-gray-600">
              Spectre de puissance calculé avec la méthode {analysisMethod.toUpperCase()}. 
              Les données respectent les standards ITTC pour l'analyse maritime.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;
