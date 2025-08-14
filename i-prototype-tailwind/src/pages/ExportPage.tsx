import React, { useState } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';
import { api } from '../api/CHNeoWaveAPI';

const ExportPage: React.FC = () => {
  // 🔄 PHASE 2 - CATÉGORIE B : Intégration API Export avec formats backend
  const { 
    currentSession, 
    sessions, 
    addNotification, 
    addError,
    isConnectedToBackend 
  } = useUnifiedApp();
  
  const [exportFormat, setExportFormat] = useState<'hdf5' | 'csv' | 'json' | 'matlab'>('csv');
  const [isExporting, setIsExporting] = useState(false);
  const [reportPreview, setReportPreview] = useState(false);
  const [selectedSession, setSelectedSession] = useState(currentSession?.id || '');
  const [includeMetadata, setIncludeMetadata] = useState(true);
  const [compression, setCompression] = useState(true);

  const handleExport = async () => {
    if (!selectedSession) {
      addError({
        level: 'warning',
        message: 'Veuillez sélectionner une session à exporter',
        timestamp: Date.now(),
        source: 'export'
      });
      return;
    }

    setIsExporting(true);
    
    try {
      let exportResult;
      
      // 🔄 CATÉGORIE B : Export MATLAB intégré (était manquant dans l'implémentation)
      switch (exportFormat) {
        case 'hdf5':
          exportResult = await api.exportToHDF5(selectedSession, { 
            includeMetadata, 
            compression 
          });
          break;
        case 'csv':
          exportResult = await api.exportToCSV(selectedSession, { includeMetadata });
          break;
        case 'json':
          exportResult = await api.exportToJSON(selectedSession, { includeMetadata });
          break;
        case 'matlab':
          exportResult = await api.exportToMatlab(selectedSession, { includeMetadata });
          break;
      }

      // Télécharger le fichier si disponible
      if (exportResult.download_url) {
        const link = document.createElement('a');
        link.href = exportResult.download_url;
        link.download = `export_${selectedSession}.${exportFormat}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }

      addNotification({
        level: 'info',
        message: `Export ${exportFormat.toUpperCase()} terminé avec succès`,
        timestamp: Date.now(),
        source: 'export',
        details: { 
          format: exportFormat, 
          session: selectedSession,
          size: exportResult.file_size_bytes 
        }
      });

    } catch (error) {
      addError({
        level: 'error',
        message: `Erreur lors de l'export ${exportFormat.toUpperCase()}`,
        timestamp: Date.now(),
        source: 'export',
        details: { error: error instanceof Error ? error.message : String(error) }
      });
    } finally {
      setIsExporting(false);
    }
  };

  const handleGenerateReport = () => {
    setReportPreview(true);
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Export et Rapports</h2>
      
      {/* Export Options */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Options d'Export</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Sélection Session */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Session à Exporter
            </label>
            <select
              value={selectedSession}
              onChange={(e) => setSelectedSession(e.target.value)}
              disabled={!isConnectedToBackend}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            >
              <option value="">Sélectionner une session...</option>
              {sessions.map(session => (
                <option key={session.id} value={session.id}>
                  {session.name} ({session.samples} échantillons)
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              {sessions.length} session(s) disponible(s)
            </p>
          </div>
          
          {/* Format Export */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Format d'Export
            </label>
            <select
              value={exportFormat}
              onChange={(e) => setExportFormat(e.target.value as 'hdf5' | 'csv' | 'json' | 'matlab')}
              disabled={!selectedSession}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            >
              <option value="hdf5">HDF5 (Scientifique)</option>
              <option value="csv">CSV (Tableur)</option>
              <option value="json">JSON (Données)</option>
              <option value="matlab">MATLAB (.mat)</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              {exportFormat === 'hdf5' && 'Format recommandé pour données scientifiques'}
              {exportFormat === 'csv' && 'Compatible Excel et tableurs'}
              {exportFormat === 'json' && 'Format léger pour applications web'}
              {exportFormat === 'matlab' && 'Compatible MATLAB/Octave'}
            </p>
          </div>
          
          {/* Options Avancées */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Options
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={includeMetadata}
                  onChange={(e) => setIncludeMetadata(e.target.checked)}
                  className="rounded mr-2"
                />
                <span className="text-sm">Inclure métadonnées</span>
              </label>
              {exportFormat === 'hdf5' && (
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={compression}
                    onChange={(e) => setCompression(e.target.checked)}
                    className="rounded mr-2"
                  />
                  <span className="text-sm">Compression GZIP</span>
                </label>
              )}
            </div>
          </div>
        </div>

        {/* Informations Session Sélectionnée */}
        {selectedSession && sessions.find(s => s.id === selectedSession) && (
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="text-sm font-semibold text-blue-800 mb-2">Session Sélectionnée</h4>
            {(() => {
              const session = sessions.find(s => s.id === selectedSession)!;
              return (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-blue-700">
                  <div>
                    <span className="font-medium">Nom:</span><br />
                    {session.name}
                  </div>
                  <div>
                    <span className="font-medium">Échantillons:</span><br />
                    {session.samples.toLocaleString()}
                  </div>
                  <div>
                    <span className="font-medium">Taille:</span><br />
                    {(session.fileSize / 1024 / 1024).toFixed(1)} MB
                  </div>
                  <div>
                    <span className="font-medium">Sondes:</span><br />
                    {session.sondes.length} sonde(s)
                  </div>
                </div>
              );
            })()}
          </div>
        )}
          
        <div className="flex items-end space-x-4">
            <button
              onClick={handleExport}
              disabled={isExporting}
              className={`flex-1 py-3 rounded-lg transition-colors font-medium ${
                isExporting
                  ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              {isExporting ? 'Export en Cours...' : 'Exporter les Données'}
            </button>
          </div>
        </div>
        
        <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="border rounded-lg p-4 text-center hover:bg-gray-50 transition-colors cursor-pointer">
            <div className="text-2xl mb-2">📊</div>
            <p className="text-sm">Données Brutes</p>
          </div>
          <div className="border rounded-lg p-4 text-center hover:bg-gray-50 transition-colors cursor-pointer">
            <div className="text-2xl mb-2">📈</div>
            <p className="text-sm">Spectres</p>
          </div>
          <div className="border rounded-lg p-4 text-center hover:bg-gray-50 transition-colors cursor-pointer">
            <div className="text-2xl mb-2">📋</div>
            <p className="text-sm">Statistiques</p>
          </div>
          <div className="border rounded-lg p-4 text-center hover:bg-gray-50 transition-colors cursor-pointer">
            <div className="text-2xl mb-2">⚙️</div>
            <p className="text-sm">Calibration</p>
          </div>
          <div className="border rounded-lg p-4 text-center hover:bg-gray-50 transition-colors cursor-pointer">
            <div className="text-2xl mb-2">📄</div>
            <p className="text-sm">Métadonnées</p>
          </div>
        </div>
        
        {/* Report Generation */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Génération de Rapports</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="border rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
            <h4 className="font-medium mb-2">Rapport Technique</h4>
            <p className="text-sm text-gray-600">
              Rapport complet avec méthodologie, résultats et validation ITTC
            </p>
          </div>
          <div className="border rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
            <h4 className="font-medium mb-2">Rapport d'Essai</h4>
            <p className="text-sm text-gray-600">
              Données brutes et statistiques des essais en bassin
            </p>
          </div>
          <div className="border rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer">
            <h4 className="font-medium mb-2">Rapport de Calibration</h4>
            <p className="text-sm text-gray-600">
              Certificat de calibration pour chaque sonde utilisée
            </p>
          </div>
        </div>
        
        <button
          onClick={handleGenerateReport}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition-colors font-medium"
        >
          Générer le Rapport
        </button>
      </div>
      
      {/* Report Preview */}
      {reportPreview && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-700">Aperçu du Rapport</h3>
            <button
              onClick={() => setReportPreview(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              Fermer
            </button>
          </div>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <div className="text-4xl mb-4">📄</div>
            <p className="text-gray-600 mb-4">
              Aperçu du rapport d'analyse maritime - CHNeoWave v1.0
            </p>
            <div className="inline-block bg-blue-100 text-blue-800 px-4 py-2 rounded-lg text-sm">
              Hs = 2.42m | Tp = 8.1s | Conformité ITTC: ✅ Validée
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExportPage;
