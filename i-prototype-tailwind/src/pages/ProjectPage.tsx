import React, { useState } from 'react';

const ProjectPage: React.FC = () => {
  const [projectName, setProjectName] = useState('Nouveau Projet');
  const [description, setDescription] = useState('');
  const [engineer, setEngineer] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Project data submitted:', projectName, description, engineer);
    // In a real app, this would connect to the backend
  };

  return (
    <div className="p-6">
      <h1 className="font-semibold mb-6" style={{color: 'var(--text-primary)', fontSize: 'var(--text-3xl)'}}>Gestion de Projet</h1>
      <div className="p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
        <h2 className="font-semibold mb-4" style={{color: 'var(--text-primary)', fontSize: 'var(--text-xl)'}}>Historique des Projets</h2>
      </div>
      <div className="bg-white rounded-xl shadow-md p-6">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
              <h2 className="font-semibold mb-4" style={{color: 'var(--text-primary)', fontSize: 'var(--text-xl)'}}>Configuration du Projet</h2>
              <div className="space-y-4">
                <div>
                  <label className="block font-medium mb-2" style={{color: 'var(--text-secondary)', fontSize: 'var(--text-sm)'}}>
                    Nom du Projet
                  </label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    className="w-full px-3 py-2" 
                    style={{backgroundColor: 'var(--secondary-bg)', border: '1px solid var(--border-color)', color: 'var(--text-primary)'}}
                  />
                </div>
                <div>
                  <label className="block font-medium mb-2" style={{color: 'var(--text-secondary)', fontSize: 'var(--text-sm)'}}>
                    Description du Projet
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="w-full px-3 py-2" 
                    style={{backgroundColor: 'var(--secondary-bg)', border: '1px solid var(--border-color)', color: 'var(--text-primary)'}}
                  />
                </div>
                <div>
                  <label className="block font-medium mb-2" style={{color: 'var(--text-secondary)', fontSize: 'var(--text-sm)'}}>
                    Ingénieur Responsable
                  </label>
                  <input
                    type="text"
                    value={engineer}
                    onChange={(e) => setEngineer(e.target.value)}
                    className="w-full px-3 py-2" 
                    style={{backgroundColor: 'var(--secondary-bg)', border: '1px solid var(--border-color)', color: 'var(--text-primary)'}}
                    placeholder="Dr. Marine Dupont"
                  />
                </div>
              </div>
            </div>
            <div className="p-4" style={{backgroundColor: 'var(--primary-bg)', border: '1px solid var(--border-color)'}}>
              <h2 className="font-semibold mb-4" style={{color: 'var(--text-primary)', fontSize: 'var(--text-xl)'}}>Informations Supplémentaires</h2>
              {/* Add additional fields here */}
            </div>
          </div>
          <div className="flex space-x-4">
            <button className="w-full py-2 px-4 font-medium transition-colors" style={{backgroundColor: 'var(--accent-blue)', color: 'white'}}>
              Sauvegarder le Projet
            </button>
            <button
              type="button"
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-lg transition-colors"
            >
              Importer un Projet
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProjectPage;
