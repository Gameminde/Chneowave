import React, { useState, useEffect } from 'react';
import {
  PlayIcon,
  PauseIcon,
  CpuChipIcon,
  SignalIcon,
  ClockIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

interface DashboardMetrics {
  acquisition: {
    status: 'active' | 'inactive' | 'error';
    duration: string;
    sampleRate: number;
    channels: number;
  };
  system: {
    cpu: number;
    memory: number;
    storage: number;
  };
  sondes: Array<{
    id: string;
    name: string;
    value: number;
    unit: string;
    status: 'ok' | 'warning' | 'error';
  }>;
}

const MinimalistDashboard: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    acquisition: {
      status: 'active',
      duration: '02:45:33',
      sampleRate: 1000,
      channels: 8
    },
    system: {
      cpu: 34,
      memory: 67,
      storage: 23
    },
    sondes: [
      { id: '1', name: 'Houle #1', value: 2.34, unit: 'm', status: 'ok' },
      { id: '2', name: 'Houle #2', value: 1.87, unit: 'm', status: 'ok' },
      { id: '3', name: 'Pression', value: 1013.4, unit: 'hPa', status: 'ok' },
      { id: '4', name: 'Accél. X', value: 0.15, unit: 'm/s²', status: 'warning' },
      { id: '5', name: 'Accél. Y', value: -0.08, unit: 'm/s²', status: 'ok' },
      { id: '6', name: 'Accél. Z', value: 9.81, unit: 'm/s²', status: 'ok' },
      { id: '7', name: 'Temp. Eau', value: 18.7, unit: '°C', status: 'ok' },
      { id: '8', name: 'Force', value: 0, unit: 'N', status: 'error' }
    ]
  });

  // Mise à jour temps réel
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      
      // Simulation légère des métriques
      setMetrics(prev => ({
        ...prev,
        system: {
          ...prev.system,
          cpu: Math.max(20, Math.min(80, prev.system.cpu + (Math.random() - 0.5) * 5))
        }
      }));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ok': case 'active':
        return <CheckCircleIcon className="w-5 h-5" style={{color: 'var(--status-success)'}} />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5" style={{color: 'var(--status-warning)'}} />;
      case 'error': case 'inactive':
        return <ExclamationTriangleIcon className="w-5 h-5" style={{color: 'var(--status-error)'}} />;
      default:
        return <ClockIcon className="w-5 h-5" style={{color: 'var(--text-muted)'}} />;
    }
  };

  const activeChannels = metrics.sondes.filter(s => s.status === 'ok').length;
  const warningChannels = metrics.sondes.filter(s => s.status === 'warning').length;
  const errorChannels = metrics.sondes.filter(s => s.status === 'error').length;

  return (
    <div className="min-h-screen" style={{backgroundColor: 'var(--bg-primary)'}}>
      <div className="golden-container py-8">
        
        {/* Header */}
        <header className="flex items-center justify-between mb-8 themed-fade-in">
          <div>
            <h1 className="text-title" style={{color: 'var(--text-primary)'}}>Tableau de Bord</h1>
            <p className="text-small mt-1" style={{color: 'var(--text-tertiary)'}}>
              Vue d'ensemble du système d'acquisition
            </p>
          </div>
          
          <div className="text-right">
            <div className="text-heading font-mono" style={{color: 'var(--accent-primary)'}}>
              {currentTime.toLocaleTimeString('fr-FR')}
            </div>
            <div className="text-small" style={{color: 'var(--text-muted)'}}>
              {currentTime.toLocaleDateString('fr-FR', { 
                weekday: 'long',
                day: 'numeric',
                month: 'long'
              })}
            </div>
          </div>
        </header>

        {/* Main Grid (Golden Ratio) */}
        <div className="golden-grid golden-grid-2 mb-8">
          
          {/* Left Column - Primary Metrics */}
          <div className="space-y-6 slide-up min-w-0">
            
            {/* Acquisition Status */}
            <div className="themed-card golden-card" style={{
              backgroundColor: 'var(--bg-elevated)',
              border: '1px solid var(--border-primary)',
              borderRadius: '0.618rem',
              boxShadow: '0 1px 3px var(--shadow-color)'
            }}>
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{
                    backgroundColor: metrics.acquisition.status === 'active' ? 'var(--status-success-bg)' : 'var(--bg-tertiary)'
                  }}>
                    {metrics.acquisition.status === 'active' ? (
                      <PlayIcon className="w-5 h-5" style={{color: 'var(--status-success)'}} />
                    ) : (
                      <PauseIcon className="w-5 h-5" style={{color: 'var(--text-muted)'}} />
                    )}
                  </div>
                  <div>
                    <h3 className="text-heading" style={{color: 'var(--text-primary)'}}>Acquisition</h3>
                    <p className="text-small" style={{color: 'var(--text-tertiary)'}}>Collecte de données</p>
                  </div>
                </div>
                <span className="status" style={{
                  backgroundColor: metrics.acquisition.status === 'active' ? 'var(--status-success-bg)' : 'var(--bg-tertiary)',
                  color: metrics.acquisition.status === 'active' ? 'var(--status-success)' : 'var(--text-muted)'
                }}>
                  {metrics.acquisition.status === 'active' ? 'Active' : 'Inactive'}
                </span>
              </div>

              <div className="golden-grid golden-grid-2">
                <div className="metric">
                  <div className="metric-value" style={{color: 'var(--text-primary)'}}>{metrics.acquisition.channels}</div>
                  <div className="metric-label" style={{color: 'var(--text-muted)'}}>Canaux</div>
                </div>
                <div className="metric">
                  <div className="metric-value" style={{color: 'var(--text-primary)'}}>
                    {metrics.acquisition.sampleRate}
                    <span className="metric-unit" style={{color: 'var(--text-tertiary)'}}>Hz</span>
                  </div>
                  <div className="metric-label" style={{color: 'var(--text-muted)'}}>Fréquence</div>
                </div>
              </div>

              <div className="mt-4 pt-4" style={{borderTop: '1px solid var(--border-primary)'}}>
                <div className="flex items-center justify-between">
                  <span className="text-small" style={{color: 'var(--text-tertiary)'}}>Durée d'acquisition</span>
                  <span className="text-body font-mono" style={{color: 'var(--text-primary)'}}>
                    {metrics.acquisition.duration}
                  </span>
                </div>
              </div>
            </div>

            {/* System Performance */}
            <div className="themed-card golden-card" style={{
              backgroundColor: 'var(--bg-elevated)',
              border: '1px solid var(--border-primary)',
              borderRadius: '0.618rem',
              boxShadow: '0 1px 3px var(--shadow-color)'
            }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{
                  backgroundColor: 'var(--status-info-bg)'
                }}>
                  <CpuChipIcon className="w-5 h-5" style={{color: 'var(--status-info)'}} />
                </div>
                <div>
                  <h3 className="text-heading" style={{color: 'var(--text-primary)'}}>Système</h3>
                  <p className="text-small" style={{color: 'var(--text-tertiary)'}}>Performance en temps réel</p>
                </div>
              </div>

              <div className="space-y-4">
                {[
                  { label: 'Processeur', value: metrics.system.cpu, unit: '%' },
                  { label: 'Mémoire', value: metrics.system.memory, unit: '%' },
                  { label: 'Stockage', value: metrics.system.storage, unit: '%' }
                ].map((item, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-small" style={{color: 'var(--text-tertiary)'}}>{item.label}</span>
                      <span className="text-small font-mono" style={{color: 'var(--text-primary)'}}>
                        {Math.round(item.value)}{item.unit}
                      </span>
                    </div>
                    <div className="progress" style={{
                      backgroundColor: 'var(--bg-tertiary)',
                      borderRadius: '0.5rem',
                      height: '0.5rem',
                      overflow: 'hidden'
                    }}>
                      <div 
                        className="progress-bar"
                        style={{ 
                          width: `${item.value}%`,
                          background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))',
                          height: '100%',
                          borderRadius: 'inherit',
                          transition: 'width 0.5s ease'
                        }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Sondes */}
          <div className="slide-up min-w-0" style={{ animationDelay: '150ms' }}>
            <div className="themed-card golden-card h-full" style={{
              backgroundColor: 'var(--bg-elevated)',
              border: '1px solid var(--border-primary)',
              borderRadius: '0.618rem',
              boxShadow: '0 1px 3px var(--shadow-color)'
            }}>
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{
                    backgroundColor: 'var(--status-info-bg)'
                  }}>
                    <SignalIcon className="w-5 h-5" style={{color: 'var(--status-info)'}} />
                  </div>
                  <div>
                    <h3 className="text-heading" style={{color: 'var(--text-primary)'}}>Sondes</h3>
                    <p className="text-small" style={{color: 'var(--text-tertiary)'}}>État du réseau</p>
                  </div>
                </div>
              </div>

              {/* Summary */}
              <div className="golden-grid golden-grid-3 mb-6">
                <div className="metric text-center">
                  <div className="metric-value" style={{color: 'var(--status-success)'}}>{activeChannels}</div>
                  <div className="metric-label" style={{color: 'var(--text-muted)'}}>Actifs</div>
                </div>
                <div className="metric text-center">
                  <div className="metric-value" style={{color: 'var(--status-warning)'}}>{warningChannels}</div>
                  <div className="metric-label" style={{color: 'var(--text-muted)'}}>Alertes</div>
                </div>
                <div className="metric text-center">
                  <div className="metric-value" style={{color: 'var(--status-error)'}}>{errorChannels}</div>
                  <div className="metric-label" style={{color: 'var(--text-muted)'}}>Erreurs</div>
                </div>
              </div>

              {/* Sonde List */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {metrics.sondes.map((sonde, index) => (
                  <div key={sonde.id} className="flex items-center justify-between p-3 rounded-lg" style={{
                    backgroundColor: 'var(--bg-secondary)'
                  }}>
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      {getStatusIcon(sonde.status)}
                      <div className="min-w-0 flex-1">
                        <div className="text-body truncate" style={{color: 'var(--text-primary)'}}>{sonde.name}</div>
                        <div className="text-meta" style={{color: 'var(--text-muted)'}}>Canal {index + 1}</div>
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0 ml-2">
                      <div className="text-body font-mono" style={{color: 'var(--text-primary)'}}>
                        {sonde.value.toFixed(sonde.unit === 'm/s²' ? 2 : 1)}
                        <span className="metric-unit ml-1" style={{color: 'var(--text-tertiary)'}}>{sonde.unit}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="themed-card golden-card slide-up" style={{ 
          animationDelay: '300ms',
          backgroundColor: 'var(--bg-elevated)',
          border: '1px solid var(--border-primary)',
          borderRadius: '0.618rem',
          boxShadow: '0 1px 3px var(--shadow-color)'
        }}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-heading mb-1" style={{color: 'var(--text-primary)'}}>Actions Rapides</h3>
              <p className="text-small" style={{color: 'var(--text-tertiary)'}}>Contrôles du système</p>
            </div>
            
            <div className="flex flex-wrap items-center gap-3">
              <button className="btn btn-secondary" style={{
                backgroundColor: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-primary)',
                padding: '0.5rem 1rem',
                borderRadius: '0.5rem',
                fontWeight: '500',
                transition: 'all 0.2s ease'
              }}>
                <Cog6ToothIcon className="w-4 h-4" />
                Calibration
              </button>
              <button className="btn btn-secondary" style={{
                backgroundColor: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                border: '1px solid var(--border-primary)',
                padding: '0.5rem 1rem',
                borderRadius: '0.5rem',
                fontWeight: '500',
                transition: 'all 0.2s ease'
              }}>
                <ChartBarIcon className="w-4 h-4" />
                Analyse
              </button>
              <button className="btn btn-primary" style={{
                backgroundColor: 'var(--accent-primary)',
                color: 'var(--text-inverse)',
                border: 'none',
                padding: '0.5rem 1rem',
                borderRadius: '0.5rem',
                fontWeight: '600',
                transition: 'all 0.2s ease'
              }}>
                {metrics.acquisition.status === 'active' ? (
                  <>
                    <PauseIcon className="w-4 h-4" />
                    Arrêter
                  </>
                ) : (
                  <>
                    <PlayIcon className="w-4 h-4" />
                    Démarrer
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MinimalistDashboard;
