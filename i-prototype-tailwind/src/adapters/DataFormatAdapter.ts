/**
 * 🔄 Data Format Adapter - CHNeoWave Integration
 * Adaptateur bidirectionnel Backend Python ↔ Frontend React
 * 
 * Selon prompt ultra-précis : Respecter contrats backend, adapter UI
 */

// ============ TYPES BACKEND (Python) ============
interface BackendSessionData {
  session_id: string;
  session_name: string;
  created_at: string;  // ISO datetime
  started_at?: string;
  completed_at?: string;
  experiment_type: 'wave_generation' | 'wave_propagation' | 'wave_breaking' | 
                   'ship_resistance' | 'ship_seakeeping' | 'offshore_structure' | 
                   'coastal_engineering' | 'free_surface_flow' | 'other';
  experiment_description: string;
  test_number?: string;
  operator: string;
  laboratory: string;
  project_name: string;
  sondes: BackendSensorData[];
  acquisition_settings?: BackendAcquisitionSettings;
  wave_conditions?: BackendWaveConditions;
  environmental_conditions?: BackendEnvironmentalConditions;
  data_files: string[];
  total_samples: number;
  file_size_bytes: number;
  data_quality_score?: number;  // 0-100
  validation_status: 'pending' | 'validated' | 'rejected';
  validation_notes: string;
  tags: string[];
  custom_fields: Record<string, any>;
  metadata_version: string;
  checksum?: string;
}

interface BackendSensorData {
  sonde_id: string;
  sensor_type: 'wave_height' | 'pressure' | 'accelerometer' | 'temperature' | 
               'flow_velocity' | 'force' | 'displacement' | 'strain' | 'generic';
  channel: number;
  position: { x: number; y: number; z: number };
  calibration?: BackendCalibrationData;
  unit: string;
  range_min: number;
  range_max: number;
}

interface BackendCalibrationData {
  slope: number;
  offset: number;
  r2: number;
  rmse: number;
  points: Array<{ reference: number; measured: number }>;
  calibration_date: string;
  calibration_status: 'pending' | 'in_progress' | 'completed' | 'failed';
}

interface BackendAcquisitionSettings {
  sampling_rate: number;  // Hz
  duration: number;       // seconds
  buffer_size: number;
  channels: number[];
  voltage_range: '±1V' | '±2V' | '±5V' | '±10V';
  trigger_mode: 'software' | 'hardware' | 'external';
  pre_trigger_samples: number;
}

interface BackendWaveConditions {
  wave_type: 'regular' | 'irregular' | 'focused' | 'breaking';
  significant_height: number;  // m
  peak_period: number;        // s
  direction: number;          // degrees
  spectrum_type: 'JONSWAP' | 'PIERSON_MOSKOWITZ' | 'BRETSCHNEIDER';
  gamma?: number;             // JONSWAP peak enhancement factor
}

interface BackendEnvironmentalConditions {
  water_temperature: number;  // °C
  air_temperature: number;    // °C
  humidity: number;           // %
  atmospheric_pressure: number; // hPa
  water_depth: number;        // m
  salinity?: number;          // ppt
}

// ============ TYPES UI (React) ============
interface UISessionData {
  id: string;
  name: string;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  type: 'wave_generation' | 'wave_propagation' | 'wave_breaking' | 
        'ship_resistance' | 'ship_seakeeping' | 'offshore_structure' | 
        'coastal_engineering' | 'free_surface_flow' | 'other';
  description: string;
  testNumber?: string;
  operator: string;
  laboratory: string;
  projectName: string;
  sondes: UISensorData[];
  config?: UIAcquisitionConfig;
  waveConditions?: UIWaveConditions;
  environmentalConditions?: UIEnvironmentalConditions;
  files: string[];
  samples: number;
  fileSize: number;
  qualityScore?: number;
  status: 'pending' | 'validated' | 'rejected';
  notes: string;
  tags: string[];
  customFields: Record<string, any>;
  version: string;
  checksum?: string;
}

interface UISensorData {
  id: string;
  type: 'wave_height' | 'pressure' | 'accelerometer' | 'temperature' | 
        'flow_velocity' | 'force' | 'displacement' | 'strain' | 'generic';
  channel: number;
  position: { x: number; y: number; z: number };
  calibration?: UICalibrationData;
  unit: string;
  rangeMin: number;
  rangeMax: number;
  // UI-specific properties
  isActive?: boolean;
  lastValue?: number;
  snr?: number;        // Signal-to-noise ratio
  saturation?: number; // Saturation percentage
}

interface UICalibrationData {
  slope: number;
  offset: number;
  r2: number;
  rmse: number;
  points: Array<{ reference: number; measured: number }>;
  date: Date;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
}

