/**
 * ⚡ Optimisations Performance - Phase 3.2
 * Selon prompt ultra-précis : éviter re-renders, mémoïsation graphes, 60fps, workers FFT
 * 
 * Système d'optimisation performance pour CHNeoWave
 */

import { useMemo, useCallback, useRef, useEffect, useState } from 'react';

// ============ HOOKS D'OPTIMISATION REACT ============

/**
 * Hook pour mémoïsation stable des callbacks
 */
export function useStableCallback<T extends (...args: any[]) => any>(callback: T): T {
  const callbackRef = useRef(callback);
  
  // Mettre à jour la référence sans changer l'identité
  useEffect(() => {
    callbackRef.current = callback;
  });
  
  // Retourner un callback stable
  return useCallback((...args: any[]) => {
    return callbackRef.current(...args);
  }, []) as T;
}

/**
 * Hook pour mémoïsation des données de graphiques
 */
export function useOptimizedChartData<T>(
  rawData: T[],
  maxPoints: number = 1000,
  sampleStrategy: 'latest' | 'uniform' | 'adaptive' = 'adaptive'
) {
  return useMemo(() => {
    if (rawData.length <= maxPoints) return rawData;

    switch (sampleStrategy) {
      case 'latest':
        // Garder les derniers points (pour données temps réel)
        return rawData.slice(-maxPoints);
      
      case 'uniform':
        // Échantillonnage uniforme
        const step = Math.ceil(rawData.length / maxPoints);
        return rawData.filter((_, index) => index % step === 0);
      
      case 'adaptive':
        // Échantillonnage adaptatif (plus de points récents)
        const recent = rawData.slice(-Math.floor(maxPoints * 0.7));
        const historical = rawData.slice(0, -Math.floor(maxPoints * 0.7));
        const historicalStep = Math.ceil(historical.length / Math.floor(maxPoints * 0.3));
        const sampledHistorical = historical.filter((_, index) => index % historicalStep === 0);
        
        return [...sampledHistorical, ...recent];
      
      default:
        return rawData.slice(-maxPoints);
    }
  }, [rawData, maxPoints, sampleStrategy]);
}

/**
 * Hook pour virtualisation de listes longues
 */
export function useVirtualizedList<T>(
  items: T[],
  containerHeight: number,
  itemHeight: number,
  buffer: number = 5
) {
  const [scrollTop, setScrollTop] = useState(0);
  
  return useMemo(() => {
    const visibleCount = Math.ceil(containerHeight / itemHeight);
    const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - buffer);
    const endIndex = Math.min(items.length - 1, startIndex + visibleCount + buffer * 2);
    
    const visibleItems = items.slice(startIndex, endIndex + 1).map((item, index) => ({
      item,
      index: startIndex + index,
      style: {
        position: 'absolute' as const,
        top: (startIndex + index) * itemHeight,
        height: itemHeight,
        width: '100%'
      }
    }));
    
    return {
      visibleItems,
      totalHeight: items.length * itemHeight,
      setScrollTop
    };
  }, [items, containerHeight, itemHeight, scrollTop, buffer]);
}

/**
 * Hook pour debouncing des mises à jour fréquentes
 */
export function useDebounced<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook pour throttling des événements haute fréquence
 */
export function useThrottled<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): T {
  const lastRun = useRef(Date.now());
  
  return useCallback((...args: any[]) => {
    if (Date.now() - lastRun.current >= delay) {
      callback(...args);
      lastRun.current = Date.now();
    }
  }, [callback, delay]) as T;
}

// ============ OPTIMISATIONS GRAPHIQUES ============

/**
 * Gestionnaire de performance pour graphiques temps réel
 */
export class ChartPerformanceManager {
  private frameId: number | null = null;
  private lastFrameTime = 0;
  private targetFPS = 60;
  private frameInterval: number;
  private updateQueue: (() => void)[] = [];

  constructor(targetFPS: number = 60) {
    this.targetFPS = targetFPS;
    this.frameInterval = 1000 / targetFPS;
  }

