import { useState, useEffect } from 'react';

const OFFLINE_CACHE_KEY = 'spiritual_qa_offline_cache';
const CACHE_EXPIRY_TIME = 24 * 60 * 60 * 1000; // 24 hours
const MAX_CACHED_RESULTS = 50;

export const useOfflineStorage = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [cachedResults, setCachedResults] = useState({});

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Load cached results
    loadCachedResults();

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const loadCachedResults = () => {
    try {
      const cached = localStorage.getItem(OFFLINE_CACHE_KEY);
      if (cached) {
        const parsedCache = JSON.parse(cached);
        // Filter out expired entries
        const now = Date.now();
        const validCache = Object.entries(parsedCache).reduce((acc, [key, value]) => {
          if (now - value.timestamp < CACHE_EXPIRY_TIME) {
            acc[key] = value;
          }
          return acc;
        }, {});
        setCachedResults(validCache);
        localStorage.setItem(OFFLINE_CACHE_KEY, JSON.stringify(validCache));
      }
    } catch (error) {
      console.error('Error loading cached results:', error);
    }
  };

  const cacheSearchResults = (query, results) => {
    if (!query.trim() || !results.length) return;

    const cacheKey = query.toLowerCase().trim();
    const cacheEntry = {
      query,
      results,
      timestamp: Date.now()
    };

    const newCache = {
      ...cachedResults,
      [cacheKey]: cacheEntry
    };

    // Limit cache size
    const cacheEntries = Object.entries(newCache);
    if (cacheEntries.length > MAX_CACHED_RESULTS) {
      // Remove oldest entries
      const sortedEntries = cacheEntries.sort(([,a], [,b]) => b.timestamp - a.timestamp);
      const limitedCache = Object.fromEntries(sortedEntries.slice(0, MAX_CACHED_RESULTS));
      setCachedResults(limitedCache);
      localStorage.setItem(OFFLINE_CACHE_KEY, JSON.stringify(limitedCache));
    } else {
      setCachedResults(newCache);
      localStorage.setItem(OFFLINE_CACHE_KEY, JSON.stringify(newCache));
    }
  };

  const getCachedResults = (query) => {
    const cacheKey = query.toLowerCase().trim();
    const cached = cachedResults[cacheKey];
    
    if (cached && Date.now() - cached.timestamp < CACHE_EXPIRY_TIME) {
      return cached.results;
    }
    
    return null;
  };

  const clearCache = () => {
    setCachedResults({});
    localStorage.removeItem(OFFLINE_CACHE_KEY);
  };

  const getCacheStats = () => {
    const entries = Object.values(cachedResults);
    return {
      totalQueries: entries.length,
      totalResults: entries.reduce((sum, entry) => sum + entry.results.length, 0),
      oldestEntry: entries.length > 0 ? Math.min(...entries.map(e => e.timestamp)) : null,
      newestEntry: entries.length > 0 ? Math.max(...entries.map(e => e.timestamp)) : null
    };
  };

  return {
    isOnline,
    cacheSearchResults,
    getCachedResults,
    clearCache,
    getCacheStats,
    hasCachedResults: Object.keys(cachedResults).length > 0
  };
};