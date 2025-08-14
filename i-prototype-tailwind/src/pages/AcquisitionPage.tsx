import React, { useState } from 'react';

const AcquisitionPage: React.FC = () => {
  const [frequency, setFrequency] = useState(100);
  const [duration, setDuration] = useState(60);
  const [selectedProbes, setSelectedProbes] = useState<number[]>([1, 2, 3, 4]);
  const [isAcquiring, setIsAcquiring] = useState(false);

  const toggleProbe = (probeId: number) => {
    setSelectedProbes(prev => 
      prev.includes(probeId) 
        ? prev.filter(id => id !== probeId)
        : [...prev, probeId]
    );
  };

  const startAcquisition = () => {
    setIsAcquiring(true);
    // Simulate acquisition process
    setTimeout(() => setIsAcquiring(false), duration * 1000);
  };

  return (
    <div className="p-6">
      <h1 className="font-semibold mb-6" style={{color: 'var(--text-primary)', fontSize: 'var(--text-3xl)'}}>Acquisition de Données</h1>
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="block font-medium mb-2" style={{color: 'var(--text-secondary)', fontSize: 'var(--text-sm)'}}>
              Fréquence d'échantillonnage (Hz)
            </label>
            <input
              type="number"
              value={frequency}
              onChange={(e) => setFrequency(parseInt(e.target.value))}
              className="w-full px-3 py-2"
              style={{backgroundColor: 'var(--secondary-bg)', border: '1px solid var(--border-color)', color: 'var(--text-primary)'}}
              min="1"
              max="1000"
            />
          </div>
          <div>
            <label className="block font-medium mb-2" style={{color: 'var(--text-secondary)', fontSize: 'var(--text-sm)'}}>
              Durée d'acquisition (secondes)
            </label>
            <input
              type="number"
              value={duration}
              onChange={(e) => setDuration(parseInt(e.target.value))}
              className="w-full px-3 py-2"
              style={{backgroundColor: 'var(--secondary-bg)', border: '1px solid var(--border-color)', color: 'var(--text-primary)'}}
              min="1"
              max="3600"
            />
          </div>
          <div className="flex items-end">
            <div className="flex space-x-3">
              <button
                onClick={startAcquisition}
                disabled={isAcquiring || selectedProbes.length === 0}
                className="flex-1 py-3 px-4 font-medium transition-colors"
                style={{
                  backgroundColor: isAcquiring || selectedProbes.length === 0 ? 'var(--border-color)' : 'var(--success-green)',
                  color: isAcquiring || selectedProbes.length === 0 ? 'var(--text-muted)' : 'white',
                  cursor: isAcquiring || selectedProbes.length === 0 ? 'not-allowed' : 'pointer'
                }}
              >
                {isAcquiring ? 'Acquisition en cours...' : 'Démarrer l\'Acquisition'}
              </button>
              <button className="px-4 py-3 font-medium transition-colors" style={{backgroundColor: 'var(--error-red)', color: 'white'}}>
                Arrêter
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-4">Sélection des Sondes</h3>
        <div className="grid grid-cols-4 gap-3">
          {[...Array(16)].map((_, i) => {
            const probeId = i + 1;
            const isSelected = selectedProbes.includes(probeId);
            return (
              <button
                key={probeId}
                onClick={() => toggleProbe(probeId)}
                className="p-3 transition-colors"
                style={{
                  backgroundColor: isSelected ? 'var(--accent-blue)' : 'var(--secondary-bg)',
                  color: isSelected ? 'white' : 'var(--text-primary)',
                  border: '1px solid var(--border-color)'
                }}
              >
                Sonde {probeId}
              </button>
            );
          })}
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
          <h2 className="font-semibold mb-4" style={{color: 'var(--text-primary)', fontSize: 'var(--text-xl)'}}>Configuration</h2>
          <div className="mb-1" style={{color: 'var(--text-secondary)', fontSize: 'var(--text-sm)'}}>Sondes sélectionnées</div>
          <div className="font-bold" style={{color: 'var(--text-primary)', fontSize: 'var(--text-lg)'}}>
            {selectedProbes.length} / 16 sondes
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Statistiques Temps Réel</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Hs</p>
              <p className="text-xl font-bold">2.42 m</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Hmax</p>
              <p className="text-xl font-bold">3.75 m</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Hmin</p>
              <p className="text-xl font-bold">0.12 m</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Tm</p>
              <p className="text-xl font-bold">7.8 s</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Tp</p>
              <p className="text-xl font-bold">8.1 s</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AcquisitionPage;
