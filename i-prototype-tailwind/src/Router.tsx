import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import DashboardPage from './pages/DashboardPage';
import ProjectPage from './pages/ProjectPage';
import CalibrationPage from './pages/CalibrationPage';
import AcquisitionPage from './pages/AcquisitionPage';
import AdvancedAnalysisPage from './pages/AdvancedAnalysisPage';
import StatisticalAnalysisPage from './pages/StatisticalAnalysisPage';
import ExportPage from './pages/ExportPage';
import SettingsPage from './pages/SettingsPage';

// Import des nouvelles pages professionnelles
import ProfessionalAcquisitionPage from './pages/ProfessionalAcquisitionPage';
import ProfessionalCalibrationPage from './pages/ProfessionalCalibrationPage';
import ProfessionalAnalysisPage from './pages/ProfessionalAnalysisPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'project', element: <ProjectPage /> },
      
      // Pages professionnelles (nouvelles versions)
      { path: 'calibration', element: <ProfessionalCalibrationPage /> },
      { path: 'acquisition', element: <ProfessionalAcquisitionPage /> },
      { path: 'analysis', element: <ProfessionalAnalysisPage /> },
      
      // Pages existantes
      { path: 'statistics', element: <StatisticalAnalysisPage /> },
      { path: 'export', element: <ExportPage /> },
      { path: 'settings', element: <SettingsPage /> },
      
      // Pages anciennes (pour comparaison/backup)
      { path: 'calibration-old', element: <CalibrationPage /> },
      { path: 'acquisition-old', element: <AcquisitionPage /> },
      { path: 'analysis-old', element: <AdvancedAnalysisPage /> },
    ],
  },
]);

const Router: React.FC = () => {
  return <RouterProvider router={router} future={{ v7_startTransition: true }} />;
};

export default Router;
