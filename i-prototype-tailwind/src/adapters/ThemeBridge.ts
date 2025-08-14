/**
 * 🎨 Theme Bridge - CHNeoWave Integration
 * Pont de synchronisation Qt Backend ↔ React Frontend
 * 
 * Selon prompt ultra-précis : Unifier le système de thème global
 */

// ============ TYPES QT BACKEND ============
interface QtThemeData {
  name: string;
  mode: 'light' | 'dark' | 'auto';
  colors: {
    background: string;
    foreground: string;
    primary: string;
    secondary: string;
    accent: string;
    surface: string;
    border: string;
    error: string;
    warning: string;
    success: string;
    info: string;
  };
  fonts: {
    family: string;
    size: number;
    weight: number;
  };
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
  };
}

// ============ TYPES CSS VARIABLES ============
interface CSSThemeVariables {
  // Backgrounds
  '--bg-primary': string;
  '--bg-secondary': string;
  '--bg-tertiary': string;
  '--bg-elevated': string;
  '--bg-surface': string;
  '--bg-overlay': string;

  // Text Colors
  '--text-primary': string;
  '--text-secondary': string;
  '--text-tertiary': string;
  '--text-muted': string;
  '--text-inverse': string;

  // Border Colors
  '--border-primary': string;
  '--border-secondary': string;
  '--border-accent': string;

  // Accent Colors
  '--accent-primary': string;
  '--accent-primary-hover': string;
  '--accent-secondary': string;
  '--accent-secondary-hover': string;

  // Status Colors
  '--status-success': string;
  '--status-success-bg': string;
  '--status-warning': string;
  '--status-warning-bg': string;
  '--status-error': string;
  '--status-error-bg': string;
  '--status-info': string;
  '--status-info-bg': string;

  // Shadow Colors
  '--shadow-color': string;
  '--shadow-strong': string;

  // Typography
  '--font-family-primary': string;
  '--font-size-base': string;

  // Spacing (Golden Ratio)
  '--space-xs': string;
  '--space-sm': string;
  '--space-md': string;
  '--space-lg': string;
  '--space-xl': string;
  '--space-xxl': string;

  // Border Radius
  '--border-radius-sm': string;
  '--border-radius-md': string;
  '--border-radius-lg': string;

  // Shadows
  '--shadow-default': string;
  '--shadow-md': string;
  '--shadow-lg': string;
}

// ============ ÉVÉNEMENTS DE SYNCHRONISATION ============
interface ThemeSyncEvent {
  source: 'qt' | 'web';
  theme: string;
  timestamp: number;
  data?: QtThemeData;
}

// ============ BRIDGE PRINCIPAL ============
export class ThemeBridge {
  private static instance: ThemeBridge | null = null;
  private eventListeners: Set<(event: ThemeSyncEvent) => void> = new Set();
  private currentTheme: string = 'light';
  private qtBridgeAvailable: boolean = false;

  constructor() {
    this.initializeBridge();
  }

  public static getInstance(): ThemeBridge {
    if (!ThemeBridge.instance) {
      ThemeBridge.instance = new ThemeBridge();
    }
    return ThemeBridge.instance;
  }

  // ============ INITIALISATION ============
  private initializeBridge(): void {
    // Vérifier si le bridge Qt est disponible
    this.qtBridgeAvailable = typeof window !== 'undefined' && !!window.qtBridge;

    if (this.qtBridgeAvailable) {
      console.log('✅ Qt Theme Bridge available');
      this.setupQtListeners();
    } else {
      console.log('⚠️ Qt Theme Bridge not available, using localStorage fallback');
      this.setupFallbackSync();
    }

    // Écouter les changements de thème web
    this.setupWebListeners();
  }

  private setupQtListeners(): void {
    if (window.qtBridge && window.qtBridge.onThemeChanged) {
      window.qtBridge.onThemeChanged((qtTheme: string) => {
        console.log('🎨 Theme changed from Qt:', qtTheme);
        this.handleQtThemeChange(qtTheme);
      });
    }
  }

