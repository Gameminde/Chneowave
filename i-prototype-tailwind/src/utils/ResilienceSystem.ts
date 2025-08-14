/**
 * 🛡️ Système de Résilience - Phase 3.3
 * Selon prompt ultra-précis : gestion erreurs réseau/capteurs, retries, messages utilisateurs, logs
 * 
 * Système de gestion d'erreurs et résilience pour CHNeoWave
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { ErrorMessages, SuccessMessages } from './AccessibilityHelpers';

// ============ TYPES D'ERREURS ============

export enum ErrorType {
  NETWORK = 'network',
  HARDWARE = 'hardware',
  SENSOR = 'sensor',
  CALIBRATION = 'calibration',
  ACQUISITION = 'acquisition',
  VALIDATION = 'validation',
  PERMISSION = 'permission',
  TIMEOUT = 'timeout',
  UNKNOWN = 'unknown'
}

export enum ErrorSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export interface CHNeoWaveError {
  id: string;
  type: ErrorType;
  severity: ErrorSeverity;
  message: string;
  details?: any;
  timestamp: number;
  source: string;
  retryable: boolean;
  retryCount?: number;
  maxRetries?: number;
  userMessage: string;
  technicalMessage: string;
}

// ============ GESTIONNAIRE D'ERREURS ============

export class ErrorManager {
  private errors = new Map<string, CHNeoWaveError>();
  private listeners: Array<(error: CHNeoWaveError) => void> = [];
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  /**
   * Enregistrer une nouvelle erreur
   */
  handleError(error: Partial<CHNeoWaveError> & { message: string; source: string }): CHNeoWaveError {
    const fullError: CHNeoWaveError = {
      id: this.generateErrorId(),
      type: error.type || ErrorType.UNKNOWN,
      severity: error.severity || ErrorSeverity.MEDIUM,
      message: error.message,
      details: error.details,
      timestamp: Date.now(),
      source: error.source,
      retryable: error.retryable ?? this.isRetryable(error.type || ErrorType.UNKNOWN),
      retryCount: error.retryCount || 0,
      maxRetries: error.maxRetries || this.getMaxRetries(error.type || ErrorType.UNKNOWN),
      userMessage: this.generateUserMessage(error),
      technicalMessage: this.generateTechnicalMessage(error)
    };

    this.errors.set(fullError.id, fullError);
    this.logger.error(fullError);
    
    // Notifier les listeners
    this.listeners.forEach(listener => listener(fullError));

    return fullError;
  }

  /**
   * Marquer une erreur comme résolue
   */
  resolveError(errorId: string) {
    const error = this.errors.get(errorId);
    if (error) {
      this.errors.delete(errorId);
      this.logger.info(`Erreur résolue: ${errorId}`, { error });
    }
  }

  /**
   * Obtenir toutes les erreurs actives
   */
  getActiveErrors(): CHNeoWaveError[] {
    return Array.from(this.errors.values());
  }

  /**
   * Obtenir erreurs par sévérité
   */
  getErrorsBySeverity(severity: ErrorSeverity): CHNeoWaveError[] {
    return this.getActiveErrors().filter(error => error.severity === severity);
  }

  /**
   * S'abonner aux nouvelles erreurs
   */
  onError(listener: (error: CHNeoWaveError) => void) {
    this.listeners.push(listener);
    
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  private generateErrorId(): string {
    return `err_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private isRetryable(type: ErrorType): boolean {
    const retryableTypes = [
      ErrorType.NETWORK,
      ErrorType.TIMEOUT,
      ErrorType.HARDWARE,
      ErrorType.SENSOR
    ];
    return retryableTypes.includes(type);
  }

  private getMaxRetries(type: ErrorType): number {
    switch (type) {
      case ErrorType.NETWORK:
        return 3;
      case ErrorType.HARDWARE:
      case ErrorType.SENSOR:
        return 2;
      case ErrorType.TIMEOUT:
        return 1;
      default:
        return 0;
    }
  }

  private generateUserMessage(error: Partial<CHNeoWaveError>): string {
    switch (error.type) {
      case ErrorType.NETWORK:
        return ErrorMessages.network(error.source || 'opération');
      case ErrorType.HARDWARE:
        return ErrorMessages.hardware(error.details?.device || 'périphérique');
      case ErrorType.SENSOR:
        return ErrorMessages.calibration(error.details?.sensorId || 'capteur');
      case ErrorType.ACQUISITION:
        return ErrorMessages.acquisition(error.details?.reason || 'erreur inconnue');
      case ErrorType.VALIDATION:
        return ErrorMessages.validation(error.details?.field || 'données');
      case ErrorType.PERMISSION:
        return ErrorMessages.permission(error.source || 'action');
      default:
        return error.message;
    }
  }

  private generateTechnicalMessage(error: Partial<CHNeoWaveError>): string {
    const base = `[${error.type?.toUpperCase()}] ${error.message}`;
    if (error.details) {
      return `${base} - Détails: ${JSON.stringify(error.details)}`;
    }
    return base;
  }
}

// ============ SYSTÈME DE RETRY ============

interface RetryConfig {
  maxAttempts: number;
  baseDelay: number;
  maxDelay: number;
  backoffFactor: number;
  retryCondition?: (error: any) => boolean;
}

export class RetryManager {
  private defaultConfig: RetryConfig = {
    maxAttempts: 3,
    baseDelay: 1000,
    maxDelay: 10000,
    backoffFactor: 2
  };

  /**
   * Exécuter une opération avec retry automatique
   */
  async executeWithRetry<T>(
    operation: () => Promise<T>,
    config: Partial<RetryConfig> = {}
  ): Promise<T> {
    const finalConfig = { ...this.defaultConfig, ...config };
    let lastError: any;

    for (let attempt = 1; attempt <= finalConfig.maxAttempts; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;

        // Vérifier si on doit retry
        if (attempt === finalConfig.maxAttempts || 
            (finalConfig.retryCondition && !finalConfig.retryCondition(error))) {
          break;
        }

        // Calculer délai avec backoff exponentiel
        const delay = Math.min(
          finalConfig.baseDelay * Math.pow(finalConfig.backoffFactor, attempt - 1),
          finalConfig.maxDelay
        );

        // Attendre avant le retry
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    throw lastError;
  }

  /**
   * Retry spécifique pour opérations réseau
   */
  async retryNetworkOperation<T>(operation: () => Promise<T>): Promise<T> {
    return this.executeWithRetry(operation, {
      maxAttempts: 3,
      baseDelay: 1000,
      retryCondition: (error) => {
        // Retry sur erreurs réseau temporaires
        return error.name === 'NetworkError' || 
               error.code === 'NETWORK_ERROR' ||
               (error.status >= 500 && error.status < 600);
      }
    });
  }

  /**
   * Retry spécifique pour opérations hardware
   */
  async retryHardwareOperation<T>(operation: () => Promise<T>): Promise<T> {
    return this.executeWithRetry(operation, {
      maxAttempts: 2,
      baseDelay: 2000,
      retryCondition: (error) => {
        // Retry sur erreurs hardware temporaires
        return error.type === 'HARDWARE_BUSY' || 
               error.type === 'SENSOR_NOT_READY';
      }
    });
  }
}

// ============ LOGGER ============

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
  CRITICAL = 4
}

export interface LogEntry {
  timestamp: number;
  level: LogLevel;
  message: string;
  data?: any;
  source: string;
}

export class Logger {
  private logs: LogEntry[] = [];
  private maxLogs = 1000;
  private minLevel = LogLevel.INFO;

  constructor(minLevel: LogLevel = LogLevel.INFO) {
    this.minLevel = minLevel;
  }

  debug(message: string, data?: any, source: string = 'system') {
    this.log(LogLevel.DEBUG, message, data, source);
  }

  info(message: string, data?: any, source: string = 'system') {
    this.log(LogLevel.INFO, message, data, source);
  }

  warn(message: string, data?: any, source: string = 'system') {
    this.log(LogLevel.WARN, message, data, source);
  }

  error(error: CHNeoWaveError | string, data?: any, source: string = 'system') {
    if (typeof error === 'string') {
      this.log(LogLevel.ERROR, error, data, source);
    } else {
      this.log(LogLevel.ERROR, error.technicalMessage, error, error.source);
    }
  }

  critical(message: string, data?: any, source: string = 'system') {
    this.log(LogLevel.CRITICAL, message, data, source);
  }

  private log(level: LogLevel, message: string, data?: any, source: string = 'system') {
    if (level < this.minLevel) return;

    const entry: LogEntry = {
      timestamp: Date.now(),
      level,
      message,
      data,
      source
    };

    this.logs.push(entry);

    // Limiter nombre de logs
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(-this.maxLogs);
    }

    // Log vers console en développement
    if (process.env.NODE_ENV === 'development') {
      const levelName = LogLevel[level];
      const timestamp = new Date(entry.timestamp).toISOString();
      
      switch (level) {
        case LogLevel.DEBUG:
          console.debug(`[${timestamp}] ${levelName} [${source}]:`, message, data);
          break;
        case LogLevel.INFO:
          console.info(`[${timestamp}] ${levelName} [${source}]:`, message, data);
          break;
        case LogLevel.WARN:
          console.warn(`[${timestamp}] ${levelName} [${source}]:`, message, data);
          break;
        case LogLevel.ERROR:
        case LogLevel.CRITICAL:
          console.error(`[${timestamp}] ${levelName} [${source}]:`, message, data);
          break;
      }
    }
  }

  /**
   * Obtenir logs récents
   */
  getRecentLogs(count: number = 50): LogEntry[] {
    return this.logs.slice(-count);
  }

  /**
   * Obtenir logs par niveau
   */
  getLogsByLevel(level: LogLevel): LogEntry[] {
    return this.logs.filter(log => log.level === level);
  }

  /**
   * Exporter logs
   */
  exportLogs(): string {
    return this.logs.map(log => {
      const timestamp = new Date(log.timestamp).toISOString();
      const level = LogLevel[log.level];
      const data = log.data ? ` - ${JSON.stringify(log.data)}` : '';
      return `[${timestamp}] ${level} [${log.source}]: ${log.message}${data}`;
    }).join('\n');
  }

  /**
   * Nettoyer anciens logs
   */
  clearOldLogs(olderThanMs: number = 24 * 60 * 60 * 1000) {
    const cutoff = Date.now() - olderThanMs;
    this.logs = this.logs.filter(log => log.timestamp > cutoff);
  }
}

// ============ HOOKS REACT ============

/**
 * Hook pour gestion d'erreurs avec retry
 */
export function useErrorHandler() {
  const errorManagerRef = useRef<ErrorManager | null>(null);
  const retryManagerRef = useRef<RetryManager | null>(null);
  const loggerRef = useRef<Logger | null>(null);

  const [activeErrors, setActiveErrors] = useState<CHNeoWaveError[]>([]);

  useEffect(() => {
    loggerRef.current = new Logger(LogLevel.INFO);
    errorManagerRef.current = new ErrorManager(loggerRef.current);
    retryManagerRef.current = new RetryManager();

    const unsubscribe = errorManagerRef.current.onError((error) => {
      setActiveErrors(prev => [...prev, error]);
    });

    return unsubscribe;
  }, []);

  const handleError = useCallback((error: Partial<CHNeoWaveError> & { message: string; source: string }) => {
    return errorManagerRef.current?.handleError(error);
  }, []);

  const resolveError = useCallback((errorId: string) => {
    errorManagerRef.current?.resolveError(errorId);
    setActiveErrors(prev => prev.filter(e => e.id !== errorId));
  }, []);

  const executeWithRetry = useCallback(async <T>(
    operation: () => Promise<T>,
    config?: Partial<RetryConfig>
  ) => {
    return retryManagerRef.current?.executeWithRetry(operation, config);
  }, []);

  const retryNetworkOperation = useCallback(async <T>(operation: () => Promise<T>) => {
    return retryManagerRef.current?.retryNetworkOperation(operation);
  }, []);

  const retryHardwareOperation = useCallback(async <T>(operation: () => Promise<T>) => {
    return retryManagerRef.current?.retryHardwareOperation(operation);
  }, []);

  const log = useCallback((level: LogLevel, message: string, data?: any, source?: string) => {
    switch (level) {
      case LogLevel.DEBUG:
        loggerRef.current?.debug(message, data, source);
        break;
      case LogLevel.INFO:
        loggerRef.current?.info(message, data, source);
        break;
      case LogLevel.WARN:
        loggerRef.current?.warn(message, data, source);
        break;
      case LogLevel.ERROR:
        loggerRef.current?.error(message, data, source);
        break;
      case LogLevel.CRITICAL:
        loggerRef.current?.critical(message, data, source);
        break;
    }
  }, []);

  return {
    activeErrors,
    handleError,
    resolveError,
    executeWithRetry,
    retryNetworkOperation,
    retryHardwareOperation,
    log
  };
}

/**
 * Hook pour monitoring de santé système
 */
export function useHealthMonitor() {
  const [health, setHealth] = useState({
    network: true,
    hardware: true,
    sensors: true,
    backend: true,
    lastCheck: Date.now()
  });

  const [healthHistory, setHealthHistory] = useState<typeof health[]>([]);

  const checkHealth = useCallback(async () => {
    try {
      // Vérifier réseau
      const networkOk = navigator.onLine;
      
      // Vérifier backend (simulé)
      let backendOk = true;
      try {
        // await fetch('/api/health', { method: 'HEAD' });
      } catch {
        backendOk = false;
      }

      const newHealth = {
        network: networkOk,
        hardware: true, // À connecter aux vrais checks
        sensors: true,  // À connecter aux vrais checks
        backend: backendOk,
        lastCheck: Date.now()
      };

      setHealth(newHealth);
      setHealthHistory(prev => [...prev.slice(-99), newHealth]);

    } catch (error) {
      console.error('Erreur vérification santé:', error);
    }
  }, []);

  useEffect(() => {
    // Vérification initiale
    checkHealth();

    // Vérifications périodiques
    const interval = setInterval(checkHealth, 30000); // 30s

    // Écouter changements réseau
    const handleOnline = () => checkHealth();
    const handleOffline = () => checkHealth();

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      clearInterval(interval);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [checkHealth]);

  const isHealthy = health.network && health.hardware && health.sensors && health.backend;

  return {
    health,
    healthHistory,
    isHealthy,
    checkHealth
  };
}

/**
 * Hook pour gestion circuit breaker
 */
export function useCircuitBreaker(
  operation: () => Promise<any>,
  options: {
    failureThreshold?: number;
    resetTimeout?: number;
    monitoringPeriod?: number;
  } = {}
) {
  const {
    failureThreshold = 5,
    resetTimeout = 60000,
    monitoringPeriod = 10000
  } = options;

  const [state, setState] = useState<'closed' | 'open' | 'half-open'>('closed');
  const [failures, setFailures] = useState(0);
  const [lastFailure, setLastFailure] = useState(0);

  const execute = useCallback(async () => {
    // Circuit ouvert
    if (state === 'open') {
      if (Date.now() - lastFailure > resetTimeout) {
        setState('half-open');
      } else {
        throw new Error('Circuit breaker ouvert - service indisponible');
      }
    }

    try {
      const result = await operation();
      
      // Succès - réinitialiser
      if (state === 'half-open') {
        setState('closed');
        setFailures(0);
      }
      
      return result;
    } catch (error) {
      const newFailures = failures + 1;
      setFailures(newFailures);
      setLastFailure(Date.now());

      // Ouvrir circuit si seuil atteint
      if (newFailures >= failureThreshold) {
        setState('open');
      }

      throw error;
    }
  }, [operation, state, failures, lastFailure, failureThreshold, resetTimeout]);

  return {
    execute,
    state,
    failures,
    isAvailable: state !== 'open'
  };
}

export default {
  ErrorManager,
  RetryManager,
  Logger,
  useErrorHandler,
  useHealthMonitor,
  useCircuitBreaker,
  ErrorType,
  ErrorSeverity,
  LogLevel
};
