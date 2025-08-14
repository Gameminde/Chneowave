import React, { useState } from 'react';

const CalibrationPage: React.FC = () => {
  const [activeProbe, setActiveProbe] = useState(1);
  const [calibrationPoints, setCalibrationPoints] = useState([
    { voltage: 0, height: 0 },
    { voltage: 1, height: 10 },
    { voltage: 2, height: 20 },
  ]);

  const addCalibrationPoint = () => {
    setCalibrationPoints([...calibrationPoints, { voltage: 0, height: 0 }]);
  };

  const updateCalibrationPoint = (index: number, field: 'voltage' | 'height', value: number) => {
    const updated = [...calibrationPoints];
    updated[index][field] = value;
    setCalibrationPoints(updated);
  };

  return (
    <div className="p-6">
      <h1 className="font-semibold mb-6" style={{color: 'var(--text-primary)', fontSize: 'var(--text-3xl)'}}>Calibration des Sondes</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Probe Selection */}
        <div className="p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
          <h2 className="font-semibold mb-4" style={{color: 'var(--text-primary)', fontSize: 'var(--text-xl)'}}>Sélection de la Sonde</h2>
          <div className="grid grid-cols-4 gap-2 mb-4">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((probe) => (
              <button
                key={probe}
                onClick={() => setActiveProbe(probe)}
                className="p-3 transition-colors"
                style={{
                  backgroundColor: activeProbe === probe ? 'var(--accent-blue)' : 'var(--secondary-bg)',
                  color: activeProbe === probe ? 'white' : 'var(--text-primary)',
                  border: '1px solid var(--border-color)'
                }}
              >
                Sonde {probe}
              </button>
            ))}
          </div>
        </div>
        
        {/* Calibration Points */}
        <div className="p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
          <h2 className="font-semibold mb-4" style={{color: 'var(--text-primary)', fontSize: 'var(--text-xl)'}}>Points de Calibration</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Point
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tension (V)
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Hauteur (m)
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {calibrationPoints.map((row, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {index + 1}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="number"
                        step="0.01"
                        value={row.voltage}
                        onChange={(e) => updateCalibrationPoint(index, 'voltage', parseFloat(e.target.value))}
                        className="w-24 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="number"
                        step="0.01"
                        value={row.height}
                        onChange={(e) => updateCalibrationPoint(index, 'height', parseFloat(e.target.value))}
                        className="w-24 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-6 flex justify-between">
            <button
              onClick={addCalibrationPoint}
              className="px-4 py-2 font-medium transition-colors"
              style={{backgroundColor: 'var(--success-green)', color: 'white'}}
            >
              Ajouter Point
            </button>
            <button className="px-4 py-2 font-medium transition-colors" style={{backgroundColor: 'var(--accent-blue)', color: 'white'}}>
              Calibrer
            </button>
          </div>
        </div>
      </div>
      
      {/* Calibration Graph Placeholder */}
      <div className="mt-8 p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
        <h4 className="font-medium mb-3" style={{color: 'var(--text-primary)', fontSize: 'var(--text-lg)'}}>Courbe de Calibration</h4>
        <div className="h-64 flex items-center justify-center" style={{backgroundColor: 'var(--secondary-bg)', border: '2px dashed var(--border-light)'}}>
          <div className="text-center">
            <p style={{color: 'var(--text-secondary)'}}>Graphique de linéarité tension/hauteur</p>
            <p className="mt-2" style={{color: 'var(--text-muted)', fontSize: 'var(--text-sm)'}}>R² = 0.998 | Pente = 0.245 | Offset = 0.02</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CalibrationPage;
