/**
 * 🌐 CHNeoWave API Client - Backend Integration
 * Client API unifié selon prompt ultra-précis
 * 
 * Respecte la vérité du logiciel : endpoints backend prioritaires
 */

import { DataFormatAdapter, BackendSessionData, UISessionData, UIAcquisitionConfig, UISensorData } from '../adapters/DataFormatAdapter';

// ============ TYPES DE REQUÊTES ============
interface CreateProjectRequest {
  name: string;
  description: string;
  operator: string;
  laboratory: string;
  experiment_type: string;
  tags?: string[];
}

interface AcquisitionConfigRequest {
  sampling_rate: number;
  duration: number;
  channels: number[];
  voltage_range: string;
  buffer_size: number;
  trigger_mode?: string;
}

interface CalibrationPointRequest {
  sonde_id: string;
  reference_value: number;
  measured_value: number;
}

interface ExportRequest {
  session_id: string;
  format: 'hdf5' | 'csv' | 'json' | 'matlab';
  include_metadata: boolean;
  compression?: boolean;
}

// ============ TYPES DE RÉPONSES ============
interface AcquisitionStatus {
  status: 'idle' | 'running' | 'paused' | 'stopped' | 'error';
  sampling_rate: number;
  duration_elapsed: number;
  samples_acquired: number;
  channels_active: number[];
  last_error?: string;
}

interface CalibrationResult {
  sonde_id: string;
  slope: number;
  offset: number;
  r2: number;
  rmse: number;
  points_count: number;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
}

interface SystemInfo {
  backend_type: 'ni-daqmx' | 'iotech' | 'demo';
  hardware_connected: boolean;
  sensors_detected: number;
  version: string;
  uptime_seconds: number;
  memory_usage_mb: number;
  cpu_usage_percent: number;
}

interface ExportResult {
  export_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  file_path?: string;
  file_size_bytes?: number;
  download_url?: string;
  error_message?: string;
}

// ============ ERREURS API ============
class CHNeoWaveAPIError extends Error {
  constructor(
    message: string,
    public status: number,
    public endpoint: string,
    public details?: any
  ) {
    super(message);
    this.name = 'CHNeoWaveAPIError';
  }
}

// ============ CLIENT API PRINCIPAL ============
export class CHNeoWaveAPI {
  private baseUrl: string;
  private timeout: number;
  private retryAttempts: number;
  private retryDelay: number;

