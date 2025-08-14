/**
 * CHNeoWave Core Bridge API - Client TypeScript
 * Interface de communication avec le Bridge API Python
 * 
 * @author CHNeoWave Integration Team
 * @version 1.0.0
 * @date 2025-01-11
 */

import { APIResponse, RealtimeData, UISensorData, UISessionData } from '../types/interfaces';

// Configuration de l'API
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3001',
  wsURL: import.meta.env.VITE_WS_URL || 'ws://localhost:3001',
  timeout: 30000,
  retryAttempts: 3,
  retryDelay: 1000
};

/**
 * Client HTTP pour les requêtes REST
 */
class HTTPClient {
  private baseURL: string;
  private timeout: number;

  constructor(baseURL: string, timeout: number = 30000) {
    this.baseURL = baseURL;
    this.timeout = timeout;
  }

  /**
   * Effectue une requête HTTP avec gestion d'erreur et retry
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: APIResponse<T> = await response.json();
      return data;

    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error) {
        return {
          success: false,
          error: {
            code: 'HTTP_ERROR',
            message: error.message,
            details: { endpoint, options }
          },
          timestamp: Date.now()
        };
      }
      
      throw error;
    }
  }

  async get<T>(endpoint: string): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

/**
 * Client WebSocket pour les données temps réel
 */
class RealtimeWebSocketClient {
  private wsURL: string;
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private listeners: Map<string, ((data: any) => void)[]> = new Map();
  private isConnecting = false;

  constructor(wsURL: string) {
    this.wsURL = wsURL;
  }

  /**
   * Connecte au WebSocket
   */
  async connect(): Promise<void> {
    if (this.isConnecting || (this.ws && this.ws.readyState === WebSocket.OPEN)) {
      return;
    }

    this.isConnecting = true;

    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(`${this.wsURL}/ws/realtime`);

        this.ws.onopen = () => {
          console.log('✅ WebSocket connecté au Bridge API');
          this.isConnecting = false;
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error('❌ Erreur parsing message WebSocket:', error);
          }
        };

        this.ws.onclose = (event) => {
          console.log(`📡 WebSocket fermé: ${event.code} ${event.reason}`);
          this.isConnecting = false;
          this.ws = null;
          
          // Reconnexion automatique
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.scheduleReconnect();
          }
        };

