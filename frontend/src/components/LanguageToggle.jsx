import React from 'react';
import { Globe } from 'lucide-react';

const LanguageToggle = ({ language, setLanguage }) => {
  const toggleLanguage = () => {
    setLanguage(language === 'hi' ? 'en' : 'hi');
  };

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 p-2 text-white hover:bg-white/10 rounded-xl transition-all duration-200"
    >
      <Globe className="w-4 h-4" />
      <span className="text-sm font-medium">
        {language === 'hi' ? 'EN' : 'हि'}
      </span>
    </button>
  );
};

export default LanguageToggle;