interface UIAcquisitionConfig {
  samplingRate: number;
  duration: number;
  bufferSize: number;
  channels: number[];
  voltageRange: '±1V' | '±2V' | '±5V' | '±10V';
  triggerMode: 'software' | 'hardware' | 'external';
  preTriggerSamples: number;
}

interface UIWaveConditions {
  type: 'regular' | 'irregular' | 'focused' | 'breaking';
  significantHeight: number;
  peakPeriod: number;
  direction: number;
  spectrumType: 'JONSWAP' | 'PIERSON_MOSKOWITZ' | 'BRETSCHNEIDER';
  gamma?: number;
}

interface UIEnvironmentalConditions {
  waterTemperature: number;
  airTemperature: number;
  humidity: number;
  atmosphericPressure: number;
  waterDepth: number;
  salinity?: number;
}

// ============ ADAPTATEUR PRINCIPAL ============
export class DataFormatAdapter {
  /**
   * Convertit les données Backend Python → Frontend React
   * RÈGLE: Respecter la vérité du logiciel, adapter l'UI
   */
  static toUIFormat(backendData: BackendSessionData): UISessionData {
    return {
      id: backendData.session_id,
      name: backendData.session_name,
      createdAt: new Date(backendData.created_at),
      startedAt: backendData.started_at ? new Date(backendData.started_at) : undefined,
      completedAt: backendData.completed_at ? new Date(backendData.completed_at) : undefined,
      type: backendData.experiment_type,
      description: backendData.experiment_description,
      testNumber: backendData.test_number,
      operator: backendData.operator,
      laboratory: backendData.laboratory,
      projectName: backendData.project_name,
      sondes: backendData.sondes.map(this.mapSensorToUI),
      config: backendData.acquisition_settings ? this.mapAcquisitionToUI(backendData.acquisition_settings) : undefined,
      waveConditions: backendData.wave_conditions ? this.mapWaveConditionsToUI(backendData.wave_conditions) : undefined,
      environmentalConditions: backendData.environmental_conditions ? this.mapEnvironmentalToUI(backendData.environmental_conditions) : undefined,
      files: backendData.data_files,
      samples: backendData.total_samples,
      fileSize: backendData.file_size_bytes,
      qualityScore: backendData.data_quality_score,
      status: backendData.validation_status,
      notes: backendData.validation_notes,
      tags: backendData.tags,
      customFields: backendData.custom_fields,
      version: backendData.metadata_version,
      checksum: backendData.checksum
    };
  }

  /**
   * Convertit les données Frontend React → Backend Python
   * RÈGLE: Préserver tous les champs requis par le backend
   */
  static toBackendFormat(uiData: UISessionData): BackendSessionData {
    return {
      session_id: uiData.id,
      session_name: uiData.name,
      created_at: uiData.createdAt.toISOString(),
      started_at: uiData.startedAt?.toISOString(),
      completed_at: uiData.completedAt?.toISOString(),
      experiment_type: uiData.type,
      experiment_description: uiData.description,
      test_number: uiData.testNumber,
      operator: uiData.operator,
      laboratory: uiData.laboratory,
      project_name: uiData.projectName,
      sondes: uiData.sondes.map(this.mapSensorToBackend),
      acquisition_settings: uiData.config ? this.mapAcquisitionToBackend(uiData.config) : undefined,
      wave_conditions: uiData.waveConditions ? this.mapWaveConditionsToBackend(uiData.waveConditions) : undefined,
      environmental_conditions: uiData.environmentalConditions ? this.mapEnvironmentalToBackend(uiData.environmentalConditions) : undefined,
      data_files: uiData.files,
      total_samples: uiData.samples,
      file_size_bytes: uiData.fileSize,
      data_quality_score: uiData.qualityScore,
      validation_status: uiData.status,
      validation_notes: uiData.notes,
      tags: uiData.tags,
      custom_fields: uiData.customFields,
      metadata_version: uiData.version,
      checksum: uiData.checksum
    };
  }

  // ============ MAPPERS SPÉCIALISÉS ============
  private static mapSensorToUI(backendSensor: BackendSensorData): UISensorData {
    return {
      id: backendSensor.sonde_id,
      type: backendSensor.sensor_type,
      channel: backendSensor.channel,
      position: backendSensor.position,
      calibration: backendSensor.calibration ? {
        slope: backendSensor.calibration.slope,
        offset: backendSensor.calibration.offset,
        r2: backendSensor.calibration.r2,
        rmse: backendSensor.calibration.rmse,
        points: backendSensor.calibration.points,
        date: new Date(backendSensor.calibration.calibration_date),
        status: backendSensor.calibration.calibration_status
      } : undefined,
      unit: backendSensor.unit,
      rangeMin: backendSensor.range_min,
      rangeMax: backendSensor.range_max,
      // UI-specific defaults
      isActive: true,
      lastValue: 0,
      snr: 25,
      saturation: 0
    };
  }

