import React, { useEffect, useState } from 'react';
import { User, Settings, Heart, Star, CircleDot, Share2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import PageShell from '../Layout/PageShell';
import { readLocalPracticeStats, shareCard } from '../../lib/practice';

const ProfilePage = ({ language, setCurrentView }) => {
  const [stats, setStats] = useState({ favorites: 0, searches: 0, beads: 0 });

  useEffect(() => {
    setStats(readLocalPracticeStats());
  }, []);

  const cards = [
    {
      icon: Heart,
      value: String(stats.favorites),
      label: language === 'hi' ? 'पसंदीदा प्रश्न' : 'Favorite Questions',
    },
    {
      icon: Star,
      value: String(stats.searches),
      label: language === 'hi' ? 'खोजे गए प्रश्न' : 'Questions Searched',
    },
    {
      icon: CircleDot,
      value: String(stats.beads),
      label: language === 'hi' ? 'आज तक के मनके' : 'Beads counted',
    },
  ];

  const shareApp = async () => {
    await shareCard({
      question: language === 'hi' ? 'उत्तर सेवा' : 'Uttar Sewa',
      answer: language === 'hi'
        ? 'प्रवचनों से पूछें, माला साथ रखें।'
        : 'Ask from the discourses. Keep a mala in hand.',
      timestampUrl: window.location.origin,
    });
  };

  return (
    <PageShell>
      <div>
        <Card className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl mb-6">
          <CardHeader className="text-center">
            <div className="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <User className="w-10 h-10 text-white" />
            </div>
            <CardTitle className="text-xl text-white">
              {language === 'hi' ? 'आध्यात्मिक साधक' : 'Spiritual Seeker'}
            </CardTitle>
            <p className="text-gray-400 text-sm">
              {language === 'hi'
                ? 'आध्यात्मिक ज्ञान की खोज में'
                : 'In search of spiritual wisdom'
              }
            </p>
          </CardHeader>
        </Card>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 mb-6">
          {cards.map((stat) => {
            const Icon = stat.icon;
            return (
              <Card key={stat.label} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
                <CardContent className="p-4 text-center">
                  <Icon className="w-6 h-6 text-white mx-auto mb-2" />
                  <div className="text-lg font-bold text-white">{stat.value}</div>
                  <div className="text-xs text-gray-400">{stat.label}</div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <Card className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
          <CardHeader>
            <CardTitle className="text-white text-lg">
              {language === 'hi' ? 'त्वरित कार्य' : 'Quick Actions'}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button
              variant="outline"
              className="w-full justify-start border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
              onClick={() => setCurrentView && setCurrentView('settings')}
            >
              <Settings className="w-4 h-4 mr-3" />
              {language === 'hi' ? 'सेटिंग्स' : 'Settings'}
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
              onClick={() => setCurrentView && setCurrentView('favorites')}
            >
              <Heart className="w-4 h-4 mr-3" />
              {language === 'hi' ? 'पसंदीदा प्रश्न' : 'Favorite Questions'}
            </Button>
            <Button
              variant="outline"
              className="w-full justify-start border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
              onClick={shareApp}
            >
              <Share2 className="w-4 h-4 mr-3" />
              {language === 'hi' ? 'ऐप साझा करें' : 'Share App'}
            </Button>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
};

export default ProfilePage;
