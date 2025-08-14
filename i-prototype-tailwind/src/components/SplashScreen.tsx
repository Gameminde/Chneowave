import React, { useEffect, useState } from 'react';

interface SplashScreenProps {
  onComplete: () => void;
}

const SplashScreen: React.FC<SplashScreenProps> = ({ onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [showLogo, setShowLogo] = useState(false);
  const [showText, setShowText] = useState(false);

  useEffect(() => {
    // Animation sequence
    const timer1 = setTimeout(() => setShowLogo(true), 300);
    const timer2 = setTimeout(() => setShowText(true), 800);
    
    // Progress bar animation
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setTimeout(onComplete, 500);
          return 100;
        }
        return prev + 2;
      });
    }, 50);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearInterval(progressInterval);
    };
  }, [onComplete]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" 
         style={{
           background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)'
         }}>
      
      {/* Animated Background Particles */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-blue-400 rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 2}s`
            }}
          />
        ))}
      </div>

      <div className="text-center z-10">
        {/* Logo Animation */}
        <div className={`transition-all duration-1000 ${showLogo ? 'opacity-100 scale-100' : 'opacity-0 scale-75'}`}>
          <div className="relative mb-8">
            {/* Hexagonal Logo Container */}
            <div className="w-32 h-32 mx-auto relative">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                {/* Hexagon Background */}
                <polygon
                  points="50,5 85,25 85,75 50,95 15,75 15,25"
                  fill="url(#logoGradient)"
                  stroke="#3b82f6"
                  strokeWidth="2"
                  className="drop-shadow-lg"
                />
                
                {/* Wave Pattern */}
                <path
                  d="M25 40 Q35 35 45 40 T65 40 T85 40"
                  stroke="#60a5fa"
                  strokeWidth="2"
                  fill="none"
                  className="animate-pulse"
                />
                <path
                  d="M25 50 Q35 45 45 50 T65 50 T85 50"
                  stroke="#93c5fd"
                  strokeWidth="1.5"
                  fill="none"
                  className="animate-pulse"
                  style={{ animationDelay: '0.5s' }}
                />
                <path
                  d="M25 60 Q35 55 45 60 T65 60 T85 60"
                  stroke="#bfdbfe"
                  strokeWidth="1"
                  fill="none"
                  className="animate-pulse"
                  style={{ animationDelay: '1s' }}
                />
                
                {/* Center Dot */}
                <circle cx="50" cy="50" r="3" fill="#ffffff" className="animate-ping" />
                
                <defs>
                  <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#1e40af" />
                    <stop offset="50%" stopColor="#3b82f6" />
                    <stop offset="100%" stopColor="#60a5fa" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>
        </div>

        {/* Text Animation */}
        <div className={`transition-all duration-1000 ${showText ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <h1 className="text-4xl font-bold text-white mb-2 tracking-wide">
            CHNeoWave
          </h1>
          <p className="text-xl text-blue-200 mb-2 font-light">
            Système d'Acquisition Maritime
          </p>
          <p className="text-sm text-slate-400 mb-8">
            Analyse Scientifique des Données Hydrodynamiques
          </p>
        </div>

        {/* Progress Bar */}
        <div className="w-80 mx-auto">
          <div className="bg-slate-700 rounded-full h-1 overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 transition-all duration-100 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-slate-400 text-xs mt-2">
            Initialisation du système... {progress}%
          </p>
        </div>

        {/* Version Info */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-center">
          <p className="text-xs text-slate-500">
            Version 2.1.0 | © 2024 CHNeoWave Laboratory Systems
          </p>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
