import React, { useState } from 'react';
import { Menu, X, User, FileText, Info, Settings, Home, Search, Database, Heart, BarChart3, MessageCircle } from 'lucide-react';
import { Button } from '../ui/button';
import LanguageToggle from '../LanguageToggle';
import { t } from '../../utils/translations';

const AppLayout = ({ children, currentView, setCurrentView, language, setLanguage }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const menuItems = [
    { id: 'chat', icon: MessageCircle, label: language === 'hi' ? 'चैट' : 'Chat' },
    { id: 'search', icon: Search, label: t('search', language) },
    { id: 'processing', icon: Database, label: t('processing', language) },
    { id: 'favorites', icon: Heart, label: language === 'hi' ? 'पसंदीदा' : 'Favorites' },
    { id: 'admin', icon: BarChart3, label: language === 'hi' ? 'एडमिन' : 'Admin' },
    { id: 'profile', icon: User, label: language === 'hi' ? 'प्रोफाइल' : 'Profile' },
    { id: 'about', icon: Info, label: language === 'hi' ? 'हमारे बारे में' : 'About' },
    { id: 'terms', icon: FileText, label: language === 'hi' ? 'नियम एवं शर्तें' : 'Terms & Conditions' },
    { id: 'settings', icon: Settings, label: language === 'hi' ? 'सेटिंग्स' : 'Settings' }
  ];

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleMenuClick = (itemId) => {
    setCurrentView(itemId);
    setIsMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden">
      {/* Mobile Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass-card border-b border-white/10">
        <div className="flex items-center justify-between p-4">
          {/* Hamburger Menu */}
          <Button
            onClick={toggleMenu}
            variant="ghost"
            size="sm"
            className="p-2 text-white hover:bg-white/10 rounded-xl interactive"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </Button>

          {/* App Title */}
          <h1 className="text-lg font-bold text-center flex-1 px-4 text-gradient">
            {language === 'hi' ? 'आध्यात्मिक खोज' : 'Spiritual Search'}
          </h1>

          {/* Language Toggle */}
          <LanguageToggle language={language} setLanguage={setLanguage} />
        </div>
      </header>

      {/* Slide-out Menu */}
      <div className={`fixed inset-0 z-40 transform transition-transform duration-300 ease-in-out ${
        isMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        {/* Backdrop */}
        <div 
          className="absolute inset-0 bg-black/60 backdrop-blur-sm"
          onClick={toggleMenu}
        />
        
        {/* Menu Content */}
        <div className="relative w-80 max-w-[85vw] h-full glass-strong border-r border-white/10 slide-in">
          {/* Menu Header */}
          <div className="p-6 border-b border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-white/20 to-white/5 rounded-xl flex items-center justify-center">
                <Home className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white text-gradient">
                  {language === 'hi' ? 'आध्यात्मिक ज्ञान' : 'Spiritual Knowledge'}
                </h2>
                <p className="text-sm text-gray-400">
                  {language === 'hi' ? 'मेनू' : 'Menu'}
                </p>
              </div>
            </div>
          </div>

          {/* Menu Items */}
          <nav className="p-4 space-y-2 custom-scrollbar overflow-y-auto" style={{ height: 'calc(100vh - 180px)' }}>
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              
              return (
                <button
                  key={item.id}
                  onClick={() => handleMenuClick(item.id)}
                  className={`w-full flex items-center gap-4 p-4 rounded-xl transition-all duration-200 interactive ${
                    isActive 
                      ? 'glass-strong text-white border border-white/20' 
                      : 'text-gray-300 hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                  {item.id === 'chat' && (
                    <div className="ml-auto w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  )}
                  {item.id === 'favorites' && (
                    <div className="ml-auto w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
                  )}
                  {item.id === 'admin' && (
                    <div className="ml-auto w-2 h-2 bg-blue-400 rounded-full"></div>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Menu Footer */}
          <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-white/10 glass-card">
            <div className="text-center text-sm text-gray-400">
              <p>{language === 'hi' ? 'संस्करण 2.0.0' : 'Version 2.0.0'}</p>
              <p className="mt-1 text-xs">
                {language === 'hi' ? '900+ आध्यात्मिक वीडियो' : '900+ Spiritual Videos'}
              </p>
              <div className="flex items-center justify-center gap-2 mt-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-xs">{language === 'hi' ? 'ऑनलाइन' : 'Online'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="pt-16 gpu-accelerated">
        {children}
      </main>
    </div>
  );
};

export default AppLayout;