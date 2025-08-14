/**
 * CHNeoWave - Point d'entrée principal JavaScript (Version Sécurisée)
 * Système d'acquisition maritime professionnel
 */

(function() {
  'use strict';

  // Vérification de l'environnement navigateur
  if (typeof window === 'undefined') {
    console.warn('CHNeoWave: Environnement non-navigateur détecté');
    return;
  }

  // Vérification de compatibilité navigateur
  function isCompatible() {
    try {
      return (
        'EventTarget' in window &&
        'CustomEvent' in window &&
        'localStorage' in window &&
        'addEventListener' in document &&
        'querySelector' in document
      );
    } catch (error) {
      return false;
    }
  }

  if (!isCompatible()) {
    console.warn('⚠️ CHNeoWave: Navigateur non compatible détecté');
    return;
  }

  // Initialisation de l'objet global CHNeoWave
  window.CHNeoWave = {
    version: '1.0.0',
    initialized: false,
    theme: 'light',
    
    // Configuration globale
    config: {
      apiUrl: 'http://localhost:3001',
      wsUrl: 'ws://localhost:3001',
      debug: true
    },

    // Gestionnaire d'événements globaux
    events: new EventTarget(),

    // Initialisation de l'application
    init: function() {
      return new Promise((resolve, reject) => {
        if (this.initialized) {
          resolve();
          return;
        }
        
        console.log(`🌊 CHNeoWave v${this.version} - Initialisation...`);
        
        try {
          // Initialiser le système de thème
          this.initThemeSystem()
            .then(() => this.initServices())
            .then(() => {
              this.initialized = true;
              this.events.dispatchEvent(new CustomEvent('app:initialized'));
              console.log('✅ CHNeoWave initialisé avec succès');
              resolve();
            })
            .catch(reject);
          
        } catch (error) {
          console.error('❌ Erreur lors de l\'initialisation:', error);
          reject(error);
        }
      });
    },

    // Initialisation du système de thème
    initThemeSystem: function() {
      return new Promise((resolve) => {
        console.log('🎨 Initialisation du système de thème...');
        
        try {
          // Charger le thème depuis localStorage
          const savedTheme = localStorage.getItem('chneowave-theme') || 'light';
          this.theme = savedTheme;
          
          // Appliquer le thème initial
          this.applyTheme(savedTheme);
          
          // Écouter les changements de thème
          this.events.addEventListener('theme:change', (event) => {
            this.applyTheme(event.detail.theme);
          });
          
          console.log(`✅ Thème "${savedTheme}" appliqué`);
          resolve();
        } catch (error) {
          console.warn('⚠️ Erreur lors de l\'initialisation du thème:', error);
          resolve(); // Continue même en cas d'erreur
        }
      });
    },

    // Appliquer un thème
    applyTheme: function(themeName) {
      const validThemes = ['light', 'dark', 'beige'];
      
      if (!validThemes.includes(themeName)) {
        console.warn(`⚠️ Thème invalide: ${themeName}, utilisation du thème par défaut`);
        themeName = 'light';
      }

      try {
        // Supprimer les anciens attributs de thème
        document.documentElement.removeAttribute('data-theme');
        document.documentElement.classList.remove('dark');
        
        // Appliquer le nouveau thème
        document.documentElement.setAttribute('data-theme', themeName);
        
        // Support Tailwind dark mode
        if (themeName === 'dark') {
          document.documentElement.classList.add('dark');
        }
        
        // Mettre à jour la classe body pour compatibilité
        if (document.body) {
          document.body.className = document.body.className
            .replace(/theme-\w+/g, '') + ` theme-${themeName}`;
        }
        
        // Sauvegarder le thème
        localStorage.setItem('chneowave-theme', themeName);
        this.theme = themeName;
        
        console.log(`🎨 Thème changé vers: ${themeName}`);
      } catch (error) {
        console.warn('⚠️ Erreur lors de l\'application du thème:', error);
      }
    },

    // Initialisation des services
    initServices: function() {
      return new Promise((resolve) => {
        console.log('🔧 Initialisation des services...');
        
        try {
          // Service de données simulées
          this.dataService = {
            generateWaveData: function() {
              return {
                timestamp: Date.now(),
                height: Math.sin(Date.now() * 0.001) * 2 + Math.random() * 0.5,
                period: 8 + Math.random() * 2,
                frequency: 0.125 + Math.random() * 0.025
              };
            },
            
            generateSensorData: function(sondeId) {
              return {
                id: sondeId,
                status: 'active',
                snr: 25 + Math.random() * 10,
                saturation: Math.random() > 0.9,
                gaps: Math.random() > 0.95 ? 1 : 0,
                lastUpdate: Date.now()
              };
            }
          };

          // Service de statistiques
          this.statsService = {
            calculateStats: function(data) {
              if (!data || data.length === 0) {
                return {
                  hMax: 0, hMin: 0, h13: 0, hSignificant: 0, period: 0, count: 0
                };
              }
              
              const heights = data.map(d => d.height || 0);
              const periods = data.map(d => d.period || 0);
              
              return {
                hMax: Math.max(...heights),
                hMin: Math.min(...heights),
                h13: heights.reduce((sum, h) => sum + h, 0) / heights.length * 1.3,
                hSignificant: heights.reduce((sum, h) => sum + h, 0) / heights.length * 1.1,
                period: periods.reduce((sum, p) => sum + p, 0) / periods.length,
                count: data.length
              };
            }
          };

          // Utilitaires globaux
          this.utils = {
            formatTime: function(seconds) {
              const mins = Math.floor(seconds / 60);
              const secs = Math.floor(seconds % 60);
              return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            },

            formatNumber: function(num, decimals) {
              decimals = decimals || 2;
              return Number(num).toFixed(decimals);
            },

            debounce: function(func, wait) {
              let timeout;
              return function executedFunction() {
                const args = Array.prototype.slice.call(arguments);
                const later = function() {
                  clearTimeout(timeout);
                  func.apply(null, args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
              };
            }
          };

          console.log('✅ Services initialisés');
          resolve();
        } catch (error) {
          console.warn('⚠️ Erreur lors de l\'initialisation des services:', error);
          resolve(); // Continue même en cas d'erreur
        }
      });
    }
  };

  // Auto-initialisation au chargement de la page
  function autoInit() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        window.CHNeoWave.init().catch(function(error) {
          console.error('Erreur d\'initialisation CHNeoWave:', error);
        });
      });
    } else {
      // DOM déjà prêt
      window.CHNeoWave.init().catch(function(error) {
        console.error('Erreur d\'initialisation CHNeoWave:', error);
      });
    }
  }

  // Lancer l'initialisation
  autoInit();

})();

// Export pour les modules ES6 (si supporté)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = typeof window !== 'undefined' ? window.CHNeoWave : null;
}
