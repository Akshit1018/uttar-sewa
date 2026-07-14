import { useState, useEffect } from 'react';

const FAVORITES_KEY = 'spiritual_qa_favorites';

export const useFavorites = () => {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    const savedFavorites = localStorage.getItem(FAVORITES_KEY);
    if (savedFavorites) {
      try {
        setFavorites(JSON.parse(savedFavorites));
      } catch (error) {
        console.error('Error loading favorites:', error);
        setFavorites([]);
      }
    }
  }, []);

  const saveFavorites = (newFavorites) => {
    setFavorites(newFavorites);
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(newFavorites));
  };

  const addToFavorites = (result) => {
    const favoriteItem = {
      id: `${result.video_id}_${result.start_time}`,
      question: result.question,
      answer: result.answer,
      video_id: result.video_id,
      video_title: result.video_title,
      start_time: result.start_time,
      end_time: result.end_time,
      confidence_score: result.confidence_score,
      youtube_url: result.youtube_url,
      timestamp_url: result.timestamp_url,
      added_at: new Date().toISOString()
    };

    const newFavorites = [favoriteItem, ...favorites.filter(fav => fav.id !== favoriteItem.id)];
    saveFavorites(newFavorites);
    return true;
  };

  const removeFromFavorites = (resultId) => {
    const newFavorites = favorites.filter(fav => fav.id !== resultId);
    saveFavorites(newFavorites);
    return true;
  };

  const isFavorite = (result) => {
    const id = `${result.video_id}_${result.start_time}`;
    return favorites.some(fav => fav.id === id);
  };

  const clearFavorites = () => {
    saveFavorites([]);
  };

  const getFavoritesByCategory = () => {
    return favorites.reduce((acc, fav) => {
      const date = new Date(fav.added_at).toDateString();
      if (!acc[date]) {
        acc[date] = [];
      }
      acc[date].push(fav);
      return acc;
    }, {});
  };

  return {
    favorites,
    addToFavorites,
    removeFromFavorites,
    isFavorite,
    clearFavorites,
    getFavoritesByCategory,
    favoritesCount: favorites.length
  };
};