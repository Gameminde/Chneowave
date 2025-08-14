/**
 * 🔄 Realtime Bridge - CHNeoWave Integration
 * Pont temps réel Signal Bus Python ↔ React Context
 * 
 * Selon prompt ultra-précis : Relier actions UI aux services existants
 */

// Browser-compatible EventEmitter implementation
class EventEmitter {
  private events: { [key: string]: Function[] } = {};

  on(event: string, listener: Function): void {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
  }

  emit(event: string, ...args: any[]): void {
    if (this.events[event]) {
      this.events[event].forEach(listener => listener(...args));
    }
  }

  removeAllListeners(event?: string): void {
    if (event) {
      delete this.events[event];
    } else {
      this.events = {};
    }
  }
}

// ============ INTERFACES TEMPS RÉEL ============
interface AcquisitionData {
  timestamp: number;
  channel_data: { [channel: string]: number[] };
  sample_count: number;
  status: 'idle' | 'running' | 'paused' | 'stopped' | 'error';
  sampling_rate: number;
  duration_elapsed: number;
}

interface CalibrationUpdate {
  sonde_id: string;
  slope: number;
  offset: number;
  r2: number;
  rmse: number;
  points_count: number;
  status: 'pending' | 'in_progress' | 'calculating' | 'completed' | 'failed';
  progress_percent: number;
}

interface SystemStatus {
  hardware_connected: boolean;
  backend_type: 'ni-daqmx' | 'iotech' | 'demo';
  sensors_active: number;
  sensors_total: number;
  acquisition_running: boolean;
  last_error: string | null;
  memory_usage_mb: number;
  cpu_usage_percent: number;
  uptime_seconds: number;
}

interface SondeStatus {
  sonde_id: string;
  channel: number;
  is_connected: boolean;
  last_value: number;
  snr_db: number;
  saturation_percent: number;
  drift_rate: number;
  status: 'active' | 'inactive' | 'error' | 'calibrating';
  error_message?: string;
}

interface ErrorNotification {
  level: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  timestamp: number;
  source: string;
  details?: Record<string, any>;
}

// ============ COMMANDES VERS BACKEND ============
interface AcquisitionCommand {
  command: 'start_acquisition' | 'stop_acquisition' | 'pause_acquisition' | 'resume_acquisition';
  config?: {
    sampling_rate: number;
    duration: number;
    channels: number[];
    voltage_range: string;
    buffer_size: number;
  };
}

interface CalibrationCommand {
  command: 'start_calibration' | 'add_calibration_point' | 'calculate_calibration' | 'stop_calibration';
  sonde_id: string;
  data?: {
    reference_value?: number;
    measured_value?: number;
    points_count?: number;
  };
}

interface SystemCommand {
  command: 'get_system_status' | 'reset_system' | 'change_backend' | 'test_connection';
  parameters?: {
    backend_type?: string;
    test_channels?: number[];
  };
}

// ============ BRIDGE PRINCIPAL ============
export class RealtimeBridge extends EventEmitter {
  private websocket: WebSocket | null = null;
  private reconnectInterval: number = 5000;
  private maxReconnectAttempts: number = 10;
  private reconnectAttempts: number = 0;
  private isConnected: boolean = false;
  private heartbeatInterval: number | null = null;
  private messageQueue: any[] = [];

  constructor(private wsUrl: string = 'ws://localhost:8080/ws') {
    super();
    this.connect();
  }

  // ============ GESTION CONNEXION ============
  private connect(): void {
    try {
      console.log(`🔌 Connecting to CHNeoWave backend: ${this.wsUrl}`);
      this.websocket = new WebSocket(this.wsUrl);
      
      this.websocket.onopen = () => {
        console.log('✅ Connected to CHNeoWave backend');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.emit('connected');
        this.startHeartbeat();
        this.flushMessageQueue();
      };

      this.websocket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.handleBackendMessage(message);
        } catch (error) {
          console.error('❌ Error parsing backend message:', error);
          this.emit('error', { type: 'parse_error', error });
        }
      };

      this.websocket.onclose = (event) => {
        console.log(`🔌 Disconnected from CHNeoWave backend (code: ${event.code})`);
        this.isConnected = false;
        this.stopHeartbeat();
        this.emit('disconnected', { code: event.code, reason: event.reason });
        this.attemptReconnect();
      };

