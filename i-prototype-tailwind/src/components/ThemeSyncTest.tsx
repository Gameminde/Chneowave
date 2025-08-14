import React from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';

const ThemeSyncTest: React.FC = () => {
  const { theme, setTheme } = useUnifiedApp();



  return (
    <div className="fixed bottom-4 left-4 bg-green-100 border border-green-400 text-green-800 px-4 py-2 rounded-lg shadow-lg z-50">
      <div className="text-sm font-medium">Synchronisation Thème</div>
      <div className="text-xs">Thème actuel: {theme}</div>
      <div className="flex gap-2 mt-2">
        <button
          onClick={() => setTheme('light')}
          className={`px-2 py-1 text-xs rounded ${theme === 'light' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Clair
        </button>
        <button
          onClick={() => setTheme('dark')}
          className={`px-2 py-1 text-xs rounded ${theme === 'dark' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Sombre
        </button>
        <button
          onClick={() => setTheme('beige')}
          className={`px-2 py-1 text-xs rounded ${theme === 'beige' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Beige
        </button>
      </div>
    </div>
  );
};

export default ThemeSyncTest;
