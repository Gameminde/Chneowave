import React, { useState, useEffect } from 'react';
import { useUnifiedApp } from './contexts/UnifiedAppContext';
import { 
  ChartBarIcon, 
  ClockIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  InformationCircleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';

interface ProjectStats {
  totalProjects: number;
  activeProjects: number;
  completedProjects: number;
  totalDataPoints: number;
  systemUptime: number;
  lastBackup: string;
}

interface RecentActivity {
  id: number;
  type: 'acquisition' | 'calibration' | 'analysis' | 'export';
  description: string;
  timestamp: string;
  status: 'success' | 'warning' | 'error';
  projectName: string;
}

const ModernDashboard: React.FC = () => {
  const { theme } = useUnifiedApp();
  const [stats, setStats] = useState<ProjectStats>({
    totalProjects: 24,
    activeProjects: 3,
    completedProjects: 21,
    totalDataPoints: 1542000,
    systemUptime: 168,
    lastBackup: '2024-01-15 14:30'
  });

  const [recentActivity] = useState<RecentActivity[]>([
    {
      id: 1,
      type: 'acquisition',
      description: 'Acquisition terminée - Projet Océan Atlantique',
      timestamp: 'Il y a 2 heures',
      status: 'success',
      projectName: 'Océan Atlantique'
    },
    {
      id: 2,
      type: 'calibration',
      description: 'Calibration des sondes - Projet Méditerranée',
      timestamp: 'Il y a 4 heures',
      status: 'success',
      projectName: 'Méditerranée'
    },
    {
      id: 3,
      type: 'analysis',
      description: 'Analyse en cours - Projet Pacifique',
      timestamp: 'Il y a 6 heures',
      status: 'warning',
      projectName: 'Pacifique'
    },
    {
      id: 4,
      type: 'export',
      description: 'Export des données - Projet Indien',
      timestamp: 'Il y a 1 jour',
      status: 'success',
      projectName: 'Océan Indien'
    }
  ]);

  const [systemHealth, setSystemHealth] = useState({
    cpu: 45,
    memory: 62,
    storage: 28,
    network: 85
  });

  // Simulation des métriques en temps réel
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemHealth(prev => ({
        cpu: Math.max(20, Math.min(80, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.max(40, Math.min(90, prev.memory + (Math.random() - 0.5) * 5)),
        storage: Math.max(20, Math.min(40, prev.storage + (Math.random() - 0.5) * 2)),
        network: Math.max(70, Math.min(95, prev.network + (Math.random() - 0.5) * 8))
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon className="w-5 h-5 text-emerald-400" />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5 text-amber-400" />;
      case 'error':
        return <ExclamationTriangleIcon className="w-5 h-5 text-rose-400" />;
      default:
        return <InformationCircleIcon className="w-5 h-5 text-blue-400" />;
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'acquisition':
        return <ChartBarIcon className="w-5 h-5 text-blue-400" />;
      case 'calibration':
        return <ClockIcon className="w-5 h-5 text-emerald-400" />;
      case 'analysis':
        return <ArrowTrendingUpIcon className="w-5 h-5 text-violet-400" />;
      case 'export':
        return <ArrowTrendingDownIcon className="w-5 h-5 text-amber-400" />;
      default:
        return <InformationCircleIcon className="w-5 h-5 text-slate-400" />;
    }
  };

  const formatUptime = (hours: number) => {
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;
    return `${days}j ${remainingHours}h`;
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      {/* En-tête du tableau de bord */}
      <div className="text-center space-y-4 mb-8">
        <h1 className="text-4xl font-bold text-white">Tableau de Bord CHNeoWave</h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Vue d'ensemble complète de vos projets, métriques système et activités récentes
        </p>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Projets totaux */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:bg-slate-800/70 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">Projets Totaux</p>
              <p className="text-3xl font-bold text-white">{stats.totalProjects}</p>
            </div>
            <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center">
              <ChartBarIcon className="w-6 h-6 text-blue-400" />
            </div>
          </div>
          <div className="mt-4 flex items-center space-x-2">
            <span className="text-sm text-slate-400">Actifs: {stats.activeProjects}</span>
            <span className="text-slate-600">|</span>
            <span className="text-sm text-slate-400">Terminés: {stats.completedProjects}</span>
          </div>
        </div>

        {/* Points de données */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:bg-slate-800/70 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">Points de Données</p>
              <p className="text-3xl font-bold text-white">{formatNumber(stats.totalDataPoints)}</p>
            </div>
            <div className="w-12 h-12 bg-emerald-500/10 rounded-lg flex items-center justify-center">
              <ArrowTrendingUpIcon className="w-6 h-6 text-emerald-400" />
            </div>
          </div>
          <div className="mt-4">
            <div className="w-full bg-slate-700 rounded-full h-2">
              <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '75%' }}></div>
            </div>
            <p className="text-xs text-slate-400 mt-1">75% de la capacité</p>
          </div>
        </div>

        {/* Temps de fonctionnement */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:bg-slate-800/70 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">Temps de Fonctionnement</p>
              <p className="text-3xl font-bold text-white">{formatUptime(stats.systemUptime)}</p>
            </div>
            <div className="w-12 h-12 bg-violet-500/10 rounded-lg flex items-center justify-center">
              <ClockIcon className="w-6 h-6 text-violet-400" />
            </div>
          </div>
          <div className="mt-4">
            <p className="text-xs text-slate-400">Dernière sauvegarde: {stats.lastBackup}</p>
          </div>
        </div>

        {/* Santé du système */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6 hover:bg-slate-800/70 transition-all duration-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">Santé Système</p>
              <p className="text-3xl font-bold text-emerald-400">Excellent</p>
            </div>
            <div className="w-12 h-12 bg-emerald-500/10 rounded-lg flex items-center justify-center">
              <CheckCircleIcon className="w-6 h-6 text-emerald-400" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
              <span className="text-xs text-emerald-400">Tous les systèmes opérationnels</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grille principale */}
      <div className="grid grid-cols-12 gap-6">
        {/* Colonne gauche - Activités récentes */}
        <div className="col-span-12 lg:col-span-4">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Activités Récentes</h3>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3 p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                  <div className="flex-shrink-0 mt-1">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white">{activity.description}</p>
                    <p className="text-xs text-slate-400 mt-1">{activity.projectName}</p>
                    <p className="text-xs text-slate-500 mt-1">{activity.timestamp}</p>
                  </div>
                  <div className="flex-shrink-0">
                    {getStatusIcon(activity.status)}
                  </div>
                </div>
              ))}
            </div>
            <button className="w-full mt-4 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white rounded-lg transition-all duration-200">
              Voir toutes les activités
            </button>
          </div>
        </div>

        {/* Colonne centrale - Graphiques et métriques */}
        <div className="col-span-12 lg:col-span-5">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Métriques Système</h3>
            
            {/* CPU */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-slate-300">CPU</span>
                <span className="text-sm text-slate-400">{systemHealth.cpu.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-3">
                <div 
                  className={`h-3 rounded-full transition-all duration-500 ${
                    systemHealth.cpu > 70 ? 'bg-rose-500' : 
                    systemHealth.cpu > 50 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${systemHealth.cpu}%` }}
                ></div>
              </div>
            </div>

            {/* Mémoire */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-slate-300">Mémoire</span>
                <span className="text-sm text-slate-400">{systemHealth.memory.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-3">
                <div 
                  className={`h-3 rounded-full transition-all duration-500 ${
                    systemHealth.memory > 80 ? 'bg-rose-500' : 
                    systemHealth.memory > 60 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${systemHealth.memory}%` }}
                ></div>
              </div>
            </div>

            {/* Stockage */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-slate-300">Stockage</span>
                <span className="text-sm text-slate-400">{systemHealth.storage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-3">
                <div 
                  className={`h-3 rounded-full transition-all duration-500 ${
                    systemHealth.storage > 80 ? 'bg-rose-500' : 
                    systemHealth.storage > 60 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${systemHealth.storage}%` }}
                ></div>
              </div>
            </div>

            {/* Réseau */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-slate-300">Réseau</span>
                <span className="text-sm text-slate-400">{systemHealth.network.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-3">
                <div 
                  className={`h-3 rounded-full transition-all duration-500 ${
                    systemHealth.network > 90 ? 'bg-rose-500' : 
                    systemHealth.network > 70 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${systemHealth.network}%` }}
                ></div>
              </div>
            </div>

            {/* Indicateur de performance global */}
            <div className="mt-6 p-4 bg-slate-700/30 rounded-lg border border-slate-600/30">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">Performance Globale</span>
                <span className="text-lg font-bold text-emerald-400">92%</span>
              </div>
              <div className="mt-2 w-full bg-slate-600 rounded-full h-2">
                <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '92%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Colonne droite - Projets et actions rapides */}
        <div className="col-span-12 lg:col-span-3">
          <div className="space-y-6">
            {/* Projets actifs */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Projets Actifs</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-white">Océan Atlantique</p>
                    <p className="text-xs text-slate-400">Acquisition en cours</p>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
                </div>
                <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-white">Méditerranée</p>
                    <p className="text-xs text-slate-400">Calibration</p>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
                </div>
                <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-white">Pacifique</p>
                    <p className="text-xs text-slate-400">Analyse</p>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></div>
                </div>
              </div>
            </div>

            {/* Actions rapides */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Actions Rapides</h3>
              <div className="space-y-3">
                <button className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200 text-sm font-medium">
                  Nouveau Projet
                </button>
                <button className="w-full px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-all duration-200 text-sm font-medium">
                  Démarrer Acquisition
                </button>
                <button className="w-full px-4 py-2 bg-violet-600 hover:bg-violet-700 text-white rounded-lg transition-all duration-200 text-sm font-medium">
                  Exporter Données
                </button>
                <button className="w-full px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 hover:text-white rounded-lg transition-all duration-200 text-sm font-medium">
                  Configuration
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModernDashboard;
