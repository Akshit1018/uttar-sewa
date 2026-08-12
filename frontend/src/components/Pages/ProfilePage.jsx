import React from 'react';
import { User, Settings, Heart, Star, Download, Share2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import PageShell from '../Layout/PageShell';

const ProfilePage = ({ language }) => {
  const stats = [
    { 
      icon: Heart, 
      value: '47', 
      label: language === 'hi' ? 'पसंदीदा प्रश्न' : 'Favorite Questions' 
    },
    { 
      icon: Star, 
      value: '156', 
      label: language === 'hi' ? 'खोजे गए प्रश्न' : 'Questions Searched' 
    },
    { 
      icon: Download, 
      value: '23', 
      label: language === 'hi' ? 'डाउनलोड किए गए' : 'Downloaded' 
    }
  ];

  return (
    <PageShell>
      <div>
        {/* Profile Header */}
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

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 mb-6">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <Card key={index} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
                <CardContent className="p-4 text-center">
                  <Icon className="w-6 h-6 text-white mx-auto mb-2" />
                  <div className="text-lg font-bold text-white">{stat.value}</div>
                  <div className="text-xs text-gray-400">{stat.label}</div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Quick Actions */}
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
            >
              <Settings className="w-4 h-4 mr-3" />
              {language === 'hi' ? 'सेटिंग्स' : 'Settings'}
            </Button>
            <Button 
              variant="outline" 
              className="w-full justify-start border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
            >
              <Heart className="w-4 h-4 mr-3" />
              {language === 'hi' ? 'पसंदीदा प्रश्न' : 'Favorite Questions'}
            </Button>
            <Button 
              variant="outline" 
              className="w-full justify-start border-white/20 text-gray-300 hover:bg-white/10 rounded-xl"
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