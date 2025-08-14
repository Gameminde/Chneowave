import React from 'react';
import { QuestionMarkCircleIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';
import EnhancedThemeSelector from './EnhancedThemeSelector';

const Header: React.FC = () => {
  return (
    <header className="shadow-sm py-4 px-6" style={{
      backgroundColor: 'var(--bg-elevated)',
      borderBottom: '1px solid var(--border-primary)'
    }}>
      <div className="flex items-center justify-between">
        {/* Brand Title */}
        <div className="flex items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>
              CHNeoWave
            </h1>
            <p className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
              Système d'Acquisition Maritime
            </p>
          </div>
        </div>
        
        {/* Status & Actions */}
        <div className="flex items-center gap-4">
          {/* Acquisition Status */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg" style={{
            backgroundColor: 'var(--status-success-bg)',
            color: 'var(--status-success)',
            border: '1px solid var(--border-primary)'
          }}>
            <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: 'var(--status-success)' }}></div>
            <span className="text-sm font-medium">Système Opérationnel</span>
          </div>
          
          {/* Theme Selector */}
          <EnhancedThemeSelector />
          
          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            <button className="p-2 rounded-lg transition-colors" style={{ color: 'var(--text-secondary)' }} title="Paramètres">
              <Cog6ToothIcon className="h-5 w-5" />
            </button>
            <button className="p-2 rounded-lg transition-colors" style={{ color: 'var(--text-secondary)' }} title="Aide">
              <QuestionMarkCircleIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
