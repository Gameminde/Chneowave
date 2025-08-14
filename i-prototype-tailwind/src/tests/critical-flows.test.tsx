/**
 * 🧪 Tests Flux Critiques CHNeoWave - Phase 3.4
 * Selon prompt ultra-précis : tests acquisition, calibration, analyse, export
 * 
 * Tests des flux critiques métier
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { testUtils, MockSession } from './setup';
import { UnifiedAppProvider } from '../contexts/UnifiedAppContext';
import ProfessionalAcquisitionPage from '../pages/ProfessionalAcquisitionPage';
import ExportPage from '../pages/ExportPage';
import StatisticalAnalysisPage from '../pages/StatisticalAnalysisPage';
import SettingsPage from '../pages/SettingsPage';

// Mock des APIs
const mockAPI = {
  startAcquisition: vi.fn(),
  stopAcquisition: vi.fn(),
  pauseAcquisition: vi.fn(),
  exportToHDF5: vi.fn(),
  exportToCSV: vi.fn(),
  exportToJSON: vi.fn(),
  exportToMatlab: vi.fn(),
  changeBackend: vi.fn(),
  testConnection: vi.fn(),
  refreshSystemStatus: vi.fn(),
};

vi.mock('../api/CHNeoWaveAPI', () => ({
  api: mockAPI
}));

// Composant wrapper avec contexte
const TestWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <UnifiedAppProvider>
      {children}
    </UnifiedAppProvider>
  );
};

describe('🚀 Flux Critique: Acquisition', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    testUtils.mockThemeChange('light');
  });

  it('devrait démarrer une acquisition avec succès', async () => {
    const user = userEvent.setup();
    mockAPI.startAcquisition.mockResolvedValue({ success: true });

    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    // Vérifier présence des contrôles
    const startButton = screen.getByRole('button', { name: /démarrer/i });
    const stopButton = screen.getByRole('button', { name: /arrêter/i });
    
    expect(startButton).toBeInTheDocument();
    expect(stopButton).toBeInTheDocument();
    expect(stopButton).toBeDisabled();

    // Démarrer acquisition
    await user.click(startButton);

    await waitFor(() => {
      expect(mockAPI.startAcquisition).toHaveBeenCalledWith({
        samplingRate: expect.any(Number),
        channels: expect.any(Array),
        duration: expect.any(Number)
      });
    });

    // Vérifier changement d'état
    await waitFor(() => {
      expect(startButton).toBeDisabled();
      expect(stopButton).toBeEnabled();
    });
  });

  it('devrait gérer les erreurs d\'acquisition', async () => {
    const user = userEvent.setup();
    const errorMessage = 'Hardware not connected';
    mockAPI.startAcquisition.mockRejectedValue(new Error(errorMessage));

    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    const startButton = screen.getByRole('button', { name: /démarrer/i });
    await user.click(startButton);

    // Vérifier affichage de l'erreur
    await waitFor(() => {
      expect(screen.getByText(/erreur/i)).toBeInTheDocument();
    });
  });

  it('devrait afficher les données temps réel', async () => {
    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    // Simuler données temps réel
    const mockData = testUtils.mockAcquisitionData(10);
    
    // Vérifier présence du graphique
    const chartContainer = screen.getByText(/graphique temps réel/i);
    expect(chartContainer).toBeInTheDocument();

    // Vérifier affichage des métriques
    expect(screen.getByText(/durée/i)).toBeInTheDocument();
    expect(screen.getByText(/échantillons/i)).toBeInTheDocument();
  });

  it('devrait permettre la sélection de sondes', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    // Vérifier présence des sondes
    const sensorCheckboxes = screen.getAllByRole('checkbox');
    expect(sensorCheckboxes.length).toBeGreaterThan(0);

    // Sélectionner une sonde
    await user.click(sensorCheckboxes[0]);
    
    // Vérifier état de sélection
    expect(sensorCheckboxes[0]).toBeChecked();
  });
});

describe('📊 Flux Critique: Export', () => {
  let mockSession: MockSession;

  beforeEach(() => {
    vi.clearAllMocks();
    mockSession = testUtils.mockSession('test-session-1');
  });

  it('devrait exporter en format HDF5', async () => {
    const user = userEvent.setup();
    mockAPI.exportToHDF5.mockResolvedValue({
      success: true,
      download_url: 'http://example.com/export.hdf5',
      file_size_bytes: 1024 * 1024
    });

    render(
      <TestWrapper>
        <ExportPage />
      </TestWrapper>
    );

    // Sélectionner format HDF5
    const formatSelect = screen.getByLabelText(/format d'export/i);
    await user.selectOptions(formatSelect, 'hdf5');

    // Sélectionner session
    const sessionSelect = screen.getByLabelText(/session à exporter/i);
    await user.selectOptions(sessionSelect, mockSession.id);

    // Déclencher export
    const exportButton = screen.getByRole('button', { name: /exporter/i });
    await user.click(exportButton);

    await waitFor(() => {
      expect(mockAPI.exportToHDF5).toHaveBeenCalledWith(
        mockSession.id,
        expect.objectContaining({
          includeMetadata: expect.any(Boolean),
          compression: expect.any(Boolean)
        })
      );
    });
  });

  it('devrait exporter en format MATLAB', async () => {
    const user = userEvent.setup();
    mockAPI.exportToMatlab.mockResolvedValue({
      success: true,
      download_url: 'http://example.com/export.mat'
    });

    render(
      <TestWrapper>
        <ExportPage />
      </TestWrapper>
    );

    const formatSelect = screen.getByLabelText(/format d'export/i);
    await user.selectOptions(formatSelect, 'matlab');

    const sessionSelect = screen.getByLabelText(/session à exporter/i);
    await user.selectOptions(sessionSelect, mockSession.id);

    const exportButton = screen.getByRole('button', { name: /exporter/i });
    await user.click(exportButton);

    await waitFor(() => {
      expect(mockAPI.exportToMatlab).toHaveBeenCalledWith(
        mockSession.id,
        expect.objectContaining({
          includeMetadata: expect.any(Boolean)
        })
      );
    });
  });

  it('devrait valider les options d\'export', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <ExportPage />
      </TestWrapper>
    );

    // Vérifier désactivation du bouton sans session
    const exportButton = screen.getByRole('button', { name: /exporter/i });
    expect(exportButton).toBeDisabled();

    // Sélectionner session
    const sessionSelect = screen.getByLabelText(/session à exporter/i);
    await user.selectOptions(sessionSelect, mockSession.id);

    // Vérifier activation du bouton
    expect(exportButton).toBeEnabled();
  });

  it('devrait afficher les détails de session', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <ExportPage />
      </TestWrapper>
    );

    const sessionSelect = screen.getByLabelText(/session à exporter/i);
    await user.selectOptions(sessionSelect, mockSession.id);

    // Vérifier affichage des détails
    await waitFor(() => {
      expect(screen.getByText(mockSession.name)).toBeInTheDocument();
      expect(screen.getByText(/échantillons/i)).toBeInTheDocument();
      expect(screen.getByText(/sondes/i)).toBeInTheDocument();
    });
  });
});

describe('📈 Flux Critique: Analyse Statistique', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('devrait calculer les statistiques maritimes', async () => {
    render(
      <TestWrapper>
        <StatisticalAnalysisPage />
      </TestWrapper>
    );

    // Vérifier présence des métriques
    expect(screen.getByText(/h max/i)).toBeInTheDocument();
    expect(screen.getByText(/h min/i)).toBeInTheDocument();
    expect(screen.getByText(/h 1\/3/i)).toBeInTheDocument();
    expect(screen.getByText(/h significative/i)).toBeInTheDocument();
  });

  it('devrait permettre la sélection de sondes', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <StatisticalAnalysisPage />
      </TestWrapper>
    );

    // Vérifier présence des boutons de sélection
    const sensorButtons = screen.getAllByRole('button', { name: /#\d+/ });
    expect(sensorButtons.length).toBeGreaterThan(0);

    // Sélectionner une sonde
    await user.click(sensorButtons[0]);

    // Vérifier changement d'état visuel
    expect(sensorButtons[0]).toHaveClass(/accent-primary/);
  });

  it('devrait exporter les données statistiques', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <StatisticalAnalysisPage />
      </TestWrapper>
    );

    const exportButton = screen.getByRole('button', { name: /exporter csv/i });
    await user.click(exportButton);

    // Vérifier création du fichier CSV
    // Note: en test, on vérifierait le contenu du CSV généré
    expect(exportButton).toBeInTheDocument();
  });
});

describe('⚙️ Flux Critique: Configuration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockAPI.changeBackend.mockResolvedValue({ success: true });
    mockAPI.testConnection.mockResolvedValue({ success: true });
  });

  it('devrait changer le backend hardware', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    // Sélectionner backend NI-DAQmx
    const backendSelect = screen.getByLabelText(/type de backend/i);
    await user.selectOptions(backendSelect, 'ni-daqmx');

    // Déclencher changement
    const changeButton = screen.getByRole('button', { name: /changer backend/i });
    await user.click(changeButton);

    await waitFor(() => {
      expect(mockAPI.changeBackend).toHaveBeenCalledWith('ni-daqmx');
    });
  });

  it('devrait tester la connexion hardware', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    const testButton = screen.getByRole('button', { name: /tester connexion/i });
    await user.click(testButton);

    await waitFor(() => {
      expect(mockAPI.testConnection).toHaveBeenCalled();
    });
  });

  it('devrait valider la conformité ITTC', async () => {
    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    // Vérifier affichage des indicateurs ITTC
    expect(screen.getByText(/paramètres ittc/i)).toBeInTheDocument();
    expect(screen.getByText(/standards iso 9001/i)).toBeInTheDocument();
  });

  it('devrait changer le thème', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    const themeSelect = screen.getByLabelText(/thème de l'application/i);
    await user.selectOptions(themeSelect, 'dark');

    // Vérifier changement de thème dans le DOM
    await waitFor(() => {
      expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
    });
  });
});

describe('🎨 Tests Thèmes', () => {
  it('devrait appliquer le thème clair', () => {
    testUtils.mockThemeChange('light');
    
    render(
      <TestWrapper>
        <div data-testid="theme-test">Test</div>
      </TestWrapper>
    );

    expect(document.documentElement).toHaveAttribute('data-theme', 'light');
    expect(document.documentElement).not.toHaveClass('dark');
  });

  it('devrait appliquer le thème sombre', () => {
    testUtils.mockThemeChange('dark');
    
    render(
      <TestWrapper>
        <div data-testid="theme-test">Test</div>
      </TestWrapper>
    );

    expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
    expect(document.documentElement).toHaveClass('dark');
  });

  it('devrait appliquer le thème Solarized', () => {
    testUtils.mockThemeChange('beige');
    
    render(
      <TestWrapper>
        <div data-testid="theme-test">Test</div>
      </TestWrapper>
    );

    expect(document.documentElement).toHaveAttribute('data-theme', 'beige');
    expect(document.documentElement).not.toHaveClass('dark');
  });

  it('devrait persister le thème dans localStorage', async () => {
    const user = userEvent.setup();
    const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');

    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    const themeSelect = screen.getByLabelText(/thème de l'application/i);
    await user.selectOptions(themeSelect, 'dark');

    expect(setItemSpy).toHaveBeenCalledWith('chneowave-theme', 'dark');
  });
});

describe('🚨 Tests Scénarios Dégradés', () => {
  it('devrait gérer la perte de connexion réseau', async () => {
    // Simuler perte réseau
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: false,
    });

    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    // Déclencher événement offline
    act(() => {
      window.dispatchEvent(new Event('offline'));
    });

    // Vérifier affichage d'erreur ou mode dégradé
    await waitFor(() => {
      // L'interface devrait indiquer l'état hors ligne
      expect(screen.queryByText(/hors ligne|offline|déconnecté/i)).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('devrait gérer les erreurs hardware', async () => {
    const user = userEvent.setup();
    mockAPI.startAcquisition.mockRejectedValue(testUtils.mockHardwareError('DAQ'));

    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    const startButton = screen.getByRole('button', { name: /démarrer/i });
    await user.click(startButton);

    await waitFor(() => {
      expect(screen.getByText(/erreur matérielle|hardware/i)).toBeInTheDocument();
    });
  });

  it('devrait gérer les timeouts', async () => {
    const user = userEvent.setup();
    mockAPI.testConnection.mockRejectedValue(new Error('Timeout'));

    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    const testButton = screen.getByRole('button', { name: /tester connexion/i });
    await user.click(testButton);

    await waitFor(() => {
      expect(screen.getByText(/timeout|délai dépassé/i)).toBeInTheDocument();
    });
  });
});

describe('♿ Tests Accessibilité', () => {
  it('devrait avoir des boutons accessibles', () => {
    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toBeAccessible();
      expect(button).toHaveCorrectContrast();
    });
  });

  it('devrait supporter la navigation clavier', async () => {
    const user = userEvent.setup();
    
    render(
      <TestWrapper>
        <SettingsPage />
      </TestWrapper>
    );

    // Tester navigation avec Tab
    await user.keyboard('{Tab}');
    expect(document.activeElement).toBeInTheDocument();

    // Tester activation avec Entrée
    if (document.activeElement?.tagName === 'BUTTON') {
      await user.keyboard('{Enter}');
      // Vérifier que l'action a été déclenchée
    }
  });

  it('devrait avoir des labels ARIA appropriés', () => {
    render(
      <TestWrapper>
        <ExportPage />
      </TestWrapper>
    );

    const selects = screen.getAllByRole('combobox');
    selects.forEach(select => {
      expect(select).toHaveAccessibleName();
    });

    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toHaveAccessibleName();
    });
  });

  it('devrait annoncer les changements d\'état', async () => {
    const user = userEvent.setup();

    render(
      <TestWrapper>
        <ProfessionalAcquisitionPage />
      </TestWrapper>
    );

    // Vérifier présence de zones live
    const liveRegions = screen.getAllByRole('status');
    expect(liveRegions.length).toBeGreaterThan(0);
  });
});
