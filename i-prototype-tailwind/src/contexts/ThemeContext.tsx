import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'beige';

interface ThemeContextType {
  currentTheme: Theme;
  setTheme: (theme: Theme) => void;
  isThemeLoading: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [currentTheme, setCurrentTheme] = useState<Theme>('light');
  const [isThemeLoading, setIsThemeLoading] = useState(true);

  // Fonction pour appliquer le thème au DOM
  const applyThemeToDOM = (theme: Theme) => {
    // Supprimer les anciens thèmes
    document.documentElement.removeAttribute('data-theme');
    document.body.classList.remove('theme-light', 'theme-dark', 'theme-beige');
    
    // Appliquer le nouveau thème
    document.documentElement.setAttribute('data-theme', theme);
    document.body.classList.add(`theme-${theme}`);

    // Support des variantes Tailwind "dark:" existantes
    document.documentElement.classList.toggle('dark', theme === 'dark');

    // Indiquer le schéma de couleur au navigateur (auto form controls, etc.)
    document.documentElement.style.setProperty('color-scheme', theme === 'dark' ? 'dark' : 'light');
    
    // Forcer la mise à jour des styles
    document.body.style.setProperty('--bg-primary', getComputedStyle(document.documentElement).getPropertyValue('--bg-primary'));
    document.body.style.setProperty('--text-primary', getComputedStyle(document.documentElement).getPropertyValue('--text-primary'));
    
    // Sauvegarder dans localStorage
    localStorage.setItem('chneowave-theme', theme);
  };

  // Fonction pour changer le thème
  const setTheme = (theme: Theme) => {
    setCurrentTheme(theme);
    applyThemeToDOM(theme);
    
    // Émettre un événement personnalisé pour synchroniser les autres composants
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
  };

  // Initialisation au montage du composant
  useEffect(() => {
    const initializeTheme = () => {
      try {
        // Récupérer le thème sauvegardé
        const savedTheme = localStorage.getItem('chneowave-theme') as Theme;
        const theme = savedTheme && ['light', 'dark', 'beige'].includes(savedTheme) ? savedTheme : 'light';
        
        setCurrentTheme(theme);
        applyThemeToDOM(theme);
      } catch (error) {
        console.error('Erreur lors de l\'initialisation du thème:', error);
        // Fallback vers le thème clair
        setCurrentTheme('light');
        applyThemeToDOM('light');
      } finally {
        setIsThemeLoading(false);
      }
    };

    initializeTheme();
  }, []);

  // Écouter les changements de thème depuis d'autres fenêtres
  useEffect(() => {
    const handleThemeChange = (event: CustomEvent) => {
      const { theme } = event.detail;
      if (theme !== currentTheme) {
        setCurrentTheme(theme);
        applyThemeToDOM(theme);
      }
    };

    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === 'chneowave-theme' && event.newValue) {
        const newTheme = event.newValue as Theme;
        if (newTheme !== currentTheme && ['light', 'dark', 'beige'].includes(newTheme)) {
          setCurrentTheme(newTheme);
          applyThemeToDOM(newTheme);
        }
      }
    };

    // Écouter les événements personnalisés
    window.addEventListener('themeChanged', handleThemeChange as EventListener);
    
    // Écouter les changements de localStorage (pour les onglets multiples)
    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('themeChanged', handleThemeChange as EventListener);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [currentTheme]);

  const value: ThemeContextType = {
    currentTheme,
    setTheme,
    isThemeLoading
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// Hook personnalisé pour utiliser le contexte
export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme doit être utilisé à l\'intérieur d\'un ThemeProvider');
  }
  return context;
};

export default ThemeContext;
