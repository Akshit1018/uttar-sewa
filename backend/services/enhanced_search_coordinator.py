"""
Enhanced Search Coordinator
Combines multiple search strategies for maximum accuracy and relevance
"""

import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
import time

from .ultra_search_engine import ultra_search_engine
from .intelligent_search_service import intelligent_search
from .llm_service import LLMService
from .video_timestamp_service import video_timestamp_service

logger = logging.getLogger(__name__)

class EnhancedSearchCoordinator:
    def __init__(self):
        self.llm_service = LLMService()
        self.search_strategies = ['ultra', 'intelligent', 'llm', 'hybrid']
        self.performance_metrics = {
            'total_searches': 0,
            'successful_searches': 0,
            'average_response_time': 0.0,
            'strategy_performance': {}
        }
    
    async def search(self, user_query: str, qa_database: List[Dict], limit: int = 5, strategy: str = 'hybrid') -> List[Dict[str, Any]]:
        """
        Coordinate search across multiple strategies for maximum accuracy
        """
        start_time = time.time()
        self.performance_metrics['total_searches'] += 1
        
        try:
            logger.info(f"Starting enhanced search for query: '{user_query}' using strategy: {strategy}")
            
            if not qa_database:
                logger.warning("Empty Q&A database provided")
                return []
            
            # Strategy selection and execution
            if strategy == 'ultra':
                results = await self._ultra_strategy(user_query, qa_database, limit)
            elif strategy == 'intelligent':
                results = await self._intelligent_strategy(user_query, qa_database, limit)
            elif strategy == 'llm':
                results = await self._llm_strategy(user_query, qa_database, limit)
            elif strategy == 'hybrid':
                results = await self._hybrid_strategy(user_query, qa_database, limit)
            else:
                logger.warning(f"Unknown strategy '{strategy}', falling back to hybrid")
                results = await self._hybrid_strategy(user_query, qa_database, limit)
            
            # Enhance results with video metadata
            enhanced_results = await self._enhance_results_with_metadata(results)
            
            # Calculate performance metrics
            response_time = time.time() - start_time
            self._update_performance_metrics(strategy, response_time, len(enhanced_results))
            
            logger.info(f"Enhanced search completed: {len(enhanced_results)} results in {response_time:.3f}s")
            return enhanced_results[:limit]
            
        except Exception as e:
            logger.error(f"Error in enhanced search: {str(e)}")
            return []
    
    async def _ultra_strategy(self, user_query: str, qa_database: List[Dict], limit: int) -> List[Dict[str, Any]]:
        """Ultra-robust search strategy"""
        try:
            results = await ultra_search_engine.ultra_search(user_query, qa_database)
            
            # Add strategy metadata
            for result in results:
                result['search_strategy'] = 'ultra'
                result['strategy_confidence'] = result.get('ultra_relevance_score', 0.8)
            
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error in ultra strategy: {str(e)}")
            return []
    
    async def _intelligent_strategy(self, user_query: str, qa_database: List[Dict], limit: int) -> List[Dict[str, Any]]:
        """Intelligent semantic search strategy"""
        try:
            # Understand query intent
            intent_analysis = intelligent_search.understand_question_intent(user_query)
            
            # Find relevant answers
            results = await intelligent_search.find_relevant_answers(intent_analysis, qa_database)
            
            # Enhance search results
            enhanced_results = intelligent_search.enhance_search_results(results, intent_analysis)
            
            # Add strategy metadata
            for result in enhanced_results:
                result['search_strategy'] = 'intelligent'
                result['strategy_confidence'] = result.get('relevance_score', 0.7)
                result['intent_analysis'] = intent_analysis
            
            return enhanced_results[:limit]
            
        except Exception as e:
            logger.error(f"Error in intelligent strategy: {str(e)}")
            return []
    
    async def _llm_strategy(self, user_query: str, qa_database: List[Dict], limit: int) -> List[Dict[str, Any]]:
        """LLM-powered search strategy"""
        try:
            results = await self.llm_service.find_relevant_answers(user_query, qa_database, limit)
            
            # Add strategy metadata
            for result in results:
                result['search_strategy'] = 'llm'
                result['strategy_confidence'] = result.get('similarity_score', 0.6)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in LLM strategy: {str(e)}")
            return []
    
    async def _hybrid_strategy(self, user_query: str, qa_database: List[Dict], limit: int) -> List[Dict[str, Any]]:
        """
        Hybrid strategy that combines multiple approaches for maximum accuracy
        """
        try:
            logger.info("Executing hybrid search strategy")
            
            # Run multiple strategies in parallel
            ultra_task = asyncio.create_task(self._ultra_strategy(user_query, qa_database, limit * 2))
            intelligent_task = asyncio.create_task(self._intelligent_strategy(user_query, qa_database, limit * 2))
            llm_task = asyncio.create_task(self._llm_strategy(user_query, qa_database, limit * 2))
            
            # Wait for all strategies to complete
            ultra_results, intelligent_results, llm_results = await asyncio.gather(
                ultra_task, intelligent_task, llm_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(ultra_results, Exception):
                logger.error(f"Ultra strategy failed: {ultra_results}")
                ultra_results = []
            
            if isinstance(intelligent_results, Exception):
                logger.error(f"Intelligent strategy failed: {intelligent_results}")
                intelligent_results = []
            
            if isinstance(llm_results, Exception):
                logger.error(f"LLM strategy failed: {llm_results}")
                llm_results = []
            
            # Combine and rank results
            all_results = self._combine_and_rank_results(
                ultra_results, intelligent_results, llm_results, user_query
            )
            
            logger.info(f"Hybrid strategy combined {len(ultra_results)} + {len(intelligent_results)} + {len(llm_results)} = {len(all_results)} results")
            
            return all_results[:limit]
            
        except Exception as e:
            logger.error(f"Error in hybrid strategy: {str(e)}")
            # Fallback to single strategy
            return await self._ultra_strategy(user_query, qa_database, limit)
    
    def _combine_and_rank_results(self, ultra_results: List[Dict], intelligent_results: List[Dict], 
                                  llm_results: List[Dict], user_query: str) -> List[Dict[str, Any]]:
        """
        Combine results from multiple strategies and create a unified ranking
        """
        try:
            # Create a result map to avoid duplicates
            result_map = {}
            
            # Weight strategies based on their reliability
            strategy_weights = {
                'ultra': 0.4,      # 40% - Most sophisticated
                'intelligent': 0.35,  # 35% - Good semantic understanding  
                'llm': 0.25        # 25% - Good for context but can be inconsistent
            }
            
            # Process ultra results
            for result in ultra_results:
                key = self._create_result_key(result)
                if key not in result_map:
                    result_map[key] = result.copy()
                    result_map[key]['combined_score'] = result.get('strategy_confidence', 0.8) * strategy_weights['ultra']
                    result_map[key]['strategy_votes'] = ['ultra']
                    result_map[key]['strategy_scores'] = {'ultra': result.get('strategy_confidence', 0.8)}
                else:
                    # Boost score for multiple strategy agreement
                    existing_score = result_map[key]['combined_score']
                    ultra_score = result.get('strategy_confidence', 0.8) * strategy_weights['ultra']
                    result_map[key]['combined_score'] = max(existing_score, ultra_score) + 0.1  # Consensus bonus
                    result_map[key]['strategy_votes'].append('ultra')
                    result_map[key]['strategy_scores']['ultra'] = result.get('strategy_confidence', 0.8)
            
            # Process intelligent results
            for result in intelligent_results:
                key = self._create_result_key(result)
                if key not in result_map:
                    result_map[key] = result.copy()
                    result_map[key]['combined_score'] = result.get('strategy_confidence', 0.7) * strategy_weights['intelligent']
                    result_map[key]['strategy_votes'] = ['intelligent']
                    result_map[key]['strategy_scores'] = {'intelligent': result.get('strategy_confidence', 0.7)}
                else:
                    existing_score = result_map[key]['combined_score']
                    intelligent_score = result.get('strategy_confidence', 0.7) * strategy_weights['intelligent']
                    result_map[key]['combined_score'] = max(existing_score, intelligent_score) + 0.1
                    result_map[key]['strategy_votes'].append('intelligent')
                    result_map[key]['strategy_scores']['intelligent'] = result.get('strategy_confidence', 0.7)
            
            # Process LLM results
            for result in llm_results:
                key = self._create_result_key(result)
                if key not in result_map:
                    result_map[key] = result.copy()
                    result_map[key]['combined_score'] = result.get('strategy_confidence', 0.6) * strategy_weights['llm']
                    result_map[key]['strategy_votes'] = ['llm']
                    result_map[key]['strategy_scores'] = {'llm': result.get('strategy_confidence', 0.6)}
                else:
                    existing_score = result_map[key]['combined_score']
                    llm_score = result.get('strategy_confidence', 0.6) * strategy_weights['llm']
                    result_map[key]['combined_score'] = max(existing_score, llm_score) + 0.1
                    result_map[key]['strategy_votes'].append('llm')
                    result_map[key]['strategy_scores']['llm'] = result.get('strategy_confidence', 0.6)
            
            # Convert to list and sort by combined score
            combined_results = list(result_map.values())
            combined_results.sort(key=lambda x: x['combined_score'], reverse=True)
            
            # Add final metadata
            for i, result in enumerate(combined_results):
                result['final_rank'] = i + 1
                result['search_strategy'] = 'hybrid'
                result['consensus_level'] = len(result['strategy_votes'])
                result['confidence_explanation'] = self._create_confidence_explanation(result)
            
            return combined_results
            
        except Exception as e:
            logger.error(f"Error combining results: {str(e)}")
            # Return best available results
            return ultra_results or intelligent_results or llm_results or []
    
    def _create_result_key(self, result: Dict) -> str:
        """Create a unique key for deduplication"""
        return f"{result.get('video_id', 'unknown')}_{result.get('start_time', 0)}"
    
    def _create_confidence_explanation(self, result: Dict) -> str:
        """Create human-readable confidence explanation"""
        votes = result.get('strategy_votes', [])
        scores = result.get('strategy_scores', {})
        
        explanations = []
        
        if 'ultra' in votes:
            explanations.append(f"Ultra algorithm: {scores.get('ultra', 0):.2f}")
        
        if 'intelligent' in votes:
            explanations.append(f"Semantic analysis: {scores.get('intelligent', 0):.2f}")
        
        if 'llm' in votes:
            explanations.append(f"LLM matching: {scores.get('llm', 0):.2f}")
        
        consensus_bonus = " (Multiple algorithm consensus)" if len(votes) > 1 else ""
        
        return " | ".join(explanations) + consensus_bonus
    
    async def _enhance_results_with_metadata(self, results: List[Dict]) -> List[Dict[str, Any]]:
        """Enhance results with video timestamp metadata"""
        enhanced_results = []
        
        for result in results:
            try:
                # Add video timestamp metadata
                video_metadata = video_timestamp_service.create_video_metadata(result)
                
                # Merge with existing result
                enhanced_result = {**result, **video_metadata}
                
                # Ensure required fields
                enhanced_result.setdefault('confidence_score', result.get('combined_score', result.get('strategy_confidence', 0.8)))
                enhanced_result.setdefault('youtube_url', f"https://www.youtube.com/watch?v={result.get('video_id', '')}" if result.get('video_id') else "")
                enhanced_result.setdefault('timestamp_url', f"https://www.youtube.com/watch?v={result.get('video_id', '')}&t={int(result.get('start_time', 0))}" if result.get('video_id') else "")
                
                enhanced_results.append(enhanced_result)
                
            except Exception as e:
                logger.error(f"Error enhancing result metadata: {str(e)}")
                # Add basic metadata
                result.setdefault('confidence_score', 0.7)
                result.setdefault('youtube_url', f"https://www.youtube.com/watch?v={result.get('video_id', '')}" if result.get('video_id') else "")
                result.setdefault('timestamp_url', f"https://www.youtube.com/watch?v={result.get('video_id', '')}&t={int(result.get('start_time', 0))}" if result.get('video_id') else "")
                enhanced_results.append(result)
        
        return enhanced_results
    
    def _update_performance_metrics(self, strategy: str, response_time: float, result_count: int):
        """Update performance tracking metrics"""
        try:
            if result_count > 0:
                self.performance_metrics['successful_searches'] += 1
            
            # Update average response time
            total_time = self.performance_metrics['average_response_time'] * (self.performance_metrics['total_searches'] - 1)
            self.performance_metrics['average_response_time'] = (total_time + response_time) / self.performance_metrics['total_searches']
            
            # Update strategy performance
            if strategy not in self.performance_metrics['strategy_performance']:
                self.performance_metrics['strategy_performance'][strategy] = {
                    'uses': 0,
                    'success_rate': 0.0,
                    'average_results': 0.0,
                    'average_time': 0.0
                }
            
            strategy_stats = self.performance_metrics['strategy_performance'][strategy]
            strategy_stats['uses'] += 1
            
            # Update success rate
            if result_count > 0:
                strategy_stats['success_rate'] = ((strategy_stats['success_rate'] * (strategy_stats['uses'] - 1)) + 1) / strategy_stats['uses']
            else:
                strategy_stats['success_rate'] = (strategy_stats['success_rate'] * (strategy_stats['uses'] - 1)) / strategy_stats['uses']
            
            # Update average results
            strategy_stats['average_results'] = ((strategy_stats['average_results'] * (strategy_stats['uses'] - 1)) + result_count) / strategy_stats['uses']
            
            # Update average time
            strategy_stats['average_time'] = ((strategy_stats['average_time'] * (strategy_stats['uses'] - 1)) + response_time) / strategy_stats['uses']
            
        except Exception as e:
            logger.error(f"Error updating performance metrics: {str(e)}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get detailed performance report"""
        return {
            'overview': {
                'total_searches': self.performance_metrics['total_searches'],
                'successful_searches': self.performance_metrics['successful_searches'],
                'success_rate': self.performance_metrics['successful_searches'] / max(1, self.performance_metrics['total_searches']),
                'average_response_time': round(self.performance_metrics['average_response_time'], 3)
            },
            'strategy_performance': self.performance_metrics['strategy_performance'],
            'recommendations': self._generate_performance_recommendations()
        }
    
    def _generate_performance_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        try:
            strategy_stats = self.performance_metrics['strategy_performance']
            
            if not strategy_stats:
                return ["No data available yet"]
            
            # Find best performing strategy
            best_strategy = max(strategy_stats.keys(), key=lambda s: strategy_stats[s]['success_rate'])
            best_success_rate = strategy_stats[best_strategy]['success_rate']
            
            recommendations.append(f"Best performing strategy: {best_strategy} ({best_success_rate:.1%} success rate)")
            
            # Check if hybrid is being used effectively
            if 'hybrid' in strategy_stats:
                hybrid_stats = strategy_stats['hybrid']
                if hybrid_stats['success_rate'] > 0.8:
                    recommendations.append("Hybrid strategy is performing well - continue using as default")
                elif hybrid_stats['success_rate'] < 0.5:
                    recommendations.append("Consider optimizing hybrid strategy or switch to best single strategy")
            
            # Check response times
            avg_time = self.performance_metrics['average_response_time']
            if avg_time > 2.0:
                recommendations.append("Response times are high - consider caching or algorithm optimization")
            elif avg_time < 0.5:
                recommendations.append("Response times are excellent")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            recommendations.append("Error generating recommendations")
        
        return recommendations

# Global instance
enhanced_search_coordinator = EnhancedSearchCoordinator()