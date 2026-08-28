import React from 'react';
import { BookOpen, Heart, Users, Zap } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import PageShell from '../Layout/PageShell';

const AboutPage = ({ language }) => {
  const features = [
    {
      icon: BookOpen,
      title: language === 'hi' ? 'इंजेस्टेड प्रवचन' : 'Ingested discourses',
      description: language === 'hi'
        ? 'जितने वीडियो इंजेस्ट हुए हैं, उतने ही उद्धृत हो सकते हैं — कोई 900+ दावा नहीं।'
        : 'Only ingested talks can be cited. There is no 900+ inventory claim.'
    },
    {
      icon: Zap,
      title: language === 'hi' ? 'उद्धृत खोज' : 'Extractive search',
      description: language === 'hi'
        ? 'उत्तर संग्रह से नकल होते हैं; मॉडल नया उपदेश नहीं लिखता।'
        : 'Answers are copied from the corpus. The model does not invent teaching.'
    },
    {
      icon: Heart,
      title: language === 'hi' ? 'साधना माला' : 'Sadhana mala',
      description: language === 'hi'
        ? 'गोल पर टैप = मनका। 108 = एक माला। दबाकर प्रवचन से पूछें।'
        : 'Tap the orb for a bead. 108 is one mala. Hold to ask from the discourses.'
    },
    {
      icon: Users,
      title: language === 'hi' ? 'बहुभाषी समर्थन' : 'Multilingual Support',
      description: language === 'hi' 
        ? 'हिंदी और अंग्रेजी दोनों भाषाओं में प्रश्न पूछें' 
        : 'Ask questions in both Hindi and English'
    }
  ];

  return (
    <PageShell>
      <div>
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <BookOpen className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">
            {language === 'hi' ? 'आध्यात्मिक ज्ञान खोज' : 'Spiritual Knowledge Search'}
          </h1>
          <p className="text-gray-400 max-w-md mx-auto leading-relaxed">
            {language === 'hi' 
              ? 'श्री हित प्रेमानंद गोविंद शरण जी महाराज के प्रवचनों से तुरंत आध्यात्मिक मार्गदर्शन प्राप्त करें'
              : 'Get instant spiritual guidance from Shri Hit Premanand Govind Sharan Ji Maharaj\'s discourses'
            }
          </p>
        </div>

        {/* Features */}
        <div className="space-y-4 mb-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
                <CardContent className="p-4">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0">
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-white font-semibold mb-2">{feature.title}</h3>
                      <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Mission */}
        <Card className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
          <CardHeader>
            <CardTitle className="text-white text-lg">
              {language === 'hi' ? 'हमारा उद्देश्य' : 'Our Mission'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-300 leading-relaxed text-sm">
              {language === 'hi'
                ? 'लक्ष्य है प्रवचनों को समय-चिह्न के साथ खोजना। उत्तर तभी मिलता है जब संग्रह में मिलान हो; नहीं तो ऐप मना कर देता है। सार्वजनिक गीता/विकिपीडिया साथी पाठ अलग से चिह्नित रहते हैं।'
                : 'The goal is to find discourses with timestamps. An answer appears only when the corpus matches; otherwise the app refuses. Public Gita/Wikipedia companions stay labeled separately.'
              }
            </p>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
};

export default AboutPage;