import React, { useEffect, useState } from 'react';
import { Settings, Globe, Bell, Download, Trash2, Moon, DownloadCloud } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Switch } from '../ui/switch';
import PageShell from '../Layout/PageShell';
import { readSettings, writeSettings } from '../../lib/practice';
import { notificationService } from '../../services/notificationService';

const SettingsPage = ({ language, setLanguage }) => {
  const [prefs, setPrefs] = useState(readSettings);
  const [canInstall, setCanInstall] = useState(false);
  const [installEvent, setInstallEvent] = useState(null);

  useEffect(() => {
    setPrefs(readSettings());
    const onPrompt = (event) => {
      event.preventDefault();
      setInstallEvent(event);
      setCanInstall(true);
    };
    window.addEventListener('beforeinstallprompt', onPrompt);
    return () => window.removeEventListener('beforeinstallprompt', onPrompt);
  }, []);

  const savePrefs = (patch) => {
    const next = { ...prefs, ...patch };
    setPrefs(next);
    writeSettings(next);
    if (patch.notifications) {
      notificationService.requestPermission();
    }
  };

  const clearData = () => {
    localStorage.clear();
    window.dispatchEvent(new Event('uttar-sewa-practice'));
    alert(language === 'hi' ? 'डेटा साफ़ कर दिया गया' : 'Data cleared');
  };

  const installApp = async () => {
    if (!installEvent) return;
    installEvent.prompt();
    await installEvent.userChoice;
    setInstallEvent(null);
    setCanInstall(false);
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
          className="border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
        >
          {language === 'hi' ? 'English' : 'हिंदी'}
        </Button>
      )
    },
    {
      icon: Bell,
      title: language === 'hi' ? 'सूचनाएं' : 'Notifications',
      description: language === 'hi' ? 'माला पूर्ण और संध्या की सूचना' : 'Mala complete and sandhya reminders',
      action: (
        <Switch
          checked={Boolean(prefs.notifications)}
          onCheckedChange={(value) => savePrefs({ notifications: value })}
        />
      )
    },
    {
      icon: Download,
      title: language === 'hi' ? 'ऑटो डाउनलोड' : 'Auto Download',
      description: language === 'hi' ? 'उत्तर स्वचालित रूप से सहेजें' : 'Automatically save answers',
      action: (
        <Switch
          checked={Boolean(prefs.autoDownload)}
          onCheckedChange={(value) => savePrefs({ autoDownload: value })}
        />
      )
    },
    {
      icon: Moon,
      title: language === 'hi' ? 'डार्क मोड' : 'Dark Mode',
      description: language === 'hi' ? 'डार्क थीम का उपयोग करें' : 'Use dark theme',
      action: (
        <Switch
          checked={Boolean(prefs.darkMode)}
          onCheckedChange={(value) => savePrefs({ darkMode: value })}
        />
      )
    }
  ];

  return (
    <PageShell>
      <div>
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

        <Card className="bg-white/5 border border-white/10 rounded-2xl mb-6">
          <CardContent className="p-4 text-sm text-gray-300 leading-relaxed">
            {language === 'hi'
              ? 'माला गोल इस ऐप पर हमेशा तैरता है। टैप = मनका, 2.5 सेकंड दबाएँ = चैट। माइक्रोफ़ोन की अनुमति पहली बार बोलने पर माँगी जाएगी। अन्य ऐप्स के ऊपर तैरना केवल Android नेटिव शेल में संभव है; iPhone इसकी अनुमति नहीं देता।'
              : 'The mala orb always floats inside this app. Tap = bead, hold 2.5s = chat. Microphone permission is requested the first time you speak. Drawing over other apps is only possible in an Android native shell; iPhone does not allow it.'}
          </CardContent>
        </Card>

        {canInstall && (
          <Card className="bg-white/5 border border-white/10 rounded-2xl mb-6">
            <CardContent className="p-4">
              <Button onClick={installApp} className="w-full bg-white text-black hover:bg-gray-100">
                <DownloadCloud className="w-4 h-4 mr-2" />
                {language === 'hi' ? 'होम स्क्रीन पर जोड़ें' : 'Add to Home Screen'}
              </Button>
            </CardContent>
          </Card>
        )}

        <div className="space-y-4 mb-8">
          {settings.map((setting, index) => {
            const Icon = setting.icon;
            return (
              <Card key={index} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
                <CardContent className="p-4">
                  <div className="settings-row">
                    <div className="flex items-start gap-4 min-w-0">
                      <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0">
                        <Icon className="w-5 h-5 text-white" />
                      </div>
                      <div className="min-w-0">
                        <h3 className="text-white font-semibold mb-1">{setting.title}</h3>
                        <p className="text-gray-400 text-sm">{setting.description}</p>
                      </div>
                    </div>
                    <div className="flex-shrink-0 self-end sm:self-auto">
                      {setting.action}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

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
    </PageShell>
  );
};

export default SettingsPage;
