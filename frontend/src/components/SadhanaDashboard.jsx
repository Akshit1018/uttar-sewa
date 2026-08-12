import React, { useEffect, useState } from 'react';
import { CircleDot } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { BEADS_PER_CYCLE, progressLabel, sankalpaRemaining } from '../lib/mala';

const HAND_KEY = 'uttar_sewa_orb_hand';
const VOW_KEY = 'uttar_sewa_sankalpa_malas';

const SadhanaDashboard = ({ language, state }) => {
  const [hand, setHand] = useState('right');
  const [vow, setVow] = useState(1);
  const beads = state.beads_today || 0;
  const malas = state.cycles_today || 0;
  const current = state.current_in_cycle || 0;
  const questions = state.questions_today || 0;
  const percent = Math.round((current / BEADS_PER_CYCLE) * 100);
  const remaining = sankalpaRemaining(malas, vow);

  useEffect(() => {
    try {
      setHand(localStorage.getItem(HAND_KEY) || 'right');
      setVow(Number(localStorage.getItem(VOW_KEY) || 1));
    } catch (error) {
      // ignore
    }
  }, []);

  const saveHand = (value) => {
    setHand(value);
    try {
      localStorage.setItem(HAND_KEY, value);
    } catch (error) {
      // ignore
    }
  };

  const saveVow = (value) => {
    const next = Math.max(0, Number(value) || 0);
    setVow(next);
    try {
      localStorage.setItem(VOW_KEY, String(next));
    } catch (error) {
      // ignore
    }
  };

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

      <div className="glass-card rounded-2xl p-4 mb-4">
        <div className="flex items-center justify-between text-sm mb-2">
          <span>{language === 'hi' ? 'आज का संकल्प' : 'Today’s sankalpa'}</span>
          <span>{malas}/{vow} {language === 'hi' ? 'माला' : 'malas'}</span>
        </div>
        <p className="text-xs text-gray-400 mb-3">
          {remaining === 0
            ? (language === 'hi' ? 'आज का संकल्प पूरा।' : 'Today’s vow is complete.')
            : (language === 'hi' ? `${remaining} माला शेष।` : `${remaining} mala(s) remaining.`)}
        </p>
        <div className="flex gap-2">
          {[1, 3, 11].map((option) => (
            <Button
              key={option}
              type="button"
              variant="outline"
              size="sm"
              className={`border-white/20 text-xs ${vow === option ? 'bg-white text-black' : 'text-gray-300'}`}
              onClick={() => saveVow(option)}
            >
              {option}
            </Button>
          ))}
        </div>
      </div>

      <div className="glass-card rounded-2xl p-4 mb-4">
        <div className="flex items-center justify-between text-sm mb-2">
          <span>{language === 'hi' ? 'इस माला की प्रगति' : 'This mala'}</span>
          <span>{percent}%</span>
        </div>
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-white" style={{ width: `${percent}%` }} />
        </div>
      </div>

      <div className="glass-card rounded-2xl p-4">
        <p className="text-sm mb-3">{language === 'hi' ? 'गोल की तरफ़' : 'Orb side'}</p>
        <div className="flex gap-2 mb-3">
          <Button
            type="button"
            variant="outline"
            size="sm"
            className={`border-white/20 ${hand === 'left' ? 'bg-white text-black' : 'text-gray-300'}`}
            onClick={() => saveHand('left')}
          >
            {language === 'hi' ? 'बायाँ हाथ' : 'Left hand'}
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className={`border-white/20 ${hand === 'right' ? 'bg-white text-black' : 'text-gray-300'}`}
            onClick={() => saveHand('right')}
          >
            {language === 'hi' ? 'दायाँ हाथ' : 'Right hand'}
          </Button>
        </div>
        <p className="text-xs text-gray-500">
          {language === 'hi'
            ? 'डबल-टैप से आखिरी मनका वापस। खींचने पर गोल किनारे चिपकता है। कोई स्ट्रीक या लीडरबोर्ड नहीं।'
            : 'Double-tap undoes the last bead. Drag snaps the orb to an edge. No streaks or leaderboards.'}
        </p>
      </div>
    </div>
  );
};

export default SadhanaDashboard;
