import React, { useState } from 'react';
import { useUnifiedApp } from '../contexts/UnifiedAppContext';
import { 
  SunIcon, 
  MoonIcon, 
  ComputerDesktopIcon,
  ChevronDownIcon,
  CheckIcon
} from '@heroicons/react/24/outline';

const EnhancedThemeSelector: React.FC = () => {
  const { theme, setTheme } = useUnifiedApp();
  const [isOpen, setIsOpen] = useState(false);

  const themes = [
    {
      id: 'light',
      name: 'Clair',
      description: 'Interface claire et moderne',
      icon: SunIcon,
      preview: '#ffffff'
    },
    {
      id: 'dark',
      name: 'Sombre',
      description: 'Interface sombre professionnelle',
      icon: MoonIcon,
      preview: '#0f172a'
    },
    {
      id: 'beige',
      name: 'Solarized Light',
      description: 'Palette beige Solarized',
      icon: ComputerDesktopIcon,
      preview: '#fdf6e3'
    }
  ];

  const currentThemeData = themes.find(t => t.id === theme) || themes[0];

  const handleThemeChange = (themeId: string) => {
    setTheme(themeId);
    setIsOpen(false);
    
    // Dispatch event for the main.js system
    if (typeof window !== 'undefined' && window.CHNeoWave) {
      window.CHNeoWave.events.dispatchEvent(
        new CustomEvent('theme:change', { detail: { theme: themeId } })
      );
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 px-4 py-2 rounded-lg transition-all"
        style={{
          backgroundColor: 'var(--bg-elevated)',
          border: '1px solid var(--border-primary)',
          color: 'var(--text-primary)'
        }}
      >
        <div className="flex items-center space-x-2">
          <div 
            className="w-4 h-4 rounded-full border-2"
            style={{ 
              backgroundColor: currentThemeData.preview,
              borderColor: 'var(--border-secondary)'
            }}
          />
          <currentThemeData.icon className="w-4 h-4" />
          <span className="font-medium">{currentThemeData.name}</span>
        </div>
        <ChevronDownIcon 
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
        />
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown */}
          <div 
            className="absolute right-0 mt-2 w-80 rounded-xl shadow-lg z-20 animate-slide-up"
            style={{
              backgroundColor: 'var(--bg-elevated)',
              border: '1px solid var(--border-primary)'
            }}
          >
            <div className="p-4 border-b" style={{ borderColor: 'var(--border-primary)' }}>
              <h3 className="font-semibold text-lg" style={{ color: 'var(--text-primary)' }}>
                Sélection du Thème
              </h3>
              <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
                Choisissez l'apparence de l'interface
              </p>
            </div>
            
            <div className="p-2">
              {themes.map((themeOption) => {
                const IconComponent = themeOption.icon;
                const isSelected = theme === themeOption.id;
                
                return (
                  <button
                    key={themeOption.id}
                    onClick={() => handleThemeChange(themeOption.id)}
                    className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all text-left ${
                      isSelected ? 'ring-2' : ''
                    }`}
                    style={{
                      backgroundColor: isSelected ? 'var(--accent-primary)' + '10' : 'transparent',
                      ringColor: isSelected ? 'var(--accent-primary)' : 'transparent',
                      color: isSelected ? 'var(--accent-primary)' : 'var(--text-primary)'
                    }}
                  >
                    <div className="flex items-center space-x-3 flex-1">
                      <div 
                        className="w-8 h-8 rounded-lg border-2 flex items-center justify-center"
                        style={{ 
                          backgroundColor: themeOption.preview,
                          borderColor: 'var(--border-secondary)'
                        }}
                      >
                        <IconComponent className="w-4 h-4" style={{ 
                          color: themeOption.id === 'light' ? '#0f172a' : '#ffffff' 
                        }} />
                      </div>
                      
                      <div className="flex-1">
                        <div className="font-medium">{themeOption.name}</div>
                        <div className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                          {themeOption.description}
                        </div>
                      </div>
                    </div>
                    
                    {isSelected && (
                      <CheckIcon className="w-5 h-5" style={{ color: 'var(--accent-primary)' }} />
                    )}
                  </button>
                );
              })}
            </div>
            
            <div className="p-4 border-t" style={{ borderColor: 'var(--border-primary)' }}>
              <div className="flex items-center space-x-2 text-sm" style={{ color: 'var(--text-muted)' }}>
                <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: 'var(--status-success)' }} />
                <span>Thème appliqué automatiquement</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default EnhancedThemeSelector;
