import React, { useState } from 'react';
import { ChevronRightIcon, PlusIcon, FolderOpenIcon } from '@heroicons/react/24/outline';

interface MinimalistWelcomeProps {
  onProjectCreate: (projectData: any) => void;
  onProjectOpen: () => void;
}

const MinimalistWelcome: React.FC<MinimalistWelcomeProps> = ({
  onProjectCreate,
  onProjectOpen
}) => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [projectData, setProjectData] = useState({
    name: '',
    description: '',
    location: '',
    investigator: ''
  });

  const handleCreateProject = () => {
    if (projectData.name.trim()) {
      onProjectCreate(projectData);
    }
  };

  const recentProjects = [
    { name: 'Houle Atlantique 2024', date: '2024-01-15', status: 'active' },
    { name: 'Étude Courants Manche', date: '2024-01-10', status: 'completed' },
    { name: 'Analyse Marées', date: '2024-01-05', status: 'draft' }
  ];

  return (
    <div className="min-h-screen" style={{backgroundColor: 'var(--bg-primary)'}}>
      {/* Golden Ratio Layout Container */}
      <div className="golden-container">
        
        {/* Header Section (φ ratio height) */}
        <header className="fade-in" style={{ minHeight: 'calc(100vh * 0.618)' }}>
          <div className="flex flex-col justify-center h-full text-center">
            
            {/* Logo & Title */}
            <div className="mb-8">
              <div className="w-16 h-16 mx-auto mb-6 bg-blue-600 rounded-xl flex items-center justify-center">
                <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L2 7v10c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7L12 2z"/>
                </svg>
              </div>
              <h1 className="text-display mb-4" style={{color: 'var(--text-primary)'}}>CHNeoWave</h1>
              <p className="text-heading max-w-2xl mx-auto" style={{color: 'var(--text-secondary)'}}>
                Système d'acquisition maritime professionnel
              </p>
            </div>

            {/* Main Actions */}
            <div className="golden-grid golden-grid-2 max-w-4xl mx-auto">
              
              {/* Create New Project */}
              <div className="themed-card golden-card text-left">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--status-info-bg)' }}>
                  <PlusIcon className="w-5 h-5" style={{ color: 'var(--status-info)' }} />
                    </div>
                    <div>
                  <h3 className="text-heading" style={{ color: 'var(--text-primary)' }}>Nouveau Projet</h3>
                  <p className="text-small" style={{ color: 'var(--text-secondary)' }}>Créer une nouvelle étude</p>
                    </div>
                  </div>
                </div>

                {!showCreateForm ? (
                  <button 
                    onClick={() => setShowCreateForm(true)}
                    className="themed-btn themed-btn-primary w-full"
                  >
                    Commencer
                    <ChevronRightIcon className="w-4 h-4" />
                  </button>
                ) : (
                  <div className="space-y-4 slide-up">
                    <div>
                      <label className="label">Nom du projet</label>
                      <input
                        type="text"
                        className="themed-input"
                        placeholder="ex: Étude Houle Méditerranée 2024"
                        value={projectData.name}
                        onChange={(e) => setProjectData({...projectData, name: e.target.value})}
                      />
                    </div>
                    
                    <div>
                      <label className="label">Localisation</label>
                      <input
                        type="text"
                        className="themed-input"
                        placeholder="ex: Côte d'Azur, France"
                        value={projectData.location}
                        onChange={(e) => setProjectData({...projectData, location: e.target.value})}
                      />
                    </div>

                    <div>
                      <label className="label">Investigateur principal</label>
                      <input
                        type="text"
                        className="themed-input"
                        placeholder="ex: Dr. Marine Dupont"
                        value={projectData.investigator}
                        onChange={(e) => setProjectData({...projectData, investigator: e.target.value})}
                      />
                    </div>

                    <div className="flex gap-3 pt-2">
                      <button 
                        onClick={handleCreateProject}
                        className="themed-btn themed-btn-primary flex-1"
                        disabled={!projectData.name.trim()}
                      >
                        Créer le projet
                      </button>
                      <button 
                        onClick={() => setShowCreateForm(false)}
                        className="themed-btn themed-btn-ghost"
                      >
                        Annuler
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Recent Projects */}
              <div className="themed-card golden-card">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: 'var(--bg-secondary)' }}>
                      <FolderOpenIcon className="w-5 h-5" style={{ color: 'var(--text-secondary)' }} />
                    </div>
                    <div>
                      <h3 className="text-heading" style={{ color: 'var(--text-primary)' }}>Projets Récents</h3>
                      <p className="text-small" style={{ color: 'var(--text-secondary)' }}>Continuer un projet existant</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  {recentProjects.map((project, index) => (
                    <button
                      key={index}
                      onClick={onProjectOpen}
                    className="w-full p-4 rounded-lg transition-all text-left group"
                    style={{ border: '1px solid var(--border-primary)' }}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="text-body font-medium" style={{ color: 'var(--text-primary)' }}>
                            {project.name}
                          </div>
                          <div className="text-small" style={{ color: 'var(--text-secondary)' }}>Modifié le {new Date(project.date).toLocaleDateString('fr-FR')}</div>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className={`status ${
                            project.status === 'active' ? 'status-success' :
                            project.status === 'completed' ? 'status-neutral' :
                            'status-warning'
                          }`}>
                            {project.status === 'active' ? 'Actif' :
                             project.status === 'completed' ? 'Terminé' :
                             'Brouillon'}
                          </span>
                          <ChevronRightIcon className="w-4 h-4 transition-colors" style={{ color: 'var(--text-muted)' }} />
                        </div>
                      </div>
                    </button>
                  ))}
                </div>

                <button className="themed-btn themed-btn-ghost w-full mt-4">
                  Voir tous les projets
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Footer Section (φ⁻¹ ratio height) */}
        <footer className="slide-up" style={{ minHeight: 'calc(100vh * 0.382)' }}>
          <div className="pt-8" style={{ borderTop: '1px solid var(--border-primary)' }}>
            
            {/* Quick Stats */}
            <div className="golden-grid golden-grid-3 text-center mb-8">
              <div className="themed-metric">
                <div className="themed-metric-value">127</div>
                <div className="themed-metric-label">Projets créés</div>
              </div>
              <div className="themed-metric">
                <div className="themed-metric-value">2.4<span className="themed-metric-unit">TB</span></div>
                <div className="themed-metric-label">Données collectées</div>
              </div>
              <div className="themed-metric">
                <div className="themed-metric-value">99.8<span className="themed-metric-unit">%</span></div>
                <div className="themed-metric-label">Disponibilité</div>
              </div>
            </div>

            {/* System Status */}
            <div className="themed-card golden-card" style={{backgroundColor: 'var(--bg-secondary)'}}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: 'var(--status-success)' }}></div>
                  <div>
                    <div className="text-body font-medium" style={{ color: 'var(--text-primary)' }}>Système opérationnel</div>
                    <div className="text-small" style={{ color: 'var(--text-secondary)' }}>Tous les sondes connectés • MCC DAQ prêt</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-small font-mono" style={{ color: 'var(--text-secondary)' }}>
                    {new Date().toLocaleTimeString('fr-FR')}
                  </div>
                  <div className="text-meta" style={{ color: 'var(--text-muted)' }}>
                    Temps système local
                  </div>
                </div>
              </div>
            </div>

            {/* Version Info */}
            <div className="text-center mt-8 pb-8">
              <p className="text-meta">
                CHNeoWave v2.1.0 • Système d'acquisition maritime
              </p>
              <p className="text-meta mt-1">
                Laboratoire Maritime • Université de Sciences
              </p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default MinimalistWelcome;
