class AnalyticsService {
  constructor() {
    this.isEnabled = true;
    this.sessionId = this.generateSessionId();
    this.events = [];
    this.startTime = Date.now();
  }

  generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  track(eventName, properties = {}) {
    if (!this.isEnabled) return;

    const event = {
      id: this.generateEventId(),
      name: eventName,
      properties,
      timestamp: Date.now(),
      sessionId: this.sessionId,
      url: window.location.href,
      userAgent: navigator.userAgent,
      language: navigator.language
    };

    this.events.push(event);
    this.saveToLocalStorage();
    
    // Console log for development
    console.log('Analytics Event:', event);
  }

  generateEventId() {
    return 'event_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  saveToLocalStorage() {
    try {
      const analyticsData = {
        events: this.events.slice(-100), // Keep only last 100 events
        sessionId: this.sessionId
      };
      localStorage.setItem('spiritual_qa_analytics', JSON.stringify(analyticsData));
    } catch (error) {
      console.error('Error saving analytics data:', error);
    }
  }

  loadFromLocalStorage() {
    try {
      const saved = localStorage.getItem('spiritual_qa_analytics');
      if (saved) {
        const data = JSON.parse(saved);
        this.events = data.events || [];
      }
    } catch (error) {
      console.error('Error loading analytics data:', error);
    }
  }

  // Predefined tracking methods
  trackPageView(pageName) {
    this.track('page_view', { page: pageName });
  }

  trackSearch(query, language, resultsCount, searchTime) {
    this.track('search_performed', {
      query: query.substring(0, 100), // Limit query length for privacy
      language,
      results_count: resultsCount,
      search_time_ms: searchTime
    });
  }

  trackVideoClick(videoId, timestamp, source = 'search_result') {
    this.track('video_clicked', {
      video_id: videoId,
      timestamp,
      source
    });
  }

  trackFavoriteAction(action, resultId) {
    this.track('favorite_action', {
      action, // 'add' or 'remove'
      result_id: resultId
    });
  }

  trackLanguageChange(fromLanguage, toLanguage) {
    this.track('language_changed', {
      from_language: fromLanguage,
      to_language: toLanguage
    });
  }

  trackVoiceSearch(duration, success, language) {
    this.track('voice_search', {
      duration_ms: duration,
      success,
      language
    });
  }

  trackProcessingStart() {
    this.track('processing_started');
  }

  trackError(errorType, errorMessage, context) {
    this.track('error_occurred', {
      error_type: errorType,
      error_message: errorMessage.substring(0, 200),
      context
    });
  }

  trackPerformance(metricName, value, unit = 'ms') {
    this.track('performance_metric', {
      metric_name: metricName,
      value,
      unit
    });
  }

  // Get analytics insights
  getSessionStats() {
    const sessionEvents = this.events.filter(e => e.sessionId === this.sessionId);
    const searchEvents = sessionEvents.filter(e => e.name === 'search_performed');
    const videoClicks = sessionEvents.filter(e => e.name === 'video_clicked');
    
    return {
      session_duration: Date.now() - this.startTime,
      total_events: sessionEvents.length,
      searches_performed: searchEvents.length,
      videos_clicked: videoClicks.length,
      unique_queries: new Set(searchEvents.map(e => e.properties.query)).size
    };
  }

  getPopularQueries(limit = 10) {
    const searchEvents = this.events.filter(e => e.name === 'search_performed');
    const queryCount = {};
    
    searchEvents.forEach(event => {
      const query = event.properties.query?.toLowerCase();
      if (query) {
        queryCount[query] = (queryCount[query] || 0) + 1;
      }
    });

    return Object.entries(queryCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, limit)
      .map(([query, count]) => ({ query, count }));
  }

  getUserInsights() {
    const events = this.events;
    const searches = events.filter(e => e.name === 'search_performed');
    const languageChanges = events.filter(e => e.name === 'language_changed');
    
    return {
      total_sessions: new Set(events.map(e => e.sessionId)).size,
      total_searches: searches.length,
      languages_used: [...new Set(searches.map(e => e.properties.language))],
      language_switches: languageChanges.length,
      avg_search_time: searches.length > 0 
        ? searches.reduce((sum, e) => sum + (e.properties.search_time_ms || 0), 0) / searches.length 
        : 0
    };
  }

  clearData() {
    this.events = [];
    localStorage.removeItem('spiritual_qa_analytics');
  }

  exportData() {
    return {
      events: this.events,
      session_stats: this.getSessionStats(),
      user_insights: this.getUserInsights(),
      exported_at: new Date().toISOString()
    };
  }

  enable() {
    this.isEnabled = true;
  }

  disable() {
    this.isEnabled = false;
  }
}

export const analyticsService = new AnalyticsService();