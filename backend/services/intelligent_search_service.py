"""
Intelligent Semantic Search Service for Spiritual Q&A
Handles question understanding, intent recognition, and semantic matching
"""

import os
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
import re
import math
from collections import Counter
import json

logger = logging.getLogger(__name__)

class IntelligentSearchService:
    def __init__(self):
        self.spiritual_keywords = {
            # Hindi spiritual terms
            'गुरु': ['teacher', 'master', 'guide', 'spiritual_teacher', 'guru'],
            'ध्यान': ['meditation', 'dhyan', 'concentration', 'mindfulness'],
            'भक्ति': ['devotion', 'bhakti', 'worship', 'love', 'surrender'],
            'कर्म': ['karma', 'action', 'deed', 'work', 'duty'],
            'मोक्ष': ['moksha', 'liberation', 'salvation', 'enlightenment'],
            'आत्मा': ['soul', 'atma', 'self', 'spirit'],
            'परमात्मा': ['god', 'divine', 'supreme', 'paramatma'],
            'शांति': ['peace', 'shanti', 'calm', 'tranquility'],
            'प्रेम': ['love', 'prem', 'divine_love', 'affection'],
            'समर्पण': ['surrender', 'dedication', 'samarpan'],
            'साधना': ['sadhana', 'practice', 'spiritual_practice'],
            'सत्संग': ['satsang', 'spiritual_gathering', 'holy_company'],
            'दीक्षा': ['diksha', 'initiation', 'blessing'],
            'मन': ['mind', 'thoughts', 'mental'],
            'गुस्सा': ['anger', 'rage', 'fury', 'emotions'],
            'दुख': ['suffering', 'pain', 'sorrow', 'sadness'],
            'सुख': ['happiness', 'joy', 'pleasure', 'bliss'],
            
            # English terms
            'meditation': ['ध्यान', 'dhyan', 'concentration', 'mindfulness'],
            'guru': ['गुरु', 'teacher', 'master', 'guide'],
            'devotion': ['भक्ति', 'bhakti', 'worship', 'love'],
            'karma': ['कर्म', 'action', 'deed', 'work'],
            'peace': ['शांति', 'shanti', 'calm', 'tranquility'],
            'love': ['प्रेम', 'prem', 'divine_love'],
            'surrender': ['समर्पण', 'samarpan', 'dedication'],
            'anger': ['गुस्सा', 'rage', 'fury', 'emotions'],
            'suffering': ['दुख', 'pain', 'sorrow'],
            'happiness': ['सुख', 'joy', 'bliss']
        }
        
        # Common question patterns
        self.question_patterns = {
            'how_to': ['कैसे', 'कैसे करें', 'how to', 'how can', 'what is the way'],
            'what_is': ['क्या है', 'what is', 'what does', 'meaning of'],
            'why': ['क्यों', 'why', 'why is', 'for what reason'],
            'when': ['कब', 'when', 'at what time'],
            'where': ['कहाँ', 'where', 'at which place'],
            'who': ['कौन', 'who', 'which person'],
            'benefits': ['फायदे', 'लाभ', 'benefits', 'advantages', 'importance'],
            'problems': ['समस्या', 'परेशानी', 'problem', 'issue', 'difficulty'],
            'solution': ['समाधान', 'उपाय', 'solution', 'remedy', 'way out']
        }
    
    def understand_question_intent(self, query: str) -> Dict[str, Any]:
        """Analyze user question to understand intent and extract key concepts"""
        query_lower = query.lower()
        
        intent_analysis = {
            'query': query,
            'language': self._detect_language(query),
            'intent_type': 'general',
            'spiritual_concepts': [],
            'question_type': 'general',
            'key_terms': [],
            'urgency': 'normal',
            'emotional_context': 'neutral'
        }
        
        # Detect question type
        for pattern_type, patterns in self.question_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                intent_analysis['question_type'] = pattern_type
                break
        
        # Extract spiritual concepts
        for concept, related_terms in self.spiritual_keywords.items():
            if concept in query_lower or any(term in query_lower for term in related_terms):
                intent_analysis['spiritual_concepts'].append(concept)
        
        # Extract key terms (remove stop words)
        words = re.findall(r'\w+', query_lower)
        stop_words = {'है', 'में', 'को', 'का', 'की', 'के', 'से', 'पर', 'और', 'या', 'भी', 'तो', 'ही', 'न', 'नहीं',
                     'the', 'is', 'in', 'to', 'of', 'for', 'on', 'and', 'or', 'but', 'not', 'a', 'an'}
        intent_analysis['key_terms'] = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Detect emotional context
        emotional_words = {
            'urgent': ['तुरंत', 'जल्दी', 'urgent', 'immediately', 'quickly'],
            'sad': ['दुखी', 'परेशान', 'sad', 'depressed', 'worried', 'troubled'],
            'confused': ['समझ नहीं आता', 'confused', 'unclear', 'doubt'],
            'seeking': ['चाहिए', 'खोज रहा', 'need', 'want', 'seeking', 'looking for']
        }
        
        for emotion, words in emotional_words.items():
            if any(word in query_lower for word in words):
                intent_analysis['emotional_context'] = emotion
                break
        
        return intent_analysis
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is primarily Hindi or English"""
        hindi_chars = re.findall(r'[\u0900-\u097F]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)
        
        if len(hindi_chars) > len(english_chars):
            return 'hi'
        elif len(english_chars) > 0:
            return 'en'
        else:
            return 'mixed'
    
    async def find_relevant_answers(self, intent_analysis: Dict[str, Any], qa_database: List[Dict]) -> List[Dict[str, Any]]:
        """Find most relevant answers using semantic matching"""
        
        if not qa_database:
            logger.warning("No Q&A database provided")
            return []
        
        scored_answers = []
        
        for qa_item in qa_database:
            try:
                relevance_score = self._calculate_relevance_score(intent_analysis, qa_item)
                
                if relevance_score > 0.3:  # Minimum threshold
                    enhanced_qa = qa_item.copy()
                    enhanced_qa['relevance_score'] = relevance_score
                    enhanced_qa['match_explanation'] = self._explain_match(intent_analysis, qa_item, relevance_score)
                    scored_answers.append(enhanced_qa)
                    
            except Exception as e:
                logger.error(f"Error scoring Q&A item: {str(e)}")
                continue
        
        # Sort by relevance score (highest first)
        scored_answers.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Return top 5 most relevant answers
        return scored_answers[:5]
    
    def _calculate_relevance_score(self, intent: Dict[str, Any], qa_item: Dict[str, Any]) -> float:
        """Calculate how relevant a Q&A item is to the user's question"""
        
        score = 0.0
        max_score = 0.0
        
        query = intent['query'].lower()
        question = qa_item.get('question', '').lower()
        answer = qa_item.get('answer', '').lower()
        tags = qa_item.get('tags', [])
        
        # 1. Direct keyword matching in question (40% weight)
        max_score += 40
        keyword_matches = 0
        for term in intent['key_terms']:
            if term in question:
                keyword_matches += 2  # Higher weight for question match
            elif term in answer:
                keyword_matches += 1  # Lower weight for answer match
        
        if intent['key_terms']:
            keyword_score = min(40, (keyword_matches / len(intent['key_terms'])) * 40)
            score += keyword_score
        
        # 2. Spiritual concept matching (30% weight)
        max_score += 30
        concept_matches = 0
        for concept in intent['spiritual_concepts']:
            if concept in question or concept in answer:
                concept_matches += 3
            # Check related terms
            related_terms = self.spiritual_keywords.get(concept, [])
            for term in related_terms:
                if term in question:
                    concept_matches += 2
                elif term in answer:
                    concept_matches += 1
        
        if intent['spiritual_concepts']:
            concept_score = min(30, (concept_matches / (len(intent['spiritual_concepts']) * 3)) * 30)
            score += concept_score
        
        # 3. Question type matching (15% weight)
        max_score += 15
        question_type_score = 0
        if intent['question_type'] != 'general':
            patterns = self.question_patterns[intent['question_type']]
            if any(pattern in question for pattern in patterns):
                question_type_score = 15
        score += question_type_score
        
        # 4. Tag matching (10% weight)
        max_score += 10
        tag_score = 0
        for concept in intent['spiritual_concepts']:
            if concept in tags or any(related in tags for related in self.spiritual_keywords.get(concept, [])):
                tag_score += 5
        score += min(10, tag_score)
        
        # 5. Language preference (5% weight)
        max_score += 5
        qa_language = qa_item.get('language', 'hi')
        if qa_language == intent['language'] or intent['language'] == 'mixed':
            score += 5
        
        # Normalize score to 0-1 range
        normalized_score = score / max_score if max_score > 0 else 0
        
        # Apply confidence boost from original Q&A confidence
        original_confidence = qa_item.get('confidence_score', 0.8)
        final_score = normalized_score * 0.8 + original_confidence * 0.2
        
        return min(1.0, final_score)
    
    def _explain_match(self, intent: Dict[str, Any], qa_item: Dict[str, Any], score: float) -> str:
        """Generate explanation for why this answer was matched"""
        explanations = []
        
        question = qa_item.get('question', '').lower()
        answer = qa_item.get('answer', '').lower()
        
        # Check keyword matches
        matched_terms = [term for term in intent['key_terms'] if term in question or term in answer]
        if matched_terms:
            explanations.append(f"Keywords: {', '.join(matched_terms[:3])}")
        
        # Check concept matches
        matched_concepts = [concept for concept in intent['spiritual_concepts'] 
                          if concept in question or concept in answer]
        if matched_concepts:
            explanations.append(f"Concepts: {', '.join(matched_concepts[:2])}")
        
        # Score interpretation
        if score > 0.8:
            quality = "Excellent match"
        elif score > 0.6:
            quality = "Good match"
        elif score > 0.4:
            quality = "Moderate match"
        else:
            quality = "Basic match"
        
        explanation = f"{quality}"
        if explanations:
            explanation += f" ({'; '.join(explanations)})"
        
        return explanation
    
    def enhance_search_results(self, results: List[Dict[str, Any]], intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enhance search results with additional metadata and formatting"""
        
        enhanced_results = []
        
        for i, result in enumerate(results):
            enhanced = result.copy()
            
            # Add ranking information
            enhanced['search_rank'] = i + 1
            enhanced['search_intent'] = intent['question_type']
            enhanced['matched_language'] = intent['language']
            
            # Format the answer based on question type
            if intent['question_type'] == 'how_to':
                enhanced['formatted_answer'] = self._format_how_to_answer(enhanced['answer'])
            elif intent['question_type'] == 'what_is':
                enhanced['formatted_answer'] = self._format_definition_answer(enhanced['answer'])
            else:
                enhanced['formatted_answer'] = enhanced['answer']
            
            # Add contextual suggestions
            enhanced['related_questions'] = self._suggest_related_questions(intent, enhanced)
            
            # Ensure proper video URLs
            enhanced['youtube_url'] = f"https://www.youtube.com/watch?v={enhanced['video_id']}"
            enhanced['timestamp_url'] = f"https://www.youtube.com/watch?v={enhanced['video_id']}&t={int(enhanced['start_time'])}s"
            
            enhanced_results.append(enhanced)
        
        return enhanced_results
    
    def _format_how_to_answer(self, answer: str) -> str:
        """Format how-to answers with better structure"""
        # Add step indicators if not present
        if '।' in answer:  # Hindi sentence endings
            sentences = answer.split('।')
            formatted = ""
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    formatted += f"{i+1}. {sentence.strip()}।\n"
            return formatted.strip()
        else:
            return answer
    
    def _format_definition_answer(self, answer: str) -> str:
        """Format definition answers with better clarity"""
        return answer  # For now, return as-is
    
    def _suggest_related_questions(self, intent: Dict[str, Any], qa_item: Dict[str, Any]) -> List[str]:
        """Suggest related questions based on the current context"""
        suggestions = []
        
        concepts = intent['spiritual_concepts']
        question_type = intent['question_type']
        
        # Generate contextual suggestions
        if 'गुरु' in concepts or 'guru' in concepts:
            suggestions.extend([
                "गुरु दीक्षा क्यों जरूरी है?",
                "गुरु की पहचान कैसे करें?",
                "How to serve the guru?"
            ])
        
        if 'ध्यान' in concepts or 'meditation' in concepts:
            suggestions.extend([
                "ध्यान में मन क्यों भटकता है?",
                "ध्यान की सही विधि क्या है?",
                "How long should I meditate?"
            ])
        
        return suggestions[:3]  # Return top 3 suggestions

# Global instance
intelligent_search = IntelligentSearchService()