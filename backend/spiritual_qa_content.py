"""
Manual Q&A Content for Spiritual Videos
This file contains manually curated Q&A pairs for videos that don't have captions.
"""

# Expanded spiritual Q&A pairs in Hindi/English for comprehensive testing
SPIRITUAL_QA_LIBRARY = [
    # Guru and Spiritual Guidance
    {
        "question": "गुरु की शरण में कैसे जाएं?",
        "answer": "गुरु की शरण में जाने के लिए पूर्ण समर्पण, विनम्रता और श्रद्धा चाहिए। अपने अहंकार को छोड़कर गुरु के चरणों में सिर झुकाना होता है। गुरु की आज्ञा का पालन करना और उनके बताए मार्ग पर चलना ही शरणागति है।",
        "tags": ["guru", "surrender", "spirituality", "guidance"],
        "confidence_score": 0.95
    },
    {
        "question": "गुरु दीक्षा क्यों जरूरी है?",
        "answer": "गुरु दीक्षा के बिना आध्यात्मिक प्रगति संभव नहीं। दीक्षा से गुरु शिष्य में अपनी शक्ति का संचार करते हैं। यह आध्यात्मिक जन्म है जो मुक्ति का मार्ग खोलता है। दीक्षा के द्वारा शिष्य को सत्य का ज्ञान प्राप्त होता है।",
        "tags": ["diksha", "guru", "initiation", "spiritual_birth"],
        "confidence_score": 0.93
    },
    {
        "question": "How to find a true guru?",
        "answer": "A true guru is selfless, has conquered their ego, and guides disciples without expecting anything in return. They possess deep spiritual knowledge and radiate peace and love. The sincere seeker's inner calling will lead them to their destined guru when the time is right.",
        "tags": ["guru", "spiritual_teacher", "guidance", "seeking"],
        "confidence_score": 0.91
    },
    
    # Bhakti and Devotion
    {
        "question": "भक्ति का सच्चा अर्थ क्या है?",
        "answer": "भक्ति का सच्चा अर्थ है परमात्मा के प्रति निस्वार्थ प्रेम। यह केवल मांगना नहीं बल्कि पूर्ण समर्पण है। भक्ति में भक्त और भगवान का अंतर मिट जाता है। सच्ची भक्ति में अहंकार का लेश भी नहीं होता।",
        "tags": ["bhakti", "devotion", "love", "surrender"],
        "confidence_score": 0.92
    },
    {
        "question": "How to develop devotion?",
        "answer": "To develop devotion, start with regular prayer and meditation. Listen to spiritual discourses, read sacred texts, and serve others selflessly. Keep the company of devotees and surrender your ego to the divine. Practice gratitude and see the divine in all beings.",
        "tags": ["devotion", "bhakti", "development", "practice"],
        "confidence_score": 0.88
    },
    {
        "question": "प्रेम और मोह में अंतर क्या है?",
        "answer": "प्रेम निस्वार्थ होता है जबकि मोह में स्वार्थ होता है। प्रेम में त्याग होता है, मोह में भोग। प्रेम मुक्ति देता है, मोह बांधता है। सच्चा प्रेम केवल परमात्मा से हो सकता है। प्रेम विस्तार करता है, मोह सिकोड़ता है।",
        "tags": ["love", "attachment", "spirituality", "difference"],
        "confidence_score": 0.94
    },
    
    # Meditation and Sadhana
    {
        "question": "साधना में मन कैसे लगाएं?",
        "answer": "साधना में मन लगाने के लिए नियमित अभ्यास जरूरी है। प्रतिदिन एक निश्चित समय पर बैठना, गुरु मंत्र का जाप करना और सत्संग सुनना आवश्यक है। धीरे-धीरे समय बढ़ाते जाना चाहिए और धैर्य रखना चाहिए।",
        "tags": ["sadhana", "meditation", "practice", "discipline"],
        "confidence_score": 0.88
    },
    {
        "question": "ध्यान में मन भटकता है क्या करें?",
        "answer": "ध्यान में मन का भटकना स्वाभाविक है। जब मन भटके तो धीरे से वापस मंत्र या सांस पर ध्यान लगाएं। जबरदस्ती न करें, धैर्य रखें। नियमित अभ्यास से मन स्थिर होगा। मन को दोस्त बनाएं, दुश्मन नहीं।",
        "tags": ["meditation", "mind", "concentration", "practice"],
        "confidence_score": 0.86
    },
    {
        "question": "What is the best time for meditation?",
        "answer": "The early morning hours (4-6 AM) are considered ideal for meditation as the mind is naturally calm and the environment is peaceful. However, consistency is more important than timing. Choose a time you can maintain daily and stick to it.",
        "tags": ["meditation", "timing", "practice", "morning"],
        "confidence_score": 0.84
    },
    {
        "question": "मंत्र जप का महत्व क्या है?",
        "answer": "मंत्र जप से मन को एकाग्र करने में सहायता मिलती है। गुरु दिया हुआ मंत्र विशेष शक्ति रखता है। मंत्र की ध्वनि से चित्त शुद्ध होता है और आध्यात्मिक उन्नति होती है। नियमित जप से अंतर्मन में शांति आती है।",
        "tags": ["mantra", "japa", "chanting", "concentration"],
        "confidence_score": 0.90
    },
    
    # Peace and Mental Health
    {
        "question": "मन की शांति कैसे मिले?",
        "answer": "मन की शांति गुरु कृपा से मिलती है। नाम जप, सत्संग, और सेवा करने से मन स्थिर होता है। अपेक्षाओं को छोड़कर प्रभु की इच्छा में चलना शांति देता है। अतीत और भविष्य की चिंता छोड़कर वर्तमान में जीना सीखें।",
        "tags": ["peace", "mind", "spirituality", "calmness"],
        "confidence_score": 0.90
    },
    {
        "question": "गुस्से को कैसे काबू करें?",
        "answer": "गुस्से को काबू करने के लिए सबसे पहले साक्षी भाव अपनाना होता है। जब गुस्सा आए तो गहरी सांस लें और गुरु को याद करें। नियमित ध्यान से मन शांत होता है। क्षमा करना सीखें और दूसरों की गलतियों को समझने की कोशिश करें।",
        "tags": ["anger", "control", "emotions", "forgiveness"],
        "confidence_score": 0.87
    },
    {
        "question": "How to handle stress and anxiety?",
        "answer": "Stress and anxiety arise from attachment to outcomes and fear of the future. Practice surrender to the divine will, live in the present moment, and maintain regular spiritual practices. Deep breathing, meditation, and prayer help calm the mind. Trust that everything happens for your highest good.",
        "tags": ["stress", "anxiety", "mental_health", "surrender"],
        "confidence_score": 0.85
    },
    {
        "question": "निराशा से कैसे निकलें?",
        "answer": "निराशा तब आती है जब हम अपनी अपेक्षाओं से जुड़े होते हैं। प्रभु की इच्छा को अपनी इच्छा बनाना सीखें। हर परिस्थिति में सीखने का अवसर देखें। सत्संग सुनें और संतों के जीवन से प्रेरणा लें। याद रखें कि ये सब परीक्षा है।",
        "tags": ["depression", "despair", "hope", "acceptance"],
        "confidence_score": 0.83
    },
    
    # Life Purpose and Meaning
    {
        "question": "What is the purpose of human life?",
        "answer": "The purpose of human life is to realize our true nature and attain union with the divine. We should use this precious human birth for spiritual growth, serve others, and ultimately return to our source - God. Life is an opportunity to evolve spiritually and break free from the cycle of birth and death.",
        "tags": ["purpose", "life", "spirituality", "self_realization"],
        "confidence_score": 0.92
    },
    {
        "question": "जीवन का अर्थ क्या है?",
        "answer": "जीवन का अर्थ है परमात्मा को पाना। मानव जन्म दुर्लभ है और इसका उपयोग आध्यात्मिक उन्नति के लिए करना चाहिए। जीवन का लक्ष्य मोक्ष प्राप्त करना है। सेवा, भक्ति और ज्ञान के द्वारा जीवन को सार्थक बनाना चाहिए।",
        "tags": ["meaning", "life", "purpose", "moksha"],
        "confidence_score": 0.91
    },
    {
        "question": "Why do we suffer?",
        "answer": "Suffering comes from attachment to the temporary world and ignorance of our true nature. It is also the result of past karmas. Suffering teaches us detachment, compassion, and helps us turn towards the divine. It purifies the soul and strengthens our faith when accepted with surrender.",
        "tags": ["suffering", "karma", "detachment", "purification"],
        "confidence_score": 0.89
    },
    
    # Karma and Action
    {
        "question": "कर्म बंधन से कैसे मुक्त हों?",
        "answer": "कर्म बंधन से मुक्ति निष्काम कर्म से होती है। फल की इच्छा न करके केवल कर्तव्य के लिए कर्म करना चाहिए। सभी कर्म प्रभु को समर्पित कर देना चाहिए। कर्म में कुशलता प्राप्त करने से भी बंधन से मुक्ति मिलती है।",
        "tags": ["karma", "liberation", "action", "detachment"],
        "confidence_score": 0.89
    },
    {
        "question": "What is the law of karma?",
        "answer": "The law of karma states that every action has consequences. Good actions lead to positive results, and negative actions lead to suffering. Karma operates across lifetimes and is the cosmic law of justice. Understanding karma helps us take responsibility for our actions and their consequences.",
        "tags": ["karma", "law", "consequence", "justice"],
        "confidence_score": 0.87
    },
    {
        "question": "बुरे कर्म का प्रायश्चित क्या है?",
        "answer": "बुरे कर्म का प्रायश्चित्त है सच्चे मन से पश्चाताप करना और भविष्य में वैसा न करने का संकल्प लेना। भगवान से क्षमा मांगना, दान-पुण्य करना, और अच्छे कर्म करना प्रायश्चित्त है। गुरु की शरण में जाना सबसे बड़ा प्रायश्चित्त है।",
        "tags": ["repentance", "forgiveness", "atonement", "purification"],
        "confidence_score": 0.85
    },
    
    # Spiritual Community and Service
    {
        "question": "सत्संग का महत्व क्या है?",
        "answer": "सत्संग आध्यात्मिक जीवन का आधार है। सत्संग से बुद्धि शुद्ध होती है, भक्ति बढ़ती है और संस्कार सुधरते हैं। संतों की संगति से मन में पवित्रता आती है। सत्संग हमें सत्य के मार्ग पर चलने की प्रेरणा देता है।",
        "tags": ["satsang", "spirituality", "company", "purification"],
        "confidence_score": 0.91
    },
    {
        "question": "सेवा का महत्व क्या है?",
        "answer": "सेवा से अहंकार का नाश होता है और हृदय में प्रेम बढ़ता है। निस्वार्थ सेवा से चित्त शुद्ध होता है। सेवा भक्ति का एक अंग है। दूसरों की सेवा करने से भगवान प्रसन्न होते हैं। सेवा से आत्मिक संतुष्टि मिलती है।",
        "tags": ["service", "seva", "selflessness", "purification"],
        "confidence_score": 0.88
    },
    
    # Happiness and Fulfillment
    {
        "question": "What is true happiness?",
        "answer": "True happiness comes from within, not from external things. It is found in connecting with the divine, serving others, and living in harmony with natural laws. Material pleasures give temporary joy, but spiritual bliss is eternal. Happiness is our natural state when the mind is at peace.",
        "tags": ["happiness", "bliss", "spirituality", "inner_peace"],
        "confidence_score": 0.90
    },
    {
        "question": "संतुष्टि कैसे पाएं?",
        "answer": "संतुष्टि इच्छाओं को कम करने से आती है, बढ़ाने से नहीं। जो मिला है उसमें खुश रहना सीखें। दूसरों से तुलना न करें। भगवान जो देते हैं उसे प्रसाद समझकर स्वीकार करें। आध्यात्मिक संपदा में वृद्धि करने से सच्ची संतुष्टि मिलती है।",
        "tags": ["contentment", "satisfaction", "desires", "acceptance"],
        "confidence_score": 0.86
    },
    
    # Death and Beyond
    {
        "question": "मृत्यु के बाद क्या होता है?",
        "answer": "मृत्यु के बाद आत्मा अपने कर्मों के अनुसार नया जन्म लेती है। अच्छे कर्म करने वाले को अच्छी योनि मिलती है। बुरे कर्म करने वाले को कष्ट भोगना पड़ता है। लेकिन गुरु कृपा से जीवन-मृत्यु के चक्र से मुक्ति पाई जा सकती है।",
        "tags": ["death", "rebirth", "karma", "liberation"],
        "confidence_score": 0.84
    },
    {
        "question": "मोक्ष कैसे प्राप्त करें?",
        "answer": "मोक्ष प्राप्त करने के लिए गुरु की शरण में जाना आवश्यक है। नियमित भक्ति, ध्यान, सेवा और सत्संग करना चाहिए। अहंकार को त्यागकर पूर्ण समर्पण करना होता है। संसार से वैराग्य और परमात्मा से प्रेम होना जरूरी है।",
        "tags": ["moksha", "liberation", "salvation", "enlightenment"],
        "confidence_score": 0.93
    },
    
    # Additional Practical Questions
    {
        "question": "How to practice non-attachment?",
        "answer": "Non-attachment means performing your duties without being attached to results. Offer all actions to God, accept whatever comes with equanimity, and remember that everything in this world is temporary. Focus on the eternal rather than the transient. Practice witnessing your thoughts and emotions without getting identified with them.",
        "tags": ["non-attachment", "detachment", "karma", "equanimity"],
        "confidence_score": 0.87
    },
    {
        "question": "परिवार के साथ कैसे रहें?",
        "answer": "परिवार में रहकर भी आध्यात्मिक जीवन जिया जा सकता है। सभी से प्रेम करें लेकिन आसक्त न हों। अपने कर्तव्यों का पालन करें। परिवारजनों को भी भक्ति के मार्ग पर लाने की कोशिश करें। घर को मंदिर की तरह पवित्र रखें।",
        "tags": ["family", "relationships", "duty", "spirituality"],
        "confidence_score": 0.82
    },
    {
        "question": "आज के युग में साधना कैसे करें?",
        "answer": "कलियुग में नाम जप सबसे उत्तम साधना है। व्यस्त जीवन में भी थोड़ा समय भगवान के लिए निकालें। सुबह-शाम नियमित ध्यान करें। सत्संग ऑनलाइन भी सुन सकते हैं। मन में सदा भगवान का स्मरण रखें।",
        "tags": ["modern_life", "kaliyuga", "practice", "busy_life"],
        "confidence_score": 0.81
    },
    {
        "question": "संदेह और अविश्वास कैसे दूर करें?",
        "answer": "संदेह अज्ञान से आता है। शास्त्र अध्ययन और सत्संग से ज्ञान बढ़ाएं। संतों के जीवन चरित्र पढ़ें। अपने अनुभव पर भरोसा रखें। धैर्य रखें और निरंतर अभ्यास करते रहें। गुरु पर पूर्ण श्रद्धा रखें।",
        "tags": ["doubt", "faith", "trust", "knowledge"],
        "confidence_score": 0.83
    }
]