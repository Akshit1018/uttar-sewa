import os
import asyncio
from typing import List, Dict, Optional, Any
import logging
import json
import re
import httpx

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        self.mistral_api_key = os.environ.get('MISTRAL_API_KEY')
        
    async def understand_user_query(self, user_query: str) -> Dict[str, Any]:
        """Use Mistral to understand user query and convert to searchable format"""
        try:
            # Use Mistral API directly for better multilingual understanding
            headers = {
                'Authorization': f'Bearer {self.mistral_api_key}',
                'Content-Type': 'application/json'
            }
            
            system_message = """You are an expert in Indian spirituality and philosophy. Your task is to understand user queries about spiritual topics in any language and convert them into a structured format for searching spiritual content.

Spiritual Concepts to Recognize:
- भक्ति (Bhakti): devotion, surrender, divine love
- ध्यान (Dhyan): meditation, concentration, mindfulness
- गुरु (Guru): spiritual teacher, guide, master
- कर्म (Karma): action, deed, law of cause and effect
- मोक्ष (Moksha): liberation, salvation, enlightenment
- आत्मा (Atma): soul, self, spirit
- परमात्मा (Paramatma): Supreme Soul, God, Divine
- शांति (Shanti): peace, tranquility, calmness
- प्रेम (Prem): divine love, spiritual love
- समर्पण (Samarpan): surrender, dedication

Rules:
1. Identify the core spiritual concept being asked about
2. Extract both Hindi and English keywords
3. Understand the intent behind the question
4. Categorize based on spiritual topics
5. Return JSON format only

Return format:
{
  "understood_query": "Clear spiritual question in simple language",
  "search_keywords": ["main_concept", "related_term1", "related_term2"],
  "hindi_keywords": ["हिंदी_कीवर्ड1", "हिंदी_कीवर्ड2"],
  "english_keywords": ["english_keyword1", "english_keyword2"],
  "category": "bhakti/meditation/guru/karma/moksha/peace/love/life-purpose",
  "intent": "What the user is really asking about",
  "language_detected": "hi/en/mr/mixed",
  "spiritual_concepts": ["concept1", "concept2"]
}"""

            payload = {
                "model": "mistral-large-latest",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Analyze this spiritual query: {user_query}"}
                ],
                "max_tokens": 800,
                "temperature": 0.2
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Parse the JSON response
                    query_analysis = self._parse_llm_response(content)
                    if query_analysis:
                        logger.info(f"Mistral analysis successful: {query_analysis}")
                        return query_analysis
                else:
                    logger.warning(f"Mistral API failed with status: {response.status_code}")
                
                # Fallback if Mistral fails
                logger.warning("Mistral API failed, using enhanced fallback analysis")
                return self._enhanced_fallback_analysis(user_query)
                
        except Exception as e:
            logger.error(f"Error in Mistral query understanding: {str(e)}")
            return self._enhanced_fallback_analysis(user_query)
    
    def _enhanced_fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Enhanced fallback query analysis with spiritual concepts"""
        query_lower = query.lower()
        
        # Enhanced spiritual keyword mapping
        spiritual_concepts = {
            'bhakti': {
                'keywords': ['भक्ति', 'bhakti', 'devotion', 'surrender', 'प्रेम', 'love', 'समर्पण'],
                'hindi': ['भक्ति', 'प्रेम', 'समर्पण', 'श्रद्धा'],
                'english': ['devotion', 'surrender', 'love', 'faith']
            },
            'meditation': {
                'keywords': ['ध्यान', 'dhyan', 'meditation', 'meditate', 'एकाग्रता', 'concentrate'],
                'hindi': ['ध्यान', 'समाधि', 'एकाग्रता', 'चित्त'],
                'english': ['meditation', 'concentration', 'mindfulness', 'focus']
            },
            'guru': {
                'keywords': ['गुरु', 'guru', 'teacher', 'guide', 'आचार्य', 'मार्गदर्शक'],
                'hindi': ['गुरु', 'आचार्य', 'शिक्षक', 'मार्गदर्शक'],
                'english': ['guru', 'teacher', 'guide', 'master']
            },
            'karma': {
                'keywords': ['कर्म', 'karma', 'action', 'deed', 'work', 'फल'],
                'hindi': ['कर्म', 'कार्य', 'फल', 'कृत्य'],
                'english': ['karma', 'action', 'deed', 'work']
            },
            'life-purpose': {
                'keywords': ['जीवन', 'life', 'उद्देश्य', 'purpose', 'meaning', 'अर्थ'],
                'hindi': ['जीवन', 'उद्देश्य', 'अर्थ', 'लक्ष्य'],
                'english': ['life', 'purpose', 'meaning', 'goal']
            },
            'peace': {
                'keywords': ['शांति', 'peace', 'शान्ति', 'calm', 'मानसिक', 'mental'],
                'hindi': ['शांति', 'चैन', 'सुकून', 'मानसिक'],
                'english': ['peace', 'calm', 'tranquil', 'mental']
            },
            'moksha': {
                'keywords': ['मोक्ष', 'moksha', 'liberation', 'salvation', 'मुक्ति', 'निर्वाण'],
                'hindi': ['मोक्ष', 'मुक्ति', 'कैवल्य', 'निर्वाण'],
                'english': ['moksha', 'liberation', 'salvation', 'enlightenment']
            }
        }
        
        # Detect language
        has_devanagari = any(char in query for char in 'अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह')
        detected_lang = 'hi' if has_devanagari else 'en'
        
        # Find matching spiritual concepts
        matched_concepts = []
        all_keywords = []
        hindi_keywords = []
        english_keywords = []
        primary_category = 'general'
        
        for concept_name, concept_data in spiritual_concepts.items():
            if any(keyword in query_lower for keyword in concept_data['keywords']):
                matched_concepts.append(concept_name)
                all_keywords.extend(concept_data['keywords'][:3])  # Limit keywords
                hindi_keywords.extend(concept_data['hindi'][:2])
                english_keywords.extend(concept_data['english'][:2])
                if primary_category == 'general':  # Take first match as primary
                    primary_category = concept_name
        
        # If no concepts matched, extract words from query
        if not matched_concepts:
            query_words = query.split()
            all_keywords = [word for word in query_words if len(word) > 2][:5]
            hindi_keywords = [word for word in query_words if any(char in word for char in 'अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह')][:3]
            english_keywords = [word for word in query_words if word.isascii() and len(word) > 2][:3]
        
        return {
            "understood_query": query,
            "search_keywords": list(set(all_keywords))[:5],  # Remove duplicates and limit
            "hindi_keywords": list(set(hindi_keywords))[:3],
            "english_keywords": list(set(english_keywords))[:3],
            "category": primary_category,
            "intent": f"User is asking about {', '.join(matched_concepts) if matched_concepts else 'general spiritual topic'}",
            "language_detected": detected_lang,
            "spiritual_concepts": matched_concepts
        }
    
    async def extract_qa_from_transcript(self, transcript_segments: List[Dict], video_title: str) -> List[Dict[str, Any]]:
        """Extract question-answer pairs from transcript segments"""
        try:
            # Combine segments into meaningful chunks
            chunks = self._create_meaningful_chunks(transcript_segments)
            
            qa_pairs = []
            
            for chunk in chunks:
                try:
                    # Use Gemini API directly for more reliable processing
                    qa_data = await self._extract_qa_with_gemini_direct(chunk, video_title)
                    
                    if qa_data:
                        for qa in qa_data:
                            qa['start_time'] = chunk['start_time']
                            qa['end_time'] = chunk['end_time']
                            qa_pairs.append(qa)
                    
                    # Add delay to avoid rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk['start_time']}: {str(e)}")
                    continue
            
            logger.info(f"Extracted {len(qa_pairs)} Q&A pairs from transcript")
            return qa_pairs
            
        except Exception as e:
            logger.error(f"Error in extract_qa_from_transcript: {str(e)}")
            return []
    
    async def _extract_qa_with_gemini_direct(self, chunk: Dict, video_title: str) -> List[Dict[str, Any]]:
        """Extract Q&A using direct Gemini API call"""
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""You are a spiritual content analyzer. Extract meaningful question-answer pairs from this Hindi/Sanskrit spiritual discourse.

Video Title: {video_title}
Transcript ({chunk['start_time']:.1f}s - {chunk['end_time']:.1f}s):
{chunk['text']}

Rules:
1. Extract clear questions (spoken or implied) and their complete answers
2. Focus on spiritual guidance, philosophy, and practical wisdom
3. Keep answers comprehensive but concise
4. Return as valid JSON only
5. Include confidence score (0.0-1.0)

Return format (JSON only):
[
  {{
    "question": "What is the spiritual question being addressed?",
    "answer": "Complete answer from the discourse",
    "confidence_score": 0.85,
    "language": "hi",
    "tags": ["spirituality", "guidance"]
  }}
]"""

            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Try to parse JSON from response
            try:
                # Clean up response text
                if response_text.startswith('```json'):
                    response_text = response_text.replace('```json', '').replace('```', '').strip()
                elif response_text.startswith('```'):
                    response_text = response_text.replace('```', '').strip()
                
                qa_data = json.loads(response_text)
                
                # Validate structure
                if isinstance(qa_data, list):
                    valid_qa = []
                    for qa in qa_data:
                        if isinstance(qa, dict) and 'question' in qa and 'answer' in qa:
                            # Ensure required fields
                            qa.setdefault('confidence_score', 0.8)
                            qa.setdefault('language', 'hi')
                            qa.setdefault('tags', ['spirituality'])
                            valid_qa.append(qa)
                    return valid_qa
                    
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                logger.error(f"Response text: {response_text}")
                
                # Fallback: try to extract manually
                return self._extract_qa_fallback(chunk, response_text)
                
        except Exception as e:
            logger.error(f"Error with Gemini direct API: {str(e)}")
            return []
        
        return []
    
    def _extract_qa_fallback(self, chunk: Dict, response_text: str) -> List[Dict[str, Any]]:
        """Fallback Q&A extraction when JSON parsing fails"""
        try:
            # Simple pattern matching for Q&A
            qa_pairs = []
            
            # Look for question patterns
            import re
            
            # Common question patterns in Hindi/English
            question_patterns = [
                r'प्रश्न[:\s]*(.+?)(?=उत्तर|Answer|\n|$)',
                r'Question[:\s]*(.+?)(?=Answer|उत्तर|\n|$)',
                r'(.+?\?)(.+?)(?=\n|$)',
            ]
            
            for pattern in question_patterns:
                matches = re.findall(pattern, response_text, re.IGNORECASE | re.DOTALL)
                for match in matches[:2]:  # Limit to 2 QA pairs per chunk
                    if isinstance(match, tuple) and len(match) >= 2:
                        question = match[0].strip()
                        answer = match[1].strip()
                    else:
                        question = f"What is discussed in this segment?"
                        answer = str(match).strip()
                    
                    if len(question) > 10 and len(answer) > 20:
                        qa_pairs.append({
                            'question': question,
                            'answer': answer,
                            'confidence_score': 0.6,  # Lower confidence for fallback
                            'language': 'hi',
                            'tags': ['spirituality']
                        })
            
            # If no patterns matched, create a general Q&A
            if not qa_pairs and len(chunk['text']) > 100:
                qa_pairs.append({
                    'question': 'इस विषय पर क्या चर्चा की गई है?',
                    'answer': chunk['text'][:500] + '...' if len(chunk['text']) > 500 else chunk['text'],
                    'confidence_score': 0.5,
                    'language': 'hi',
                    'tags': ['general', 'spirituality']
                })
            
            return qa_pairs
            
        except Exception as e:
            logger.error(f"Error in fallback extraction: {str(e)}")
            return []
            
        except Exception as e:
            logger.error(f"Error in Q&A extraction: {str(e)}")
            return []
    
    async def find_relevant_answers(self, user_query: str, qa_database: List[Dict], limit: int = 3) -> List[Dict]:
        """Find relevant answers using enhanced search with Mistral understanding"""
        try:
            # First, understand the user query using Mistral
            query_analysis = await self.understand_user_query(user_query)
            
            # Create search context with understood query
            search_query = query_analysis.get('understood_query', user_query)
            search_keywords = query_analysis.get('search_keywords', [user_query])
            hindi_keywords = query_analysis.get('hindi_keywords', [])
            english_keywords = query_analysis.get('english_keywords', [])
            category = query_analysis.get('category', 'general')
            
            logger.info(f"Original query: {user_query}")
            logger.info(f"Understood query: {search_query}")
            logger.info(f"Search keywords: {search_keywords}")
            logger.info(f"Hindi keywords: {hindi_keywords}")
            logger.info(f"English keywords: {english_keywords}")
            logger.info(f"Category: {category}")
            
            # Enhanced keyword matching with spiritual concepts
            spiritual_concept_map = {
                'bhakti': ['भक्ति', 'devotion', 'surrender', 'प्रेम', 'love', 'समर्पण'],
                'meditation': ['ध्यान', 'dhyan', 'meditate', 'concentration', 'focus', 'एकाग्रता'],
                'life': ['जीवन', 'purpose', 'meaning', 'उद्देश्य', 'अर्थ'],
                'guru': ['गुरु', 'teacher', 'guide', 'मार्गदर्शक', 'आचार्य'],
                'karma': ['कर्म', 'action', 'deed', 'work', 'फल'],
                'peace': ['शांति', 'शान्ति', 'mental peace', 'calm', 'tranquil', 'मानसिक'],
                'moksha': ['मोक्ष', 'liberation', 'salvation', 'मुक्ति', 'निर्वाण'],
                'love': ['प्रेम', 'प्यार', 'love', 'affection', 'स्नेह'],
                'soul': ['आत्मा', 'soul', 'spirit', 'self', 'स्वरूप'],
                'god': ['भगवान', 'परमात्मा', 'god', 'divine', 'ईश्वर']
            }
            
            # Enhanced semantic search
            scored_answers = []
            
            for qa in qa_database:
                score = 0
                qa_text = f"{qa.get('question', '')} {qa.get('answer', '')} {' '.join(qa.get('tags', []))}".lower()
                qa_question = qa.get('question', '').lower()
                qa_answer = qa.get('answer', '').lower()
                qa_tags = [tag.lower() for tag in qa.get('tags', [])]
                
                # 1. Direct keyword matching (highest priority)
                all_search_terms = search_keywords + hindi_keywords + english_keywords
                for keyword in all_search_terms:
                    keyword_lower = keyword.lower()
                    if keyword_lower in qa_question:
                        score += 10  # Question match is highest priority
                    elif keyword_lower in qa_answer:
                        score += 5   # Answer match is medium priority
                    elif keyword_lower in ' '.join(qa_tags):
                        score += 3   # Tag match is lower priority
                
                # 2. Spiritual concept matching
                user_query_lower = user_query.lower()
                for concept, related_terms in spiritual_concept_map.items():
                    user_has_concept = any(term.lower() in user_query_lower for term in related_terms)
                    qa_has_concept = any(term.lower() in qa_text for term in related_terms)
                    
                    if user_has_concept and qa_has_concept:
                        score += 8  # High relevance for spiritual concept match
                
                # 3. Category-based matching
                if category in qa_tags or category.replace('-', '') in qa_text:
                    score += 4
                
                # 4. Language preference (slight boost for same language)
                detected_lang = query_analysis.get('language_detected', 'hi')
                qa_lang = qa.get('language', 'hi')
                if detected_lang == qa_lang:
                    score += 1
                
                # 5. Special handling for common spiritual questions
                special_patterns = {
                    'bhakti': ['भक्ति', 'devotion', 'bhakti'],
                    'meditation': ['ध्यान', 'meditat', 'dhyan'],
                    'meaning': ['अर्थ', 'meaning', 'purpose', 'उद्देश्य'],
                    'peace': ['शांति', 'peace', 'शान्ति', 'calm'],
                    'guru': ['गुरु', 'guru', 'teacher'],
                    'life': ['जीवन', 'life', 'zindagi'],
                    'karma': ['कर्म', 'karma', 'action'],
                    'moksha': ['मोक्ष', 'moksha', 'liberation', 'मुक्ति']
                }
                
                for pattern_key, pattern_terms in special_patterns.items():
                    user_matches = any(term.lower() in user_query_lower for term in pattern_terms)
                    qa_matches = any(term.lower() in qa_text for term in pattern_terms)
                    
                    if user_matches and qa_matches:
                        score += 6  # Boost for specific spiritual pattern match
                
                # Only include results with meaningful scores
                if score > 0:
                    qa_copy = qa.copy()
                    qa_copy['similarity_score'] = min(score / 15.0, 1.0)  # Normalize to 0-1
                    qa_copy['match_reason'] = f"Spiritual concept match (score: {score})"
                    qa_copy['debug_score'] = score
                    scored_answers.append(qa_copy)
            
            # Sort by score and return top results
            scored_answers.sort(key=lambda x: x['debug_score'], reverse=True)
            
            logger.info(f"Found {len(scored_answers)} potential matches")
            for i, answer in enumerate(scored_answers[:limit]):
                logger.info(f"Match {i+1}: Score={answer['debug_score']}, Question='{answer['question'][:50]}...'")
            
            # If no good matches found, try fallback search
            if not scored_answers:
                logger.warning("No semantic matches found, trying keyword fallback")
                return self._keyword_fallback_search([user_query] + search_keywords, qa_database, limit)
            
            return scored_answers[:limit]
            
        except Exception as e:
            logger.error(f"Error finding relevant answers: {str(e)}")
            # Fallback to simple search
            return self._keyword_fallback_search([user_query], qa_database, limit)
    
    def _keyword_fallback_search(self, keywords: List[str], qa_database: List[Dict], limit: int) -> List[Dict]:
        """Fallback search using simple keyword matching"""
        scored_answers = []
        
        for qa in qa_database:
            score = 0
            qa_text = f"{qa.get('question', '')} {qa.get('answer', '')} {' '.join(qa.get('tags', []))}".lower()
            
            for keyword in keywords:
                if keyword.lower() in qa_text:
                    score += 1
            
            if score > 0:
                qa_copy = qa.copy()
                qa_copy['similarity_score'] = min(score / len(keywords), 1.0)
                qa_copy['match_reason'] = f"Keyword match: {score}/{len(keywords)}"
                scored_answers.append(qa_copy)
        
        # Sort by score and return top results
        scored_answers.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_answers[:limit]
    
    def _create_meaningful_chunks(self, segments: List[Dict], max_chunk_duration: float = 180) -> List[Dict]:
        """Create meaningful chunks from transcript segments"""
        chunks = []
        current_chunk = {
            'start_time': 0,
            'end_time': 0,
            'text': ''
        }
        
        for segment in segments:
            # If adding this segment would exceed max duration, finalize current chunk
            if (segment['end_time'] - current_chunk['start_time']) > max_chunk_duration and current_chunk['text']:
                chunks.append(current_chunk.copy())
                current_chunk = {
                    'start_time': segment['start_time'],
                    'end_time': segment['end_time'],
                    'text': segment['text']
                }
            else:
                if not current_chunk['text']:
                    current_chunk['start_time'] = segment['start_time']
                
                current_chunk['end_time'] = segment['end_time']
                current_chunk['text'] += ' ' + segment['text']
        
        # Add the last chunk
        if current_chunk['text']:
            chunks.append(current_chunk)
        
        return chunks
    
    def _parse_llm_response(self, response: str) -> Optional[Dict]:
        """Parse JSON response from LLM"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            
            # If no JSON brackets found, try parsing the whole response
            return json.loads(response)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {str(e)}")
            logger.debug(f"Response was: {response}")
            return None
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return None