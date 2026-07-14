import { useState, useEffect } from 'react';

const SEARCH_HISTORY_KEY = 'spiritual_qa_search_history';
const MAX_HISTORY_ITEMS = 20;

export const useSearchHistory = () => {
  const [searchHistory, setSearchHistory] = useState([]);

  useEffect(() => {
    const savedHistory = localStorage.getItem(SEARCH_HISTORY_KEY);
    if (savedHistory) {
      try {
        setSearchHistory(JSON.parse(savedHistory));
      } catch (error) {
        console.error('Error loading search history:', error);
        setSearchHistory([]);
      }
    }
  }, []);

  const saveHistory = (newHistory) => {
    setSearchHistory(newHistory);
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(newHistory));
  };

  const addToHistory = (query, results = []) => {
    if (!query.trim()) return;

    const historyItem = {
      id: Date.now().toString(),
      query: query.trim(),
      results_count: results.length,
      searched_at: new Date().toISOString(),
      language: results[0]?.language || 'auto'
    };

    // Remove duplicate queries
    const newHistory = [
      historyItem,
      ...searchHistory.filter(item => item.query.toLowerCase() !== query.toLowerCase())
    ].slice(0, MAX_HISTORY_ITEMS);

    saveHistory(newHistory);
  };

  const removeFromHistory = (itemId) => {
    const newHistory = searchHistory.filter(item => item.id !== itemId);
    saveHistory(newHistory);
  };

  const clearHistory = () => {
    saveHistory([]);
  };

  const getRecentSearches = (limit = 5) => {
    return searchHistory.slice(0, limit);
  };

  const getPopularSearches = (limit = 5) => {
    // Group by query and count occurrences
    const queryCount = searchHistory.reduce((acc, item) => {
      const query = item.query.toLowerCase();
      acc[query] = (acc[query] || 0) + 1;
      return acc;
    }, {});

    // Sort by count and return top queries
    return Object.entries(queryCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, limit)
      .map(([query, count]) => ({ query, count }));
  };

  return {
    searchHistory,
    addToHistory,
    removeFromHistory,
    clearHistory,
    getRecentSearches,
    getPopularSearches,
    historyCount: searchHistory.length
  };
};