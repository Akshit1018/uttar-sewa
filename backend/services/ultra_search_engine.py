"""
ULTRA-ROBUST SPIRITUAL Q&A SEARCH ENGINE
Enterprise-grade system for 80%+ question understanding and relevance matching
"""

import os
import asyncio
import logging
import re
import math
import json
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
import difflib
from datetime import datetime

logger = logging.getLogger(__name__)

class UltraRobustSearchEngine:
    def __init__(self):
        """Initialize the ultra-robust search engine with multiple strategies"""
        
        # Enhanced spiritual vocabulary with synonyms and variations
        self.spiritual_vocabulary = {
            # Guru related terms
            'guru_terms': {
                'hindi': ['गुरु', 'गुरुजी', 'गुरुदेव', 'महाराज', 'मास्टर', 'शिक्षक', 'गुरुदीक्षा', 'गुरुकृपा'],
                'english': ['guru', 'teacher', 'master', 'guide', 'spiritual_teacher', 'preceptor', 'mentor'],
                'concepts': ['guidance', 'teaching', 'initiation', 'blessing', 'grace', 'surrender']
            },
            
            # Meditation related terms
            'meditation_terms': {
                'hindi': ['ध्यान', 'धारणा', 'समाधि', 'एकाग्रता', 'मनन', 'चिंतन', 'अध्यात्म'],
                'english': ['meditation', 'dhyan', 'concentration', 'mindfulness', 'contemplation', 'focus'],
                'concepts': ['practice', 'technique', 'method', 'sitting', 'breathing', 'awareness']
            },
            
            # Devotion related terms
            'devotion_terms': {
                'hindi': ['भक्ति', 'प्रेम', 'श्रद्धा', 'समर्पण', 'सेवा', 'पूजा', 'प्रार्थना', 'आराधना'],
                'english': ['devotion', 'bhakti', 'love', 'worship', 'prayer', 'service', 'surrender'],
                'concepts': ['faith', 'dedication', 'commitment', 'offering', 'ritual', 'divine_love']
            },
            
            # Spiritual problems terms
            'problem_terms': {
                'hindi': ['समस्या', 'परेशानी', 'दुख', 'कष्ट', 'बाधा', 'विकार', 'गुस्सा', 'क्रोध', 'भय', 'चिंता'],
                'english': ['problem', 'issue', 'suffering', 'pain', 'anger', 'fear', 'worry', 'trouble', 'difficulty'],
                'concepts': ['solution', 'remedy', 'cure', 'relief', 'healing', 'overcome']
            },
            
            # Spiritual goals terms
            'goal_terms': {
                'hindi': ['मोक्ष', 'मुक्ति', 'शांति', 'आनंद', 'प्रकाश', 'ज्ञान', 'सत्य', 'परमात्मा'],
                'english': ['liberation', 'moksha', 'peace', 'bliss', 'enlightenment', 'truth', 'realization'],
                'concepts': ['attainment', 'achievement', 'goal', 'purpose', 'destination', 'ultimate']
            }
        }
        
        # Advanced question patterns with weights
        self.question_patterns = {
            'how_to_patterns': {
                'patterns': ['कैसे', 'कैसे करें', 'कैसे करूं', 'विधि', 'तरीका', 'उपाय', 'how to', 'how can', 'how do', 'method', 'way to'],
                'weight': 1.0,
                'intent': 'procedural'
            },
            'what_is_patterns': {
                'patterns': ['क्या है', 'क्या होता है', 'अर्थ', 'मतलब', 'परिभाषा', 'what is', 'what does', 'meaning', 'definition'],
                'weight': 0.9,
                'intent': 'definitional'
            },
            'why_patterns': {
                'patterns': ['क्यों', 'किसलिए', 'कारण', 'वजह', 'why', 'reason', 'purpose', 'for what'],
                'weight': 0.8,
                'intent': 'causal'
            },
            'when_patterns': {
                'patterns': ['कब', 'कितनी देर', 'समय', 'when', 'how long', 'duration', 'time'],
                'weight': 0.7,
                'intent': 'temporal'
            },
            'problem_patterns': {
                'patterns': ['समस्या', 'परेशानी', 'दिक्कत', 'problem', 'issue', 'trouble', 'difficulty'],
                'weight': 1.2,  # Higher weight for problems
                'intent': 'problem_solving'
            }
        }
        
        # Context enhancers
        self.context_enhancers = {
            'urgency_indicators': ['तुरंत', 'जल्दी', 'urgent', 'immediately', 'quickly', 'help'],
            'emotional_indicators': ['दुखी', 'परेशान', 'खुश', 'sad', 'happy', 'troubled', 'peaceful'],
            'depth_indicators': ['गहरा', 'विस्तार', 'detailed', 'deep', 'thorough', 'complete']
        }
        
        # Scoring weights for different matching strategies
        self.scoring_weights = {
            'exact_match': 0.25,        # 25% - Exact question match
            'semantic_similarity': 0.30, # 30% - Semantic understanding
            'keyword_relevance': 0.20,   # 20% - Keyword matching
            'context_match': 0.15,       # 15% - Context understanding
            'intent_match': 0.10         # 10% - Intent matching
        }
    
    async def ultra_search(self, user_query: str, qa_database: List[Dict]) -> List[Dict[str, Any]]:
        """
        Ultra-robust search that combines multiple strategies for maximum accuracy
        """
        if not qa_database:
            logger.warning("Empty Q&A database")
            return []
        
        # Step 1: Advanced Query Analysis
        query_analysis = self._ultra_analyze_query(user_query)
        logger.info(f"Ultra Query Analysis: {query_analysis}")
        
        # Step 2: Multi-Strategy Matching
        scored_results = []
        
        for qa_item in qa_database:
            try:
                # Get scores from multiple strategies
                scores = self._get_multi_strategy_scores(query_analysis, qa_item)
                
                # Calculate weighted final score
                final_score = self._calculate_weighted_score(scores)
                
                if final_score > 0.2:  # Minimum threshold
                    enhanced_qa = qa_item.copy()
                    enhanced_qa['ultra_relevance_score'] = final_score
                    enhanced_qa['scoring_breakdown'] = scores
                    enhanced_qa['match_confidence'] = self._calculate_confidence(scores, query_analysis)
                    enhanced_qa['match_explanation'] = self._generate_detailed_explanation(scores, query_analysis, qa_item)
                    scored_results.append(enhanced_qa)
                    
            except Exception as e:
                logger.error(f"Error in ultra-search scoring: {str(e)}")
                continue
        
        # Step 3: Advanced Ranking and Re-ranking
        ranked_results = self._ultra_rank_results(scored_results, query_analysis)
        
        # Step 4: Quality Assurance and Filtering
        final_results = self._quality_filter_results(ranked_results, query_analysis)
        
        logger.info(f"Ultra-search found {len(final_results)} high-quality results")
        return final_results[:5]  # Return top 5
    
    def _ultra_analyze_query(self, query: str) -> Dict[str, Any]:
        """Ultra-detailed query analysis with advanced NLP"""
        
        analysis = {
            'original_query': query,
            'normalized_query': self._normalize_text(query),
            'language': self._detect_language_advanced(query),
            'query_length': len(query.split()),
            'complexity_score': self._calculate_query_complexity(query),
            
            # Advanced extractions
            'spiritual_concepts': self._extract_spiritual_concepts(query),
            'question_intent': self._classify_question_intent(query),
            'emotional_context': self._analyze_emotional_context(query),
            'specificity_level': self._analyze_specificity(query),
            'urgency_level': self._analyze_urgency(query),
            
            # Keywords and phrases
            'primary_keywords': self._extract_primary_keywords(query),
            'secondary_keywords': self._extract_secondary_keywords(query),
            'key_phrases': self._extract_key_phrases(query),
            'negation_terms': self._extract_negations(query),
            
            # Context
            'requires_examples': self._needs_examples(query),
            'requires_steps': self._needs_step_by_step(query),
            'is_comparative': self._is_comparative_question(query),
            'is_personal': self._is_personal_question(query)
        }
        
        return analysis
    
    def _get_multi_strategy_scores(self, query_analysis: Dict, qa_item: Dict) -> Dict[str, float]:
        """Get scores from multiple matching strategies"""
        
        scores = {}
        
        # Strategy 1: Exact Match Score
        scores['exact_match'] = self._calculate_exact_match_score(query_analysis, qa_item)
        
        # Strategy 2: Semantic Similarity Score
        scores['semantic_similarity'] = self._calculate_semantic_similarity(query_analysis, qa_item)
        
        # Strategy 3: Keyword Relevance Score
        scores['keyword_relevance'] = self._calculate_keyword_relevance(query_analysis, qa_item)
        
        # Strategy 4: Context Match Score
        scores['context_match'] = self._calculate_context_match(query_analysis, qa_item)
        
        # Strategy 5: Intent Match Score
        scores['intent_match'] = self._calculate_intent_match(query_analysis, qa_item)
        
        return scores
    
    def _calculate_exact_match_score(self, query_analysis: Dict, qa_item: Dict) -> float:
        """Calculate exact match score with fuzzy matching"""
        
        query = query_analysis['normalized_query']
        question = self._normalize_text(qa_item.get('question', ''))
        answer = self._normalize_text(qa_item.get('answer', ''))
        
        # Direct similarity
        question_similarity = difflib.SequenceMatcher(None, query, question).ratio()
        
        # Check for exact phrase matches
        query_words = set(query.split())
        question_words = set(question.split())
        
        exact_word_matches = len(query_words.intersection(question_words))
        total_query_words = len(query_words) if query_words else 1
        
        word_match_ratio = exact_word_matches / total_query_words
        
        # Combined score
        exact_score = (question_similarity * 0.7) + (word_match_ratio * 0.3)
        
        return min(1.0, exact_score)
    
    def _calculate_semantic_similarity(self, query_analysis: Dict, qa_item: Dict) -> float:
        """Advanced semantic similarity using concept matching"""
        
        score = 0.0
        max_score = 0.0
        
        query_concepts = query_analysis['spiritual_concepts']
        question = qa_item.get('question', '').lower()
        answer = qa_item.get('answer', '').lower()
        
        # Concept-based matching
        for concept_category, concepts in query_concepts.items():
            max_score += 1.0
            
            category_score = 0.0
            
            # Check if concepts appear in question/answer
            for concept in concepts:
                if concept in question:
                    category_score += 0.6  # Higher weight for question
                elif concept in answer:
                    category_score += 0.4  # Lower weight for answer
                
                # Check synonyms and related terms
                related_terms = self._get_related_terms(concept)
                for term in related_terms:
                    if term in question:
                        category_score += 0.3
                    elif term in answer:
                        category_score += 0.2
            
            score += min(1.0, category_score)
        
        return score / max_score if max_score > 0 else 0.0
    
    def _calculate_keyword_relevance(self, query_analysis: Dict, qa_item: Dict) -> float:
        """Calculate keyword relevance with TF-IDF style weighting"""
        
        primary_keywords = query_analysis['primary_keywords']
        secondary_keywords = query_analysis['secondary_keywords']
        
        question = qa_item.get('question', '').lower()
        answer = qa_item.get('answer', '').lower()
        
        score = 0.0
        total_weight = 0.0
        
        # Primary keywords (higher weight)
        for keyword in primary_keywords:
            total_weight += 3.0
            if keyword in question:
                score += 3.0
            elif keyword in answer:
                score += 1.5
        
        # Secondary keywords (lower weight)
        for keyword in secondary_keywords:
            total_weight += 1.0
            if keyword in question:
                score += 1.0
            elif keyword in answer:
                score += 0.5
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def _calculate_context_match(self, query_analysis: Dict, qa_item: Dict) -> float:
        """Calculate context matching score"""
        
        score = 0.0
        
        # Intent matching
        query_intent = query_analysis['question_intent']['type']
        if self._matches_intent(query_intent, qa_item):
            score += 0.4
        
        # Emotional context matching
        if query_analysis['emotional_context']['emotion'] != 'neutral':
            if self._matches_emotional_context(query_analysis['emotional_context'], qa_item):
                score += 0.3
        
        # Specificity matching
        if query_analysis['specificity_level'] == 'high':
            if self._is_detailed_answer(qa_item):
                score += 0.3
        
        return min(1.0, score)
    
    def _calculate_intent_match(self, query_analysis: Dict, qa_item: Dict) -> float:
        """Calculate intent matching score"""
        
        query_intent = query_analysis['question_intent']
        
        # Check if the Q&A matches the intent type
        if query_intent['type'] == 'procedural' and self._has_procedural_content(qa_item):
            return 0.9
        elif query_intent['type'] == 'definitional' and self._has_definitional_content(qa_item):
            return 0.8
        elif query_intent['type'] == 'problem_solving' and self._has_solution_content(qa_item):
            return 1.0
        else:
            return 0.3  # Partial match
    
    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """Calculate final weighted score"""
        
        final_score = 0.0
        
        for strategy, weight in self.scoring_weights.items():
            if strategy in scores:
                final_score += scores[strategy] * weight
        
        return min(1.0, final_score)
    
    def _ultra_rank_results(self, results: List[Dict], query_analysis: Dict) -> List[Dict]:
        """Advanced ranking with multiple criteria"""
        
        # Primary sort by ultra_relevance_score
        results.sort(key=lambda x: x['ultra_relevance_score'], reverse=True)
        
        # Secondary ranking adjustments
        for i, result in enumerate(results):
            # Boost for exact matches
            if result['scoring_breakdown'].get('exact_match', 0) > 0.8:
                result['ranking_boost'] = 0.1
            
            # Boost for problem-solving queries
            if query_analysis['question_intent']['type'] == 'problem_solving':
                if self._has_solution_content(result):
                    result['ranking_boost'] = result.get('ranking_boost', 0) + 0.15
            
            # Apply ranking boost
            if 'ranking_boost' in result:
                result['ultra_relevance_score'] = min(1.0, result['ultra_relevance_score'] + result['ranking_boost'])
        
        # Re-sort after boosts
        results.sort(key=lambda x: x['ultra_relevance_score'], reverse=True)
        
        return results
    
    def _quality_filter_results(self, results: List[Dict], query_analysis: Dict) -> List[Dict]:
        """Quality assurance filtering"""
        
        filtered_results = []
        
        for result in results:
            # Minimum quality threshold
            if result['ultra_relevance_score'] < 0.3:
                continue
            
            # Ensure answer is substantive
            answer_length = len(result.get('answer', ''))
            if answer_length < 20:  # Too short
                continue
            
            # Ensure relevance explanation makes sense
            if not result.get('match_explanation'):
                continue
            
            filtered_results.append(result)
        
        return filtered_results
    
    # Helper methods for analysis
    def _normalize_text(self, text: str) -> str:
        """Advanced text normalization"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip().lower())
        
        # Remove punctuation but keep meaning
        text = re.sub(r'[^\w\s\u0900-\u097F]', ' ', text)
        
        return text
    
    def _detect_language_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced language detection"""
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = hindi_chars + english_chars
        
        if total_chars == 0:
            return {'primary': 'unknown', 'confidence': 0.0, 'is_mixed': False}
        
        hindi_ratio = hindi_chars / total_chars
        english_ratio = english_chars / total_chars
        
        if hindi_ratio > 0.6:
            return {'primary': 'hi', 'confidence': hindi_ratio, 'is_mixed': english_ratio > 0.2}
        elif english_ratio > 0.6:
            return {'primary': 'en', 'confidence': english_ratio, 'is_mixed': hindi_ratio > 0.2}
        else:
            return {'primary': 'mixed', 'confidence': 0.5, 'is_mixed': True}
    
    def _extract_spiritual_concepts(self, query: str) -> Dict[str, List[str]]:
        """Extract spiritual concepts from query"""
        concepts = defaultdict(list)
        query_lower = query.lower()
        
        for category, terms_dict in self.spiritual_vocabulary.items():
            for term_type, terms in terms_dict.items():
                for term in terms:
                    if term in query_lower:
                        concepts[category].append(term)
        
        return dict(concepts)
    
    def _classify_question_intent(self, query: str) -> Dict[str, Any]:
        """Classify the intent of the question"""
        query_lower = query.lower()
        
        for pattern_type, pattern_info in self.question_patterns.items():
            for pattern in pattern_info['patterns']:
                if pattern in query_lower:
                    return {
                        'type': pattern_info['intent'],
                        'confidence': pattern_info['weight'],
                        'pattern_matched': pattern
                    }
        
        return {'type': 'general', 'confidence': 0.5, 'pattern_matched': None}
    
    def _extract_primary_keywords(self, query: str) -> List[str]:
        """Extract primary keywords"""
        # Remove stop words and extract meaningful terms
        stop_words = {
            'है', 'हैं', 'में', 'को', 'का', 'की', 'के', 'से', 'पर', 'और', 'या', 'भी', 'तो', 'ही', 'न', 'नहीं',
            'the', 'is', 'are', 'in', 'to', 'of', 'for', 'on', 'and', 'or', 'but', 'not', 'a', 'an', 'how', 'what', 'why'
        }
        
        words = re.findall(r'\w+', query.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:5]  # Top 5 primary keywords
    
    def _extract_secondary_keywords(self, query: str) -> List[str]:
        """Extract secondary keywords"""
        # Extract related terms and synonyms
        primary = self._extract_primary_keywords(query)
        secondary = []
        
        for keyword in primary:
            related = self._get_related_terms(keyword)
            secondary.extend(related[:2])  # Top 2 related terms per keyword
        
        return list(set(secondary))
    
    def _get_related_terms(self, term: str) -> List[str]:
        """Get related terms for a given term"""
        related = []
        
        # Check in spiritual vocabulary
        for category, terms_dict in self.spiritual_vocabulary.items():
            for term_type, terms in terms_dict.items():
                if term in terms:
                    related.extend([t for t in terms if t != term])
        
        return related[:5]  # Top 5 related terms
    
    def _calculate_confidence(self, scores: Dict[str, float], query_analysis: Dict) -> float:
        """Calculate overall confidence in the match"""
        
        # Base confidence from weighted score
        base_confidence = sum(scores.values()) / len(scores)
        
        # Boost for high exact matches
        if scores.get('exact_match', 0) > 0.7:
            base_confidence += 0.2
        
        # Boost for multiple strategy agreement
        high_scores = sum(1 for score in scores.values() if score > 0.6)
        if high_scores >= 3:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _generate_detailed_explanation(self, scores: Dict[str, float], query_analysis: Dict, qa_item: Dict) -> str:
        """Generate detailed explanation of why this match was selected"""
        
        explanations = []
        
        # Exact match explanation
        if scores.get('exact_match', 0) > 0.7:
            explanations.append(f"High exact match ({scores['exact_match']:.2f})")
        
        # Semantic similarity explanation
        if scores.get('semantic_similarity', 0) > 0.6:
            concepts = query_analysis.get('spiritual_concepts', {})
            if concepts:
                concept_names = list(concepts.keys())[:2]
                explanations.append(f"Strong concept match ({', '.join(concept_names)})")
        
        # Keyword explanation
        if scores.get('keyword_relevance', 0) > 0.5:
            explanations.append(f"Keyword relevance ({scores['keyword_relevance']:.2f})")
        
        # Intent explanation
        intent = query_analysis.get('question_intent', {}).get('type', 'general')
        if scores.get('intent_match', 0) > 0.7:
            explanations.append(f"Intent match ({intent})")
        
        if not explanations:
            explanations.append("Basic relevance match")
        
        return " | ".join(explanations)
    
    # Additional helper methods
    def _calculate_query_complexity(self, query: str) -> float:
        """Calculate complexity of the query"""
        word_count = len(query.split())
        char_count = len(query)
        
        # Simple complexity based on length and structure
        complexity = (word_count * 0.1) + (char_count * 0.01)
        return min(1.0, complexity)
    
    def _analyze_emotional_context(self, query: str) -> Dict[str, Any]:
        """Analyze emotional context of query"""
        query_lower = query.lower()
        
        emotions = {
            'urgent': ['तुरंत', 'जल्दी', 'urgent', 'help', 'immediately'],
            'sad': ['दुखी', 'परेशान', 'sad', 'depressed', 'trouble'],
            'confused': ['समझ नहीं', 'confused', 'unclear', 'doubt'],
            'seeking': ['चाहिए', 'want', 'need', 'seeking']
        }
        
        for emotion, indicators in emotions.items():
            if any(indicator in query_lower for indicator in indicators):
                return {'emotion': emotion, 'confidence': 0.8}
        
        return {'emotion': 'neutral', 'confidence': 0.5}
    
    def _analyze_specificity(self, query: str) -> str:
        """Analyze how specific the query is"""
        word_count = len(query.split())
        specific_indicators = ['exactly', 'specifically', 'detailed', 'step by step', 'विस्तार', 'specific']
        
        if word_count > 10 or any(indicator in query.lower() for indicator in specific_indicators):
            return 'high'
        elif word_count > 5:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_urgency(self, query: str) -> str:
        """Analyze urgency level of query"""
        urgent_indicators = ['urgent', 'help', 'immediately', 'तुरंत', 'जल्दी']
        
        if any(indicator in query.lower() for indicator in urgent_indicators):
            return 'high'
        else:
            return 'normal'
    
    def _extract_key_phrases(self, query: str) -> List[str]:
        """Extract key phrases from query"""
        # Simple phrase extraction (could be enhanced with NLP)
        words = query.split()
        phrases = []
        
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)
        
        return phrases[:3]  # Top 3 phrases
    
    def _extract_negations(self, query: str) -> List[str]:
        """Extract negation terms"""
        negations = ['नहीं', 'न', 'बिना', 'not', 'no', 'without', 'never']
        return [neg for neg in negations if neg in query.lower()]
    
    def _needs_examples(self, query: str) -> bool:
        """Check if query needs examples"""
        example_indicators = ['example', 'उदाहरण', 'जैसे', 'like', 'such as']
        return any(indicator in query.lower() for indicator in example_indicators)
    
    def _needs_step_by_step(self, query: str) -> bool:
        """Check if query needs step-by-step answer"""
        step_indicators = ['step', 'steps', 'how to', 'कैसे', 'method', 'process']
        return any(indicator in query.lower() for indicator in step_indicators)
    
    def _is_comparative_question(self, query: str) -> bool:
        """Check if it's a comparative question"""
        comparative_indicators = ['difference', 'vs', 'versus', 'अंतर', 'better', 'best']
        return any(indicator in query.lower() for indicator in comparative_indicators)
    
    def _is_personal_question(self, query: str) -> bool:
        """Check if it's a personal question"""
        personal_indicators = ['my', 'mine', 'मेरा', 'मुझे', 'I', 'me']
        return any(indicator in query.lower() for indicator in personal_indicators)
    
    def _matches_intent(self, intent: str, qa_item: Dict) -> bool:
        """Check if Q&A matches the intent"""
        answer = qa_item.get('answer', '').lower()
        
        if intent == 'procedural':
            return any(word in answer for word in ['करें', 'करना', 'method', 'way', 'steps'])
        elif intent == 'definitional':
            return any(word in answer for word in ['है', 'होता', 'means', 'is', 'definition'])
        elif intent == 'problem_solving':
            return any(word in answer for word in ['समाधान', 'उपाय', 'solution', 'solve', 'remedy'])
        
        return False
    
    def _matches_emotional_context(self, emotional_context: Dict, qa_item: Dict) -> bool:
        """Check if Q&A matches emotional context"""
        emotion = emotional_context.get('emotion')
        answer = qa_item.get('answer', '').lower()
        
        if emotion == 'urgent':
            return any(word in answer for word in ['तुरंत', 'immediately', 'quick'])
        elif emotion == 'sad':
            return any(word in answer for word in ['शांति', 'peace', 'comfort', 'relief'])
        
        return False
    
    def _is_detailed_answer(self, qa_item: Dict) -> bool:
        """Check if answer is detailed"""
        answer = qa_item.get('answer', '')
        return len(answer) > 100  # Detailed if more than 100 characters
    
    def _has_procedural_content(self, qa_item: Dict) -> bool:
        """Check if Q&A has procedural content"""
        content = (qa_item.get('question', '') + ' ' + qa_item.get('answer', '')).lower()
        procedural_words = ['करें', 'करना', 'विधि', 'तरीका', 'how to', 'method', 'steps', 'process']
        return any(word in content for word in procedural_words)
    
    def _has_definitional_content(self, qa_item: Dict) -> bool:
        """Check if Q&A has definitional content"""
        content = (qa_item.get('question', '') + ' ' + qa_item.get('answer', '')).lower()
        definitional_words = ['है', 'होता', 'अर्थ', 'मतलब', 'is', 'means', 'definition']
        return any(word in content for word in definitional_words)
    
    def _has_solution_content(self, qa_item: Dict) -> bool:
        """Check if Q&A has solution content"""
        content = (qa_item.get('question', '') + ' ' + qa_item.get('answer', '')).lower()
        solution_words = ['समाधान', 'उपाय', 'हल', 'solution', 'solve', 'remedy', 'cure', 'fix']
        return any(word in content for word in solution_words)

# Global instance
ultra_search_engine = UltraRobustSearchEngine()