      this.websocket.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        this.emit('error', { type: 'websocket_error', error });
      };

    } catch (error) {
      console.error('❌ Failed to connect to backend:', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      setTimeout(() => this.connect(), this.reconnectInterval);
    } else {
      console.error('❌ Max reconnection attempts reached');
      this.emit('maxReconnectAttemptsReached');
    }
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      this.sendCommand('ping', {});
    }, 30000); // 30 seconds
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  private flushMessageQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.sendMessage(message);
    }
  }

  // ============ GESTION DES MESSAGES ============
  private handleBackendMessage(message: any): void {
    switch (message.type) {
      case 'acquisition_data':
        this.emit('acquisitionData', this.adaptAcquisitionData(message.data));
        break;
      case 'calibration_update':
        this.emit('calibrationUpdate', this.adaptCalibrationUpdate(message.data));
        break;
      case 'system_status':
        this.emit('systemStatus', this.adaptSystemStatus(message.data));
        break;
      case 'sensor_status':
        this.emit('sensorStatus', this.adaptSensorStatus(message.data));
        break;
      case 'error':
        this.emit('error', this.adaptErrorNotification(message.data));
        break;
      case 'notification':
        this.emit('notification', this.adaptErrorNotification(message.data));
        break;
      case 'pong':
        // Heartbeat response
        break;
      default:
        console.warn('⚠️ Unknown message type:', message.type);
        this.emit('unknownMessage', message);
    }
  }

  // ============ ADAPTATEURS DE DONNÉES ============
  private adaptAcquisitionData(backendData: any): AcquisitionData {
    return {
      timestamp: backendData.timestamp || Date.now(),
      channel_data: backendData.channels || backendData.channel_data || {},
      sample_count: backendData.samples || backendData.sample_count || 0,
      status: this.mapAcquisitionStatus(backendData.status),
      sampling_rate: backendData.sampling_rate || backendData.fs || 1000,
      duration_elapsed: backendData.duration_elapsed || backendData.elapsed || 0
    };
  }

  private adaptCalibrationUpdate(backendData: any): CalibrationUpdate {
    return {
      sonde_id: backendData.sonde_id || backendData.sondeId || '',
      slope: backendData.slope || 1.0,
      offset: backendData.offset || 0.0,
      r2: backendData.r2 || backendData.r_squared || 0.0,
      rmse: backendData.rmse || backendData.error || 0.0,
      points_count: backendData.points_count || backendData.points?.length || 0,
      status: this.mapCalibrationStatus(backendData.status),
      progress_percent: backendData.progress_percent || backendData.progress || 0
    };
  }

  private adaptSystemStatus(backendData: any): SystemStatus {
    return {
      hardware_connected: backendData.hardware_connected || false,
      backend_type: backendData.backend_type || 'demo',
      sensors_active: backendData.sensors_active || 0,
      sensors_total: backendData.sensors_total || 0,
      acquisition_running: backendData.acquisition_running || false,
      last_error: backendData.last_error || null,
      memory_usage_mb: backendData.memory_usage_mb || 0,
      cpu_usage_percent: backendData.cpu_usage_percent || 0,
      uptime_seconds: backendData.uptime_seconds || 0
    };
  }

  private adaptSensorStatus(backendData: any): SondeStatus {
    return {
      sonde_id: backendData.sonde_id || backendData.id || '',
      channel: backendData.channel || 0,
      is_connected: backendData.is_connected || backendData.connected || false,
      last_value: backendData.last_value || backendData.value || 0,
      snr_db: backendData.snr_db || backendData.snr || 25,
      saturation_percent: backendData.saturation_percent || backendData.saturation || 0,
      drift_rate: backendData.drift_rate || backendData.drift || 0,
      status: this.mapSensorStatus(backendData.status),
      error_message: backendData.error_message || backendData.error
    };
  }

  private adaptErrorNotification(backendData: any): ErrorNotification {
    return {
      level: this.mapErrorLevel(backendData.level),
      message: backendData.message || 'Unknown error',
      timestamp: backendData.timestamp || Date.now(),
      source: backendData.source || 'backend',
      details: backendData.details || backendData.data
    };
  }

  // ============ MAPPERS D'ÉTAT ============
  private mapAcquisitionStatus(status: string): AcquisitionData['status'] {
    const mapping: Record<string, AcquisitionData['status']> = {
      'IDLE': 'idle',
      'RUNNING': 'running',
      'PAUSED': 'paused',
      'STOPPED': 'stopped',
      'ERROR': 'error',
      'idle': 'idle',
      'running': 'running',
      'paused': 'paused',
      'stopped': 'stopped',
      'error': 'error'
    };
    return mapping[status] || 'idle';
  }

  private mapCalibrationStatus(status: string): CalibrationUpdate['status'] {
    const mapping: Record<string, CalibrationUpdate['status']> = {
      'PENDING': 'pending',
      'IN_PROGRESS': 'in_progress',
      'CALCULATING': 'calculating',
      'COMPLETED': 'completed',
      'FAILED': 'failed',
      'pending': 'pending',
      'in_progress': 'in_progress',
      'calculating': 'calculating',
      'completed': 'completed',
      'failed': 'failed'
    };
    return mapping[status] || 'pending';
  }

  private mapSensorStatus(status: string): SondeStatus['status'] {
    const mapping: Record<string, SondeStatus['status']> = {
      'ACTIVE': 'active',
      'INACTIVE': 'inactive',
      'ERROR': 'error',
      'CALIBRATING': 'calibrating',
      'active': 'active',
      'inactive': 'inactive',
      'error': 'error',
      'calibrating': 'calibrating'
    };
    return mapping[status] || 'inactive';
  }

  private mapErrorLevel(level: string): ErrorNotification['level'] {
    const mapping: Record<string, ErrorNotification['level']> = {
      'INFO': 'info',
      'WARNING': 'warning',
      'ERROR': 'error',
      'CRITICAL': 'critical',
      'info': 'info',
      'warning': 'warning',
      'error': 'error',
      'critical': 'critical'
    };
    return mapping[level] || 'info';
  }

  // ============ API PUBLIQUE - COMMANDES ============
  private sendMessage(message: any): void {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify(message));
    } else {
      console.warn('⚠️ WebSocket not connected, queuing message');
      this.messageQueue.push(message);
    }
  }

  public sendCommand(command: string, data?: any): void {
    this.sendMessage({ command, data, timestamp: Date.now() });
  }

  // ============ ACQUISITION COMMANDS ============
  public startAcquisition(config: {
    samplingRate: number;
    duration: number;
    channels: number[];
    voltageRange: string;
    bufferSize?: number;
  }): void {
    this.sendCommand('start_acquisition', {
      sampling_rate: config.samplingRate,
      duration: config.duration,
      channels: config.channels,
      voltage_range: config.voltageRange,
      buffer_size: config.bufferSize || 10000
    });
  }

  public stopAcquisition(): void {
    this.sendCommand('stop_acquisition');
  }

  public pauseAcquisition(): void {
    this.sendCommand('pause_acquisition');
  }

  public resumeAcquisition(): void {
    this.sendCommand('resume_acquisition');
  }

  // ============ CALIBRATION COMMANDS ============
  public startCalibration(sondeId: string): void {
    this.sendCommand('start_calibration', { sonde_id: sondeId });
  }

  public addCalibrationPoint(sondeId: string, referenceValue: number, measuredValue: number): void {
    this.sendCommand('add_calibration_point', {
      sonde_id: sondeId,
      reference_value: referenceValue,
      measured_value: measuredValue
    });
  }

  public calculateCalibration(sondeId: string): void {
    this.sendCommand('calculate_calibration', { sonde_id: sondeId });
  }

  public stopCalibration(sondeId: string): void {
    this.sendCommand('stop_calibration', { sonde_id: sondeId });
  }

  // ============ SYSTEM COMMANDS ============
  public getSystemStatus(): void {
    this.sendCommand('get_system_status');
  }

  public changeBackend(backendType: 'ni-daqmx' | 'iotech' | 'demo'): void {
    this.sendCommand('change_backend', { backend_type: backendType });
  }

  public testConnection(channels?: number[]): void {
    this.sendCommand('test_connection', { test_channels: channels });
  }

  public resetSystem(): void {
    this.sendCommand('reset_system');
  }

  // ============ GESTION CONNEXION PUBLIQUE ============
  public isConnectedToBackend(): boolean {
    return this.isConnected;
  }

  public disconnect(): void {
    if (this.websocket) {
      this.websocket.close();
    }
    this.stopHeartbeat();
  }

  public reconnect(): void {
    this.disconnect();
    this.reconnectAttempts = 0;
    setTimeout(() => this.connect(), 1000);
  }

  // ============ NETTOYAGE ============
  public destroy(): void {
    this.disconnect();
    this.removeAllListeners();
    this.messageQueue = [];
  }
}

// ============ EXPORTS ============
export type {
  AcquisitionData,
  CalibrationUpdate,
  SystemStatus,
  SondeStatus,
  ErrorNotification,
  AcquisitionCommand,
  CalibrationCommand,
  SystemCommand
};
