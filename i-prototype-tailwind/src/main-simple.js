/**
 * CHNeoWave - Point d'entrée JavaScript simplifié
 * Version ultra-sécurisée sans erreurs de syntaxe
 */

// Vérification de l'environnement
if (typeof window === 'undefined') {
  console.warn('CHNeoWave: Environnement serveur détecté, arrêt de l\'initialisation');
} else {
  // Initialisation dans un bloc try-catch global
  try {
    // Vérification des APIs nécessaires
    var hasRequiredAPIs = (
      typeof EventTarget !== 'undefined' &&
      typeof CustomEvent !== 'undefined' &&
      typeof localStorage !== 'undefined' &&
      typeof document !== 'undefined' &&
      typeof document.addEventListener !== 'undefined'
    );

    if (!hasRequiredAPIs) {
      console.warn('CHNeoWave: APIs requises non disponibles');
    } else {
      // Création de l'objet CHNeoWave
      window.CHNeoWave = {
        version: '1.0.0',
        initialized: false,
        theme: 'light',
        
        config: {
          apiUrl: 'http://localhost:3001',
          wsUrl: 'ws://localhost:3001',
          debug: true
        },

        events: new EventTarget(),

        init: function() {
          var self = this;
          
          if (self.initialized) {
            console.log('CHNeoWave déjà initialisé');
            return Promise.resolve();
          }

          console.log('🌊 CHNeoWave v' + self.version + ' - Initialisation...');
          
          return new Promise(function(resolve, reject) {
            try {
              // Initialiser le système de thème
              self.initThemeSystem();
              
              // Initialiser les services
              self.initServices();
              
              // Marquer comme initialisé
              self.initialized = true;
              
              // Émettre l'événement d'initialisation
              try {
                self.events.dispatchEvent(new CustomEvent('app:initialized'));
              } catch (eventError) {
                console.warn('Erreur lors de l\'émission de l\'événement:', eventError);
              }
              
              console.log('✅ CHNeoWave initialisé avec succès');
              resolve();
            } catch (error) {
              console.error('❌ Erreur lors de l\'initialisation:', error);
              reject(error);
            }
          });
        },

        initThemeSystem: function() {
          console.log('🎨 Initialisation du système de thème...');
          
          try {
            // Charger le thème depuis localStorage
            var savedTheme = 'light';
            try {
              savedTheme = localStorage.getItem('chneowave-theme') || 'light';
            } catch (storageError) {
              console.warn('localStorage non accessible:', storageError);
            }
            
            this.theme = savedTheme;
            this.applyTheme(savedTheme);
            
            // Écouter les changements de thème
            var self = this;
            try {
              this.events.addEventListener('theme:change', function(event) {
                if (event.detail && event.detail.theme) {
                  self.applyTheme(event.detail.theme);
                }
              });
            } catch (listenerError) {
              console.warn('Erreur lors de l\'ajout du listener de thème:', listenerError);
            }
            
            console.log('✅ Thème "' + savedTheme + '" appliqué');
          } catch (error) {
            console.warn('⚠️ Erreur lors de l\'initialisation du thème:', error);
          }
        },

        applyTheme: function(themeName) {
          var validThemes = ['light', 'dark', 'beige'];
          
          if (validThemes.indexOf(themeName) === -1) {
            console.warn('⚠️ Thème invalide: ' + themeName + ', utilisation du thème par défaut');
            themeName = 'light';
          }

          try {
            // Supprimer les anciens attributs de thème
            if (document.documentElement) {
              document.documentElement.removeAttribute('data-theme');
              document.documentElement.classList.remove('dark');
              
              // Appliquer le nouveau thème
              document.documentElement.setAttribute('data-theme', themeName);
              
              // Support Tailwind dark mode
              if (themeName === 'dark') {
                document.documentElement.classList.add('dark');
              }
            }
            
            // Mettre à jour la classe body
            if (document.body) {
              var bodyClass = document.body.className || '';
              bodyClass = bodyClass.replace(/theme-\w+/g, '');
              document.body.className = bodyClass + ' theme-' + themeName;
            }
            
            // Sauvegarder le thème
            try {
              localStorage.setItem('chneowave-theme', themeName);
            } catch (storageError) {
              console.warn('Impossible de sauvegarder le thème:', storageError);
            }
            
            this.theme = themeName;
            console.log('🎨 Thème changé vers: ' + themeName);
          } catch (error) {
            console.warn('⚠️ Erreur lors de l\'application du thème:', error);
          }
        },

        initServices: function() {
          console.log('🔧 Initialisation des services...');
          
          try {
            // Service de données simulées
            this.dataService = {
              generateWaveData: function() {
                var now = Date.now();
                return {
                  timestamp: now,
                  height: Math.sin(now * 0.001) * 2 + Math.random() * 0.5,
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
                
                var heights = [];
                var periods = [];
                
                for (var i = 0; i < data.length; i++) {
                  heights.push(data[i].height || 0);
                  periods.push(data[i].period || 0);
                }
                
                var hMax = Math.max.apply(Math, heights);
                var hMin = Math.min.apply(Math, heights);
                var avgHeight = heights.reduce(function(sum, h) { return sum + h; }, 0) / heights.length;
                var avgPeriod = periods.reduce(function(sum, p) { return sum + p; }, 0) / periods.length;
                
                return {
                  hMax: hMax,
                  hMin: hMin,
                  h13: avgHeight * 1.3,
                  hSignificant: avgHeight * 1.1,
                  period: avgPeriod,
                  count: data.length
                };
              }
            };

            // Utilitaires
            this.utils = {
              formatTime: function(seconds) {
                var mins = Math.floor(seconds / 60);
                var secs = Math.floor(seconds % 60);
                return (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
              },

              formatNumber: function(num, decimals) {
                decimals = decimals || 2;
                return Number(num).toFixed(decimals);
              },

              debounce: function(func, wait) {
                var timeout;
                return function() {
                  var args = arguments;
                  var later = function() {
                    timeout = null;
                    func.apply(null, args);
                  };
                  clearTimeout(timeout);
                  timeout = setTimeout(later, wait);
                };
              }
            };

            console.log('✅ Services initialisés');
          } catch (error) {
            console.warn('⚠️ Erreur lors de l\'initialisation des services:', error);
          }
        }
      };

      // Auto-initialisation
      function startInit() {
        window.CHNeoWave.init().catch(function(error) {
          console.error('Erreur d\'initialisation CHNeoWave:', error);
        });
      }

      // Attendre que le DOM soit prêt
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startInit);
      } else {
        startInit();
      }
    }
  } catch (globalError) {
    console.error('CHNeoWave: Erreur critique lors de l\'initialisation:', globalError);
  }
}
