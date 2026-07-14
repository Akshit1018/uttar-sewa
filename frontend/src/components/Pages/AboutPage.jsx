import React from 'react';
import { BookOpen, Heart, Users, Zap } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

const AboutPage = ({ language }) => {
  const features = [
    {
      icon: BookOpen,
      title: language === 'hi' ? '900+ आध्यात्मिक वीडियो' : '900+ Spiritual Videos',
      description: language === 'hi' 
        ? 'गुरुजी के सभी प्रवचनों से तुरंत उत्तर प्राप्त करें' 
        : 'Get instant answers from all spiritual discourses'
    },
    {
      icon: Zap,
      title: language === 'hi' ? 'तुरंत खोज' : 'Instant Search',
      description: language === 'hi' 
        ? 'AI की मदद से सेकंडों में प्रासंगिक उत्तर पाएं' 
        : 'Get relevant answers in seconds with AI assistance'
    },
    {
      icon: Heart,
      title: language === 'hi' ? 'सटीक समय चिह्न' : 'Precise Timestamps',
      description: language === 'hi' 
        ? 'वीडियो के सटीक समय पर जाकर उत्तर सुनें' 
        : 'Jump to exact moments in videos for answers'
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
    <div className="min-h-screen bg-black text-white">
      <div className="px-4 py-8 sm:px-6">
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
                ? 'हमारा लक्ष्य है आध्यात्मिक ज्ञान को सभी के लिए सुलभ बनाना। इस ऐप के माध्यम से, आप गुरुजी के 900+ प्रवचनों से किसी भी आध्यात्मिक प्रश्न का तुरंत उत्तर पा सकते हैं। AI तकनीक की मदद से, हम आपके प्रश्न को समझकर सबसे प्रासंगिक उत्तर ढूंढकर लाते हैं।'
                : 'Our goal is to make spiritual knowledge accessible to everyone. Through this app, you can instantly find answers to any spiritual question from Guruji\'s 900+ discourses. With AI technology, we understand your question and find the most relevant answers.'
              }
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AboutPage;