  /**
   * Programmer une mise à jour de graphique
   */
  scheduleUpdate(updateFn: () => void) {
    this.updateQueue.push(updateFn);
    
    if (!this.frameId) {
      this.frameId = requestAnimationFrame(this.processUpdates.bind(this));
    }
  }

  /**
   * Traiter les mises à jour en respectant le framerate
   */
  private processUpdates = (currentTime: number) => {
    const elapsed = currentTime - this.lastFrameTime;
    
    if (elapsed >= this.frameInterval) {
      // Traiter toutes les mises à jour en attente
      while (this.updateQueue.length > 0) {
        const updateFn = this.updateQueue.shift();
        updateFn?.();
      }
      
      this.lastFrameTime = currentTime;
    }
    
    // Programmer la prochaine frame si nécessaire
    if (this.updateQueue.length > 0) {
      this.frameId = requestAnimationFrame(this.processUpdates.bind(this));
    } else {
      this.frameId = null;
    }
  };

  /**
   * Arrêter le gestionnaire
   */
  stop() {
    if (this.frameId) {
      cancelAnimationFrame(this.frameId);
      this.frameId = null;
    }
    this.updateQueue = [];
  }
}

/**
 * Hook pour gestionnaire de performance graphique
 */
export function useChartPerformance(targetFPS: number = 60) {
  const managerRef = useRef<ChartPerformanceManager | null>(null);
  
  useEffect(() => {
    managerRef.current = new ChartPerformanceManager(targetFPS);
    
    return () => {
      managerRef.current?.stop();
    };
  }, [targetFPS]);
  
  const scheduleUpdate = useCallback((updateFn: () => void) => {
    managerRef.current?.scheduleUpdate(updateFn);
  }, []);
  
  return { scheduleUpdate };
}

// ============ WEB WORKERS POUR FFT ============

/**
 * Configuration pour Web Worker FFT
 */
interface FFTWorkerConfig {
  sampleRate: number;
  windowSize: number;
  overlap: number;
  windowFunction: 'hanning' | 'hamming' | 'blackman';
}

/**
 * Gestionnaire Web Worker pour calculs FFT lourds
 */
export class FFTWorkerManager {
  private worker: Worker | null = null;
  private workerPromises = new Map<number, { resolve: Function; reject: Function }>();
  private requestId = 0;

  constructor() {
    this.initWorker();
  }

