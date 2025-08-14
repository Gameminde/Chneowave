/**
 * 🔄 Formatage Unités Scientifiques - Phase 2 Catégorie D  
 * Selon prompt ultra-précis : Respecter unités métier existantes (m, Hz, V)
 * 
 * Unifier vers les unités scientifiques du backend CHNeoWave
 */

// Unités conformes aux standards ITTC et backend CHNeoWave
export enum ScientificUnit {
  // Unités de longueur/hauteur
  METER = 'm',
  CENTIMETER = 'cm', 
  MILLIMETER = 'mm',
  
  // Unités de fréquence
  HERTZ = 'Hz',
  KILOHERTZ = 'kHz',
  
  // Unités électriques
  VOLT = 'V',
  MILLIVOLT = 'mV',
  AMPERE = 'A',
  MILLIAMPERE = 'mA',
  
  // Unités de temps
  SECOND = 's',
  MILLISECOND = 'ms',
  MINUTE = 'min',
  HOUR = 'h',
  
  // Unités de pression
  PASCAL = 'Pa',
  HECTOPASCAL = 'hPa',
  KILOPASCAL = 'kPa',
  
  // Unités d'angle
  DEGREE = '°',
  RADIAN = 'rad',
  
  // Unités de données
  BYTE = 'B',
  KILOBYTE = 'KB',
  MEGABYTE = 'MB',
  GIGABYTE = 'GB',
  
  // Unités sans dimension
  DIMENSIONLESS = '',
  PERCENT = '%',
  DECIBEL = 'dB',
  
  // Unités composées maritimes
  METER_PER_SECOND = 'm/s',
  METER_PER_SECOND_SQUARED = 'm/s²',
  NEWTON = 'N',
  JOULE = 'J'
}

// Configuration des capteurs selon le backend CHNeoWave
export const SensorUnitsConfig = {
  wave_height: {
    primary: ScientificUnit.METER,
    precision: 3,
    range: { min: -5.0, max: 5.0 },
    description: 'Élévation de surface libre'
  },
  pressure: {
    primary: ScientificUnit.PASCAL,
    precision: 1,
    range: { min: 0, max: 100000 },
    description: 'Pression hydrostatique'
  },
  accelerometer: {
    primary: ScientificUnit.METER_PER_SECOND_SQUARED,
    precision: 2,
    range: { min: -20.0, max: 20.0 },
    description: 'Accélération'
  },
  temperature: {
    primary: ScientificUnit.DEGREE,
    precision: 1,
    range: { min: -10.0, max: 50.0 },
    description: 'Température de l\'eau'
  },
  flow_velocity: {
    primary: ScientificUnit.METER_PER_SECOND,
    precision: 2,
    range: { min: 0, max: 10.0 },
    description: 'Vitesse d\'écoulement'
  },
  force: {
    primary: ScientificUnit.NEWTON,
    precision: 1,
    range: { min: 0, max: 1000.0 },
    description: 'Force appliquée'
  },
  displacement: {
    primary: ScientificUnit.METER,
    precision: 4,
    range: { min: -1.0, max: 1.0 },
    description: 'Déplacement'
  },
  strain: {
    primary: ScientificUnit.DIMENSIONLESS,
    precision: 6,
    range: { min: -0.001, max: 0.001 },
    description: 'Déformation'
  },
  generic: {
    primary: ScientificUnit.VOLT,
    precision: 3,
    range: { min: -10.0, max: 10.0 },
    description: 'Signal générique'
  }
};

export class UnitsFormatter {
  /**
   * Formate une valeur avec son unité scientifique
   */
  static formatValue(
    value: number, 
    unit: ScientificUnit, 
    precision: number = 2,
    showUnit: boolean = true
  ): string {
    if (!isFinite(value)) {
      return showUnit ? `-- ${unit}` : '--';
    }

    const formattedValue = value.toFixed(precision);
    return showUnit ? `${formattedValue} ${unit}` : formattedValue;
  }

  /**
   * Formate une valeur de capteur selon sa configuration
   */
  static formatSensorValue(
    value: number,
    sensorType: keyof typeof SensorUnitsConfig,
    showUnit: boolean = true
  ): string {
    const config = SensorUnitsConfig[sensorType];
    if (!config) {
      return this.formatValue(value, ScientificUnit.VOLT, 3, showUnit);
    }

    return this.formatValue(value, config.primary, config.precision, showUnit);
  }

  /**
   * Formate une fréquence d'échantillonnage
   */
  static formatSamplingRate(frequency: number): string {
    if (frequency >= 1000) {
      return this.formatValue(frequency / 1000, ScientificUnit.KILOHERTZ, 1);
    }
    return this.formatValue(frequency, ScientificUnit.HERTZ, 0);
  }

