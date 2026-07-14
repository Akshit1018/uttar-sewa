export const translations = {
  hi: {
    // Header
    title: "आध्यात्मिक ज्ञान खोज",
    subtitle: "900+ आध्यात्मिक वीडियो से तुरंत उत्तर पाएं",
    searchPlaceholder: "अपना आध्यात्मिक प्रश्न यहाँ लिखें...",
    searchButton: "खोजें",
    
    // Navigation
    search: "खोज",
    processing: "प्रोसेसिंग",
    
    // Stats
    totalVideos: "कुल वीडियो",
    qaTotal: "प्रश्न-उत्तर",
    processedVideos: "प्रोसेस किए गए",
    
    // Search Results
    searchResults: "खोज परिणाम",
    noResultsTitle: "कोई परिणाम नहीं मिला",
    noResultsDesc: "कृपया अपना प्रश्न दोबारा लिखकर देखें",
    noSearchTitle: "कोई खोज शुरू करें",
    noSearchDesc: "अपना आध्यात्मिक प्रश्न लिखें या सुझाए गए प्रश्नों में से चुनें",
    
    // Video Actions
    watchVideo: "वीडियो देखें",
    fullVideo: "पूरा वीडियो",
    match: "मैच",
    
    // Suggested Questions
    suggestedQuestions: "सुझाए गए प्रश्न",
    suggestedNote: "ये सुझाए गए प्रश्न आपकी खोज में मदद कर सकते हैं",
    
    // Processing
    processingTitle: "वीडियो प्रोसेसिंग स्थिति",
    startProcessing: "वीडियो प्रोसेसिंग शुरू करें",
    startProcessingDesc: "सभी 900+ वीडियो को प्रोसेस करके Q&A डेटाबेस तैयार करें",
    processingStarted: "प्रोसेसिंग शुरू हो गई",
    processingStartedDesc: "सभी वीडियो प्रोसेस होने में कुछ समय लगेगा",
    processingComplete: "प्रोसेसिंग पूरी हो गई! 🎉",
    processingCompleteDesc: "अब आप सभी वीडियो में खोज कर सकते हैं",
    
    // Status
    pending: "प्रतीक्षा में",
    processing: "प्रोसेसिंग चल रही है",
    completed: "पूर्ण",
    failed: "असफल",
    progress: "प्रगति",
    currentVideo: "वर्तमान वीडियो:",
    refreshStatus: "स्थिति रीफ्रेश करें",
    startSearch: "खोज शुरू करें",
    
    // Toasts
    enterQuestion: "कृपया प्रश्न दर्ज करें",
    enterQuestionDesc: "खोजने के लिए कोई प्रश्न या विषय लिखें",
    searchError: "खोज में त्रुटि",
    searchErrorDesc: "कृपया कुछ देर बाद पुनः प्रयास करें",
    processingError: "त्रुटि",
    processingErrorDesc: "प्रोसेसिंग शुरू करने में समस्या हुई",
    
    // Sample Questions
    sampleQuestions: [
      "भक्ति का वास्तविक अर्थ क्या है?",
      "ध्यान कैसे करना चाहिए?",
      "मानसिक शांति कैसे पाएं?",
      "आध्यात्मिक जीवन कैसे जिएं?",
      "गुरु की आवश्यकता क्यों है?",
      "कर्म का सिद्धांत क्या है?",
      "मोक्ष कैसे प्राप्त करें?",
      "प्रेम और भक्ति में क्या अंतर है?",
      "जीवन का उद्देश्य क्या है?",
      "आत्मा और परमात्मा में क्या संबंध है?"
    ]
  },
  
  en: {
    // Header
    title: "Spiritual Knowledge Search",
    subtitle: "Get instant answers from 900+ spiritual videos",
    searchPlaceholder: "Ask your spiritual question here...",
    searchButton: "Search",
    
    // Navigation
    search: "Search",
    processing: "Processing",
    
    // Stats
    totalVideos: "Total Videos",
    qaTotal: "Q&A Pairs",
    processedVideos: "Processed Videos",
    
    // Search Results
    searchResults: "Search Results",
    noResultsTitle: "No Results Found",
    noResultsDesc: "Please try rephrasing your question",
    noSearchTitle: "Start a Search",
    noSearchDesc: "Enter your spiritual question or choose from suggested questions",
    
    // Video Actions
    watchVideo: "Watch Video",
    fullVideo: "Full Video",
    match: "Match",
    
    // Suggested Questions
    suggestedQuestions: "Suggested Questions",
    suggestedNote: "These suggested questions can help with your search",
    
    // Processing
    processingTitle: "Video Processing Status",
    startProcessing: "Start Video Processing",
    startProcessingDesc: "Process all 900+ videos to create Q&A database",
    processingStarted: "Processing Started",
    processingStartedDesc: "All videos will take some time to process",
    processingComplete: "Processing Complete! 🎉",
    processingCompleteDesc: "You can now search across all videos",
    
    // Status
    pending: "Pending",
    processing: "Processing",
    completed: "Completed",
    failed: "Failed",
    progress: "Progress",
    currentVideo: "Current Video:",
    refreshStatus: "Refresh Status",
    startSearch: "Start Search",
    
    // Toasts
    enterQuestion: "Please enter a question",
    enterQuestionDesc: "Write a question or topic to search",
    searchError: "Search Error",
    searchErrorDesc: "Please try again later",
    processingError: "Error",
    processingErrorDesc: "Problem starting processing",
    
    // Sample Questions
    sampleQuestions: [
      "What is the real meaning of bhakti?",
      "How should one practice meditation?",
      "How to achieve mental peace?",
      "How to live a spiritual life?",
      "Why do we need a guru?",
      "What is the principle of karma?",
      "How to attain liberation?",
      "What is the difference between love and devotion?",
      "What is the purpose of life?",
      "What is the relationship between soul and God?"
    ]
  }
};

export const t = (key, language = 'hi') => {
  return translations[language][key] || translations['hi'][key] || key;
};