  /**
   * Initialiser le Web Worker
   */
  private initWorker() {
    // Code du worker inline pour éviter les fichiers séparés
    const workerCode = `
      // FFT Worker pour calculs lourds côté UI
      class FFTProcessor {
        constructor() {
          this.sampleRate = 1000;
          this.windowSize = 1024;
        }

        // FFT simplifiée (en production, utiliser une librairie optimisée)
        computeFFT(samples, config) {
          const { sampleRate, windowSize, windowFunction } = config;
          
          // Appliquer la fenêtre
          const windowed = this.applyWindow(samples, windowFunction);
          
          // FFT simplifiée (placeholder - utiliser ml-fft en production)
          const frequencies = [];
          const magnitudes = [];
          
          for (let k = 0; k < windowSize / 2; k++) {
            const freq = (k * sampleRate) / windowSize;
            frequencies.push(freq);
            
            // Calcul simplifié de magnitude
            let real = 0, imag = 0;
            for (let n = 0; n < windowed.length; n++) {
              const angle = -2 * Math.PI * k * n / windowSize;
              real += windowed[n] * Math.cos(angle);
              imag += windowed[n] * Math.sin(angle);
            }
            
            magnitudes.push(Math.sqrt(real * real + imag * imag));
          }
          
          return {
            frequencies,
            magnitudes,
            peakFrequency: this.findPeakFrequency(frequencies, magnitudes)
          };
        }

        applyWindow(samples, windowFunction) {
          const windowed = new Array(samples.length);
          
          for (let i = 0; i < samples.length; i++) {
            let windowValue = 1;
            
            switch (windowFunction) {
              case 'hanning':
                windowValue = 0.5 - 0.5 * Math.cos(2 * Math.PI * i / (samples.length - 1));
                break;
              case 'hamming':
                windowValue = 0.54 - 0.46 * Math.cos(2 * Math.PI * i / (samples.length - 1));
                break;
              case 'blackman':
                windowValue = 0.42 - 0.5 * Math.cos(2 * Math.PI * i / (samples.length - 1)) + 
                             0.08 * Math.cos(4 * Math.PI * i / (samples.length - 1));
                break;
            }
            
            windowed[i] = samples[i] * windowValue;
          }
          
          return windowed;
        }

        findPeakFrequency(frequencies, magnitudes) {
          let maxMagnitude = 0;
          let peakFreq = 0;
          
          for (let i = 0; i < magnitudes.length; i++) {
            if (magnitudes[i] > maxMagnitude) {
              maxMagnitude = magnitudes[i];
              peakFreq = frequencies[i];
            }
          }
          
          return peakFreq;
        }
      }

      const processor = new FFTProcessor();

      self.onmessage = function(e) {
        const { id, samples, config } = e.data;
        
        try {
          const result = processor.computeFFT(samples, config);
          self.postMessage({ id, result });
        } catch (error) {
          self.postMessage({ id, error: error.message });
        }
      };
    `;

    const blob = new Blob([workerCode], { type: 'application/javascript' });
    this.worker = new Worker(URL.createObjectURL(blob));
    
    this.worker.onmessage = (e) => {
      const { id, result, error } = e.data;
      const promise = this.workerPromises.get(id);
      
      if (promise) {
        if (error) {
          promise.reject(new Error(error));
        } else {
          promise.resolve(result);
        }
        this.workerPromises.delete(id);
      }
    };
  }

  /**
   * Calculer FFT de manière asynchrone
   */
  async computeFFT(samples: number[], config: FFTWorkerConfig) {
    if (!this.worker) {
      throw new Error('Worker FFT non initialisé');
    }

    const id = ++this.requestId;
    
    return new Promise((resolve, reject) => {
      this.workerPromises.set(id, { resolve, reject });
      this.worker!.postMessage({ id, samples, config });
    });
  }

  /**
   * Nettoyer le worker
   */
  terminate() {
    if (this.worker) {
      this.worker.terminate();
      this.worker = null;
    }
    this.workerPromises.clear();
  }
}

/**
 * Hook pour Web Worker FFT
 */
export function useFFTWorker() {
  const workerRef = useRef<FFTWorkerManager | null>(null);
  
  useEffect(() => {
    workerRef.current = new FFTWorkerManager();
    
    return () => {
      workerRef.current?.terminate();
    };
  }, []);
  
  const computeFFT = useCallback(async (samples: number[], config: FFTWorkerConfig) => {
    if (!workerRef.current) {
      throw new Error('Worker FFT non disponible');
    }
    
    return workerRef.current.computeFFT(samples, config);
  }, []);
  
  return { computeFFT };
}

// ============ MONITORING PERFORMANCE ============

/**
 * Moniteur de performance temps réel
 */
export class PerformanceMonitor {
  private frameCount = 0;
  private lastTime = performance.now();
  private fps = 60;
  private memoryUsage = 0;
  private renderTime = 0;
  
  private callbacks: Array<(metrics: PerformanceMetrics) => void> = [];

  /**
   * Commencer le monitoring
   */
  start() {
    this.tick();
  }

  /**
   * Ajouter un callback pour les métriques
   */
  onMetrics(callback: (metrics: PerformanceMetrics) => void) {
    this.callbacks.push(callback);
  }

