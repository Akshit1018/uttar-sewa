import React, { useState, useEffect, useRef } from 'react';
import { Search, Loader2, Play, Clock, Sparkles, AlertCircle, Heart, HeartIcon, Mic, MicOff, History, Zap, Star, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { useToast } from '../hooks/use-toast';
import { useFavorites } from '../hooks/useFavorites';
import { useSearchHistory } from '../hooks/useSearchHistory';
import { useVoiceSearch } from '../hooks/useVoiceSearch';
import { useOfflineStorage } from '../hooks/useOfflineStorage';
import { useDebounce, usePerformanceMonitor } from '../hooks/usePerformance';
import { notificationService } from '../services/notificationService';
import { analyticsService } from '../services/analyticsService';
import { t } from '../utils/translations';
import { formatTimestamp } from '../lib/youtube';
import { VideoTimestampLink, VideoHomeLink } from './VideoTimestampLink';
import ChannelSelector from './ChannelSelector';
import { useChannels } from '../hooks/useChannels';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SearchInterface = ({ language }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const [stats, setStats] = useState(null);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showVoiceSearch, setShowVoiceSearch] = useState(false);
  const { channels, channelId, setChannelId } = useChannels();
  
  const searchInputRef = useRef(null);
  const { toast } = useToast();
  
  // Custom hooks
  const { addToFavorites, removeFromFavorites, isFavorite } = useFavorites();
  const { searchHistory, addToHistory, getRecentSearches, getPopularSearches } = useSearchHistory();
  const { isOnline, getCachedResults, cacheSearchResults } = useOfflineStorage();
  const { measureSearchTime } = usePerformanceMonitor();
  
  // Voice search
  const { isListening, isSupported: voiceSupported, startListening, stopListening } = useVoiceSearch(
    (transcript) => {
      setQuery(transcript);
      handleSearch(transcript);
      setShowVoiceSearch(false);
      analyticsService.trackVoiceSearch(0, true, language);
    },
    language
  );

  // Debounced search for auto-suggestions
  const { debouncedCallback: debouncedSuggestions } = useDebounce((searchQuery) => {
    if (searchQuery.length > 2) {
      // Load suggestions based on query
      loadContextualSuggestions(searchQuery);
    }
  }, 500);

  useEffect(() => {
    loadSuggestedQuestions();
    loadStats();
    analyticsService.trackPageView('search');
    
    // Request notification permission
    notificationService.requestPermission();
  }, [language]);

  useEffect(() => {
    debouncedSuggestions(query);
  }, [query, debouncedSuggestions]);

  const loadSuggestedQuestions = async () => {
    try {
      const response = await fetch(`${API}/questions/suggested`);
      const data = await response.json();
      
      const apiQuestions = data.suggested_questions || [];
      const translatedQuestions = t('sampleQuestions', language);
      
      const allQuestions = [...translatedQuestions, ...apiQuestions];
      setSuggestedQuestions(allQuestions.slice(0, 12));
    } catch (error) {
      console.error('Error loading suggested questions:', error);
      setSuggestedQuestions(t('sampleQuestions', language));
    }
  };

  const loadContextualSuggestions = async (searchQuery) => {
    // Load suggestions based on search query context
    const popularQueries = getPopularSearches(3);
    const recentQueries = getRecentSearches(3);
    
    // Combine with default suggestions
    const contextualSuggestions = [
      ...popularQueries.map(q => q.query),
      ...recentQueries.map(q => q.query),
      ...suggestedQuestions.slice(0, 6)
    ];
    
    // Filter unique suggestions
    const uniqueSuggestions = [...new Set(contextualSuggestions)];
    setSuggestedQuestions(uniqueSuggestions.slice(0, 12));
  };

  const loadStats = async () => {
    try {
      const response = await fetch(`${API}/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleSearch = async (searchQuery = query) => {
    if (!searchQuery.trim()) {
      toast({
        title: t('enterQuestion', language),
        description: t('enterQuestionDesc', language),
        variant: "destructive"
      });
      return;
    }

    const searchStartTime = performance.now();
    setLoading(true);
    setSearchPerformed(true);
    setShowHistory(false);

    try {
      // Check for cached results first if offline
      let data = [];
      
      if (!isOnline) {
        const cached = getCachedResults(searchQuery);
        if (cached) {
          data = cached;
          toast({
            title: language === 'hi' ? 'ऑफ़लाइन परिणाम' : 'Offline Results',
            description: language === 'hi' ? 'कैश से परिणाम लोड किए गए' : 'Results loaded from cache',
          });
        }
      }

      if (data.length === 0) {
        const response = await fetch(`${API}/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: searchQuery,
            limit: 5,
            language,
            channel_id: channelId === 'all' ? null : channelId,
          }),
        });

        if (!response.ok) {
          throw new Error('Search failed');
        }

        data = await response.json();
        
        // Cache results for offline use
        if (data.length > 0 && isOnline) {
          cacheSearchResults(searchQuery, data);
        }
      }

      const searchTime = measureSearchTime(searchStartTime);
      setResults(data);
      
      // Add to search history
      addToHistory(searchQuery, data);
      
      // Track analytics
      analyticsService.trackSearch(searchQuery, language, data.length, searchTime);
      
      if (data.length === 0) {
        toast({
          title: t('noResultsTitle', language),
          description: t('noResultsDesc', language),
        });
      } else {
        // Show notification for successful search
        if (data.length > 0) {
          notificationService.showSearchCompleteNotification(data.length, language);
        }
        
        toast({
          title: language === 'hi' ? "खोज सफल!" : "Search Successful!",
          description: language === 'hi' ? `${data.length} परिणाम मिले (${Math.round(searchTime)}ms)` : `Found ${data.length} results (${Math.round(searchTime)}ms)`,
        });
      }
    } catch (error) {
      console.error('Search error:', error);
      analyticsService.trackError('search_error', error.message, { query: searchQuery });
      
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
    setQuery(question);
    handleSearch(question);
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

  const handleHistoryClick = (historyItem) => {
    setQuery(historyItem.query);
    handleSearch(historyItem.query);
    setShowHistory(false);
  };

  const handleVoiceSearch = () => {
    if (isListening) {
      stopListening();
    } else {
      setShowVoiceSearch(true);
      startListening();
    }
  };

  const getRecentHistory = () => getRecentSearches(5);
  const getPopularHistory = () => getPopularSearches(5);

  return (
    <div className="min-h-[calc(100dvh-4rem)] bg-black text-white">
      {/* Hero Section - Mobile Optimized */}
      <div className="px-4 py-8 sm:px-6 sm:py-12 relative">
        {/* Online/Offline Indicator */}
        <div className="absolute top-4 right-4 flex items-center gap-2">
          <ChannelSelector
            language={language}
            channelId={channelId}
            setChannelId={setChannelId}
            channels={channels}
          />
          <div className={`w-3 h-3 rounded-full ${isOnline ? 'bg-green-400' : 'bg-red-400'} animate-pulse`}>
          </div>
        </div>

        {/* Stats Cards - Mobile Stack */}
        {stats && (
          <div className="grid grid-cols-3 gap-3 mb-8 sm:gap-4 fade-in">
            {[
              { value: stats.total_videos, label: t('totalVideos', language), color: 'from-blue-500/20 to-blue-500/5', icon: Play },
              { value: stats.total_qa_pairs, label: t('qaTotal', language), color: 'from-green-500/20 to-green-500/5', icon: Sparkles },
              { value: stats.processed_videos, label: t('processedVideos', language), color: 'from-purple-500/20 to-purple-500/5', icon: Zap }
            ].map((stat, index) => {
              const IconComponent = stat.icon;
              return (
                <div key={index} className="glass-card rounded-2xl p-4 text-center glass-card-hover">
                  <div className="flex items-center justify-center mb-2">
                    <IconComponent className="w-4 h-4 text-white/70" />
                  </div>
                  <div className="text-xl sm:text-2xl font-bold text-white">
                    {stat.value}
                  </div>
                  <div className="text-xs sm:text-sm text-gray-400 mt-1">{stat.label}</div>
                </div>
              );
            })}
          </div>
        )}

        {/* Enhanced Search Bar */}
        <div className="relative zoom-in">
          <div className="relative group">
            <div className="glass-strong rounded-2xl p-1 shadow-2xl">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center ml-2">
                  <Search className="w-5 h-5 text-gray-400" />
                </div>
                <Input
                  ref={searchInputRef}
                  type="text"
                  placeholder={t('searchPlaceholder', language)}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  onFocus={() => query.length === 0 && setShowHistory(true)}
                  className="flex-1 bg-transparent border-none text-base text-white placeholder-gray-400 focus:outline-none focus:ring-0 p-0 h-12 focus-ring"
                />
                
                {/* Voice Search Button */}
                {voiceSupported && (
                  <Button
                    onClick={handleVoiceSearch}
                    variant="ghost"
                    className={`h-12 w-12 p-0 ${isListening ? 'bg-red-500/20 text-red-400' : 'hover:bg-white/10'}`}
                  >
                    {isListening ? <MicOff className="w-5 h-5 animate-pulse" /> : <Mic className="w-5 h-5" />}
                  </Button>
                )}

                {/* History Button */}
                <Button
                  onClick={() => setShowHistory(!showHistory)}
                  variant="ghost"
                  className="h-12 w-12 p-0 hover:bg-white/10"
                >
                  <History className="w-5 h-5" />
                </Button>

                <Button
                  onClick={() => handleSearch()}
                  disabled={loading}
                  className="h-12 px-6 bg-white text-black hover:bg-gray-100 font-semibold rounded-xl transition-all duration-300 disabled:opacity-50 btn-mobile"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <span className="hidden sm:inline">{t('searchButton', language)}</span>
                  )}
                  {!loading && <Search className="w-5 h-5 sm:hidden" />}
                </Button>
              </div>
            </div>
          </div>

          {/* Voice Search Indicator */}
          {showVoiceSearch && (
            <div className="absolute top-full left-0 right-0 mt-2 p-4 glass-card rounded-xl text-center">
              <div className="flex items-center justify-center gap-3 mb-2">
                <div className="w-4 h-4 bg-red-400 rounded-full animate-pulse"></div>
                <span className="text-sm text-white">
                  {language === 'hi' ? 'सुन रहा है...' : 'Listening...'}
                </span>
              </div>
              <p className="text-xs text-gray-400">
                {language === 'hi' ? 'अपना प्रश्न बोलें' : 'Speak your question'}
              </p>
            </div>
          )}

          {/* Search History Dropdown */}
          {showHistory && (getRecentHistory().length > 0 || getPopularHistory().length > 0) && (
            <div className="absolute top-full left-0 right-0 mt-2 glass-card rounded-xl p-4 z-10 slide-up">
              {getRecentHistory().length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
                    <History className="w-4 h-4" />
                    {language === 'hi' ? 'हाल ही की खोजें' : 'Recent Searches'}
                  </h4>
                  <div className="space-y-1">
                    {getRecentHistory().map((item) => (
                      <button
                        key={item.id}
                        onClick={() => handleHistoryClick(item)}
                        className="w-full text-left p-2 rounded-lg hover:bg-white/10 text-sm text-gray-300 hover:text-white transition-colors"
                      >
                        {item.query}
                        <span className="text-xs text-gray-500 ml-2">
                          ({item.results_count} {language === 'hi' ? 'परिणाम' : 'results'})
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {getPopularHistory().length > 0 && (
                <div>
                  <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" />
                    {language === 'hi' ? 'लोकप्रिय खोजें' : 'Popular Searches'}
                  </h4>
                  <div className="space-y-1">
                    {getPopularHistory().map((item, index) => (
                      <button
                        key={index}
                        onClick={() => handleHistoryClick({ query: item.query })}
                        className="w-full text-left p-2 rounded-lg hover:bg-white/10 text-sm text-gray-300 hover:text-white transition-colors flex items-center justify-between"
                      >
                        <span>{item.query}</span>
                        <Badge variant="secondary" className="bg-white/20 text-white text-xs">
                          {item.count}x
                        </Badge>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Processing Warning */}
        {stats && stats.processed_videos === 0 && (
          <div className="mt-6 bounce-in">
            <div className="glass-card rounded-2xl p-4 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-yellow-400 mt-0.5 flex-shrink-0" />
              <div className="text-left">
                <div className="text-white font-medium mb-1 text-sm">
                  {language === 'hi' ? 'प्रोसेसिंग आवश्यक' : 'Processing Required'}
                </div>
                <div className="text-gray-400 text-xs">
                  {language === 'hi' 
                    ? 'खोज करने के लिए पहले वीडियो प्रोसेसिंग शुरू करें।'
                    : 'Start video processing first to enable search.'
                  }
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="px-4 pb-6 sm:px-6">
        {/* Results Section */}
        {results.length > 0 && (
          <div className="space-y-4 mb-8 fade-in">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-white" />
              {t('searchResults', language)}
              <Badge variant="secondary" className="bg-white/20 text-white ml-2">
                {results.length}
              </Badge>
            </h2>
            
            {results.map((result, index) => (
              <Card key={index} className="glass-card rounded-2xl glass-card-hover">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-white text-base leading-relaxed font-semibold flex-1 mr-4">
                      {result.question}
                    </CardTitle>
                    <Button
                      onClick={() => handleFavoriteToggle(result)}
                      variant="ghost"
                      size="sm"
                      className={`p-2 ${isFavorite(result) ? 'text-red-400' : 'text-gray-400 hover:text-red-400'}`}
                    >
                      {isFavorite(result) ? (
                        <Heart className="w-5 h-5 fill-current" />
                      ) : (
                        <HeartIcon className="w-5 h-5" />
                      )}
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-3">
                    <Badge className="bg-white/10 text-white border-white/20 rounded-full px-3 py-1 text-xs">
                      {(result.video_title || '').substring(0, 40)}...
                    </Badge>
                    <Badge className="bg-white/10 text-white border-white/20 rounded-full px-3 py-1 text-xs">
                      <Clock className="w-3 h-3 mr-1" />
                      {formatTimestamp(result.start_time)}
                    </Badge>
                    <Badge className="bg-green-500/20 text-green-400 border-green-500/30 rounded-full px-3 py-1 text-xs">
                      <Star className="w-3 h-3 mr-1" />
                      {Math.round(result.confidence_score * 100)}%
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-gray-300 leading-relaxed mb-4 text-sm">
                    {result.answer}
                  </p>
                  
                  <div className="flex flex-col sm:flex-row gap-3">
                    <VideoTimestampLink
                      videoId={result.video_id}
                      startTime={result.start_time}
                      timestampUrl={result.timestamp_url}
                      label={`${t('watchVideo', language)} (${formatTimestamp(result.start_time)})`}
                      className="bg-white text-black hover:bg-gray-100 rounded-xl px-4 py-3 font-medium transition-colors duration-200 flex-1 btn-mobile"
                    />
                    <VideoHomeLink
                      videoId={result.video_id}
                      youtubeUrl={result.youtube_url}
                      label={t('fullVideo', language)}
                      className="border-white/20 text-gray-300 hover:bg-white/10 rounded-xl px-4 py-3 backdrop-blur-sm btn-mobile"
                    />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* No Results */}
        {results.length === 0 && searchPerformed && !loading && (
          <div className="text-center py-12 fade-in">
            <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Search className="w-8 h-8 text-gray-500" />
            </div>
            <h3 className="text-lg font-semibold text-gray-400 mb-2">
              {t('noResultsTitle', language)}
            </h3>
            <p className="text-gray-500 text-sm">
              {t('noResultsDesc', language)}
            </p>
          </div>
        )}

        {/* Suggested Questions - Mobile Optimized */}
        {!searchPerformed && (
          <div className="slide-up">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-white" />
              {t('suggestedQuestions', language)}
            </h3>
            <div className="grid gap-3">
              {suggestedQuestions.slice(0, 6).map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedQuestionClick(question)}
                  className="w-full text-left p-4 rounded-xl glass-card hover:bg-white/10 text-gray-300 hover:text-white transition-all duration-200 text-sm leading-relaxed glass-hover interactive"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchInterface;