import React from 'react';
import { Globe } from 'lucide-react';

const LanguageToggle = ({ language, setLanguage }) => {
  const toggleLanguage = () => {
    setLanguage(language === 'hi' ? 'en' : 'hi');
  };

  return (
    <button
      type="button"
      onClick={toggleLanguage}
      className="touch-target flex items-center justify-center gap-1.5 px-2.5 text-white hover:bg-white/10 rounded-xl transition-all duration-200 shrink-0"
      aria-label={language === 'hi' ? 'Switch to English' : 'हिंदी में बदलें'}
    >
      <Globe className="w-4 h-4" />
      <span className="text-sm font-medium">
        {language === 'hi' ? 'EN' : 'हि'}
      </span>
    </button>
  );
};

export default LanguageToggle;
