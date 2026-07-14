import React, { useState } from 'react';
import { Settings, Globe, Bell, Download, Trash2, Moon } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Switch } from '../ui/switch';

const SettingsPage = ({ language, setLanguage }) => {
  const [notifications, setNotifications] = useState(true);
  const [autoDownload, setAutoDownload] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const clearData = () => {
    localStorage.clear();
    alert(language === 'hi' ? 'डेटा साफ़ कर दिया गया' : 'Data cleared');
  };

  const settings = [
    {
      icon: Globe,
      title: language === 'hi' ? 'भाषा' : 'Language',
      description: language === 'hi' ? 'ऐप की भाषा चुनें' : 'Choose app language',
      action: (
        <Button 
          onClick={() => setLanguage(language === 'hi' ? 'en' : 'hi')}
          variant="outline"
          size="sm"
          className="border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
        >
          {language === 'hi' ? 'English' : 'हिंदी'}
        </Button>
      )
    },
    {
      icon: Bell,
      title: language === 'hi' ? 'सूचनाएं' : 'Notifications',
      description: language === 'hi' ? 'नई सामग्री की सूचना पाएं' : 'Get notified of new content',
      action: (
        <Switch 
          checked={notifications} 
          onCheckedChange={setNotifications}
        />
      )
    },
    {
      icon: Download,
      title: language === 'hi' ? 'ऑटो डाउनलोड' : 'Auto Download',
      description: language === 'hi' ? 'उत्तर स्वचालित रूप से सहेजें' : 'Automatically save answers',
      action: (
        <Switch 
          checked={autoDownload} 
          onCheckedChange={setAutoDownload}
        />
      )
    },
    {
      icon: Moon,
      title: language === 'hi' ? 'डार्क मोड' : 'Dark Mode',
      description: language === 'hi' ? 'डार्क थीम का उपयोग करें' : 'Use dark theme',
      action: (
        <Switch 
          checked={darkMode} 
          onCheckedChange={setDarkMode}
        />
      )
    }
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="px-4 py-8 sm:px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Settings className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">
            {language === 'hi' ? 'सेटिंग्स' : 'Settings'}
          </h1>
          <p className="text-gray-400 text-sm">
            {language === 'hi' ? 'अपनी प्राथमिकताएं सेट करें' : 'Customize your preferences'}
          </p>
        </div>

        {/* Settings List */}
        <div className="space-y-4 mb-8">
          {settings.map((setting, index) => {
            const Icon = setting.icon;
            return (
              <Card key={index} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-start gap-4">
                      <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0">
                        <Icon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h3 className="text-white font-semibold mb-1">{setting.title}</h3>
                        <p className="text-gray-400 text-sm">{setting.description}</p>
                      </div>
                    </div>
                    <div className="flex-shrink-0">
                      {setting.action}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Danger Zone */}
        <Card className="bg-white/5 backdrop-blur-xl border border-red-500/20 rounded-2xl">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-3 text-lg">
              <Trash2 className="w-5 h-5 text-red-400" />
              {language === 'hi' ? 'डेटा प्रबंधन' : 'Data Management'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-400 text-sm mb-4 leading-relaxed">
              {language === 'hi' 
                ? 'यह सभी स्थानीय डेटा को हटा देगा, जिसमें आपकी खोज का इतिहास और पसंदीदा प्रश्न शामिल हैं।'
                : 'This will remove all local data including your search history and favorite questions.'
              }
            </p>
            <Button 
              onClick={clearData}
              variant="outline"
              className="border-red-500/30 text-red-400 hover:bg-red-500/10 rounded-xl w-full"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              {language === 'hi' ? 'सभी डेटा साफ़ करें' : 'Clear All Data'}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SettingsPage;