        this.ws.onerror = (error) => {
          console.error('❌ Erreur WebSocket:', error);
          this.isConnecting = false;
          reject(error);
        };

      } catch (error) {
        this.isConnecting = false;
        reject(error);
      }
    });
  }

  /**
   * Déconnecte du WebSocket
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }
    this.listeners.clear();
  }

  /**
   * Envoie un message via WebSocket
   */
  send(message: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('⚠️ WebSocket non connecté, message ignoré:', message);
    }
  }

  /**
   * Ajoute un listener pour un type de message
   */
  on(eventType: string, callback: (data: any) => void): void {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType)!.push(callback);
  }

  /**
   * Supprime un listener
   */
  off(eventType: string, callback: (data: any) => void): void {
    const listeners = this.listeners.get(eventType);
    if (listeners) {
      const index = listeners.indexOf(callback);
      if (index !== -1) {
        listeners.splice(index, 1);
      }
    }
  }

  /**
   * Gère les messages reçus
   */
  private handleMessage(data: any): void {
    const { type } = data;
    const listeners = this.listeners.get(type) || [];
    
    listeners.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`❌ Erreur dans listener ${type}:`, error);
      }
    });

    // Listeners génériques
    const allListeners = this.listeners.get('*') || [];
    allListeners.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error('❌ Erreur dans listener générique:', error);
      }
    });
  }

  /**
   * Programme une reconnexion
   */
  private scheduleReconnect(): void {
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`🔄 Reconnexion WebSocket dans ${delay}ms (tentative ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
    
    setTimeout(() => {
      this.connect().catch(error => {
        console.error('❌ Échec reconnexion WebSocket:', error);
      });
    }, delay);
  }

  /**
   * Vérifie l'état de la connexion
   */
  get isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

/**
 * API Client principal pour CHNeoWave Bridge
 */
export class CoreBridgeAPI {
  private http: HTTPClient;
  private ws: RealtimeWebSocketClient;
  private isInitialized = false;

  constructor() {
    this.http = new HTTPClient(API_CONFIG.baseURL, API_CONFIG.timeout);
    this.ws = new RealtimeWebSocketClient(API_CONFIG.wsURL);
  }

  /**
   * Initialise la connexion API
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    try {
      // Test de connexion HTTP
      const healthCheck = await this.getHealth();
      if (!healthCheck.success) {
        throw new Error('API Bridge non disponible');
      }

      console.log('✅ Bridge API connecté:', healthCheck.data);

      // Connexion WebSocket
      await this.ws.connect();

      this.isInitialized = true;
      console.log('🚀 CoreBridgeAPI initialisé avec succès');

    } catch (error) {
      console.error('❌ Échec initialisation CoreBridgeAPI:', error);
      throw error;
    }
  }

  /**
   * Termine les connexions
   */
  dispose(): void {
    this.ws.disconnect();
    this.isInitialized = false;
  }

  // =========================================================================
  // ENDPOINTS SYSTÈME
  // =========================================================================

  async getHealth(): Promise<APIResponse<any>> {
    return this.http.get('/health');
  }

  async getSystemStatus(): Promise<APIResponse<any>> {
    return this.http.get('/system/status');
  }

  // =========================================================================
  // ENDPOINTS HARDWARE
  // =========================================================================

  async getHardwareBackends(): Promise<APIResponse<{
    backends: string[];
    current: string;
    descriptions: Record<string, string>;
  }>> {
    return this.http.get('/hardware/backends');
  }

  async switchHardwareBackend(backend: string): Promise<APIResponse<any>> {
    return this.http.post('/hardware/switch', { backend });
  }

  async scanHardwareDevices(): Promise<APIResponse<{
    devices: any[];
    count: number;
    timestamp: string;
  }>> {
    return this.http.get('/hardware/scan');
  }

  // =========================================================================
  // ENDPOINTS ACQUISITION
  // =========================================================================

  async startAcquisition(config: {
    sampling_rate: number;
    channels: number[];
    duration?: number;
    voltage_range: string;
    buffer_size: number;
    project_name: string;
  }): Promise<APIResponse<{
    session_id: string;
    status: string;
    config: any;
  }>> {
    return this.http.post('/acquisition/start', config);
  }

  async stopAcquisition(): Promise<APIResponse<{
    status: string;
    timestamp: string;
  }>> {
    return this.http.post('/acquisition/stop');
  }

  async pauseAcquisition(): Promise<APIResponse<{
    status: string;
    timestamp: string;
  }>> {
    return this.http.post('/acquisition/pause');
  }

  async getAcquisitionStatus(): Promise<APIResponse<any>> {
    return this.http.get('/acquisition/status');
  }

  // =========================================================================
  // ENDPOINTS TRAITEMENT
  // =========================================================================

  async computeFFT(data: {
    signal_data: number[];
    sampling_rate: number;
    normalize?: boolean;
  }): Promise<APIResponse<{
    fft_magnitude: number[];
    fft_phase: number[];
    frequencies: number[];
    length: number;
    sampling_rate: number;
  }>> {
    return this.http.post('/processing/fft', data);
  }

  // =========================================================================
  // WEBSOCKET TEMPS RÉEL
  // =========================================================================

  /**
   * Abonne à un type d'événement temps réel
   */
  onRealtimeData(callback: (data: RealtimeData) => void): void {
    this.ws.on('acquisition_data', callback);
  }

  /**
   * Désabonne d'un type d'événement
   */
  offRealtimeData(callback: (data: RealtimeData) => void): void {
    this.ws.off('acquisition_data', callback);
  }

  /**
   * Abonne à tous les événements WebSocket
   */
  onAnyRealtimeEvent(callback: (data: any) => void): void {
    this.ws.on('*', callback);
  }

  /**
   * Envoie un ping WebSocket
   */
  pingWebSocket(): void {
    this.ws.send({ type: 'ping', timestamp: Date.now() });
  }

  /**
   * S'abonne à des canaux spécifiques
   */
  subscribeToChannels(channels: string[]): void {
    this.ws.send({ type: 'subscribe', channels });
  }

  /**
   * État de la connexion WebSocket
   */
  get isWebSocketConnected(): boolean {
    return this.ws.isConnected;
  }

  // =========================================================================
  // ADAPTATEURS DE DONNÉES
  // =========================================================================

  /**
   * Adapte les données d'acquisition Python vers le format UI React
   */
  adaptAcquisitionData(pythonData: any): RealtimeData {
    return {
      type: 'acquisition_data',
      timestamp: pythonData.timestamp || Date.now(),
      data: {
        channel_data: pythonData.data?.channels || {},
        sample_count: pythonData.data?.sample_count || 0,
        status: pythonData.data?.status || 'unknown',
        fft_results: pythonData.data?.fft_results || [],
        system_metrics: pythonData.data?.system_metrics || {}
      }
    };
  }

  /**
   * Adapte une configuration de canal Python vers le format UI
   */
  adaptChannelConfig(pythonChannel: any): UISensorData {
    return {
      id: pythonChannel.channel?.toString() || '0',
      name: pythonChannel.label || `Canal ${pythonChannel.channel}`,
      type: pythonChannel.sensor_type || 'generic',
      isActive: pythonChannel.enabled || false,
      channel: pythonChannel.channel || 0,
      unit: pythonChannel.physical_units || 'V',
      sensitivity: pythonChannel.sensor_sensitivity || 1.0,
      lastValue: 0,
      status: pythonChannel.enabled ? 'active' : 'inactive'
    };
  }

  /**
   * Adapte une session d'acquisition Python vers le format UI
   */
  adaptAcquisitionSession(pythonSession: any): UISessionData {
    return {
      id: pythonSession.session_id || 'unknown',
      name: pythonSession.project_name || 'Session sans nom',
      startTime: pythonSession.start_time ? new Date(pythonSession.start_time) : new Date(),
      endTime: pythonSession.end_time ? new Date(pythonSession.end_time) : null,
      samplingRate: pythonSession.sampling_rate || 1000,
      totalSamples: pythonSession.total_samples || 0,
      channels: pythonSession.channels?.map(this.adaptChannelConfig) || [],
      metadata: pythonSession.metadata || {}
    };
  }
}

// Instance singleton
export const coreBridgeAPI = new CoreBridgeAPI();

// Auto-initialisation
let autoInitAttempted = false;
export const initializeCoreAPI = async (): Promise<boolean> => {
  if (autoInitAttempted) return coreBridgeAPI.isInitialized;
  
  autoInitAttempted = true;
  
  try {
    await coreBridgeAPI.initialize();
    return true;
  } catch (error) {
    console.warn('⚠️ Bridge API non disponible, utilisation des mocks:', error);
    return false;
  }
};

// Export des types pour référence
export type { APIResponse, RealtimeData, UISensorData, UISessionData };