  private static mapSensorToBackend(uiSensor: UISensorData): BackendSensorData {
    return {
      sonde_id: uiSensor.id,
      sensor_type: uiSensor.type,
      channel: uiSensor.channel,
      position: uiSensor.position,
      calibration: uiSensor.calibration ? {
        slope: uiSensor.calibration.slope,
        offset: uiSensor.calibration.offset,
        r2: uiSensor.calibration.r2,
        rmse: uiSensor.calibration.rmse,
        points: uiSensor.calibration.points,
        calibration_date: uiSensor.calibration.date.toISOString(),
        calibration_status: uiSensor.calibration.status
      } : undefined,
      unit: uiSensor.unit,
      range_min: uiSensor.rangeMin,
      range_max: uiSensor.rangeMax
    };
  }

  private static mapAcquisitionToUI(backend: BackendAcquisitionSettings): UIAcquisitionConfig {
    return {
      samplingRate: backend.sampling_rate,
      duration: backend.duration,
      bufferSize: backend.buffer_size,
      channels: backend.channels,
      voltageRange: backend.voltage_range,
      triggerMode: backend.trigger_mode,
      preTriggerSamples: backend.pre_trigger_samples
    };
  }

  private static mapAcquisitionToBackend(ui: UIAcquisitionConfig): BackendAcquisitionSettings {
    return {
      sampling_rate: ui.samplingRate,
      duration: ui.duration,
      buffer_size: ui.bufferSize,
      channels: ui.channels,
      voltage_range: ui.voltageRange,
      trigger_mode: ui.triggerMode,
      pre_trigger_samples: ui.preTriggerSamples
    };
  }

  private static mapWaveConditionsToUI(backend: BackendWaveConditions): UIWaveConditions {
    return {
      type: backend.wave_type,
      significantHeight: backend.significant_height,
      peakPeriod: backend.peak_period,
      direction: backend.direction,
      spectrumType: backend.spectrum_type,
      gamma: backend.gamma
    };
  }

  private static mapWaveConditionsToBackend(ui: UIWaveConditions): BackendWaveConditions {
    return {
      wave_type: ui.type,
      significant_height: ui.significantHeight,
      peak_period: ui.peakPeriod,
      direction: ui.direction,
      spectrum_type: ui.spectrumType,
      gamma: ui.gamma
    };
  }

  private static mapEnvironmentalToUI(backend: BackendEnvironmentalConditions): UIEnvironmentalConditions {
    return {
      waterTemperature: backend.water_temperature,
      airTemperature: backend.air_temperature,
      humidity: backend.humidity,
      atmosphericPressure: backend.atmospheric_pressure,
      waterDepth: backend.water_depth,
      salinity: backend.salinity
    };
  }

  private static mapEnvironmentalToBackend(ui: UIEnvironmentalConditions): BackendEnvironmentalConditions {
    return {
      water_temperature: ui.waterTemperature,
      air_temperature: ui.airTemperature,
      humidity: ui.humidity,
      atmospheric_pressure: ui.atmosphericPressure,
      water_depth: ui.waterDepth,
      salinity: ui.salinity
    };
  }

  // ============ UTILITAIRES DE VALIDATION ============
  static validateBackendData(data: any): data is BackendSessionData {
    return (
      typeof data === 'object' &&
      typeof data.session_id === 'string' &&
      typeof data.session_name === 'string' &&
      typeof data.created_at === 'string' &&
      typeof data.experiment_type === 'string' &&
      Array.isArray(data.sondes) &&
      Array.isArray(data.data_files) &&
      typeof data.total_samples === 'number' &&
      typeof data.validation_status === 'string'
    );
  }

  static validateUIData(data: any): data is UISessionData {
    return (
      typeof data === 'object' &&
      typeof data.id === 'string' &&
      typeof data.name === 'string' &&
      data.createdAt instanceof Date &&
      typeof data.type === 'string' &&
      Array.isArray(data.sondes) &&
      Array.isArray(data.files) &&
      typeof data.samples === 'number'
    );
  }
}

// ============ EXPORTS ============
export type {
  BackendSessionData,
  BackendSensorData,
  BackendCalibrationData,
  BackendAcquisitionSettings,
  BackendWaveConditions,
  BackendEnvironmentalConditions,
  UISessionData,
  UISensorData,
  UICalibrationData,
  UIAcquisitionConfig,
  UIWaveConditions,
  UIEnvironmentalConditions
};