  /**
   * Formate une durée en format approprié
   */
  static formatDuration(seconds: number): string {
    if (seconds < 60) {
      return this.formatValue(seconds, ScientificUnit.SECOND, 1);
    } else if (seconds < 3600) {
      const minutes = seconds / 60;
      return this.formatValue(minutes, ScientificUnit.MINUTE, 1);
    } else {
      const hours = seconds / 3600;
      return this.formatValue(hours, ScientificUnit.HOUR, 2);
    }
  }

  /**
   * Formate une taille de fichier
   */
  static formatFileSize(bytes: number): string {
    if (bytes < 1024) {
      return this.formatValue(bytes, ScientificUnit.BYTE, 0);
    } else if (bytes < 1024 * 1024) {
      return this.formatValue(bytes / 1024, ScientificUnit.KILOBYTE, 1);
    } else if (bytes < 1024 * 1024 * 1024) {
      return this.formatValue(bytes / (1024 * 1024), ScientificUnit.MEGABYTE, 1);
    } else {
      return this.formatValue(bytes / (1024 * 1024 * 1024), ScientificUnit.GIGABYTE, 2);
    }
  }

  /**
   * Formate un pourcentage
   */
  static formatPercentage(value: number, precision: number = 1): string {
    return this.formatValue(value * 100, ScientificUnit.PERCENT, precision);
  }

  /**
   * Formate un rapport signal/bruit
   */
  static formatSNR(snr: number): string {
    return this.formatValue(snr, ScientificUnit.DECIBEL, 1);
  }

  /**
   * Formate un angle
   */
  static formatAngle(degrees: number): string {
    return this.formatValue(degrees, ScientificUnit.DEGREE, 1);
  }

  /**
   * Formate une tension électrique
   */
  static formatVoltage(voltage: number): string {
    if (Math.abs(voltage) < 1.0) {
      return this.formatValue(voltage * 1000, ScientificUnit.MILLIVOLT, 1);
    }
    return this.formatValue(voltage, ScientificUnit.VOLT, 3);
  }

  /**
   * Valide qu'une valeur est dans la plage du capteur
   */
  static isValueInRange(
    value: number, 
    sensorType: keyof typeof SensorUnitsConfig
  ): boolean {
    const config = SensorUnitsConfig[sensorType];
    if (!config || !config.range) return true;

    return value >= config.range.min && value <= config.range.max;
  }

  /**
   * Obtient la description d'un type de capteur
   */
  static getSensorDescription(sensorType: keyof typeof SensorUnitsConfig): string {
    const config = SensorUnitsConfig[sensorType];
    return config?.description || 'Capteur générique';
  }

  /**
   * Obtient l'unité principale d'un type de capteur
   */
  static getSensorUnit(sensorType: keyof typeof SensorUnitsConfig): ScientificUnit {
    const config = SensorUnitsConfig[sensorType];
    return config?.primary || ScientificUnit.VOLT;
  }

  /**
   * Convertit une valeur générique vers l'unité scientifique appropriée
   */
  static normalizeToScientific(
    value: number,
    fromUnit: string,
    targetSensorType: keyof typeof SensorUnitsConfig
  ): number {
    // Facteurs de conversion courants
    const conversions: Record<string, Record<string, number>> = {
      // Longueur vers mètres
      'cm': { [ScientificUnit.METER]: 0.01 },
      'mm': { [ScientificUnit.METER]: 0.001 },
      
      // Fréquence vers Hz
      'kHz': { [ScientificUnit.HERTZ]: 1000 },
      
      // Tension vers Volts
      'mV': { [ScientificUnit.VOLT]: 0.001 },
      
      // Temps vers secondes
      'ms': { [ScientificUnit.SECOND]: 0.001 },
      'min': { [ScientificUnit.SECOND]: 60 },
      'h': { [ScientificUnit.SECOND]: 3600 }
    };

    const targetUnit = this.getSensorUnit(targetSensorType);
    const conversionFactor = conversions[fromUnit]?.[targetUnit];
    
    return conversionFactor ? value * conversionFactor : value;
  }
}

// Constantes pour validation ITTC
export const ITTCStandards = {
  samplingRate: {
    min: 32, // Hz
    max: 1000, // Hz
    recommended: [50, 100, 200, 500, 1000]
  },
  waveHeight: {
    min: -5.0, // m
    max: 5.0,  // m
    precision: 0.001 // mm
  },
  duration: {
    min: 60,    // s (1 minute minimum)
    max: 3600,  // s (1 heure maximum)
    recommended: [300, 600, 1200, 1800] // 5, 10, 20, 30 minutes
  }
};

export default UnitsFormatter;
