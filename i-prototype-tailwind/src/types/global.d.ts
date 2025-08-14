// Déclarations TypeScript globales pour CHNeoWave

declare global {
  interface Window {
    CHNeoWave: {
      version: string;
      initialized: boolean;
      theme: string;
      config: {
        apiUrl: string;
        wsUrl: string;
        debug: boolean;
      };
      events: EventTarget;
      init(): Promise<void>;
      initThemeSystem(): Promise<void>;
      applyTheme(themeName: string): void;
      initServices(): Promise<void>;
      dataService: {
        generateWaveData(): {
          timestamp: number;
          height: number;
          period: number;
          frequency: number;
        };
        generateSensorData(sondeId: number): {
          id: number;
          status: string;
          snr: number;
          saturation: boolean;
          gaps: number;
          lastUpdate: number;
        };
      };
      statsService: {
        calculateStats(data: any[]): {
          hMax: number;
          hMin: number;
          h13: number;
          hSignificant: number;
          period: number;
          count: number;
        };
      };
      utils: {
        formatTime(seconds: number): string;
        formatNumber(num: number, decimals?: number): string;
        debounce(func: Function, wait: number): Function;
      };
    };
  }

  // Déclarations pour les variables d'environnement Vite
  interface ImportMetaEnv {
    readonly VITE_APP_NAME?: string;
    readonly VITE_APP_VERSION?: string;
    readonly VITE_API_URL?: string;
    readonly VITE_WS_URL?: string;
    readonly VITE_DEBUG_MODE?: string;
    readonly VITE_ENABLE_LOGGING?: string;
    readonly VITE_DEFAULT_THEME?: string;
    readonly VITE_AVAILABLE_THEMES?: string;
    readonly VITE_ENABLE_ANIMATIONS?: string;
    readonly VITE_ENABLE_SOUND?: string;
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
}

export {};
