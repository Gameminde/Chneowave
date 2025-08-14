/**
 * 🔄 Unified App Context - CHNeoWave Integration
 * Context unifié selon prompt ultra-précis : Une seule source de vérité
 * 
 * Intègre : ThemeProvider + RealtimeBridge + DataAdapter + State Management
 */

import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { RealtimeBridge, AcquisitionData, CalibrationUpdate, SystemStatus, SondeStatus, ErrorNotification } from '../adapters/RealtimeBridge';
import { DataFormatAdapter, UISessionData, UISensorData, UIAcquisitionConfig } from '../adapters/DataFormatAdapter';
import { themeBridge, ThemeSyncEvent } from '../adapters/ThemeBridge';

// ============ TYPES UNIFIÉS ============
type Theme = 'light' | 'dark' | 'beige';

interface AppState {
  // Session et Projet
  currentSession: UISessionData | null;
  sessions: UISessionData[];
  
  // Acquisition
  acquisitionData: AcquisitionData | null;
  isAcquiring: boolean;
  acquisitionConfig: UIAcquisitionConfig | null;
  
  // Calibration
  calibrationUpdates: Map<string, CalibrationUpdate>;
  isCalibrating: boolean;
  currentCalibratingSensor: string | null;
  
  // Sondes
  sondes: UISensorData[];
  sensorStatuses: Map<string, SondeStatus>;
  
  // Système
  systemStatus: SystemStatus | null;
  isConnectedToBackend: boolean;
  
  // Erreurs et Notifications
  errors: ErrorNotification[];
  notifications: ErrorNotification[];
  
  // UI State
  currentTheme: Theme;
  isThemeLoading: boolean;
  sidebarCollapsed: boolean;
  currentPage: string;
}

interface AppActions {
  // Thème
  setTheme: (theme: Theme) => void;
  
  // Session
  setCurrentSession: (session: UISessionData | null) => void;
  createSession: (sessionData: Partial<UISessionData>) => Promise<UISessionData>;
  updateSession: (sessionId: string, updates: Partial<UISessionData>) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  loadSessions: () => Promise<void>;
  
  // Acquisition
  startAcquisition: (config: UIAcquisitionConfig) => Promise<void>;
  stopAcquisition: () => Promise<void>;
  pauseAcquisition: () => Promise<void>;
  resumeAcquisition: () => Promise<void>;
  updateAcquisitionConfig: (config: UIAcquisitionConfig) => void;
  
  // Calibration
  startCalibration: (sondeId: string) => Promise<void>;
  addCalibrationPoint: (sondeId: string, reference: number, measured: number) => Promise<void>;
  calculateCalibration: (sondeId: string) => Promise<void>;
  stopCalibration: (sondeId: string) => Promise<void>;
  
  // Sondes
  updateSensors: (sondes: UISensorData[]) => void;
  toggleSensor: (sondeId: string, active: boolean) => void;
  
  // Système
  refreshSystemStatus: () => Promise<void>;
  changeBackend: (backendType: 'ni-daqmx' | 'iotech' | 'demo') => Promise<void>;
  testConnection: (channels?: number[]) => Promise<void>;
  
  // Erreurs et Notifications
  addError: (error: ErrorNotification) => void;
  addNotification: (notification: ErrorNotification) => void;
  clearErrors: () => void;
  clearNotifications: () => void;
  dismissError: (index: number) => void;
  dismissNotification: (index: number) => void;
  
  // UI
  setSidebarCollapsed: (collapsed: boolean) => void;
  setCurrentPage: (page: string) => void;
}

type UnifiedAppContextType = AppState & AppActions;

const UnifiedAppContext = createContext<UnifiedAppContextType | undefined>(undefined);

// ============ PROVIDER UNIFIÉ ============
interface UnifiedAppProviderProps {
  children: ReactNode;
}

