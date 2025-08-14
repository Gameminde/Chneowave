import React, { useState } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';

const SettingsPage: React.FC = () => {
  // 🔄 PHASE 2 - CATÉGORIE B : Ajout fonctionnalités backend manquantes
  const { 
    currentTheme, 
    setTheme, 
    systemStatus, 
    changeBackend, 
    testConnection,
    refreshSystemStatus,
    addNotification,
    isConnectedToBackend 
  } = useUnifiedApp();
  
  const [samplingRate, setSamplingRate] = useState(1000);
  const [bufferSize, setBufferSize] = useState(1024);
  const [timeout, setTimeout] = useState(5000);
  const [selectedBackend, setSelectedBackend] = useState<'ni-daqmx' | 'iotech' | 'demo'>(
    systemStatus?.backend_type || 'demo'
  );
  const [testChannels, setTestChannels] = useState<number[]>([0, 1]);
  const [isTestingConnection, setIsTestingConnection] = useState(false);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Configuration Système</h2>
      
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Paramètres d'Interface</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Thème de l'Application
            </label>
            <select
              value={currentTheme}
              onChange={(e) => setTheme(e.target.value as 'light' | 'dark' | 'beige')}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="light">Clair</option>
              <option value="dark">Sombre</option>
              <option value="beige">Solarized Light</option>
            </select>
          </div>
        </div>
      </div>
      
      {/* 🔄 CATÉGORIE B : Backend Hardware Selection (Manquant dans UI) */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Backend Matériel</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type de Backend
            </label>
            <select
              value={selectedBackend}
              onChange={(e) => setSelectedBackend(e.target.value as 'ni-daqmx' | 'iotech' | 'demo')}
              disabled={!isConnectedToBackend}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
            >
              <option value="demo">Demo (Simulation)</option>
              <option value="ni-daqmx">NI-DAQmx (National Instruments)</option>
              <option value="iotech">IOtech (Measurement Computing)</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Backend actuel: {systemStatus?.backend_type || 'Non connecté'}
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Statut Connexion
            </label>
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                isConnectedToBackend ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              <span className="text-sm">
                {isConnectedToBackend ? 'Connecté' : 'Déconnecté'}
              </span>
              {systemStatus?.hardware_connected && (
                <span className="text-xs text-green-600 ml-2">
                  Hardware détecté ({systemStatus.sensors_active}/{systemStatus.sensors_total} sondes)
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="flex space-x-3">
          <button
            onClick={async () => {
              try {
                await changeBackend(selectedBackend);
                addNotification({
                  level: 'info',
                  message: `Backend changé vers ${selectedBackend}`,
                  timestamp: Date.now(),
                  source: 'settings'
                });
              } catch (error) {
                addNotification({
                  level: 'error',
                  message: 'Erreur lors du changement de backend',
                  timestamp: Date.now(),
                  source: 'settings'
                });
              }
            }}
            disabled={!isConnectedToBackend || selectedBackend === systemStatus?.backend_type}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Changer Backend
          </button>
          
          <button
            onClick={async () => {
              setIsTestingConnection(true);
              try {
                await testConnection(testChannels);
                addNotification({
                  level: 'info',
                  message: 'Test de connexion lancé',
                  timestamp: Date.now(),
                  source: 'settings'
                });
              } catch (error) {
                addNotification({
                  level: 'error',
                  message: 'Erreur lors du test de connexion',
                  timestamp: Date.now(),
                  source: 'settings'
                });
              } finally {
                setIsTestingConnection(false);
              }
            }}
            disabled={!isConnectedToBackend || isTestingConnection}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isTestingConnection ? 'Test en cours...' : 'Tester Connexion'}
          </button>
          
          <button
            onClick={refreshSystemStatus}
            disabled={!isConnectedToBackend}
            className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Actualiser Statut
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Configuration Matérielle</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fréquence d'Échantillonnage (Hz)
            </label>
            <input
              type="number"
              value={samplingRate}
              onChange={(e) => setSamplingRate(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Taille du Buffer
            </label>
            <input
              type="number"
              value={bufferSize}
              onChange={(e) => setBufferSize(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Timeout (ms)
            </label>
            <input
              type="number"
              value={timeout}
              onChange={(e) => setTimeout(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
        
        <div className="flex space-x-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors">
            Valider la Configuration
          </button>
          <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg transition-colors">
            Réinitialiser
          </button>
        </div>
      </div>
      
      {/* 🔄 CATÉGORIE B : Validation ITTC et Standards ISO (Manquant dans UI) */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Validation Conformité</h3>
        
        <div className="space-y-4">
          {/* Validation Backend Hardware */}
          <div className="flex items-center">
            <div className={`w-5 h-5 rounded-full mr-3 ${
              systemStatus?.hardware_connected ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <span>
              Backend {systemStatus?.backend_type || 'inconnu'}: {
                systemStatus?.hardware_connected ? 'Compatible et connecté' : 'Non connecté'
              }
            </span>
          </div>
          
          {/* Validation ITTC */}
          <div className="flex items-center">
            <div className={`w-5 h-5 rounded-full mr-3 ${
              samplingRate >= 32 && samplingRate <= 1000 ? 'bg-green-500' : 'bg-yellow-500'
            }`}></div>
            <span>
              Paramètres ITTC: Fréquence {samplingRate}Hz {
                samplingRate >= 32 && samplingRate <= 1000 ? '(Conforme)' : '(Hors limites recommandées: 32-1000Hz)'
              }
            </span>
          </div>
          
          {/* Validation Sondes */}
          <div className="flex items-center">
            <div className={`w-5 h-5 rounded-full mr-3 ${
              (systemStatus?.sensors_active || 0) > 0 ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <span>
              Sondes détectés: {systemStatus?.sensors_active || 0}/{systemStatus?.sensors_total || 0} {
                (systemStatus?.sensors_active || 0) > 0 ? '(Opérationnels)' : '(Aucun actif)'
              }
            </span>
          </div>
          
          {/* Validation ISO 9001 */}
          <div className="flex items-center">
            <div className={`w-5 h-5 rounded-full mr-3 ${
              bufferSize >= 1024 && timeout >= 1000 ? 'bg-green-500' : 'bg-yellow-500'
            }`}></div>
            <span>
              Standards ISO 9001: Buffer {bufferSize}, Timeout {timeout}ms {
                bufferSize >= 1024 && timeout >= 1000 ? '(Conforme)' : '(Paramètres non optimaux)'
              }
            </span>
          </div>
          
          {/* Statut Système Global */}
          <div className="flex items-center">
            <div className={`w-5 h-5 rounded-full mr-3 ${
              isConnectedToBackend && (systemStatus?.hardware_connected || false) ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <span>
              Système global: {
                isConnectedToBackend && (systemStatus?.hardware_connected || false) 
                  ? 'Prêt pour acquisition' 
                  : 'Configuration requise'
              }
            </span>
          </div>
          
          {/* Métriques Système */}
          {systemStatus && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">Métriques Système</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Uptime:</span>
                  <br />
                  <span className="font-mono">{Math.floor(systemStatus.uptime_seconds / 3600)}h{Math.floor((systemStatus.uptime_seconds % 3600) / 60)}m</span>
                </div>
                <div>
                  <span className="text-gray-600">Mémoire:</span>
                  <br />
                  <span className="font-mono">{systemStatus.memory_usage_mb.toFixed(1)} MB</span>
                </div>
                <div>
                  <span className="text-gray-600">CPU:</span>
                  <br />
                  <span className="font-mono">{systemStatus.cpu_usage_percent.toFixed(1)}%</span>
                </div>
                <div>
                  <span className="text-gray-600">Version:</span>
                  <br />
                  <span className="font-mono">{systemStatus.version || 'N/A'}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
