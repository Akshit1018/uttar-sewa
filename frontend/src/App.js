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
import SadhanaDashboard from "./components/SadhanaDashboard";
import JapaOrb from "./components/JapaOrb";
import JapaChatSheet from "./components/JapaChatSheet";
import { useMala } from "./hooks/useMala";
import { analyticsService } from "./services/analyticsService";
import { msUntil, nextSandhya, readPractice, readSettings } from "./lib/practice";
import { notificationService } from "./services/notificationService";

import { API } from './lib/backend';
import { useChannels } from './hooks/useChannels';

const MainApp = () => {
  const [currentView, setCurrentView] = useState('chat');
  const [stats, setStats] = useState(null);
  const [language, setLanguage] = useState('hi'); // Default to Hindi as requested
  const [chatOpen, setChatOpen] = useState(false);
  const { state: malaState, tap, undo, recordQuestion, practice, reload } = useMala(language);
  const { channelId } = useChannels();

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

    if (readSettings().notifications || readPractice().sandhya) {
      notificationService.requestPermission();
    }

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

  useEffect(() => {
    let sentinel;
    const lock = async () => {
      if (!practice.japaFocus || !navigator.wakeLock) return;
      try {
        sentinel = await navigator.wakeLock.request('screen');
      } catch (error) {
        // unsupported or battery saver
      }
    };
    lock();
    return () => {
      if (sentinel) sentinel.release();
    };
  }, [practice.japaFocus]);

  useEffect(() => {
    if (!practice.sandhya) return undefined;
    const upcoming = nextSandhya();
    const timer = setTimeout(() => {
      notificationService.showSandhyaNotification(upcoming.kind, language);
    }, msUntil(upcoming.at));
    return () => clearTimeout(timer);
  }, [practice.sandhya, language]);

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
        return <ChatInterface language={language} stats={stats} />;
      case 'sadhana':
        return <SadhanaDashboard language={language} state={malaState} onPracticeChange={reload} />;
      case 'search':
        return <SearchInterface language={language} />;
      case 'processing':
        return <ProcessingStatus language={language} />;
      case 'favorites':
        return <FavoritesPage language={language} />;
      case 'admin':
        return <AdminDashboard language={language} />;
      case 'profile':
        return <ProfilePage language={language} setCurrentView={setCurrentView} />;
      case 'about':
        return <AboutPage language={language} stats={stats} />;
      case 'terms':
        return <TermsPage language={language} />;
      case 'settings':
        return <SettingsPage language={language} setLanguage={setLanguage} />;
      default:
        return <ChatInterface language={language} stats={stats} />;
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
      <JapaOrb
        language={language}
        state={malaState}
        onTap={tap}
        onHold={() => setChatOpen(true)}
        onUndo={undo}
      />
      <JapaChatSheet
        language={language}
        open={chatOpen}
        onClose={() => setChatOpen(false)}
        onAsked={recordQuestion}
        channelId={channelId}
      />
      <Toaster />
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