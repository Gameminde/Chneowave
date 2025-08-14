import React from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';

interface ThemeSelectorProps {
  className?: string;
}

const ThemeSelector: React.FC<ThemeSelectorProps> = ({ className = '' }) => {
  const { theme, setTheme } = useUnifiedApp();

  const themes = [
    { 
      id: 'light' as const, 
      name: 'Clair', 
      icon: '☀️',
      gradient: 'from-white to-gray-100',
      textColor: 'text-gray-800'
    },
    { 
      id: 'dark' as const, 
      name: 'Sombre', 
      icon: '🌙',
      gradient: 'from-gray-900 to-gray-700',
      textColor: 'text-white'
    },
    { 
      id: 'beige' as const, 
      name: 'Beige', 
      icon: '🏛️',
      gradient: 'from-amber-50 to-yellow-100',
      textColor: 'text-amber-900'
    }
  ];

  const handleThemeChange = (theme: 'light' | 'dark' | 'beige') => {
    setTheme(theme);
  };

  return (
    <div className={`theme-selector ${className}`}>
      {themes.map((themeOption) => (
        <button
          key={themeOption.id}
          onClick={() => handleThemeChange(themeOption.id)}
          className={`theme-option theme-${themeOption.id} ${theme === themeOption.id ? 'active' : ''}`}
          title={`Thème ${themeOption.name}`}
          aria-label={`Basculer vers le thème ${themeOption.name}`}
        >
          <span className="text-xs">{themeOption.icon}</span>
        </button>
      ))}
    </div>
  );
};

export default ThemeSelector;