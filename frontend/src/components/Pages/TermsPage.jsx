import React from 'react';
import { FileText, Shield, Eye, Heart } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import PageShell from '../Layout/PageShell';

const TermsPage = ({ language }) => {
  const sections = [
    {
      icon: FileText,
      title: language === 'hi' ? 'उपयोग की शर्तें' : 'Terms of Use',
      content: language === 'hi' 
        ? 'यह ऐप आध्यात्मिक शिक्षा और मार्गदर्शन के लिए बनाया गया है। कृपया इसका उपयोग सम्मानजनक तरीके से करें।'
        : 'This app is created for spiritual education and guidance. Please use it respectfully.'
    },
    {
      icon: Shield,
      title: language === 'hi' ? 'गोपनीयता' : 'Privacy',
      content: language === 'hi' 
        ? 'आपकी व्यक्तिगत जानकारी सुरक्षित है। हम आपकी खोज का इतिहास केवल बेहतर अनुभव के लिए उपयोग करते हैं।'
        : 'Your personal information is secure. We use your search history only to improve your experience.'
    },
    {
      icon: Eye,
      title: language === 'hi' ? 'डेटा उपयोग' : 'Data Usage',
      content: language === 'hi' 
        ? 'आपके द्वारा खोजे गए प्रश्न और पसंदीदा उत्तर स्थानीय रूप से संग्रहीत किए जाते हैं।'
        : 'Your searched questions and favorite answers are stored locally on your device.'
    },
    {
      icon: Heart,
      title: language === 'hi' ? 'आध्यात्मिक उपयोग' : 'Spiritual Use',
      content: language === 'hi' 
        ? 'यह ऐप आध्यात्मिक विकास के लिए है। कृपया इसे व्यावसायिक उद्देश्यों के लिए उपयोग न करें।'
        : 'This app is for spiritual development. Please do not use it for commercial purposes.'
    }
  ];

  return (
    <PageShell>
      <div>
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">
            {language === 'hi' ? 'नियम एवं शर्तें' : 'Terms & Conditions'}
          </h1>
          <p className="text-gray-400 text-sm">
            {language === 'hi' 
              ? 'कृपया इन नियमों को ध्यान से पढ़ें'
              : 'Please read these terms carefully'
            }
          </p>
        </div>

        {/* Terms Sections */}
        <div className="space-y-4">
          {sections.map((section, index) => {
            const Icon = section.icon;
            return (
              <Card key={index} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl">
                <CardHeader>
                  <CardTitle className="text-white flex items-center gap-3 text-lg">
                    <Icon className="w-5 h-5" />
                    {section.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300 leading-relaxed text-sm">
                    {section.content}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Contact */}
        <Card className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl mt-6">
          <CardHeader>
            <CardTitle className="text-white text-lg">
              {language === 'hi' ? 'संपर्क करें' : 'Contact Us'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-300 text-sm leading-relaxed">
              {language === 'hi' 
                ? 'यदि आपके कोई प्रश्न हैं, तो कृपया हमसे संपर्क करें। हमारी टीम आपकी सहायता के लिए तैयार है।'
                : 'If you have any questions, please contact us. Our team is ready to assist you.'
              }
            </p>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
};

export default TermsPage;