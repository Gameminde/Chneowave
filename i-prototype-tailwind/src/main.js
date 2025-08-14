/**
 * CHNeoWave - Point d'entrée principal JavaScript
 * Système d'acquisition maritime professionnel
 */

// Initialisation globale de l'application
window.CHNeoWave = {
  version: '1.0.0',
  initialized: false,
  theme: 'light',
  
  // Configuration globale
  config: {
    apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:3001',
    wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:3001',
    debug: import.meta.env.DEV || false
  },

  // Gestionnaire d'événements globaux
  events: new EventTarget(),

  // Initialisation de l'application
  async init() {
    if (this.initialized) return;
    
    console.log(`🌊 CHNeoWave v${this.version} - Initialisation...`);
    
    try {
      // Initialiser le système de thème
      await this.initThemeSystem();
      
      // Initialiser les services
      await this.initServices();
      
      // Marquer comme initialisé
      this.initialized = true;
      
      // Émettre l'événement d'initialisation
      this.events.dispatchEvent(new CustomEvent('app:initialized'));
      
      console.log('✅ CHNeoWave initialisé avec succès');
      
    } catch (error) {
      console.error('❌ Erreur lors de l\'initialisation:', error);
      throw error;
    }
  },

  // Initialisation du système de thème
  async initThemeSystem() {
    console.log('🎨 Initialisation du système de thème...');
    
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
  },

  // Appliquer un thème
  applyTheme(themeName) {
    const validThemes = ['light', 'dark', 'beige'];
    
    if (!validThemes.includes(themeName)) {
      console.warn(`⚠️ Thème invalide: ${themeName}, utilisation du thème par défaut`);
      themeName = 'light';
    }

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
    document.body.className = document.body.className
      .replace(/theme-\w+/g, '') + ` theme-${themeName}`;
    
    // Sauvegarder le thème
    localStorage.setItem('chneowave-theme', themeName);
    this.theme = themeName;
    
    console.log(`🎨 Thème changé vers: ${themeName}`);
  },

  // Initialisation des services
  async initServices() {
    console.log('🔧 Initialisation des services...');
    
    // Service de données simulées
    this.dataService = {
      generateWaveData: () => ({
        timestamp: Date.now(),
        height: Math.sin(Date.now() * 0.001) * 2 + Math.random() * 0.5,
        period: 8 + Math.random() * 2,
        frequency: 0.125 + Math.random() * 0.025
      }),
      
      generateSensorData: (sondeId) => ({
        id: sondeId,
        status: 'active',
        snr: 25 + Math.random() * 10,
        saturation: Math.random() > 0.9,
        gaps: Math.random() > 0.95 ? 1 : 0,
        lastUpdate: Date.now()
      })
    };

    // Service de statistiques
    this.statsService = {
      calculateStats: (data) => ({
        hMax: Math.max(...data.map(d => d.height)),
        hMin: Math.min(...data.map(d => d.height)),
        h13: data.reduce((sum, d) => sum + d.height, 0) / data.length * 1.3,
        hSignificant: data.reduce((sum, d) => sum + d.height, 0) / data.length * 1.1,
        period: data.reduce((sum, d) => sum + d.period, 0) / data.length,
        count: data.length
      })
    };

    console.log('✅ Services initialisés');
  },

  // Utilitaires globaux
  utils: {
    formatTime: (seconds) => {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },

    formatNumber: (num, decimals = 2) => {
      return Number(num).toFixed(decimals);
    },

    debounce: (func, wait) => {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    }
  }
};

// Auto-initialisation au chargement de la page
if (typeof window !== 'undefined') {
  // Vérification de compatibilité navigateur
  const isCompatible = () => {
    return (
      'EventTarget' in window &&
      'CustomEvent' in window &&
      'localStorage' in window &&
      'addEventListener' in document
    );
  };

  if (!isCompatible()) {
    console.warn('⚠️ CHNeoWave: Navigateur non compatible détecté');
    // Exit gracefully without return statement
  } else {

    // Initialiser dès que le DOM est prêt
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        window.CHNeoWave.init().catch(console.error);
      });
    } else {
      // DOM déjà prêt
      window.CHNeoWave.init().catch(console.error);
    }
  }
}

// Export pour les modules ES6
export default typeof window !== 'undefined' ? window.CHNeoWave : null;
