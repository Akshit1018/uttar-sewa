import { useState, useCallback, useRef } from 'react';

export const useDebounce = (callback, delay) => {
  const [debouncing, setDebouncing] = useState(false);
  const timeoutRef = useRef(null);

  const debouncedCallback = useCallback((...args) => {
    setDebouncing(true);
    
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      callback(...args);
      setDebouncing(false);
    }, delay);
  }, [callback, delay]);

  const cancel = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      setDebouncing(false);
    }
  }, []);

  return { debouncedCallback, debouncing, cancel };
};

export const useIntersectionObserver = (options = {}) => {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const [hasIntersected, setHasIntersected] = useState(false);
  const elementRef = useRef(null);
  const observerRef = useRef(null);

  const setRef = useCallback((node) => {
    if (elementRef.current) {
      observerRef.current?.disconnect();
    }

    if (node) {
      const observer = new IntersectionObserver(([entry]) => {
        setIsIntersecting(entry.isIntersecting);
        if (entry.isIntersecting && !hasIntersected) {
          setHasIntersected(true);
        }
      }, options);

      observer.observe(node);
      observerRef.current = observer;
      elementRef.current = node;
    }
  }, [options, hasIntersected]);

  return { ref: setRef, isIntersecting, hasIntersected };
};

export const useLazyLoad = (threshold = 0.1) => {
  const { ref, isIntersecting, hasIntersected } = useIntersectionObserver({
    threshold,
    rootMargin: '100px'
  });

  return { ref, shouldLoad: hasIntersected, isVisible: isIntersecting };
};

export const usePerformanceMonitor = () => {
  const [metrics, setMetrics] = useState({
    loadTime: 0,
    renderTime: 0,
    searchTime: 0
  });

  const measureLoadTime = useCallback(() => {
    if (window.performance && window.performance.timing) {
      const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
      setMetrics(prev => ({ ...prev, loadTime }));
    }
  }, []);

  const measureRenderTime = useCallback((startTime) => {
    const endTime = performance.now();
    const renderTime = endTime - startTime;
    setMetrics(prev => ({ ...prev, renderTime }));
    return renderTime;
  }, []);

  const measureSearchTime = useCallback((startTime) => {
    const endTime = performance.now();
    const searchTime = endTime - startTime;
    setMetrics(prev => ({ ...prev, searchTime }));
    return searchTime;
  }, []);

  return {
    metrics,
    measureLoadTime,
    measureRenderTime,
    measureSearchTime
  };
};