export const UnifiedAppProvider: React.FC<UnifiedAppProviderProps> = ({ children }) => {
  // ============ STATE PRINCIPAL ============
  const [state, setState] = useState<AppState>({
    // Session et Projet
    currentSession: null,
    sessions: [],
    
    // Acquisition
    acquisitionData: null,
    isAcquiring: false,
    acquisitionConfig: null,
    
    // Calibration
    calibrationUpdates: new Map(),
    isCalibrating: false,
    currentCalibratingSensor: null,
    
    // Sondes
    sondes: [],
    sensorStatuses: new Map(),
    
    // Système
    systemStatus: null,
    isConnectedToBackend: false,
    
    // Erreurs et Notifications
    errors: [],
    notifications: [],
    
    // UI State
    currentTheme: 'light',
    isThemeLoading: true,
    sidebarCollapsed: false,
    currentPage: 'dashboard'
  });

  // ============ REALTIME BRIDGE ============
  const [realtimeBridge] = useState(() => new RealtimeBridge());

  // ============ INITIALISATION ============
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Initialiser le thème
        const savedTheme = localStorage.getItem('chneowave-theme') as Theme;
        const theme = savedTheme && ['light', 'dark', 'beige'].includes(savedTheme) ? savedTheme : 'light';
        
        setState(prev => ({ 
          ...prev, 
          currentTheme: theme,
          isThemeLoading: false 
        }));
        
        // Appliquer le thème
        themeBridge.applyThemeToWeb(theme);
        
        // Charger les sessions
        await loadSessions();
        
        // Initialiser les sondes par défaut
        initializeDefaultSensors();
        
      } catch (error) {
        console.error('❌ Error initializing app:', error);
        addError({
          level: 'error',
          message: 'Erreur lors de l\'initialisation de l\'application',
          timestamp: Date.now(),
          source: 'app_init',
          details: { error: error instanceof Error ? error.message : String(error) }
        });
      }
    };

    initializeApp();
  }, []);

  // ============ LISTENERS REALTIME ============
  useEffect(() => {
    // Connexion backend
    realtimeBridge.on('connected', () => {
      setState(prev => ({ ...prev, isConnectedToBackend: true }));
      addNotification({
        level: 'info',
        message: 'Connecté au backend CHNeoWave',
        timestamp: Date.now(),
        source: 'backend'
      });
    });

    realtimeBridge.on('disconnected', () => {
      setState(prev => ({ ...prev, isConnectedToBackend: false }));
      addNotification({
        level: 'warning',
        message: 'Déconnecté du backend CHNeoWave',
        timestamp: Date.now(),
        source: 'backend'
      });
    });

    // Données d'acquisition
    realtimeBridge.on('acquisitionData', (data: AcquisitionData) => {
      setState(prev => ({ 
        ...prev, 
        acquisitionData: data,
        isAcquiring: data.status === 'running'
      }));
    });

    // Mises à jour calibration
    realtimeBridge.on('calibrationUpdate', (update: CalibrationUpdate) => {
      setState(prev => {
        const newUpdates = new Map(prev.calibrationUpdates);
        newUpdates.set(update.sonde_id, update);
        
        return {
          ...prev,
          calibrationUpdates: newUpdates,
          isCalibrating: update.status === 'in_progress',
          currentCalibratingSensor: update.status === 'in_progress' ? update.sonde_id : null
        };
      });
    });

    // Statut système
    realtimeBridge.on('systemStatus', (status: SystemStatus) => {
      setState(prev => ({ ...prev, systemStatus: status }));
    });

    // Statut sondes
    realtimeBridge.on('sensorStatus', (status: SondeStatus) => {
      setState(prev => {
        const newStatuses = new Map(prev.sensorStatuses);
        newStatuses.set(status.sonde_id, status);
        
        // Mettre à jour les sondes avec les nouvelles données
        const updatedSensors = prev.sondes.map(sonde => {
          if (sonde.id === status.sonde_id) {
            return {
              ...sonde,
              isActive: status.status === 'active',
              lastValue: status.last_value,
              snr: status.snr_db,
              saturation: status.saturation_percent / 100
            };
          }
          return sonde;
        });
        
        return {
          ...prev,
          sensorStatuses: newStatuses,
          sondes: updatedSensors
        };
      });
    });

    // Erreurs
    realtimeBridge.on('error', (error: ErrorNotification) => {
      addError(error);
    });

    // Nettoyage
    return () => {
      realtimeBridge.removeAllListeners();
    };
  }, [realtimeBridge]);

  // ============ LISTENERS THÈME ============
  useEffect(() => {
    const handleThemeSync = (event: ThemeSyncEvent) => {
      if (event.source === 'qt') {
        setState(prev => ({ ...prev, currentTheme: event.theme as Theme }));
      }
    };

    themeBridge.addEventListener(handleThemeSync);

    return () => {
      themeBridge.removeEventListener(handleThemeSync);
    };
  }, []);

  // ============ ACTIONS - THÈME ============
  const setTheme = useCallback((theme: Theme) => {
    setState(prev => ({ ...prev, currentTheme: theme }));
    themeBridge.applyThemeToWeb(theme);
    themeBridge.syncToQt(theme);
    localStorage.setItem('chneowave-theme', theme);
    
    // Émettre événement pour compatibilité
    window.dispatchEvent(new CustomEvent('themeChanged', { 
      detail: { theme, source: 'web' } 
    }));
  }, []);

  // ============ ACTIONS - SESSION ============
  const setCurrentSession = useCallback((session: UISessionData | null) => {
    setState(prev => ({ ...prev, currentSession: session }));
  }, []);

  const createSession = useCallback(async (sessionData: Partial<UISessionData>): Promise<UISessionData> => {
    const newSession: UISessionData = {
      id: `session_${Date.now()}`,
      name: sessionData.name || 'Nouvelle Session',
      createdAt: new Date(),
      type: sessionData.type || 'wave_generation',
      description: sessionData.description || '',
      operator: sessionData.operator || 'Opérateur',
      laboratory: sessionData.laboratory || 'Laboratoire',
      projectName: sessionData.projectName || 'Projet',
      sondes: sessionData.sondes || state.sondes,
      files: [],
      samples: 0,
      fileSize: 0,
      status: 'pending',
      notes: '',
      tags: sessionData.tags || [],
      customFields: {},
      version: '1.0.0',
      ...sessionData
    };

    setState(prev => ({
      ...prev,
      sessions: [...prev.sessions, newSession],
      currentSession: newSession
    }));

    // Sauvegarder en localStorage (temporaire)
    const sessions = JSON.parse(localStorage.getItem('chneowave-sessions') || '[]');
    sessions.push(DataFormatAdapter.toBackendFormat(newSession));
    localStorage.setItem('chneowave-sessions', JSON.stringify(sessions));

    return newSession;
  }, [state.sondes]);

  const updateSession = useCallback(async (sessionId: string, updates: Partial<UISessionData>): Promise<void> => {
    setState(prev => {
      const updatedSessions = prev.sessions.map(session =>
        session.id === sessionId ? { ...session, ...updates } : session
      );
      
      const updatedCurrentSession = prev.currentSession?.id === sessionId 
        ? { ...prev.currentSession, ...updates }
        : prev.currentSession;

      return {
        ...prev,
        sessions: updatedSessions,
        currentSession: updatedCurrentSession
      };
    });

    // Sauvegarder
    const sessions = JSON.parse(localStorage.getItem('chneowave-sessions') || '[]');
    const updatedSessions = sessions.map((session: any) =>
      session.session_id === sessionId ? { ...session, ...updates } : session
    );
    localStorage.setItem('chneowave-sessions', JSON.stringify(updatedSessions));
  }, []);

  const deleteSession = useCallback(async (sessionId: string): Promise<void> => {
    setState(prev => ({
      ...prev,
      sessions: prev.sessions.filter(session => session.id !== sessionId),
      currentSession: prev.currentSession?.id === sessionId ? null : prev.currentSession
    }));

    // Supprimer du localStorage
    const sessions = JSON.parse(localStorage.getItem('chneowave-sessions') || '[]');
    const filteredSessions = sessions.filter((session: any) => session.session_id !== sessionId);
    localStorage.setItem('chneowave-sessions', JSON.stringify(filteredSessions));
  }, []);

  const loadSessions = useCallback(async (): Promise<void> => {
    try {
      // Charger depuis localStorage (temporaire)
      const savedSessions = JSON.parse(localStorage.getItem('chneowave-sessions') || '[]');
      const uiSessions = savedSessions.map((session: any) => 
        DataFormatAdapter.toUIFormat(session)
      );

      setState(prev => ({ ...prev, sessions: uiSessions }));
    } catch (error) {
      console.error('❌ Error loading sessions:', error);
    }
  }, []);

  // ============ ACTIONS - ACQUISITION ============
  const startAcquisition = useCallback(async (config: UIAcquisitionConfig): Promise<void> => {
    try {
      setState(prev => ({ ...prev, acquisitionConfig: config, isAcquiring: true }));
      
      realtimeBridge.startAcquisition({
        samplingRate: config.samplingRate,
        duration: config.duration,
        channels: config.channels,
        voltageRange: config.voltageRange,
        bufferSize: config.bufferSize
      });

      addNotification({
        level: 'info',
        message: 'Acquisition démarrée',
        timestamp: Date.now(),
        source: 'acquisition'
      });
    } catch (error) {
      setState(prev => ({ ...prev, isAcquiring: false }));
      addError({
        level: 'error',
        message: 'Erreur lors du démarrage de l\'acquisition',
        timestamp: Date.now(),
        source: 'acquisition',
        details: { error: error instanceof Error ? error.message : String(error) }
      });
    }
  }, [realtimeBridge]);

  const stopAcquisition = useCallback(async (): Promise<void> => {
    try {
      setState(prev => ({ ...prev, isAcquiring: false }));
      realtimeBridge.stopAcquisition();

      addNotification({
        level: 'info',
        message: 'Acquisition arrêtée',
        timestamp: Date.now(),
        source: 'acquisition'
      });
    } catch (error) {
      addError({
        level: 'error',
        message: 'Erreur lors de l\'arrêt de l\'acquisition',
        timestamp: Date.now(),
        source: 'acquisition',
        details: { error: error instanceof Error ? error.message : String(error) }
      });
    }
  }, [realtimeBridge]);

  const pauseAcquisition = useCallback(async (): Promise<void> => {
    realtimeBridge.pauseAcquisition();
  }, [realtimeBridge]);

  const resumeAcquisition = useCallback(async (): Promise<void> => {
    realtimeBridge.resumeAcquisition();
  }, [realtimeBridge]);

  const updateAcquisitionConfig = useCallback((config: UIAcquisitionConfig) => {
    setState(prev => ({ ...prev, acquisitionConfig: config }));
  }, []);

  // ============ ACTIONS - CALIBRATION ============
  const startCalibration = useCallback(async (sondeId: string): Promise<void> => {
    try {
      setState(prev => ({ 
        ...prev, 
        isCalibrating: true, 
        currentCalibratingSensor: sondeId 
      }));
      
      realtimeBridge.startCalibration(sondeId);

      addNotification({
        level: 'info',
        message: `Calibration démarrée pour le sonde ${sondeId}`,
        timestamp: Date.now(),
        source: 'calibration'
      });
    } catch (error) {
      setState(prev => ({ ...prev, isCalibrating: false, currentCalibratingSensor: null }));
      addError({
        level: 'error',
        message: 'Erreur lors du démarrage de la calibration',
        timestamp: Date.now(),
        source: 'calibration',
        details: { sondeId, error: error instanceof Error ? error.message : String(error) }
      });
    }
  }, [realtimeBridge]);

  const addCalibrationPoint = useCallback(async (sondeId: string, reference: number, measured: number): Promise<void> => {
    realtimeBridge.addCalibrationPoint(sondeId, reference, measured);
  }, [realtimeBridge]);

  const calculateCalibration = useCallback(async (sondeId: string): Promise<void> => {
    realtimeBridge.calculateCalibration(sondeId);
  }, [realtimeBridge]);

  const stopCalibration = useCallback(async (sondeId: string): Promise<void> => {
    setState(prev => ({ ...prev, isCalibrating: false, currentCalibratingSensor: null }));
    realtimeBridge.stopCalibration(sondeId);
  }, [realtimeBridge]);

  // ============ ACTIONS - SONDES ============
  const updateSensors = useCallback((sondes: UISensorData[]) => {
    setState(prev => ({ ...prev, sondes }));
  }, []);

  const toggleSensor = useCallback((sondeId: string, active: boolean) => {
    setState(prev => ({
      ...prev,
      sondes: prev.sondes.map(sonde =>
        sonde.id === sondeId ? { ...sonde, isActive: active } : sonde
      )
    }));
  }, []);

  // ============ ACTIONS - SYSTÈME ============
  const refreshSystemStatus = useCallback(async (): Promise<void> => {
    realtimeBridge.getSystemStatus();
  }, [realtimeBridge]);

  const changeBackend = useCallback(async (backendType: 'ni-daqmx' | 'iotech' | 'demo'): Promise<void> => {
    realtimeBridge.changeBackend(backendType);
    addNotification({
      level: 'info',
      message: `Backend changé vers ${backendType}`,
      timestamp: Date.now(),
      source: 'system'
    });
  }, [realtimeBridge]);

  const testConnection = useCallback(async (channels?: number[]): Promise<void> => {
    realtimeBridge.testConnection(channels);
  }, [realtimeBridge]);

  // ============ ACTIONS - ERREURS ET NOTIFICATIONS ============
  const addError = useCallback((error: ErrorNotification) => {
    setState(prev => ({ ...prev, errors: [...prev.errors, error] }));
    console.error('🚨 Error:', error);
  }, []);

  const addNotification = useCallback((notification: ErrorNotification) => {
    setState(prev => ({ ...prev, notifications: [...prev.notifications, notification] }));
  }, []);

  const clearErrors = useCallback(() => {
    setState(prev => ({ ...prev, errors: [] }));
  }, []);

  const clearNotifications = useCallback(() => {
    setState(prev => ({ ...prev, notifications: [] }));
  }, []);

  const dismissError = useCallback((index: number) => {
    setState(prev => ({
      ...prev,
      errors: prev.errors.filter((_, i) => i !== index)
    }));
  }, []);

  const dismissNotification = useCallback((index: number) => {
    setState(prev => ({
      ...prev,
      notifications: prev.notifications.filter((_, i) => i !== index)
    }));
  }, []);

  // ============ ACTIONS - UI ============
  const setSidebarCollapsed = useCallback((collapsed: boolean) => {
    setState(prev => ({ ...prev, sidebarCollapsed: collapsed }));
  }, []);

  const setCurrentPage = useCallback((page: string) => {
    setState(prev => ({ ...prev, currentPage: page }));
  }, []);

  // ============ UTILITAIRES ============
  const initializeDefaultSensors = useCallback(() => {
    const defaultSensors: UISensorData[] = [
      {
        id: 'sensor_01',
        type: 'wave_height',
        channel: 0,
        position: { x: 0, y: 0, z: 0 },
        unit: 'm',
        rangeMin: -1.0,
        rangeMax: 1.0,
        isActive: true,
        lastValue: 0,
        snr: 25,
        saturation: 0
      },
      {
        id: 'sensor_02',
        type: 'wave_height',
        channel: 1,
        position: { x: 1, y: 0, z: 0 },
        unit: 'm',
        rangeMin: -1.0,
        rangeMax: 1.0,
        isActive: true,
        lastValue: 0,
        snr: 25,
        saturation: 0
      },
      {
        id: 'sensor_03',
        type: 'pressure',
        channel: 2,
        position: { x: 0, y: 1, z: -0.5 },
        unit: 'Pa',
        rangeMin: 0,
        rangeMax: 10000,
        isActive: false,
        lastValue: 0,
        snr: 22,
        saturation: 0
      }
    ];

    setState(prev => ({ ...prev, sondes: defaultSensors }));
  }, []);

  // ============ VALEUR DU CONTEXTE ============
  const contextValue: UnifiedAppContextType = {
    // State
    ...state,
    
    // Actions
    setTheme,
    setCurrentSession,
    createSession,
    updateSession,
    deleteSession,
    loadSessions,
    startAcquisition,
    stopAcquisition,
    pauseAcquisition,
    resumeAcquisition,
    updateAcquisitionConfig,
    startCalibration,
    addCalibrationPoint,
    calculateCalibration,
    stopCalibration,
    updateSensors,
    toggleSensor,
    refreshSystemStatus,
    changeBackend,
    testConnection,
    addError,
    addNotification,
    clearErrors,
    clearNotifications,
    dismissError,
    dismissNotification,
    setSidebarCollapsed,
    setCurrentPage
  };

  return (
    <UnifiedAppContext.Provider value={contextValue}>
      {children}
    </UnifiedAppContext.Provider>
  );
};

// ============ HOOK PERSONNALISÉ ============
export const useUnifiedApp = (): UnifiedAppContextType => {
  const context = useContext(UnifiedAppContext);
  if (context === undefined) {
    throw new Error('useUnifiedApp doit être utilisé à l\'intérieur d\'un UnifiedAppProvider');
  }
  return context;
};

// ============ EXPORTS ============
export type { UnifiedAppContextType, AppState, AppActions, Theme };
export default UnifiedAppContext;
