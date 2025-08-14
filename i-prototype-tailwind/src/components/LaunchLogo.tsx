import React, { useState, useEffect } from 'react';

interface LaunchLogoProps {
  onComplete?: () => void;
  duration?: number;
}

const LaunchLogo: React.FC<LaunchLogoProps> = ({ 
  onComplete, 
  duration = 4000 
}) => {
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState('initializing'); // initializing, connecting, analyzing, ready
  const [waveAnimation, setWaveAnimation] = useState(0);
  const [systemChecks, setSystemChecks] = useState([
    { name: 'Sondes MCC DAQ', status: 'pending', icon: '📡' },
    { name: 'Interface Maritime', status: 'pending', icon: '🌊' },
    { name: 'Système Temps Réel', status: 'pending', icon: '⚡' },
    { name: 'Base de Données', status: 'pending', icon: '💾' }
  ]);

  useEffect(() => {
    // Animation des vagues continues
    const waveTimer = setInterval(() => {
      setWaveAnimation(prev => (prev + 2) % 360);
    }, 50);

    // Progression avec étapes
    const timer = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + (100 / (duration / 100));
        
        // Mise à jour des étapes et vérifications
        if (newProgress > 15 && newProgress < 25) {
          setStage('connecting');
          setSystemChecks(checks => checks.map((check, index) => 
            index === 0 ? { ...check, status: 'success' } : check
          ));
        } else if (newProgress > 35 && newProgress < 45) {
          setSystemChecks(checks => checks.map((check, index) => 
            index === 1 ? { ...check, status: 'success' } : check
          ));
        } else if (newProgress > 55 && newProgress < 65) {
          setStage('analyzing');
          setSystemChecks(checks => checks.map((check, index) => 
            index === 2 ? { ...check, status: 'success' } : check
          ));
        } else if (newProgress > 75 && newProgress < 85) {
          setSystemChecks(checks => checks.map((check, index) => 
            index === 3 ? { ...check, status: 'success' } : check
          ));
        } else if (newProgress >= 95) {
          setStage('ready');
        }
        
        if (newProgress >= 100) {
          clearInterval(timer);
          setTimeout(() => {
            onComplete && onComplete();
          }, 1000);
          return 100;
        }
        
        return newProgress;
      });
    }, 100);

    return () => {
      clearInterval(timer);
      clearInterval(waveTimer);
    };
  }, [duration, onComplete]);

  const getStageMessage = () => {
    switch (stage) {
      case 'initializing': return 'Initialisation du système...';
      case 'connecting': return 'Connexion aux sondes...';
      case 'analyzing': return 'Analyse de l\'environnement...';
      case 'ready': return 'Système prêt !';
      default: return 'Chargement...';
    }
  };

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-blue-50 via-white to-cyan-50 flex items-center justify-center z-50">
      
      {/* Particules flottantes */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-blue-200 rounded-full opacity-30 animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${2 + Math.random() * 3}s`
            }}
          />
        ))}
      </div>

      <div className="text-center relative z-10">
        
        {/* Logo principal animé */}
        <div className="relative mb-8">
          
          {/* Cercles animés en arrière-plan */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div 
              className="w-40 h-40 border-2 border-blue-200 rounded-full animate-spin"
              style={{ animationDuration: '8s' }}
            />
            <div 
              className="absolute w-32 h-32 border-2 border-cyan-200 rounded-full animate-spin"
              style={{ animationDuration: '6s', animationDirection: 'reverse' }}
            />
            <div 
              className="absolute w-24 h-24 border-2 border-blue-300 rounded-full animate-spin"
              style={{ animationDuration: '4s' }}
            />
          </div>

          {/* Logo central avec effet de vague */}
          <div className="relative w-24 h-24 mx-auto bg-gradient-to-br from-blue-600 to-cyan-500 rounded-2xl flex items-center justify-center shadow-2xl transform transition-all duration-1000"
               style={{ 
                 transform: `scale(${1 + Math.sin(waveAnimation * Math.PI / 180) * 0.1}) rotate(${waveAnimation * 0.5}deg)`,
                 boxShadow: `0 0 ${20 + Math.sin(waveAnimation * Math.PI / 180) * 10}px rgba(59, 130, 246, 0.5)`
               }}>
            <div className="text-white text-2xl font-bold">
              CHN
            </div>
            
            {/* Effet de pulsation */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-2xl opacity-30 animate-ping" />
          </div>

          {/* Vagues animées */}
          <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2">
            <svg width="120" height="20" viewBox="0 0 120 20">
              <path
                d={`M0,10 Q30,${5 + Math.sin(waveAnimation * Math.PI / 180) * 3} 60,10 T120,10`}
                stroke="url(#waveGradient)"
                strokeWidth="2"
                fill="none"
                className="animate-pulse"
              />
              <defs>
                <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#3b82f6" />
                  <stop offset="50%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#3b82f6" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>

        {/* Titre avec animation */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent mb-2 animate-pulse">
            CHNeoWave
          </h1>
          <p className="text-lg text-gray-600 animate-fade-in">
            Système d'Acquisition Maritime Professionnel
          </p>
        </div>

        {/* Message d'étape */}
        <div className="mb-6">
          <p className="text-blue-600 font-medium text-lg">
            {getStageMessage()}
          </p>
        </div>

        {/* Barre de progression avancée */}
        <div className="w-80 mx-auto mb-8">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>Progression</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden shadow-inner">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-300 relative"
              style={{ width: `${progress}%` }}
            >
              {/* Effet de brillance */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30 animate-pulse" />
            </div>
          </div>
        </div>

        {/* Vérifications système */}
        <div className="space-y-3 max-w-sm mx-auto">
          {systemChecks.map((check, index) => (
            <div 
              key={index} 
              className={`flex items-center justify-between p-3 rounded-lg transition-all duration-500 ${
                check.status === 'success' ? 'bg-green-50 border border-green-200' : 
                check.status === 'pending' ? 'bg-gray-50 border border-gray-200' : 
                'bg-red-50 border border-red-200'
              }`}
            >
              <div className="flex items-center space-x-3">
                <span className="text-lg">{check.icon}</span>
                <span className={`text-sm font-medium ${
                  check.status === 'success' ? 'text-green-700' : 
                  check.status === 'pending' ? 'text-gray-600' : 
                  'text-red-700'
                }`}>
                  {check.name}
                </span>
              </div>
              <div className="flex items-center">
                {check.status === 'success' && (
                  <div className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
                {check.status === 'pending' && (
                  <div className="w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Footer avec version */}
        <div className="mt-8 text-center">
          <p className="text-xs text-gray-400">
            Version 2.1.0 • Laboratoire Maritime
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Powered by Golden Ratio Design System
          </p>
        </div>
      </div>

      {/* Styles CSS animés */}
      <style>
        {`
          @keyframes fade-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
          
          .animate-fade-in {
            animation: fade-in 1s ease-out;
          }
        `}
      </style>
    </div>
  );
};

export default LaunchLogo;