  private setupFallbackSync(): void {
    // Synchronisation via localStorage pour les cas où Qt n'est pas disponible
    const checkForQtThemeUpdates = () => {
      const qtTheme = localStorage.getItem('qt_theme_sync');
      if (qtTheme && qtTheme !== this.currentTheme) {
        this.handleQtThemeChange(qtTheme);
      }
    };

    setInterval(checkForQtThemeUpdates, 1000); // Vérifier toutes les secondes
  }

  private setupWebListeners(): void {
    // Écouter les événements de changement de thème web
    window.addEventListener('themeChanged', (event: CustomEvent) => {
      const { theme, source } = event.detail;
      if (source !== 'qt') {
        this.syncToQt(theme);
      }
    });

    // Écouter les changements de localStorage (onglets multiples)
    window.addEventListener('storage', (event: StorageEvent) => {
      if (event.key === 'chneowave-theme' && event.newValue) {
        this.syncToQt(event.newValue);
      }
    });
  }

  // ============ SYNCHRONISATION QT → WEB ============
  private handleQtThemeChange(qtTheme: string): void {
    this.currentTheme = qtTheme;

    // Appliquer le thème au web
    this.applyThemeToWeb(qtTheme);

    // Notifier les listeners
    const event: ThemeSyncEvent = {
      source: 'qt',
      theme: qtTheme,
      timestamp: Date.now()
    };

    this.eventListeners.forEach(listener => listener(event));

    // Déclencher l'événement web pour synchroniser React
    window.dispatchEvent(new CustomEvent('themeChanged', {
      detail: { theme: qtTheme, source: 'qt' }
    }));
  }

  // ============ SYNCHRONISATION WEB → QT ============
  public syncToQt(webTheme: string): void {
    if (webTheme === this.currentTheme) return;

    this.currentTheme = webTheme;

    if (this.qtBridgeAvailable && window.qtBridge) {
      console.log('🎨 Syncing theme to Qt:', webTheme);
      try {
        window.qtBridge.setTheme(webTheme);
      } catch (error) {
        console.error('❌ Error syncing theme to Qt:', error);
        this.fallbackQtSync(webTheme);
      }
    } else {
      this.fallbackQtSync(webTheme);
    }
  }

  private fallbackQtSync(webTheme: string): void {
    // Fallback: utiliser localStorage pour synchronisation différée
    localStorage.setItem('qt_theme_sync', webTheme);
    localStorage.setItem('qt_theme_sync_timestamp', Date.now().toString());
  }

  // ============ APPLICATION DES THÈMES ============
  public applyThemeToWeb(themeName: string): void {
    const themeData = this.getThemeData(themeName);
    const cssVariables = this.qtThemeToCssVariables(themeData);

    // Appliquer les variables CSS
    const root = document.documentElement;
    Object.entries(cssVariables).forEach(([property, value]) => {
      root.style.setProperty(property, value);
    });

    // Appliquer les classes et attributs
    root.setAttribute('data-theme', themeName);
    root.classList.toggle('dark', themeName === 'dark');

    // Indiquer le schéma de couleur au navigateur
    root.style.setProperty('color-scheme', themeName === 'dark' ? 'dark' : 'light');

    console.log(`🎨 Applied theme to web: ${themeName}`);
  }

  private getThemeData(themeName: string): QtThemeData {
    // Si le bridge Qt est disponible, récupérer les données du backend
    if (this.qtBridgeAvailable && window.qtBridge && window.qtBridge.getThemeData) {
      try {
        return window.qtBridge.getThemeData(themeName);
      } catch (error) {
        console.error('❌ Error getting theme data from Qt:', error);
      }
    }

    // Fallback: utiliser les thèmes prédéfinis
    return this.getPredefinedThemeData(themeName);
  }