  constructor(
    baseUrl: string = 'http://localhost:8000/api',
    options: {
      timeout?: number;
      retryAttempts?: number;
      retryDelay?: number;
    } = {}
  ) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Supprimer le slash final
    this.timeout = options.timeout || 30000; // 30 secondes
    this.retryAttempts = options.retryAttempts || 3;
    this.retryDelay = options.retryDelay || 1000; // 1 seconde
  }

  // ============ MÉTHODES HTTP GÉNÉRIQUES ============
  private async request<T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    endpoint: string,
    data?: any,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers
      },
      signal: AbortSignal.timeout(this.timeout),
      ...options
    };

    if (data && (method === 'POST' || method === 'PUT')) {
      config.body = JSON.stringify(data);
    }

    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= this.retryAttempts; attempt++) {
      try {
        const response = await fetch(url, config);

        if (!response.ok) {
          const errorText = await response.text();
          let errorData;
          try {
            errorData = JSON.parse(errorText);
          } catch {
            errorData = { message: errorText };
          }

          throw new CHNeoWaveAPIError(
            errorData.message || `HTTP ${response.status}: ${response.statusText}`,
            response.status,
            endpoint,
            errorData
          );
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          return await response.json();
        } else {
          return await response.text() as unknown as T;
        }

      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        
        // Ne pas retry sur les erreurs 4xx (erreurs client)
        if (error instanceof CHNeoWaveAPIError && error.status >= 400 && error.status < 500) {
          break;
        }

        // Attendre avant le prochain essai
        if (attempt < this.retryAttempts) {
          await new Promise(resolve => setTimeout(resolve, this.retryDelay * (attempt + 1)));
        }
      }
    }

    throw lastError;
  }

  private async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>('GET', endpoint, undefined, options);
  }

  private async post<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>('POST', endpoint, data, options);
  }

  private async put<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>('PUT', endpoint, data, options);
  }

  private async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>('DELETE', endpoint, undefined, options);
  }

  // ============ ENDPOINTS - ACQUISITION ============
  async startAcquisition(config: UIAcquisitionConfig): Promise<void> {
    const backendConfig: AcquisitionConfigRequest = {
      sampling_rate: config.samplingRate,
      duration: config.duration,
      channels: config.channels,
      voltage_range: config.voltageRange,
      buffer_size: config.bufferSize,
      trigger_mode: config.triggerMode
    };

    await this.post('/acquisition/start', backendConfig);
  }

  async stopAcquisition(): Promise<void> {
    await this.post('/acquisition/stop');
  }

  async pauseAcquisition(): Promise<void> {
    await this.post('/acquisition/pause');
  }

  async resumeAcquisition(): Promise<void> {
    await this.post('/acquisition/resume');
  }

  async getAcquisitionStatus(): Promise<AcquisitionStatus> {
    return await this.get<AcquisitionStatus>('/acquisition/status');
  }

  async getRealtimeData(): Promise<any> {
    return await this.get('/acquisition/data/realtime');
  }

  async setAcquisitionConfig(config: UIAcquisitionConfig): Promise<void> {
    const backendConfig: AcquisitionConfigRequest = {
      sampling_rate: config.samplingRate,
      duration: config.duration,
      channels: config.channels,
      voltage_range: config.voltageRange,
      buffer_size: config.bufferSize,
      trigger_mode: config.triggerMode
    };

    await this.post('/acquisition/config', backendConfig);
  }

  // ============ ENDPOINTS - CALIBRATION ============
  async startCalibration(sondeId: string): Promise<void> {
    await this.post(`/calibration/start/${sondeId}`);
  }

  async stopCalibration(sondeId: string): Promise<void> {
    await this.post(`/calibration/stop/${sondeId}`);
  }

  async addCalibrationPoint(sondeId: string, referenceValue: number, measuredValue: number): Promise<void> {
    const point: CalibrationPointRequest = {
      sonde_id: sondeId,
      reference_value: referenceValue,
      measured_value: measuredValue
    };

    await this.post('/calibration/point', point);
  }

  async calculateCalibration(sondeId: string): Promise<CalibrationResult> {
    return await this.post<CalibrationResult>(`/calibration/calculate/${sondeId}`);
  }

  async getCalibrationStatus(sondeId: string): Promise<CalibrationResult> {
    return await this.get<CalibrationResult>(`/calibration/status/${sondeId}`);
  }

  async getCalibrationResults(sondeId: string): Promise<CalibrationResult> {
    return await this.get<CalibrationResult>(`/calibration/results/${sondeId}`);
  }

  // ============ ENDPOINTS - PROJETS/SESSIONS ============
  async getProjects(): Promise<UISessionData[]> {
    const backendProjects = await this.get<BackendSessionData[]>('/projects');
    return backendProjects.map(project => DataFormatAdapter.toUIFormat(project));
  }

  async createProject(projectData: CreateProjectRequest): Promise<UISessionData> {
    const backendProject = await this.post<BackendSessionData>('/projects', projectData);
    return DataFormatAdapter.toUIFormat(backendProject);
  }

  async getProject(projectId: string): Promise<UISessionData> {
    const backendProject = await this.get<BackendSessionData>(`/projects/${projectId}`);
    return DataFormatAdapter.toUIFormat(backendProject);
  }

  async updateProject(projectId: string, updates: Partial<UISessionData>): Promise<UISessionData> {
    const backendUpdates = DataFormatAdapter.toBackendFormat(updates as UISessionData);
    const backendProject = await this.put<BackendSessionData>(`/projects/${projectId}`, backendUpdates);
    return DataFormatAdapter.toUIFormat(backendProject);
  }

  async deleteProject(projectId: string): Promise<void> {
    await this.delete(`/projects/${projectId}`);
  }

  async getProjectSessions(projectId: string): Promise<UISessionData[]> {
    const backendSessions = await this.get<BackendSessionData[]>(`/projects/${projectId}/sessions`);
    return backendSessions.map(session => DataFormatAdapter.toUIFormat(session));
  }

  // ============ ENDPOINTS - EXPORT ============
  async exportToHDF5(sessionId: string, options: { includeMetadata?: boolean; compression?: boolean } = {}): Promise<ExportResult> {
    const request: ExportRequest = {
      session_id: sessionId,
      format: 'hdf5',
      include_metadata: options.includeMetadata ?? true,
      compression: options.compression ?? true
    };

    return await this.post<ExportResult>('/export/hdf5', request);
  }

  async exportToCSV(sessionId: string, options: { includeMetadata?: boolean } = {}): Promise<ExportResult> {
    const request: ExportRequest = {
      session_id: sessionId,
      format: 'csv',
      include_metadata: options.includeMetadata ?? true
    };

    return await this.post<ExportResult>('/export/csv', request);
  }

  async exportToJSON(sessionId: string, options: { includeMetadata?: boolean } = {}): Promise<ExportResult> {
    const request: ExportRequest = {
      session_id: sessionId,
      format: 'json',
      include_metadata: options.includeMetadata ?? true
    };

    return await this.post<ExportResult>('/export/json', request);
  }

  async exportToMatlab(sessionId: string, options: { includeMetadata?: boolean } = {}): Promise<ExportResult> {
    const request: ExportRequest = {
      session_id: sessionId,
      format: 'matlab',
      include_metadata: options.includeMetadata ?? true
    };

    return await this.post<ExportResult>('/export/matlab', request);
  }

  async getExportStatus(exportId: string): Promise<ExportResult> {
    return await this.get<ExportResult>(`/export/status/${exportId}`);
  }

  async downloadExport(exportId: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/export/download/${exportId}`, {
      method: 'GET',
      signal: AbortSignal.timeout(this.timeout)
    });

    if (!response.ok) {
      throw new CHNeoWaveAPIError(
        `Download failed: ${response.statusText}`,
        response.status,
        `/export/download/${exportId}`
      );
    }

    return await response.blob();
  }

  // ============ ENDPOINTS - SYSTÈME ============
  async getSystemInfo(): Promise<SystemInfo> {
    return await this.get<SystemInfo>('/system/info');
  }

  async getSystemStatus(): Promise<SystemInfo> {
    return await this.get<SystemInfo>('/system/status');
  }

  async changeBackend(backendType: 'ni-daqmx' | 'iotech' | 'demo'): Promise<void> {
    await this.post('/system/backend', { backend_type: backendType });
  }

  async testConnection(channels?: number[]): Promise<{ success: boolean; message: string; details?: any }> {
    return await this.post('/system/test', { channels });
  }

  async resetSystem(): Promise<void> {
    await this.post('/system/reset');
  }

  // ============ ENDPOINTS - SONDES ============
  async getSensors(): Promise<UISensorData[]> {
    const backendSensors = await this.get<any[]>('/sondes');
    return backendSensors.map(sonde => ({
      id: sonde.sonde_id,
      type: sonde.sensor_type,
      channel: sonde.channel,
      position: sonde.position,
      calibration: sonde.calibration ? {
        slope: sonde.calibration.slope,
        offset: sonde.calibration.offset,
        r2: sonde.calibration.r2,
        rmse: sonde.calibration.rmse,
        points: sonde.calibration.points,
        date: new Date(sonde.calibration.calibration_date),
        status: sonde.calibration.calibration_status
      } : undefined,
      unit: sonde.unit,
      rangeMin: sonde.range_min,
      rangeMax: sonde.range_max,
      isActive: sonde.is_active || true,
      lastValue: sonde.last_value || 0,
      snr: sonde.snr_db || 25,
      saturation: sonde.saturation_percent ? sonde.saturation_percent / 100 : 0
    }));
  }

  async updateSensorConfig(sondeId: string, config: Partial<UISensorData>): Promise<void> {
    const backendConfig = {
      sonde_id: sondeId,
      sensor_type: config.type,
      channel: config.channel,
      position: config.position,
      unit: config.unit,
      range_min: config.rangeMin,
      range_max: config.rangeMax,
      is_active: config.isActive
    };

    await this.put(`/sondes/${sondeId}`, backendConfig);
  }

  // ============ UTILITAIRES ============
  async ping(): Promise<{ status: string; timestamp: number }> {
    return await this.get('/ping');
  }

  async getVersion(): Promise<{ version: string; build: string; timestamp: string }> {
    return await this.get('/version');
  }

  // Configuration de l'instance
  setBaseUrl(baseUrl: string): void {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  setTimeout(timeout: number): void {
    this.timeout = timeout;
  }

  setRetryConfig(attempts: number, delay: number): void {
    this.retryAttempts = attempts;
    this.retryDelay = delay;
  }
}

// ============ INSTANCE SINGLETON ============
export const api = new CHNeoWaveAPI();

// ============ EXPORTS ============
export type {
  CreateProjectRequest,
  AcquisitionConfigRequest,
  CalibrationPointRequest,
  ExportRequest,
  AcquisitionStatus,
  CalibrationResult,
  SystemInfo,
  ExportResult
};

export { CHNeoWaveAPIError };
