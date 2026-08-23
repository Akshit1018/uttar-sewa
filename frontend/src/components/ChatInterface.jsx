import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader2, Clock, Heart, HeartIcon, Mic, MicOff, Bot, User, Sparkles, Star, Share2 } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { useToast } from '../hooks/use-toast';
import { useFavorites } from '../hooks/useFavorites';
import { useSearchHistory } from '../hooks/useSearchHistory';
import { useVoiceSearch } from '../hooks/useVoiceSearch';
import { useOfflineStorage } from '../hooks/useOfflineStorage';
import { usePerformanceMonitor } from '../hooks/usePerformance';
import { notificationService } from '../services/notificationService';
import { analyticsService } from '../services/analyticsService';
import { t } from '../utils/translations';
import { formatTimestamp } from '../lib/youtube';
import { VideoTimestampLink, VideoHomeLink } from './VideoTimestampLink';
import ChannelSelector from './ChannelSelector';
import { useChannels } from '../hooks/useChannels';
import { shareCard } from '../lib/practice';

import { API } from '../lib/backend';
import { controlHeaders } from '../lib/control';

const ChatInterface = ({ language, stats: statsFromApp, channels: channelsProp, channelId: channelIdProp, setChannelId: setChannelIdProp }) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const [localStats, setLocalStats] = useState(null);
  const stats = statsFromApp || localStats;
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [followUps, setFollowUps] = useState([]);
  const [ingestUrl, setIngestUrl] = useState('');
  const [ingesting, setIngesting] = useState(false);
  const localChannels = useChannels();
  const channels = channelsProp || localChannels.channels;
  const channelId = channelIdProp ?? localChannels.channelId;
  const setChannelId = setChannelIdProp || localChannels.setChannelId;
  
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);
  const { toast } = useToast();
  
  // Custom hooks
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const { addToHistory } = useSearchHistory();
  const { isOnline, cacheSearchResults } = useOfflineStorage();
  const { measureSearchTime } = usePerformanceMonitor();
  
  // Voice search
  const { isListening, isSupported: voiceSupported, startListening, stopListening } = useVoiceSearch(
    (transcript) => {
      setQuery(transcript);
      handleSendMessage(transcript);
      analyticsService.trackVoiceSearch(0, true, language);
    },
    language
  );

  useEffect(() => {
    loadSuggestedQuestions();
    loadStats();
    loadRecommendations();
    analyticsService.trackPageView('chat');
    
    // Add welcome message
    const welcomeMessage = {
      id: 'welcome',
      type: 'bot',
      content: language === 'hi' 
        ? 'नमस्ते! मैं आपके आध्यात्मिक प्रश्नों का उत्तर देने के लिए यहाँ हूँ। कोई भी प्रश्न पूछें या नीचे दिए गए सुझावों में से चुनें।'
        : 'Hello! I\'m here to answer your spiritual questions. Ask anything or choose from the suggestions below.',
      timestamp: new Date(),
      suggestions: []
    };
    setMessages([welcomeMessage]);
    
    // Request notification permission
    notificationService.requestPermission();
  }, [language]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadSuggestedQuestions = async () => {
    try {
      const response = await fetch(`${API}/questions/suggested`);
      const data = await response.json();
      
      const apiQuestions = data.suggested_questions || [];
      const translatedQuestions = t('sampleQuestions', language);
      
      const allQuestions = [...translatedQuestions, ...apiQuestions];
      setSuggestedQuestions(allQuestions.slice(0, 8));
    } catch (error) {
      console.error('Error loading suggested questions:', error);
      setSuggestedQuestions(t('sampleQuestions', language));
    }
  };

  const loadRecommendations = async () => {
    try {
      const history = JSON.parse(localStorage.getItem('spiritual_qa_search_history') || '[]');
      const recentQueries = history.slice(0, 6).map((item) => item.query).filter(Boolean);
      const response = await fetch(`${API}/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recent_queries: recentQueries,
          language,
          channel_id: channelId === 'all' ? null : channelId,
          limit: 6,
        }),
      });
      if (!response.ok) return;
      const data = await response.json();
      if (Array.isArray(data.recommendations) && data.recommendations.length > 0) {
        setSuggestedQuestions((current) => {
          const merged = [...data.recommendations, ...current];
          return [...new Set(merged)].slice(0, 8);
        });
      }
    } catch (error) {
      console.error('Error loading recommendations:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch(`${API}/stats`);
      const data = await response.json();
      setLocalStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleIngestUrl = async () => {
    const url = ingestUrl.trim();
    if (!url) {
      toast({
        title: language === 'hi' ? 'URL दर्ज करें' : 'Enter a URL',
        description: language === 'hi' ? 'YouTube वीडियो या चैनल का पता चिपकाएँ।' : 'Paste a YouTube video or channel address.',
        variant: 'destructive',
      });
      return;
    }
    setIngesting(true);
    try {
      const response = await fetch(`${API}/process/from-url`, {
        method: 'POST',
        headers: controlHeaders(),
        body: JSON.stringify({ url }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.detail || 'Ingest failed');
      }
      setIngestUrl('');
      await loadStats();
      toast({
        title: language === 'hi' ? 'इंजेस्ट शुरू' : 'Ingest started',
        description: language === 'hi'
          ? 'प्रवचन जुड़ गए तो प्रश्न पूछें।'
          : 'Ask again once the discourse is stored.',
      });
    } catch (error) {
      toast({
        title: language === 'hi' ? 'इंजेस्ट नहीं हुआ' : 'Ingest failed',
        description: error.message || (language === 'hi' ? 'YouTube कुंजी या नेट देखें।' : 'Check the YouTube key or network.'),
        variant: 'destructive',
      });
    } finally {
      setIngesting(false);
    }
  };

  const handleSendMessage = async (messageText = query) => {
    if (!messageText.trim()) {
      toast({
        title: t('enterQuestion', language),
        description: t('enterQuestionDesc', language),
        variant: "destructive"
      });
      return;
    }

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setShowSuggestions(false);
    setLoading(true);

    const searchStartTime = performance.now();

    try {
      // Check for cached results first if offline
      let data = [];
      
      if (!isOnline) {
        throw new Error('offline');
      }

      if (data.length === 0) {
        const response = await fetch(`${API}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: messageText,
            limit: 3,
            language,
            conversation_history: messages
              .filter((item) => item.type === 'user')
              .slice(-4)
              .map((item) => item.content),
            channel_id: channelId === 'all' ? null : channelId,
            include_companions: true,
          }),
        });

        if (!response.ok) {
          throw new Error('Ask failed');
        }

        const payload = await response.json();
        data = (payload.clips || []).map((clip) => ({
          question: clip.source_question || payload.answer,
          answer: clip.source_answer || payload.answer,
          video_id: clip.video_id,
          video_title: clip.video_title,
          start_time: clip.start_time,
          timestamp_url: clip.timestamp_url,
          youtube_url: clip.youtube_url,
          confidence_score: clip.confidence_score,
          related_questions: payload.related_questions || clip.related_questions || [],
          citation_kind: clip.citation_kind,
        }));
        data.refused = !!payload.refused;
        data.answer = payload.answer || '';
        data.evidence_kind = payload.evidence_kind;
        data.seed_only = !!payload.seed_only;
        data.companions = payload.companions || [];
        
        // Cache results for offline use
        if (data.length > 0 && isOnline) {
          cacheSearchResults(messageText, data);
        }
      }

      const searchTime = measureSearchTime(searchStartTime);
      
      // Add to search history
      addToHistory(messageText, data);
      
      // Track analytics
      analyticsService.trackSearch(messageText, language, data.length, searchTime);

      const answerText = data.answer
        || (data.length > 0 ? data[0].answer : '');
      const refused = !!data.refused || data.length === 0;

      // Create bot response message
      const botMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: answerText
          || (language === 'hi'
            ? 'इस विषय पर संकलित प्रवचनों में स्पष्ट उत्तर नहीं मिला।'
            : 'The collected discourses do not contain a clear answer to this.'),
        timestamp: new Date(),
        results: data,
        refused,
        seedOnly: !!data.seed_only,
        evidenceKind: data.evidence_kind,
        companions: data.companions || [],
        searchTime: Math.round(searchTime)
      };

      setMessages(prev => [...prev, botMessage]);

      const related = (data[0] && data[0].related_questions) || [];
      setFollowUps(related);
      
      if (data.length > 0) {
        notificationService.showSearchCompleteNotification(data.length, language);
      }

    } catch (error) {
      console.error('Search error:', error);
      analyticsService.trackError('search_error', error.message, { query: messageText });
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: error.message === 'offline'
          ? (language === 'hi' ? 'ऑफ़लाइन हैं — जप चल सकता है, प्रश्न के लिए नेट चाहिए।' : 'You are offline. Japa still works; asking needs the network.')
          : (language === 'hi'
          ? 'खुशी से खोज में कोई समस्या हुई। कृपया बाद में पुनः प्रयास करें।'
          : 'Sorry, there was an issue with the search. Please try again later.'),
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
      
      toast({
        title: t('searchError', language),
        description: t('searchErrorDesc', language),
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestedQuestionClick = (question) => {
    handleSendMessage(question);
    analyticsService.track('suggested_question_clicked', { question });
  };

  const handleFavoriteToggle = (result) => {
    const resultId = `${result.video_id}_${result.start_time}`;
    
    if (isFavorite(result)) {
      removeFromFavorites(resultId);
      analyticsService.trackFavoriteAction('remove', resultId);
      toast({
        title: language === 'hi' ? 'पसंदीदा से हटाया गया' : 'Removed from Favorites',
        description: language === 'hi' ? 'यह प्रश्न-उत्तर पसंदीदा से हटा दिया गया' : 'This Q&A was removed from favorites',
      });
    } else {
      addToFavorites(result);
      analyticsService.trackFavoriteAction('add', resultId);
      toast({
        title: language === 'hi' ? 'पसंदीदा में जोड़ा गया' : 'Added to Favorites',
        description: language === 'hi' ? 'यह प्रश्न-उत्तर पसंदीदा में सेव हो गया' : 'This Q&A was saved to favorites',
      });
    }
  };

  const handleVoiceSearch = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const renderMessage = (message) => {
    const isUser = message.type === 'user';
    
    return (
      <div key={message.id} className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 fade-in`}>
        <div className={`chat-bubble ${isUser ? 'order-2' : 'order-1'}`}>
          {/* Avatar */}
          <div className={`flex items-center gap-2 mb-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              isUser ? 'bg-white/10' : 'bg-gradient-to-br from-blue-500/20 to-purple-500/20'
            }`}>
              {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>
            <span className="text-xs text-gray-400">
              {isUser ? (language === 'hi' ? 'आप' : 'You') : (language === 'hi' ? 'सहायक' : 'Assistant')}
            </span>
          </div>

          {/* Message Content */}
          <Card className={`${
            isUser 
              ? 'bg-white text-black' 
              : message.isError 
                ? 'bg-red-500/10 border-red-500/20' 
                : 'glass-card'
          } rounded-2xl`}>
            <CardContent className="p-4">
              <p className={`text-sm leading-relaxed ${
                isUser ? 'text-black' : message.refused ? 'text-amber-200' : 'text-white'
              }`}>
                {message.content}
              </p>
              {message.seedOnly && (
                <p className="mt-2 text-xs text-amber-200">
                  {language === 'hi'
                    ? 'यह बीज पुस्तकालय है, आपके गुरु का प्रवचन नहीं।'
                    : 'This is the seed library, not your guru’s discourse.'}
                </p>
              )}

              {/* Search Results */}
              {message.results && message.results.length > 0 && (
                <div className="mt-4 space-y-3">
                  {message.results.map((result, index) => (
                    <div key={index} className="bg-white/5 rounded-xl p-3 border border-white/10 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <h4 className="text-white text-sm font-medium leading-relaxed flex-1 min-w-0">
                          {result.question}
                        </h4>
                        <div className="flex shrink-0">
                        <Button
                          onClick={() => handleFavoriteToggle(result)}
                          variant="ghost"
                          size="icon"
                          aria-label={language === 'hi' ? 'पसंदीदा' : 'Favorite'}
                          className={`shrink-0 ${isFavorite(result) ? 'text-red-400' : 'text-gray-400 hover:text-red-400'}`}
                        >
                          {isFavorite(result) ? (
                            <Heart className="w-4 h-4 fill-current" />
                          ) : (
                            <HeartIcon className="w-4 h-4" />
                          )}
                        </Button>
                        <Button
                          onClick={() => shareCard({
                            question: result.question,
                            answer: result.answer,
                            timestampUrl: result.timestamp_url,
                          })}
                          variant="ghost"
                          size="icon"
                          className="shrink-0 text-gray-400 hover:text-white"
                        >
                          <Share2 className="w-4 h-4" />
                        </Button>
                        </div>
                      </div>

                      <p className="text-gray-300 text-xs leading-relaxed mb-3">
                        {result.answer}
                      </p>

                      <div className="flex flex-wrap gap-2 mb-3">
                        <Badge className="bg-white/10 text-white text-xs px-2 py-1">
                          {(result.video_title || '').substring(0, 30)}...
                        </Badge>
                        <Badge className="bg-white/10 text-white text-xs px-2 py-1">
                          <Clock className="w-3 h-3 mr-1" />
                          {formatTimestamp(result.start_time)}
                        </Badge>
                        <Badge className="bg-green-500/20 text-green-400 text-xs px-2 py-1">
                          <Star className="w-3 h-3 mr-1" />
                          {Number.isFinite(Number(result.confidence_score)) ? `${Math.round(result.confidence_score * 100)}%` : '—'}
                        </Badge>
                        {result.citation_kind === 'curated' && (
                          <Badge className="bg-amber-500/20 text-amber-200 text-xs px-2 py-1">
                            {language === 'hi' ? 'संग्रहित' : 'Curated'}
                          </Badge>
                        )}
                      </div>

                      <div className="flex flex-col sm:flex-row gap-2">
                        <VideoTimestampLink
                          videoId={result.video_id}
                          startTime={result.start_time}
                          timestampUrl={result.timestamp_url}
                          label={formatTimestamp(result.start_time)}
                          className="bg-white text-black hover:bg-gray-100 text-xs px-3 py-2 h-auto flex-1"
                        />
                        <VideoHomeLink
                          videoId={result.video_id}
                          youtubeUrl={result.youtube_url}
                          label=""
                          className="border-white/20 text-gray-300 hover:bg-white/10 text-xs px-3 py-2 h-auto"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {message.companions && message.companions.length > 0 && (
                <div className="mt-3 space-y-2">
                  <p className="text-xs text-gray-400">
                    {language === 'hi' ? 'सार्वजनिक पाठ (वीडियो नहीं)' : 'Public texts (not videos)'}
                  </p>
                  {message.companions.slice(0, 3).map((card, index) => (
                    <p key={`${card.title || card.source}-${index}`} className="text-xs text-gray-300 leading-relaxed">
                      {(card.title || card.source || 'Companion')}: {(card.text || card.excerpt || '').slice(0, 180)}
                    </p>
                  ))}
                </div>
              )}

              {/* Performance info */}
              {message.searchTime && (
                <div className="mt-2 text-xs text-gray-500">
                  {language === 'hi' ? 'खोज समय:' : 'Search time:'} {message.searchTime}ms
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    );
  };

  return (
    <div className="chat-shell bg-black text-white flex flex-col overflow-hidden">
      {/* Header with Stats */}
      <div className="flex-shrink-0 px-3 py-3 sm:px-4 sm:py-4 border-b border-white/10 glass-card">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="min-w-0">
            <h1 className="text-base sm:text-lg font-bold text-white">
              {language === 'hi' ? 'आध्यात्मिक सहायक' : 'Spiritual Assistant'}
            </h1>
            <p className="text-xs text-gray-400">
              {language === 'hi' ? 'उत्तर केवल इंजेस्टेड प्रवचनों से उद्धृत होते हैं।' : 'Answers are copied from ingested discourses only.'}
            </p>
          </div>
          <div className="flex items-center gap-2 min-w-0">
            <ChannelSelector
              language={language}
              channelId={channelId}
              setChannelId={setChannelId}
              channels={channels}
            />
            <div className={`w-3 h-3 rounded-full shrink-0 ${isOnline ? 'bg-green-400' : 'bg-red-400'} animate-pulse`}></div>
          </div>
        </div>

        {stats && Number(stats.ingested_qa || 0) === 0 && (
          <div className="mt-3 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-xs text-amber-100 space-y-2">
            <p>
              {language === 'hi'
                ? Number(stats.curated_qa || 0) > 0
                  ? 'अभी केवल बीज पुस्तकालय है। अपना प्रवचन जोड़ने के लिए YouTube URL चिपकाएँ।'
                  : 'संग्रह खाली है। अपना पहला प्रवचन जोड़ने के लिए YouTube URL चिपकाएँ।'
                : Number(stats.curated_qa || 0) > 0
                  ? 'Only the seed library is present. Paste a YouTube URL to add a real discourse.'
                  : 'The corpus is empty. Paste a YouTube URL to add the first discourse.'}
            </p>
            <div className="flex flex-col sm:flex-row gap-2">
              <Input
                type="url"
                value={ingestUrl}
                onChange={(event) => setIngestUrl(event.target.value)}
                placeholder="https://www.youtube.com/watch?v=…"
                className="bg-black/30 border-amber-500/30 text-white placeholder-amber-100/50"
                aria-label={language === 'hi' ? 'YouTube पता' : 'YouTube URL'}
              />
              <Button
                onClick={handleIngestUrl}
                disabled={ingesting}
                className="bg-white text-black hover:bg-gray-100"
              >
                {ingesting
                  ? (language === 'hi' ? 'जोड़ रहे हैं…' : 'Adding…')
                  : (language === 'hi' ? 'जोड़ें' : 'Add')}
              </Button>
            </div>
          </div>
        )}

        {stats && (
          <div className="grid grid-cols-3 gap-2 mt-3">
            {[
              { value: stats.ingested_qa ?? 0, label: language === 'hi' ? 'इंजेस्टेड' : 'Ingested' },
              { value: stats.curated_qa ?? 0, label: language === 'hi' ? 'बीज' : 'Seed' },
              { value: stats.processed_videos, label: t('processedVideos', language) }
            ].map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-sm font-bold text-white">{stat.value}</div>
                <div className="text-xs text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto px-3 py-3 sm:px-4 sm:py-4 custom-scrollbar">
        {messages.map(renderMessage)}
        
        {loading && (
          <div className="flex justify-start mb-4">
            <div className="chat-bubble">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center">
                  <Bot className="w-4 h-4" />
                </div>
                <span className="text-xs text-gray-400">
                  {language === 'hi' ? 'सहायक' : 'Assistant'}
                </span>
              </div>
              <Card className="glass-card rounded-2xl">
                <CardContent className="p-4">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm text-white">
                      {language === 'hi' ? 'खोज रहा है...' : 'Searching...'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
        
        <div ref={chatEndRef} />
      </div>

      {/* Suggested Questions */}
      {showSuggestions && suggestedQuestions.length > 0 && (
        <div className="flex-shrink-0 px-4 py-3 border-t border-white/10">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-white" />
            <span className="text-sm font-medium text-white">
              {t('suggestedQuestions', language)}
            </span>
          </div>
          <div className="chip-scroll">
            {suggestedQuestions.slice(0, 6).map((question, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuestionClick(question)}
                className="flex-shrink-0 px-3 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs text-gray-300 hover:text-white transition-colors border border-white/10"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Follow-up questions */}
      {!showSuggestions && followUps.length > 0 && !loading && (
        <div className="flex-shrink-0 px-4 py-2 border-t border-white/10">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-white" />
            <span className="text-sm font-medium text-white">
              {t('followUps', language)}
            </span>
          </div>
          <div className="chip-scroll">
            {followUps.map((question, index) => (
              <button
                key={`${question}-${index}`}
                onClick={() => handleSuggestedQuestionClick(question)}
                className="flex-shrink-0 px-3 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-xs text-gray-300 hover:text-white transition-colors border border-white/10"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="flex-shrink-0 chat-composer border-t border-white/10 glass-card">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="flex-1 relative min-w-0">
            <Input
              ref={inputRef}
              type="text"
              placeholder={t('searchPlaceholder', language)}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              className="bg-white/5 border-white/20 text-white placeholder-gray-400 rounded-xl h-12 pr-12 focus-ring"
              disabled={loading}
            />
            
            {/* Voice Search Button */}
            {voiceSupported && (
              <Button
                onClick={handleVoiceSearch}
                variant="ghost"
                size="icon"
                aria-label={language === 'hi' ? 'बोलें' : 'Speak'}
                className={`absolute right-1 top-1/2 transform -translate-y-1/2 ${
                  isListening ? 'bg-red-500/20 text-red-400' : 'hover:bg-white/10'
                }`}
                disabled={loading}
              >
                {isListening ? <MicOff className="w-4 h-4 animate-pulse" /> : <Mic className="w-4 h-4" />}
              </Button>
            )}
          </div>

          <Button
            onClick={() => handleSendMessage()}
            disabled={loading || !query.trim()}
            size="icon"
            aria-label={language === 'hi' ? 'भेजें' : 'Send'}
            className="bg-white text-black hover:bg-gray-100 rounded-xl transition-all duration-300 shrink-0"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </Button>
        </div>

        {isListening && (
          <div className="mt-2 flex items-center justify-center gap-2">
            <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-white">
              {language === 'hi' ? 'सुन रहा है...' : 'Listening...'}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;