  private getPredefinedThemeData(themeName: string): QtThemeData {
    const themes: Record<string, QtThemeData> = {
      light: {
        name: 'light',
        mode: 'light',
        colors: {
          background: '#ffffff',
          foreground: '#1e293b',
          primary: '#3b82f6',
          secondary: '#06b6d4',
          accent: '#3b82f6',
          surface: '#f8fafc',
          border: '#e2e8f0',
          error: '#ef4444',
          warning: '#f59e0b',
          success: '#10b981',
          info: '#3b82f6'
        },
        fonts: {
          family: 'Inter, sans-serif',
          size: 14,
          weight: 400
        },
        spacing: {
          xs: 8,
          sm: 13,
          md: 21,
          lg: 34,
          xl: 55
        },
        borderRadius: {
          sm: 4,
          md: 8,
          lg: 12
        },
        shadows: {
          sm: '0 1px 3px rgba(0,0,0,0.1)',
          md: '0 4px 6px rgba(0,0,0,0.1)',
          lg: '0 10px 15px rgba(0,0,0,0.1)'
        }
      },
      dark: {
        name: 'dark',
        mode: 'dark',
        colors: {
          background: '#1a1a1a',
          foreground: '#e4e4e7',
          primary: '#3b82f6',
          secondary: '#06b6d4',
          accent: '#60a5f6',
          surface: '#2d2d2d',
          border: '#3a3a3a',
          error: '#ef4444',
          warning: '#f59e0b',
          success: '#22c55e',
          info: '#3b82f6'
        },
        fonts: {
          family: 'Inter, sans-serif',
          size: 14,
          weight: 400
        },
        spacing: {
          xs: 8,
          sm: 13,
          md: 21,
          lg: 34,
          xl: 55
        },
        borderRadius: {
          sm: 4,
          md: 8,
          lg: 12
        },
        shadows: {
          sm: '0 1px 3px rgba(0,0,0,0.35)',
          md: '0 4px 6px rgba(0,0,0,0.35)',
          lg: '0 10px 15px rgba(0,0,0,0.35)'
        }
      },
      beige: {
        name: 'beige',
        mode: 'light',
        colors: {
          background: '#fdf6e3',
          foreground: '#657b83',
          primary: '#268bd2',
          secondary: '#2aa198',
          accent: '#268bd2',
          surface: '#eee8d5',
          border: '#93a1a1',
          error: '#dc322f',
          warning: '#b58900',
          success: '#859900',
          info: '#268bd2'
        },
        fonts: {
          family: 'Inter, sans-serif',
          size: 14,
          weight: 400
        },
        spacing: {
          xs: 8,
          sm: 13,
          md: 21,
          lg: 34,
          xl: 55
        },
        borderRadius: {
          sm: 4,
          md: 8,
          lg: 12
        },
        shadows: {
          sm: '0 1px 3px rgba(101,123,131,0.1)',
          md: '0 4px 6px rgba(101,123,131,0.1)',
          lg: '0 10px 15px rgba(101,123,131,0.1)'
        }
      }
    };

    return themes[themeName] || themes.light;
  }

