import React from 'react';
import { CircleDot } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { BEADS_PER_CYCLE, progressLabel } from '../lib/mala';

const SadhanaDashboard = ({ language, state }) => {
  const beads = state.beads_today || 0;
  const malas = state.cycles_today || 0;
  const current = state.current_in_cycle || 0;
  const questions = state.questions_today || 0;
  const percent = Math.round((current / BEADS_PER_CYCLE) * 100);

  const stats = [
    { value: beads, label: language === 'hi' ? 'आज के मनके' : 'Beads today' },
    { value: malas, label: language === 'hi' ? 'आज की माला' : 'Malas today' },
    { value: progressLabel(state), label: language === 'hi' ? 'वर्तमान चक्र' : 'This cycle' },
    { value: questions, label: language === 'hi' ? 'आज के प्रश्न' : 'Questions today' },
  ];

  return (
    <div className="min-h-[calc(100dvh-4rem)] bg-black text-white px-4 py-8">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <CircleDot className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold mb-2">
          {language === 'hi' ? 'साधना' : 'Sadhana'}
        </h1>
        <p className="text-gray-400 text-sm">
          {language === 'hi'
            ? 'गोल पर टैप = एक मनका। 108 = एक माला। 2.5 सेकंड दबाएँ = प्रवचन से पूछें।'
            : 'Tap the orb for one bead. 108 is one mala. Hold 2.5s to ask from the discourses.'}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-6">
        {stats.map((stat) => (
          <Card key={stat.label} className="glass-card border-white/10">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-white">{stat.value}</div>
              <div className="text-xs text-gray-400 mt-1">{stat.label}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="glass-card rounded-2xl p-4">
        <div className="flex items-center justify-between text-sm mb-2">
          <span>{language === 'hi' ? 'इस माला की प्रगति' : 'This mala'}</span>
          <span>{percent}%</span>
        </div>
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-white" style={{ width: `${percent}%` }} />
        </div>
        <p className="text-xs text-gray-500 mt-3">
          {language === 'hi'
            ? 'डबल-टैप से आखिरी मनका वापस। गोल को खींचकर हटाएँ। iOS अन्य ऐप्स के ऊपर नहीं तैर सकता; यह गोल इस ऐप में हमेशा रहता है।'
            : 'Double-tap undoes the last bead. Drag the orb aside. iOS cannot float over other apps; this orb stays on top inside this app.'}
        </p>
      </div>
    </div>
  );
};

export default SadhanaDashboard;
