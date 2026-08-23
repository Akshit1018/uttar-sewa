import React, { useRef, useState } from 'react';
import { Loader2, Mic, MicOff, Send, Share2, Volume2, X } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useVoiceSearch } from '../hooks/useVoiceSearch';
import { VideoTimestampLink } from './VideoTimestampLink';
import { t } from '../utils/translations';
import { shareCard } from '../lib/practice';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const JapaChatSheet = ({ language, open, onClose, onAsked }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [micError, setMicError] = useState('');
  const askRef = useRef(async () => {});

  const handleAsk = async (text) => {
    const question = (text || '').trim();
    if (!question) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch(`${API}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: question,
          language,
          conversation_history: history.slice(-4),
          limit: 3,
        }),
      });
      if (!response.ok) {
        throw new Error('Ask failed');
      }
      const data = await response.json();
      setResult(data);
      setHistory((current) => [...current, question].slice(-8));
      setQuery('');
      if (onAsked) onAsked();
    } catch (askError) {
      setResult({
        refused: true,
        answer: language === 'hi' ? 'उत्तर नहीं मिल सका।' : 'Could not fetch an answer.',
        clips: [],
      });
    } finally {
      setLoading(false);
    }
  };

  askRef.current = handleAsk;

  const speakAnswer = (text) => {
    if (!text || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'hi' ? 'hi-IN' : 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  const { isListening, isSupported, startListening, stopListening, error } = useVoiceSearch(
    (transcript) => {
      setQuery(transcript);
      askRef.current(transcript);
    },
    language
  );

  const requestMic = () => {
    setMicError('');
    if (!isSupported) {
      setMicError(language === 'hi'
        ? 'इस फ़ोन पर वॉइस इनपुट उपलब्ध नहीं है।'
        : 'Voice input is not available on this phone.');
      return;
    }
    if (isListening) {
      stopListening();
      return;
    }
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          stream.getTracks().forEach((track) => track.stop());
          startListening();
        })
        .catch(() => {
          setMicError(language === 'hi'
            ? 'माइक्रोफ़ोन की अनुमति दें, फिर बोलें।'
            : 'Allow the microphone, then speak.');
        });
      return;
    }
    startListening();
  };

  if (!open) {
    return null;
  }

  return (
    <div className="japa-sheet-backdrop" role="dialog" aria-modal="true">
      <div className="japa-sheet">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-base font-semibold">
            {language === 'hi' ? 'प्रवचन से पूछें' : 'Ask from the discourses'}
          </h2>
          <Button variant="ghost" size="icon" onClick={onClose} className="text-white shrink-0">
            <X className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-xs text-gray-400 mb-3">
          {language === 'hi'
            ? 'उत्तर केवल वीडियो/संग्रहित प्रवचनों से, समय-चिह्न के साथ।'
            : 'Answers only from the videos, with timestamps.'}
        </p>

        {result && (
          <div className="mb-4 space-y-3 max-h-[40vh] overflow-y-auto custom-scrollbar">
            {(result.clips || []).map((clip, index) => (
              <div key={`${clip.source_question}-${index}`} className="bg-white/5 rounded-xl p-3 border border-white/10">
                <p className="text-xs text-white font-medium mb-1">{clip.video_title || clip.source_question}</p>
                {clip.citation_kind === 'curated' ? (
                  <p className="text-xs text-amber-200 mb-2">
                    {language === 'hi' ? 'संग्रहित शिक्षण, समय-चिह्न नहीं।' : 'Curated teaching, not a timestamped clip.'}
                  </p>
                ) : (
                  <p className="text-xs text-gray-400 mb-2">
                    {language === 'en' ? 'Original clip (Hindi/source audio).' : 'मूल क्लिप।'}
                  </p>
                )}
                {clip.source_answer ? (
                  <p className="text-xs text-gray-500 mb-2 leading-relaxed">
                    “{(clip.source_answer || '').slice(0, 160)}{(clip.source_answer || '').length > 160 ? '…' : ''}”
                  </p>
                ) : null}
                <VideoTimestampLink
                  videoId={clip.video_id}
                  startTime={clip.start_time}
                  timestampUrl={clip.timestamp_url}
                  label={clip.formatted_start_time || t('watchVideo', language)}
                  className="bg-white text-black text-xs w-full"
                />
              </div>
            ))}
            <div className="flex items-start justify-between gap-2">
              <p className={`text-sm leading-relaxed min-w-0 ${result.refused ? 'text-amber-200' : 'text-white'}`}>
                {result.answer}
              </p>
              <div className="flex shrink-0">
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="text-white"
                  onClick={() => speakAnswer(result.answer)}
                  aria-label={language === 'hi' ? 'उत्तर सुनें' : 'Hear answer'}
                >
                  <Volume2 className="w-4 h-4" />
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="text-white"
                  onClick={() => shareCard({
                    question: history[history.length - 1] || '',
                    answer: result.answer,
                    timestampUrl: (result.clips && result.clips[0] && result.clips[0].timestamp_url) || '',
                  })}
                  aria-label={language === 'hi' ? 'कार्ड साझा करें' : 'Share card'}
                >
                  <Share2 className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        )}

        <div className="flex items-center gap-2">
          <Input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => event.key === 'Enter' && handleAsk(query)}
            placeholder={t('searchPlaceholder', language)}
            className="bg-white/5 border-white/20 text-white min-w-0 flex-1"
            disabled={loading}
          />
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={requestMic}
            className={isListening ? 'text-red-400 shrink-0' : 'text-white shrink-0'}
            aria-label={language === 'hi' ? 'बोलें' : 'Speak'}
          >
            {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </Button>
          <Button
            type="button"
            size="icon"
            onClick={() => handleAsk(query)}
            disabled={loading || !query.trim()}
            className="bg-white text-black shrink-0"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </Button>
        </div>
        {(micError || error) && (
          <p className="text-xs text-amber-300 mt-2">{micError || error}</p>
        )}
      </div>
    </div>
  );
};

export default JapaChatSheet;
