import React from 'react';

const DashboardPage: React.FC = () => {
  return (
    <div className="p-6" style={{ backgroundColor: 'var(--bg-primary)' }}>
      {/* Titre */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>Projet</h1>
        <span className="themed-status themed-status-success">Actif</span>
      </div>

      {/* Résumé Projet */}
      <div className="themed-card golden-card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <div className="text-meta mb-1">Nom du projet</div>
            <div className="text-heading" style={{ color: 'var(--text-primary)' }}>Essai de Houle Atlantique</div>
          </div>
          <div>
            <div className="text-meta mb-1">Responsable</div>
            <div className="text-body" style={{ color: 'var(--text-primary)' }}>Dr. Marine Dupont</div>
          </div>
          <div>
            <div className="text-meta mb-1">Dernière mise à jour</div>
            <div className="text-body" style={{ color: 'var(--text-primary)' }}>Aujourd'hui, 12:34</div>
          </div>
        </div>
      </div>

      {/* Détails */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="themed-card golden-card lg:col-span-2">
          <h3 className="text-heading mb-4" style={{ color: 'var(--text-primary)' }}>Informations</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-meta mb-1">ID Projet</div>
              <div className="text-body" style={{ color: 'var(--text-primary)' }}>PRJ-2025-ATL-001</div>
            </div>
            <div>
              <div className="text-meta mb-1">Laboratoire</div>
              <div className="text-body" style={{ color: 'var(--text-primary)' }}>CHNeoWave</div>
            </div>
            <div>
              <div className="text-meta mb-1">Date de début</div>
              <div className="text-body" style={{ color: 'var(--text-primary)' }}>02/06/2025</div>
            </div>
            <div>
              <div className="text-meta mb-1">État</div>
              <div className="text-body" style={{ color: 'var(--status-success)' }}>En cours</div>
            </div>
          </div>
        </div>

        <div className="themed-card golden-card">
          <h3 className="text-heading mb-4" style={{ color: 'var(--text-primary)' }}>Équipe</h3>
          <ul className="space-y-2">
            <li className="flex items-center justify-between">
              <span className="text-body" style={{ color: 'var(--text-primary)' }}>M. Chen</span>
              <span className="text-meta">Hydrodynamique</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-body" style={{ color: 'var(--text-primary)' }}>S. Martin</span>
              <span className="text-meta">Instrumentation</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-body" style={{ color: 'var(--text-primary)' }}>A. Rossi</span>
              <span className="text-meta">Analyse</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Jalons */}
      <div className="themed-card golden-card mt-6">
        <h3 className="text-heading mb-4" style={{ color: 'var(--text-primary)' }}>Jalons</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-3" style={{ backgroundColor: 'var(--bg-secondary)', borderRadius: '.5rem' }}>
            <div className="text-meta">Préparation</div>
            <div className="text-body" style={{ color: 'var(--text-primary)' }}>Complété</div>
          </div>
          <div className="p-3" style={{ backgroundColor: 'var(--bg-secondary)', borderRadius: '.5rem' }}>
            <div className="text-meta">Acquisition</div>
            <div className="text-body" style={{ color: 'var(--text-primary)' }}>Semaine 28</div>
          </div>
          <div className="p-3" style={{ backgroundColor: 'var(--bg-secondary)', borderRadius: '.5rem' }}>
            <div className="text-meta">Analyse</div>
            <div className="text-body" style={{ color: 'var(--text-primary)' }}>En cours</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
