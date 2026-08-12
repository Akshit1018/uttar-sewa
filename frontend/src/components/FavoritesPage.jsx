import React, { useState } from 'react';
import { Heart, Clock, Trash2, Share2, X } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { useFavorites } from '../hooks/useFavorites';
import { useToast } from '../hooks/use-toast';
import { t } from '../utils/translations';
import { formatTimestamp } from '../lib/youtube';
import { VideoTimestampLink, VideoHomeLink } from './VideoTimestampLink';

const FavoritesPage = ({ language }) => {
  const { favorites, removeFromFavorites, clearFavorites, getFavoritesByCategory } = useFavorites();
  const { toast } = useToast();
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categorizedFavorites = getFavoritesByCategory();
  const categories = ['all', ...Object.keys(categorizedFavorites).sort().reverse()];

  const handleRemoveFavorite = (favoriteId) => {
    removeFromFavorites(favoriteId);
    toast({
      title: language === 'hi' ? 'पसंदीदा से हटाया गया' : 'Removed from Favorites',
      description: language === 'hi' ? 'आइटम सफलतापूर्वक हटाया गया' : 'Item removed successfully',
    });
  };

  const handleClearAll = () => {
    clearFavorites();
    toast({
      title: language === 'hi' ? 'सभी पसंदीदा साफ किए गए' : 'All Favorites Cleared',
      description: language === 'hi' ? 'सभी पसंदीदा आइटम हटा दिए गए' : 'All favorite items have been removed',
    });
  };

  const handleShare = async (favorite) => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: favorite.question,
          text: favorite.answer,
          url: favorite.timestamp_url
        });
      } catch (error) {
        console.error('Error sharing:', error);
      }
    } else {
      // Fallback to clipboard
      navigator.clipboard.writeText(favorite.timestamp_url);
      toast({
        title: language === 'hi' ? 'लिंक कॉपी किया गया' : 'Link Copied',
        description: language === 'hi' ? 'लिंक क्लिपबोर्ड में कॉपी हो गया' : 'Link copied to clipboard',
      });
    }
  };

  const getFilteredFavorites = () => {
    if (selectedCategory === 'all') {
      return favorites;
    }
    return categorizedFavorites[selectedCategory] || [];
  };

  const filteredFavorites = getFilteredFavorites();

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="px-4 py-8 sm:px-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white mb-2 flex items-center gap-3">
            <Heart className="w-6 h-6 text-red-400" />
            {language === 'hi' ? 'पसंदीदा' : 'Favorites'}
          </h1>
          <p className="text-gray-400 text-sm">
            {language === 'hi' 
              ? `आपके ${favorites.length} पसंदीदा प्रश्न-उत्तर`
              : `Your ${favorites.length} favorite Q&As`
            }
          </p>
        </div>

        {/* Category Filter */}
        {categories.length > 1 && (
          <div className="mb-6">
            <div className="flex gap-2 overflow-x-auto custom-scrollbar pb-2">
              {categories.map((category) => (
                <Button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  variant={selectedCategory === category ? "default" : "outline"}
                  className={`whitespace-nowrap text-sm ${
                    selectedCategory === category
                      ? 'bg-white text-black'
                      : 'border-white/20 text-gray-300 hover:bg-white/10'
                  }`}
                >
                  {category === 'all' 
                    ? (language === 'hi' ? 'सभी' : 'All')
                    : new Date(category).toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                        month: 'short',
                        day: 'numeric'
                      })
                  }
                  {category !== 'all' && (
                    <Badge variant="secondary" className="ml-2 bg-white/20 text-white">
                      {categorizedFavorites[category]?.length || 0}
                    </Badge>
                  )}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Clear All Button */}
        {favorites.length > 0 && (
          <div className="mb-6 flex justify-end">
            <Button
              onClick={handleClearAll}
              variant="outline"
              className="border-red-500/50 text-red-400 hover:bg-red-500/10"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              {language === 'hi' ? 'सभी साफ करें' : 'Clear All'}
            </Button>
          </div>
        )}

        {/* Favorites List */}
        {filteredFavorites.length > 0 ? (
          <div className="space-y-4">
            {filteredFavorites.map((favorite) => (
              <Card 
                key={favorite.id} 
                className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl hover:bg-white/10 transition-all duration-300 glass-card-hover"
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-white text-base leading-relaxed font-semibold flex-1 mr-4">
                      {favorite.question}
                    </CardTitle>
                    <div className="flex gap-2">
                      <Button
                        onClick={() => handleShare(favorite)}
                        variant="ghost"
                        size="sm"
                        className="text-gray-400 hover:text-white p-2"
                      >
                        <Share2 className="w-4 h-4" />
                      </Button>
                      <Button
                        onClick={() => handleRemoveFavorite(favorite.id)}
                        variant="ghost"
                        size="sm"
                        className="text-red-400 hover:text-red-300 p-2"
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-3">
                    <Badge className="bg-white/10 text-white border-white/20 rounded-full px-3 py-1 text-xs">
                      {(favorite.video_title || '').substring(0, 40)}...
                    </Badge>
                    <Badge className="bg-white/10 text-white border-white/20 rounded-full px-3 py-1 text-xs">
                      <Clock className="w-3 h-3 mr-1" />
                      {formatTimestamp(favorite.start_time)}
                    </Badge>
                    <Badge className="bg-green-500/20 text-green-400 border-green-500/30 rounded-full px-3 py-1 text-xs">
                      <Heart className="w-3 h-3 mr-1" />
                      {language === 'hi' ? 'पसंदीदा' : 'Favorite'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-gray-300 leading-relaxed mb-4 text-sm">
                    {favorite.answer}
                  </p>
                  
                  <div className="flex flex-col sm:flex-row gap-3">
                    <VideoTimestampLink
                      videoId={favorite.video_id}
                      startTime={favorite.start_time}
                      timestampUrl={favorite.timestamp_url}
                      label={`${language === 'hi' ? 'वीडियो देखें' : 'Watch Video'} (${formatTimestamp(favorite.start_time)})`}
                      className="bg-white text-black hover:bg-gray-100 rounded-xl px-4 py-3 font-medium transition-colors duration-200 flex-1"
                    />
                    <VideoHomeLink
                      videoId={favorite.video_id}
                      youtubeUrl={favorite.youtube_url}
                      label={language === 'hi' ? 'पूरा वीडियो' : 'Full Video'}
                      className="border-white/20 text-gray-300 hover:bg-white/10 rounded-xl px-4 py-3 backdrop-blur-sm"
                    />
                  </div>

                  <div className="mt-3 text-xs text-gray-500">
                    {language === 'hi' ? 'जोड़ा गया:' : 'Added:'} {' '}
                    {new Date(favorite.added_at).toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Heart className="w-8 h-8 text-gray-500" />
            </div>
            <h3 className="text-lg font-semibold text-gray-400 mb-2">
              {selectedCategory === 'all'
                ? (language === 'hi' ? 'कोई पसंदीदा नहीं' : 'No Favorites Yet')
                : (language === 'hi' ? 'इस दिनांक में कोई पसंदीदा नहीं' : 'No Favorites for This Date')
              }
            </h3>
            <p className="text-gray-500 text-sm">
              {language === 'hi' 
                ? 'खोज परिणामों में दिल आइकन पर टैप करके अपने पसंदीदा जोड़ें'
                : 'Tap the heart icon on search results to add your favorites'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FavoritesPage;