import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import SystemStatus from '../components/SystemStatus';

const MainLayout: React.FC = () => {
  return (
    <div className="flex h-screen" style={{ backgroundColor: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-4 md:p-6" style={{ backgroundColor: 'var(--bg-primary)' }}>
          <div className="mx-auto w-full max-w-[79.4rem] golden-container">
            <Outlet />
          </div>
        </main>
      </div>
      <SystemStatus />
    </div>
  );
};

export default MainLayout;
