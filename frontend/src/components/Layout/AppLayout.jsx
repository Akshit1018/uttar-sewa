import React, { useState } from 'react';
import { Menu, X, User, FileText, Info, Settings, Home, Search, Database, Heart, BarChart3, MessageCircle, CircleDot, MoreHorizontal } from 'lucide-react';
import { Button } from '../ui/button';
import LanguageToggle from '../LanguageToggle';
import { t } from '../../utils/translations';

const AppLayout = ({ children, currentView, setCurrentView, language, setLanguage }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const menuItems = [
    { id: 'chat', icon: MessageCircle, label: language === 'hi' ? 'चैट' : 'Chat' },
    { id: 'sadhana', icon: CircleDot, label: language === 'hi' ? 'साधना' : 'Sadhana' },
    { id: 'search', icon: Search, label: t('search', language) },
    { id: 'favorites', icon: Heart, label: language === 'hi' ? 'पसंदीदा' : 'Favorites' },
    { id: 'processing', icon: Database, label: t('processing', language) },
    { id: 'admin', icon: BarChart3, label: language === 'hi' ? 'एडमिन' : 'Admin' },
    { id: 'profile', icon: User, label: language === 'hi' ? 'प्रोफाइल' : 'Profile' },
    { id: 'about', icon: Info, label: language === 'hi' ? 'हमारे बारे में' : 'About' },
    { id: 'terms', icon: FileText, label: language === 'hi' ? 'नियम' : 'Terms' },
    { id: 'settings', icon: Settings, label: language === 'hi' ? 'सेटिंग्स' : 'Settings' }
  ];

  const tabItems = menuItems.slice(0, 4);
  const moreActive = !tabItems.some((item) => item.id === currentView);

  const toggleMenu = () => setIsMenuOpen((open) => !open);

  const handleMenuClick = (itemId) => {
    setCurrentView(itemId);
    setIsMenuOpen(false);
  };

  const renderNavButtons = (items, compact = false) => items.map((item) => {
    const Icon = item.icon;
    const isActive = currentView === item.id;
    return (
      <button
        key={item.id}
        type="button"
        onClick={() => handleMenuClick(item.id)}
        className={`touch-target w-full flex items-center gap-3 rounded-xl transition-colors ${
          compact ? 'flex-col justify-center gap-1 px-1 py-2 text-[11px]' : 'p-3 text-sm'
        } ${
          isActive
            ? 'glass-strong text-white border border-white/20'
            : 'text-gray-300 hover:bg-white/5 hover:text-white'
        }`}
      >
        <Icon className={compact ? 'w-5 h-5' : 'w-5 h-5 shrink-0'} />
        <span className={`font-medium truncate ${compact ? 'max-w-full' : ''}`}>{item.label}</span>
      </button>
    );
  });

  return (
    <div className="app-frame bg-black text-white">
      <header className="app-header glass-card border-b border-white/10">
        <div className="flex items-center justify-between gap-2 px-3 py-2 sm:px-4 min-h-[3.5rem]">
          <Button
            onClick={toggleMenu}
            variant="ghost"
            size="icon"
            className="touch-target text-white hover:bg-white/10 rounded-xl lg:hidden"
            aria-label={language === 'hi' ? 'मेनू' : 'Menu'}
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </Button>
          <h1 className="text-base sm:text-lg font-bold text-center flex-1 px-2 text-gradient truncate">
            {language === 'hi' ? 'उत्तर सेवा' : 'Uttar Sewa'}
          </h1>
          <LanguageToggle language={language} setLanguage={setLanguage} />
        </div>
      </header>

      <aside className="app-sidebar glass-strong border-r border-white/10 hidden lg:flex flex-col">
        <div className="p-5 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 bg-white/10 rounded-xl flex items-center justify-center">
              <Home className="w-5 h-5" />
            </div>
            <div className="min-w-0">
              <h2 className="text-lg font-bold truncate">{language === 'hi' ? 'आध्यात्मिक ज्ञान' : 'Spiritual Knowledge'}</h2>
              <p className="text-xs text-gray-400">{language === 'hi' ? 'मेनू' : 'Menu'}</p>
            </div>
          </div>
        </div>
        <nav className="flex-1 overflow-y-auto p-3 space-y-1 custom-scrollbar">
          {renderNavButtons(menuItems)}
        </nav>
        <div className="p-4 border-t border-white/10 text-center text-xs text-gray-400">
          {language === 'hi' ? 'संस्करण 2.1.0' : 'Version 2.1.0'}
        </div>
      </aside>

      <div className={`app-drawer lg:hidden ${isMenuOpen ? 'is-open' : ''}`}>
        <div className="app-drawer-backdrop" onClick={toggleMenu} />
        <div className="app-drawer-panel glass-strong border-r border-white/10">
          <div className="p-5 border-b border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 bg-white/10 rounded-xl flex items-center justify-center">
                <Home className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-bold">{language === 'hi' ? 'आध्यात्मिक ज्ञान' : 'Spiritual Knowledge'}</h2>
                <p className="text-xs text-gray-400">{language === 'hi' ? 'मेनू' : 'Menu'}</p>
              </div>
            </div>
          </div>
          <nav className="flex-1 overflow-y-auto p-3 space-y-1 custom-scrollbar pb-8">
            {renderNavButtons(menuItems)}
          </nav>
        </div>
      </div>

      <main className="app-main">
        {children}
      </main>

      <nav className="app-tabbar lg:hidden glass-card border-t border-white/10" aria-label={language === 'hi' ? 'मुख्य नेविगेशन' : 'Main'}>
        {tabItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => handleMenuClick(item.id)}
              className={`touch-target flex flex-1 flex-col items-center justify-center gap-0.5 py-1 text-[11px] ${
                isActive ? 'text-white' : 'text-gray-400'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="truncate max-w-[4.5rem]">{item.label}</span>
            </button>
          );
        })}
        <button
          type="button"
          onClick={toggleMenu}
          className={`touch-target flex flex-1 flex-col items-center justify-center gap-0.5 py-1 text-[11px] ${
            moreActive || isMenuOpen ? 'text-white' : 'text-gray-400'
          }`}
        >
          <MoreHorizontal className="w-5 h-5" />
          <span>{language === 'hi' ? 'और' : 'More'}</span>
        </button>
      </nav>
    </div>
  );
};

export default AppLayout;
