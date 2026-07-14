class NotificationService {
  constructor() {
    this.isSupported = 'Notification' in window;
    this.permission = this.isSupported ? Notification.permission : 'denied';
  }

  async requestPermission() {
    if (!this.isSupported) {
      return 'denied';
    }

    try {
      const permission = await Notification.requestPermission();
      this.permission = permission;
      return permission;
    } catch (error) {
      console.error('Error requesting notification permission:', error);
      return 'denied';
    }
  }

  showNotification(title, options = {}) {
    if (this.permission !== 'granted') {
      return null;
    }

    const defaultOptions = {
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
      tag: 'spiritual-qa',
      renotify: false,
      requireInteraction: false,
      ...options
    };

    try {
      return new Notification(title, defaultOptions);
    } catch (error) {
      console.error('Error showing notification:', error);
      return null;
    }
  }

  showSearchCompleteNotification(resultsCount, language = 'en') {
    const title = language === 'hi' 
      ? 'खोज पूर्ण!' 
      : 'Search Complete!';
    
    const body = language === 'hi'
      ? `${resultsCount} परिणाम मिले`
      : `Found ${resultsCount} results`;

    return this.showNotification(title, {
      body,
      icon: '/icons/search-icon.png',
      tag: 'search-complete'
    });
  }

  showProcessingCompleteNotification(videosProcessed, language = 'en') {
    const title = language === 'hi'
      ? 'प्रोसेसिंग पूर्ण!'
      : 'Processing Complete!';
    
    const body = language === 'hi'
      ? `${videosProcessed} वीडियो प्रोसेस किए गए`
      : `${videosProcessed} videos processed`;

    return this.showNotification(title, {
      body,
      icon: '/icons/process-icon.png',
      tag: 'processing-complete'
    });
  }

  showNewContentNotification(newVideosCount, language = 'en') {
    const title = language === 'hi'
      ? 'नई सामग्री उपलब्ध!'
      : 'New Content Available!';
    
    const body = language === 'hi'
      ? `${newVideosCount} नए वीडियो जोड़े गए`
      : `${newVideosCount} new videos added`;

    return this.showNotification(title, {
      body,
      icon: '/icons/new-content-icon.png',
      tag: 'new-content',
      requireInteraction: true
    });
  }

  scheduleNotification(title, options, delay) {
    setTimeout(() => {
      this.showNotification(title, options);
    }, delay);
  }

  clearNotifications(tag) {
    // Clear notifications with specific tag (browser-dependent)
    if (tag) {
      // This is a placeholder as there's no standard way to clear notifications by tag
      console.log(`Clearing notifications with tag: ${tag}`);
    }
  }
}

export const notificationService = new NotificationService();