  private qtThemeToCssVariables(qtTheme: QtThemeData): CSSThemeVariables {
    return {
      // Backgrounds
      '--bg-primary': qtTheme.colors.background,
      '--bg-secondary': qtTheme.colors.surface,
      '--bg-tertiary': this.lightenColor(qtTheme.colors.surface, qtTheme.mode === 'dark' ? 10 : -10),
      '--bg-elevated': qtTheme.colors.surface,
      '--bg-surface': qtTheme.colors.surface,
      '--bg-overlay': this.addAlpha(qtTheme.colors.background, 0.95),

      // Text Colors
      '--text-primary': qtTheme.colors.foreground,
      '--text-secondary': this.lightenColor(qtTheme.colors.foreground, qtTheme.mode === 'dark' ? -20 : 20),
      '--text-tertiary': this.lightenColor(qtTheme.colors.foreground, qtTheme.mode === 'dark' ? -40 : 40),
      '--text-muted': this.lightenColor(qtTheme.colors.foreground, qtTheme.mode === 'dark' ? -60 : 60),
      '--text-inverse': qtTheme.colors.background,

      // Border Colors
      '--border-primary': qtTheme.colors.border,
      '--border-secondary': this.lightenColor(qtTheme.colors.border, qtTheme.mode === 'dark' ? 20 : -20),
      '--border-accent': qtTheme.colors.accent,

      // Accent Colors
      '--accent-primary': qtTheme.colors.primary,
      '--accent-primary-hover': this.lightenColor(qtTheme.colors.primary, -10),
      '--accent-secondary': qtTheme.colors.secondary,
      '--accent-secondary-hover': this.lightenColor(qtTheme.colors.secondary, -10),

      // Status Colors
      '--status-success': qtTheme.colors.success,
      '--status-success-bg': this.addAlpha(qtTheme.colors.success, 0.12),
      '--status-warning': qtTheme.colors.warning,
      '--status-warning-bg': this.addAlpha(qtTheme.colors.warning, 0.12),
      '--status-error': qtTheme.colors.error,
      '--status-error-bg': this.addAlpha(qtTheme.colors.error, 0.12),
      '--status-info': qtTheme.colors.info,
      '--status-info-bg': this.addAlpha(qtTheme.colors.info, 0.12),

      // Shadow Colors
      '--shadow-color': qtTheme.mode === 'dark' ? 'rgba(0, 0, 0, 0.35)' : 'rgba(0, 0, 0, 0.1)',
      '--shadow-strong': qtTheme.mode === 'dark' ? 'rgba(0, 0, 0, 0.6)' : 'rgba(0, 0, 0, 0.15)',

      // Typography
      '--font-family-primary': qtTheme.fonts.family,
      '--font-size-base': `${qtTheme.fonts.size}px`,

      // Spacing (Golden Ratio)
      '--space-xs': `${qtTheme.spacing.xs}px`,
      '--space-sm': `${qtTheme.spacing.sm}px`,
      '--space-md': `${qtTheme.spacing.md}px`,
      '--space-lg': `${qtTheme.spacing.lg}px`,
      '--space-xl': `${qtTheme.spacing.xl}px`,
      '--space-xxl': `${qtTheme.spacing.xl * 1.618}px`,

      // Border Radius
      '--border-radius-sm': `${qtTheme.borderRadius.sm}px`,
      '--border-radius-md': `${qtTheme.borderRadius.md}px`,
      '--border-radius-lg': `${qtTheme.borderRadius.lg}px`,

      // Shadows
      '--shadow-default': qtTheme.shadows.sm,
      '--shadow-md': qtTheme.shadows.md,
      '--shadow-lg': qtTheme.shadows.lg
    };
  }

  // ============ UTILITAIRES COULEUR ============
  private lightenColor(color: string, percent: number): string {
    // Implémentation simplifiée - dans un vrai projet, utiliser une librairie comme chroma.js
    const num = parseInt(color.replace("#", ""), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
      (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
      (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1);
  }

  private addAlpha(color: string, alpha: number): string {
    const num = parseInt(color.replace("#", ""), 16);
    const R = num >> 16;
    const G = num >> 8 & 0x00FF;
    const B = num & 0x0000FF;
    return `rgba(${R}, ${G}, ${B}, ${alpha})`;
  }

  // ============ API PUBLIQUE ============
  public getCurrentTheme(): string {
    return this.currentTheme;
  }

  public isQtBridgeAvailable(): boolean {
    return this.qtBridgeAvailable;
  }

  public addEventListener(listener: (event: ThemeSyncEvent) => void): void {
    this.eventListeners.add(listener);
  }

  public removeEventListener(listener: (event: ThemeSyncEvent) => void): void {
    this.eventListeners.delete(listener);
  }

  public getThemeVariables(themeName: string): CSSThemeVariables {
    const themeData = this.getThemeData(themeName);
    return this.qtThemeToCssVariables(themeData);
  }

  public webToQtTheme(cssTheme: string): QtThemeData {
    return this.getPredefinedThemeData(cssTheme);
  }
}

// ============ EXTENSION WINDOW POUR QT BRIDGE ============
declare global {
  interface Window {
    qtBridge?: {
      setTheme(theme: string): void;
      getTheme(): string;
      getThemeData(theme: string): QtThemeData;
      onThemeChanged(callback: (theme: string) => void): void;
    };
  }
}

// ============ INSTANCE SINGLETON ============
export const themeBridge = ThemeBridge.getInstance();

// ============ EXPORTS ============
export type {
  QtThemeData,
  CSSThemeVariables,
  ThemeSyncEvent
};
