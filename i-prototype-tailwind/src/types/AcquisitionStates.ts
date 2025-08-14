/**
 * 🔄 États d'Acquisition Normalisés - Phase 2 Catégorie D
 * Selon prompt ultra-précis : Normaliser côté UI pour coller au logiciel
 * 
 * Adopte l'enum SessionState du backend Python
 */

// Enum conforme au backend CHNeoWave (src/hrneowave/core/signal_bus.py)
export enum AcquisitionState {
  IDLE = 'idle',
  RUNNING = 'running', 
  PAUSED = 'paused',
  STOPPED = 'stopped',
  ERROR = 'error'
}

// Enum conforme au backend CHNeoWave
export enum CalibrationState {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  CALCULATING = 'calculating',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// Enum conforme au backend CHNeoWave
export enum SensorState {
  ACTIVE = 'active',
  INACTIVE = 'inactive', 
  ERROR = 'error',
  CALIBRATING = 'calibrating'
}

// Enum conforme au backend CHNeoWave
export enum SystemState {
  CONNECTED = 'connected',
  DISCONNECTED = 'disconnected',
  CONNECTING = 'connecting',
  ERROR = 'error'
}

// Mappings pour conversion backend ↔ frontend
export const AcquisitionStateMapper = {
  // Backend → Frontend
  fromBackend(backendState: string): AcquisitionState {
    const mapping: Record<string, AcquisitionState> = {
      'IDLE': AcquisitionState.IDLE,
      'RUNNING': AcquisitionState.RUNNING,
      'PAUSED': AcquisitionState.PAUSED,
      'STOPPED': AcquisitionState.STOPPED,
      'ERROR': AcquisitionState.ERROR,
      // Variants minuscules
      'idle': AcquisitionState.IDLE,
      'running': AcquisitionState.RUNNING,
      'paused': AcquisitionState.PAUSED,
      'stopped': AcquisitionState.STOPPED,
      'error': AcquisitionState.ERROR
    };
    return mapping[backendState] || AcquisitionState.IDLE;
  },

  // Frontend → Backend
  toBackend(frontendState: AcquisitionState): string {
    return frontendState.toUpperCase();
  },

  // Vérification d'état valide
  isValidState(state: string): boolean {
    return Object.values(AcquisitionState).includes(state as AcquisitionState);
  }
};

export const CalibrationStateMapper = {
  fromBackend(backendState: string): CalibrationState {
    const mapping: Record<string, CalibrationState> = {
      'PENDING': CalibrationState.PENDING,
      'IN_PROGRESS': CalibrationState.IN_PROGRESS,
      'CALCULATING': CalibrationState.CALCULATING,
      'COMPLETED': CalibrationState.COMPLETED,
      'FAILED': CalibrationState.FAILED,
      // Variants minuscules
      'pending': CalibrationState.PENDING,
      'in_progress': CalibrationState.IN_PROGRESS,
      'calculating': CalibrationState.CALCULATING,
      'completed': CalibrationState.COMPLETED,
      'failed': CalibrationState.FAILED
    };
    return mapping[backendState] || CalibrationState.PENDING;
  },

  toBackend(frontendState: CalibrationState): string {
    return frontendState.toUpperCase();
  },

  isValidState(state: string): boolean {
    return Object.values(CalibrationState).includes(state as CalibrationState);
  }
};

export const SensorStateMapper = {
  fromBackend(backendState: string): SensorState {
    const mapping: Record<string, SensorState> = {
      'ACTIVE': SensorState.ACTIVE,
      'INACTIVE': SensorState.INACTIVE,
      'ERROR': SensorState.ERROR,
      'CALIBRATING': SensorState.CALIBRATING,
      // Variants minuscules
      'active': SensorState.ACTIVE,
      'inactive': SensorState.INACTIVE,
      'error': SensorState.ERROR,
      'calibrating': SensorState.CALIBRATING
    };
    return mapping[backendState] || SensorState.INACTIVE;
  },

  toBackend(frontendState: SensorState): string {
    return frontendState.toUpperCase();
  },

  isValidState(state: string): boolean {
    return Object.values(SensorState).includes(state as SensorState);
  }
};

// Utilitaires pour l'affichage UI
export const StateDisplayUtils = {
  // Couleurs pour les états d'acquisition
  getAcquisitionColor(state: AcquisitionState): string {
    switch (state) {
      case AcquisitionState.RUNNING:
        return 'text-green-500';
      case AcquisitionState.PAUSED:
        return 'text-yellow-500';
      case AcquisitionState.ERROR:
        return 'text-red-500';
      case AcquisitionState.STOPPED:
      case AcquisitionState.IDLE:
      default:
        return 'text-gray-500';
    }
  },

  // Couleurs pour les états de calibration
  getCalibrationColor(state: CalibrationState): string {
    switch (state) {
      case CalibrationState.COMPLETED:
        return 'text-green-500';
      case CalibrationState.IN_PROGRESS:
      case CalibrationState.CALCULATING:
        return 'text-blue-500';
      case CalibrationState.FAILED:
        return 'text-red-500';
      case CalibrationState.PENDING:
      default:
        return 'text-gray-500';
    }
  },

  // Couleurs pour les états de capteur
  getSensorColor(state: SensorState): string {
    switch (state) {
      case SensorState.ACTIVE:
        return 'text-green-500';
      case SensorState.CALIBRATING:
        return 'text-blue-500';
      case SensorState.ERROR:
        return 'text-red-500';
      case SensorState.INACTIVE:
      default:
        return 'text-gray-500';
    }
  },

  // Labels français pour l'affichage
  getAcquisitionLabel(state: AcquisitionState): string {
    switch (state) {
      case AcquisitionState.IDLE:
        return 'Inactif';
      case AcquisitionState.RUNNING:
        return 'En cours';
      case AcquisitionState.PAUSED:
        return 'En pause';
      case AcquisitionState.STOPPED:
        return 'Arrêté';
      case AcquisitionState.ERROR:
        return 'Erreur';
      default:
        return 'Inconnu';
    }
  },

  getCalibrationLabel(state: CalibrationState): string {
    switch (state) {
      case CalibrationState.PENDING:
        return 'En attente';
      case CalibrationState.IN_PROGRESS:
        return 'En cours';
      case CalibrationState.CALCULATING:
        return 'Calcul en cours';
      case CalibrationState.COMPLETED:
        return 'Terminé';
      case CalibrationState.FAILED:
        return 'Échec';
      default:
        return 'Inconnu';
    }
  },

  getSensorLabel(state: SensorState): string {
    switch (state) {
      case SensorState.ACTIVE:
        return 'Actif';
      case SensorState.INACTIVE:
        return 'Inactif';
      case SensorState.ERROR:
        return 'Erreur';
      case SensorState.CALIBRATING:
        return 'Calibration';
      default:
        return 'Inconnu';
    }
  }
};

// Types pour compatibilité avec l'interface existante
export type AcquisitionStateType = AcquisitionState;
export type CalibrationStateType = CalibrationState;
export type SensorStateType = SensorState;
