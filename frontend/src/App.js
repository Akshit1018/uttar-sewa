import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "./components/ui/toaster";
import AppLayout from "./components/Layout/AppLayout";
import ChatInterface from "./components/ChatInterface";
import SearchInterface from "./components/SearchInterface";
import ProcessingStatus from "./components/ProcessingStatus";
import FavoritesPage from "./components/FavoritesPage";
import AdminDashboard from "./components/AdminDashboard";
import ProfilePage from "./components/Pages/ProfilePage";
import AboutPage from "./components/Pages/AboutPage";
import TermsPage from "./components/Pages/TermsPage";
import SettingsPage from "./components/Pages/SettingsPage";
import { analyticsService } from "./services/analyticsService";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MainApp = () => {
  const [currentView, setCurrentView] = useState('chat');
  const [stats, setStats] = useState(null);
  const [language, setLanguage] = useState('hi'); // Default to Hindi as requested

  useEffect(() => {
    loadStats();
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage) {
      setLanguage(savedLanguage);
    }

    // Initialize analytics
    analyticsService.trackPageView('app_start');
    
    // Handle PWA shortcuts
    const urlParams = new URLSearchParams(window.location.search);
    const shortcut = urlParams.get('shortcut');
    if (shortcut) {
      setCurrentView(shortcut);
    }

    // Register service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
        .then(registration => {
          console.log('SW registered: ', registration);
        })
        .catch(registrationError => {
          console.log('SW registration failed: ', registrationError);
        });
    }

    // Handle app install prompt
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      // You can show install button here
    });

    // Performance monitoring
    if (window.performance && window.performance.timing) {
      window.addEventListener('load', () => {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        analyticsService.trackPerformance('page_load_time', loadTime);
      });
    }

  }, []);

  useEffect(() => {
    localStorage.setItem('preferredLanguage', language);
    analyticsService.trackLanguageChange(
      localStorage.getItem('previousLanguage') || 'en', 
      language
    );
    localStorage.setItem('previousLanguage', language);
  }, [language]);

  const loadStats = async () => {
    try {
      const response = await fetch(`${API}/stats`);
      const data = await response.json();
      setStats(data);
      
      // If no videos are processed and user is on search, suggest processing
      if (data.processed_videos === 0 && (currentView === 'search' || currentView === 'chat')) {
        // Don't force switch to processing, just suggest it in the UI
      }
    } catch (error) {
      console.error('Error loading stats:', error);
      analyticsService.trackError('stats_load_error', error.message, { context: 'main_app' });
    }
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'chat':
        return <ChatInterface language={language} />;
      case 'search':
        return <SearchInterface language={language} />;
      case 'processing':
        return <ProcessingStatus language={language} />;
      case 'favorites':
        return <FavoritesPage language={language} />;
      case 'admin':
        return <AdminDashboard language={language} />;
      case 'profile':
        return <ProfilePage language={language} />;
      case 'about':
        return <AboutPage language={language} />;
      case 'terms':
        return <TermsPage language={language} />;
      case 'settings':
        return <SettingsPage language={language} setLanguage={setLanguage} />;
      default:
        return <ChatInterface language={language} />;
    }
  };

  return (
    <AppLayout 
      currentView={currentView} 
      setCurrentView={setCurrentView}
      language={language}
      setLanguage={setLanguage}
    >
      {renderCurrentView()}
      {/* Fix notification positioning - move below header with proper z-index */}
      <div className="fixed top-16 left-0 right-0 z-30 pointer-events-none">
        <Toaster />
      </div>
    </AppLayout>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainApp />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;