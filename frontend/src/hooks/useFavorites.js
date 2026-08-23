import { useState, useEffect, useCallback } from 'react';

import { API } from '../lib/backend';
import { controlHeaders } from '../lib/control';

const FAVORITES_KEY = 'spiritual_qa_favorites';

const favoriteId = (item) => `${item.video_id || ''}_${item.start_time || 0}_${item.question || ''}`;

const toFavorite = (result) => ({
  id: favoriteId(result),
  question: result.question,
  answer: result.answer,
  video_id: result.video_id,
  video_title: result.video_title,
  start_time: result.start_time,
  end_time: result.end_time,
  confidence_score: result.confidence_score,
  youtube_url: result.youtube_url,
  timestamp_url: result.timestamp_url,
  added_at: result.added_at || result.pinned_at || new Date().toISOString(),
});

const readLocal = () => {
  try {
    return JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]');
  } catch (error) {
    return [];
  }
};

const writeLocal = (items) => {
  try {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(items));
  } catch (error) {
    // private mode
  }
};

const mergeFavorites = (localItems, remoteItems) => {
  const byId = new Map();
  [...remoteItems, ...localItems].forEach((item) => {
    const row = toFavorite(item);
    byId.set(row.id, row);
  });
  return Array.from(byId.values());
};

export const useFavorites = () => {
  const [favorites, setFavorites] = useState(readLocal);

  const saveFavorites = (newFavorites) => {
    setFavorites(newFavorites);
    writeLocal(newFavorites);
  };

  const loadRemote = useCallback(async () => {
    try {
      const response = await fetch(`${API}/control/qa/pinned`);
      if (!response.ok) return;
      const data = await response.json();
      const remote = (data.items || []).map(toFavorite);
      saveFavorites(mergeFavorites(readLocal(), remote));
    } catch (error) {
      // offline: keep local
    }
  }, []);

  useEffect(() => {
    loadRemote();
  }, [loadRemote]);

  const addToFavorites = async (result) => {
    const favoriteItem = toFavorite(result);
    const newFavorites = [favoriteItem, ...favorites.filter((fav) => fav.id !== favoriteItem.id)];
    saveFavorites(newFavorites);
    try {
      await fetch(`${API}/control/qa/pin`, {
        method: 'POST',
        headers: controlHeaders(),
        body: JSON.stringify({
          question: favoriteItem.question,
          answer: favoriteItem.answer,
          video_id: favoriteItem.video_id,
          video_title: favoriteItem.video_title,
          start_time: favoriteItem.start_time || 0,
          timestamp_url: favoriteItem.timestamp_url,
        }),
      });
    } catch (error) {
      // local remains source if API is down
    }
    return true;
  };

  const removeFromFavorites = async (resultId) => {
    const target = favorites.find((fav) => fav.id === resultId);
    const newFavorites = favorites.filter((fav) => fav.id !== resultId);
    saveFavorites(newFavorites);
    if (target) {
      try {
        await fetch(`${API}/control/qa/unpin`, {
          method: 'POST',
          headers: controlHeaders(),
          body: JSON.stringify({
            video_id: target.video_id || '',
            question: target.question || '',
          }),
        });
      } catch (error) {
        // ignore
      }
    }
    return true;
  };

  const isFavorite = (result) => {
    const id = favoriteId(result);
    return favorites.some((fav) => fav.id === id);
  };

  const clearFavorites = async () => {
    const snapshot = [...favorites];
    saveFavorites([]);
    await Promise.all(
      snapshot.map((item) =>
        fetch(`${API}/control/qa/unpin`, {
          method: 'POST',
          headers: controlHeaders(),
          body: JSON.stringify({ video_id: item.video_id || '', question: item.question || '' }),
        }).catch(() => null)
      )
    );
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
    favoritesCount: favorites.length,
  };
};