  /**
   * Tick du monitor
   */
  private tick = () => {
    const now = performance.now();
    this.frameCount++;
    
    // Calculer FPS chaque seconde
    if (now - this.lastTime >= 1000) {
      this.fps = Math.round((this.frameCount * 1000) / (now - this.lastTime));
      this.frameCount = 0;
      this.lastTime = now;
      
      // Mesurer mémoire si disponible
      if ('memory' in performance) {
        const memory = (performance as any).memory;
        this.memoryUsage = Math.round(memory.usedJSHeapSize / 1024 / 1024); // MB
      }
      
      // Notifier les callbacks
      const metrics: PerformanceMetrics = {
        fps: this.fps,
        memoryUsage: this.memoryUsage,
        renderTime: this.renderTime,
        timestamp: now
      };
      
      this.callbacks.forEach(callback => callback(metrics));
    }
    
    requestAnimationFrame(this.tick);
  };

  /**
   * Mesurer temps de rendu
   */
  measureRenderTime<T>(fn: () => T): T {
    const start = performance.now();
    const result = fn();
    this.renderTime = performance.now() - start;
    return result;
  }
}

export interface PerformanceMetrics {
  fps: number;
  memoryUsage: number;
  renderTime: number;
  timestamp: number;
}

/**
 * Hook pour monitoring performance
 */
export function usePerformanceMonitor() {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    fps: 60,
    memoryUsage: 0,
    renderTime: 0,
    timestamp: 0
  });
  
  const monitorRef = useRef<PerformanceMonitor | null>(null);
  
  useEffect(() => {
    monitorRef.current = new PerformanceMonitor();
    monitorRef.current.onMetrics(setMetrics);
    monitorRef.current.start();
    
    return () => {
      // Le monitor continue en arrière-plan
    };
  }, []);
  
  const measureRenderTime = useCallback(<T>(fn: () => T): T => {
    return monitorRef.current?.measureRenderTime(fn) || fn();
  }, []);
  
  return { metrics, measureRenderTime };
}

// ============ UTILITAIRES D'OPTIMISATION ============

/**
 * Optimiseur pour listes de données
 */
export const DataOptimizer = {
  /**
   * Réduire la précision des nombres pour économiser mémoire
   */
  reducePrecision(numbers: number[], decimals: number = 3): number[] {
    const factor = Math.pow(10, decimals);
    return numbers.map(n => Math.round(n * factor) / factor);
  },

  /**
   * Compresser données temporelles redondantes
   */
  compressTimeSeries(data: Array<{ timestamp: number; value: number }>, tolerance: number = 0.001) {
    if (data.length <= 2) return data;
    
    const compressed = [data[0]];
    
    for (let i = 1; i < data.length - 1; i++) {
      const prev = compressed[compressed.length - 1];
      const current = data[i];
      const next = data[i + 1];
      
      // Calculer la différence par rapport à l'interpolation linéaire
      const expectedValue = prev.value + 
        ((next.value - prev.value) * (current.timestamp - prev.timestamp)) / 
        (next.timestamp - prev.timestamp);
      
      const diff = Math.abs(current.value - expectedValue);
      
      // Garder le point si la différence dépasse la tolérance
      if (diff > tolerance) {
        compressed.push(current);
      }
    }
    
    compressed.push(data[data.length - 1]);
    return compressed;
  },

  /**
   * Échantillonner données selon importance
   */
  importanceSampling<T>(
    data: T[],
    maxPoints: number,
    importanceFn: (item: T, index: number) => number
  ): T[] {
    if (data.length <= maxPoints) return data;
    
    // Calculer scores d'importance
    const scored = data.map((item, index) => ({
      item,
      score: importanceFn(item, index),
      index
    }));
    
    // Trier par importance et garder les plus importants
    scored.sort((a, b) => b.score - a.score);
    
    return scored
      .slice(0, maxPoints)
      .sort((a, b) => a.index - b.index)
      .map(s => s.item);
  }
};

export default {
  useStableCallback,
  useOptimizedChartData,
  useVirtualizedList,
  useDebounced,
  useThrottled,
  ChartPerformanceManager,
  useChartPerformance,
  FFTWorkerManager,
  useFFTWorker,
  PerformanceMonitor,
  usePerformanceMonitor,
  DataOptimizer
};
