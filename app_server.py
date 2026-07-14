#!/usr/bin/env python3
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, '/app')

from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta
import uuid

# Import models and services
from backend.models import (
    VideoModel, TranscriptSegment, QuestionAnswer, 
    SearchQuery, SearchResult, ProcessingStatus
)
from backend.services.processing_service import ProcessingService
from backend.services.llm_service import LLMService
from backend.services.youtube_service import YouTubeService

ROOT_DIR = Path('/app/backend')
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Spiritual Q&A API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize services
processing_service = ProcessingService(db)
llm_service = LLMService()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@api_router.get("/")
async def root():
    return {
        "message": "Spiritual Q&A API",
        "status": "running",
        "description": "API for searching spiritual questions and answers from video transcripts"
    }

@api_router.post("/process/start")
async def start_processing(request: dict = None):
    """Start processing videos from the YouTube channel"""
    try:
        channel_url = None
        if request and 'channel_url' in request:
            channel_url = request['channel_url']
            logger.info(f"Starting custom channel processing for: {channel_url}")
        
        status_id = await processing_service.start_channel_processing(channel_url)
        return {
            "message": "Processing started",
            "status_id": status_id,
            "note": "This will process videos from the channel. Check status using /process/status/{status_id}",
            "channel_url": channel_url if channel_url else "default"
        }
    except Exception as e:
        logger.error(f"Error starting processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/process/status/{status_id}")
async def get_processing_status(status_id: str):
    """Get processing status"""
    try:
        status = await processing_service.get_processing_status(status_id)
        return status
    except Exception as e:
        logger.error(f"Error getting processing status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/search", response_model=List[SearchResult])
async def search_questions(query: SearchQuery):
    """Intelligent search for relevant questions and answers"""
    try:
        from backend.services.intelligent_search_service import intelligent_search
        from backend.services.video_timestamp_service import video_timestamp_service
        
        # Step 1: Understand the user's question intent
        intent_analysis = intelligent_search.understand_question_intent(query.query)
        logger.info(f"Question intent: {intent_analysis}")
        
        # Step 2: Get all Q&A pairs from database
        qa_docs = await db.question_answers.find().to_list(1000)
        
        if not qa_docs:
            logger.warning("No Q&A pairs found in database")
            return []
        
        # Step 3: Find relevant answers using intelligent matching
        relevant_answers = await intelligent_search.find_relevant_answers(intent_analysis, qa_docs)
        
        if not relevant_answers:
            logger.info(f"No relevant answers found for query: {query.query}")
            return []
        
        # Step 4: Enhance results with video metadata and formatting
        enhanced_results = intelligent_search.enhance_search_results(relevant_answers, intent_analysis)
        
        # Step 5: Add proper video timestamp URLs
        final_results = []
        for result in enhanced_results[:query.limit]:
            # Add video timestamp metadata
            video_metadata = video_timestamp_service.create_video_metadata(result)
            
            # Create the final search result
            search_result = SearchResult(
                question=result["question"],
                answer=result.get("formatted_answer", result["answer"]),
                video_id=result["video_id"],
                video_title=result["video_title"],
                start_time=result["start_time"],
                end_time=result.get("end_time", result["start_time"] + 60),
                confidence_score=result["relevance_score"],  # Use our calculated relevance
                youtube_url=video_metadata["urls"]["basic_url"],
                timestamp_url=video_metadata["urls"]["web_url"]
            )
            final_results.append(search_result)
        
        logger.info(f"Found {len(final_results)} relevant answers for query: '{query.query}'")
        return final_results
        
    except Exception as e:
        logger.error(f"Error in intelligent search: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@api_router.post("/search/explain")
async def explain_search_results(query: SearchQuery):
    """Get detailed explanation of how search results were found"""
    try:
        from backend.services.intelligent_search_service import intelligent_search
        
        # Analyze the query
        intent_analysis = intelligent_search.understand_question_intent(query.query)
        
        # Get Q&A pairs
        qa_docs = await db.question_answers.find().to_list(100)
        
        # Find relevant answers with scoring details
        relevant_answers = await intelligent_search.find_relevant_answers(intent_analysis, qa_docs)
        
        explanation = {
            "query_analysis": intent_analysis,
            "total_database_items": len(qa_docs),
            "relevant_results_found": len(relevant_answers),
            "top_results_with_scores": [
                {
                    "question": ans["question"][:100] + "..." if len(ans["question"]) > 100 else ans["question"],
                    "relevance_score": ans["relevance_score"],
                    "match_explanation": ans["match_explanation"],
                    "video_id": ans["video_id"]
                }
                for ans in relevant_answers[:3]
            ],
            "search_strategy": {
                "keyword_matching": "40% weight - direct term matches in questions/answers",
                "concept_matching": "30% weight - spiritual concept understanding",
                "question_type": "15% weight - how/what/why pattern matching",
                "tag_matching": "10% weight - topic tag relevance",
                "language_preference": "5% weight - language compatibility"
            }
        }
        
        return explanation
        
    except Exception as e:
        logger.error(f"Error explaining search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        video_count = await db.videos.count_documents({})
        processed_videos = await db.videos.count_documents({"transcript_processed": True})
        qa_count = await db.question_answers.count_documents({})
        transcript_segments = await db.transcript_segments.count_documents({})
        
        return {
            "total_videos": video_count,
            "processed_videos": processed_videos,
            "total_qa_pairs": qa_count,
            "total_transcript_segments": transcript_segments,
            "processing_progress": f"{processed_videos}/{video_count}" if video_count > 0 else "0/0"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/videos", response_model=List[VideoModel])
async def get_videos(limit: int = 20, skip: int = 0):
    """Get list of videos"""
    try:
        videos = await db.videos.find().skip(skip).limit(limit).to_list(limit)
        return [VideoModel(**video) for video in videos]
    except Exception as e:
        logger.error(f"Error getting videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/questions/suggested")
async def get_suggested_questions():
    """Get suggested questions based on real Q&A data"""
    try:
        # Get real questions from processed videos
        real_qa = await db.question_answers.aggregate([
            {"$sample": {"size": 8}},
            {"$project": {"question": 1, "tags": 1, "language": 1}}
        ]).to_list(8)
        
        suggestions = []
        
        # Add real questions from database
        for qa in real_qa:
            if qa.get('question'):
                suggestions.append(qa['question'])
        
        # If we don't have enough real questions, add some default spiritual ones
        if len(suggestions) < 5:
            default_suggestions = [
                "जीवन का उद्देश्य क्या है?",
                "ध्यान कैसे करें?",
                "मानसिक शांति कैसे पाएं?",
                "आध्यात्मिक जीवन कैसे जिएं?",
                "गुरु की आवश्यकता क्यों है?"
            ]
            suggestions.extend(default_suggestions[:10-len(suggestions)])
        
        return {
            "suggested_questions": suggestions[:10],
            "note": "वास्तविक वीडियो से प्राप्त प्रश्न" if suggestions else "अभी तक कोई प्रश्न उपलब्ध नहीं हैं",
            "real_questions_count": len([q for q in suggestions if any(qa.get('question') == q for qa in real_qa)])
        }
        
    except Exception as e:
        logger.error(f"Error getting suggested questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/system/status")
async def get_system_status():
    """Get comprehensive system status"""
    try:
        # Get database stats
        video_count = await db.videos.count_documents({})
        processed_videos = await db.videos.count_documents({"transcript_processed": True})
        qa_count = await db.question_answers.count_documents({})
        transcript_segments = await db.transcript_segments.count_documents({})
        
        # Get processing status
        active_processing = await db.processing_status.find_one(
            {"status": {"$in": ["pending", "processing"]}},
            sort=[("started_at", -1)]
        )
        
        # Check if we have real data
        sample_videos = await db.videos.count_documents({
            "video_id": {"$regex": "^(sample|bhakti_|meditation_|life_|guru_|karma_|peace_|love_|moksha_)"}
        })
        
        return {
            "database": {
                "total_videos": video_count,
                "processed_videos": processed_videos,
                "unprocessed_videos": video_count - processed_videos,
                "total_qa_pairs": qa_count,
                "total_transcript_segments": transcript_segments,
                "processing_progress": f"{processed_videos}/{video_count}",
                "real_data_only": sample_videos == 0
            },
            "processing": {
                "is_active": active_processing is not None,
                "current_status": active_processing["status"] if active_processing else None,
                "current_progress": f"{active_processing.get('processed_videos', 0)}/{active_processing.get('total_videos', 0)}" if active_processing else None
            },
            "api_optimization": {
                "youtube_api_calls_needed": video_count - processed_videos,
                "gemini_api_calls_needed": (video_count - processed_videos) * 3,  # Approximate
                "estimated_cost": "Based on usage"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/process/clear")
async def clear_processing_status():
    """Clear all processing status data"""
    try:
        # Clear processing status collection
        await db.processing_status.delete_many({})
        
        return {
            "message": "Processing status cleared successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error clearing processing status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary for admin dashboard"""
    try:
        # Get video and processing stats
        video_count = await db.videos.count_documents({})
        processed_videos = await db.videos.count_documents({"transcript_processed": True})
        qa_count = await db.question_answers.count_documents({})
        transcript_segments = await db.transcript_segments.count_documents({})
        
        # Get recent activity (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_qa = await db.question_answers.count_documents({
            "created_at": {"$gte": yesterday}
        })
        
        # Get language distribution
        language_pipeline = [
            {"$group": {"_id": "$language", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        language_stats = await db.question_answers.aggregate(language_pipeline).to_list(10)
        
        # Get top video contributors
        video_pipeline = [
            {"$group": {"_id": "$video_id", "qa_count": {"$sum": 1}}},
            {"$sort": {"qa_count": -1}},
            {"$limit": 10}
        ]
        top_videos = await db.question_answers.aggregate(video_pipeline).to_list(10)
        
        # Enhance with video titles
        for video in top_videos:
            video_doc = await db.videos.find_one({"video_id": video["_id"]})
            video["title"] = video_doc["title"] if video_doc else "Unknown Video"
        
        return {
            "overview": {
                "total_videos": video_count,
                "processed_videos": processed_videos,
                "total_qa_pairs": qa_count,
                "total_transcript_segments": transcript_segments,
                "processing_percentage": round((processed_videos / video_count * 100) if video_count > 0 else 0, 2)
            },
            "recent_activity": {
                "new_qa_pairs_24h": recent_qa,
                "last_updated": datetime.utcnow().isoformat()
            },
            "language_distribution": language_stats,
            "top_contributing_videos": top_videos,
            "system_health": {
                "database_status": "healthy",
                "last_processing": await get_last_processing_time(),
                "api_status": "operational"
            }
        }
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_last_processing_time():
    """Get the timestamp of last processing activity"""
    try:
        last_processing = await db.processing_status.find_one(
            {},
            sort=[("updated_at", -1)]
        )
        return last_processing["updated_at"].isoformat() if last_processing else None
    except:
        return None

@api_router.get("/search/suggestions")
async def get_search_suggestions(query: str = "", limit: int = 5):
    """Get contextual search suggestions based on query"""
    try:
        suggestions = []
        
        if query and len(query) > 2:
            # Search for similar questions in database
            similar_questions = await db.question_answers.find(
                {"question": {"$regex": query, "$options": "i"}},
                {"question": 1}
            ).limit(limit).to_list(limit)
            
            suggestions.extend([q["question"] for q in similar_questions])
        
        # Add popular/trending questions if we need more suggestions
        if len(suggestions) < limit:
            popular_questions = await db.question_answers.aggregate([
                {"$sample": {"size": limit - len(suggestions)}},
                {"$project": {"question": 1}}
            ]).to_list(limit - len(suggestions))
            
            suggestions.extend([q["question"] for q in popular_questions])
        
        return {
            "suggestions": suggestions[:limit],
            "query": query,
            "count": len(suggestions)
        }
    except Exception as e:
        logger.error(f"Error getting search suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/feedback")
async def submit_feedback(feedback_data: dict):
    """Submit user feedback"""
    try:
        feedback_entry = {
            "id": str(uuid.uuid4()),
            "type": feedback_data.get("type", "general"),
            "rating": feedback_data.get("rating"),
            "message": feedback_data.get("message", ""),
            "user_agent": feedback_data.get("user_agent", ""),
            "page": feedback_data.get("page", ""),
            "language": feedback_data.get("language", "en"),
            "timestamp": datetime.utcnow()
        }
        
        await db.feedback.insert_one(feedback_entry)
        
        return {
            "success": True,
            "feedback_id": feedback_entry["id"],
            "message": "Feedback submitted successfully"
        }
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/videos/popular")
async def get_popular_videos(limit: int = 10):
    """Get most popular videos based on Q&A count"""
    try:
        popular_pipeline = [
            {"$group": {
                "_id": "$video_id",
                "qa_count": {"$sum": 1},
                "avg_confidence": {"$avg": "$confidence_score"}
            }},
            {"$sort": {"qa_count": -1}},
            {"$limit": limit}
        ]
        
        popular_video_stats = await db.question_answers.aggregate(popular_pipeline).to_list(limit)
        
        # Enhance with video details
        result = []
        for stat in popular_video_stats:
            video = await db.videos.find_one({"video_id": stat["_id"]})
            if video:
                result.append({
                    "video_id": stat["_id"],
                    "title": video["title"],
                    "description": video.get("description", "")[:200] + "...",
                    "duration": video.get("duration", ""),
                    "upload_date": video.get("upload_date"),
                    "view_count": video.get("view_count", 0),
                    "qa_count": stat["qa_count"],
                    "avg_confidence": round(stat["avg_confidence"], 2),
                    "youtube_url": f"https://www.youtube.com/watch?v={stat['_id']}"
                })
        
        return {
            "popular_videos": result,
            "total_count": len(result)
        }
    except Exception as e:
        logger.error(f"Error getting popular videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/cloud/backup")
async def backup_to_cloud():
    """Backup local data to Google Cloud Firestore"""
    try:
        # Import conditionally to handle missing module gracefully
        try:
            from backend.services.cloud_database_service import cloud_db
        except ImportError:
            return {
                "success": False,
                "error": "Cloud database module not found. Please install google-cloud-firestore package.",
                "setup_url": "https://console.cloud.google.com/firestore"
            }
        
        if not hasattr(cloud_db, 'enabled') or not cloud_db.enabled:
            return {
                "success": False,
                "error": "Cloud database not configured. Please setup Google Cloud Firestore.",
                "setup_url": "https://console.cloud.google.com/firestore"
            }
        
        # Perform backup
        result = await cloud_db.backup_local_to_cloud(db)
        
        return {
            "success": result.get('success', False),
            "backup_stats": result,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Backup completed successfully" if result.get('success') else "Backup failed"
        }
        
    except Exception as e:
        logger.error(f"Error during cloud backup: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/cloud/restore")
async def restore_from_cloud():
    """Restore data from Google Cloud Firestore"""
    try:
        # Import conditionally to handle missing module gracefully
        try:
            from backend.services.cloud_database_service import cloud_db
        except ImportError:
            return {
                "success": False,
                "error": "Cloud database module not found. Please install google-cloud-firestore package.",
                "setup_url": "https://console.cloud.google.com/firestore"
            }
        
        if not hasattr(cloud_db, 'enabled') or not cloud_db.enabled:
            return {
                "success": False,
                "error": "Cloud database not configured. Please setup Google Cloud Firestore.",
                "setup_url": "https://console.cloud.google.com/firestore"
            }
        
        # Perform restore
        result = await cloud_db.restore_from_cloud(db)
        
        return {
            "success": result.get('success', False),
            "restore_stats": result,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Restore completed successfully" if result.get('success') else "Restore failed"
        }
        
    except Exception as e:
        logger.error(f"Error during cloud restore: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/cloud/status")
async def get_cloud_status():
    """Get cloud database connection status and statistics"""
    try:
        # Import conditionally to handle missing module gracefully
        try:
            from backend.services.cloud_database_service import cloud_db
        except ImportError:
            return {
                "enabled": False,
                "error": "Cloud database module not found. Please install google-cloud-firestore package.",
                "setup_instructions": {
                    "step_1": "Go to https://console.cloud.google.com/firestore",
                    "step_2": "Create a new Firestore database in Native mode",
                    "step_3": "Download service account key as 'google-cloud-key.json'",
                    "step_4": "Place the key file in /app/backend/ directory",
                    "step_5": "Restart the backend service"
                }
            }
        
        if not hasattr(cloud_db, 'enabled') or not cloud_db.enabled:
            return {
                "enabled": False,
                "error": "Cloud database not configured",
                "setup_instructions": {
                    "step_1": "Go to https://console.cloud.google.com/firestore",
                    "step_2": "Create a new Firestore database in Native mode",
                    "step_3": "Download service account key as 'google-cloud-key.json'",
                    "step_4": "Place the key file in /app/backend/ directory",
                    "step_5": "Restart the backend service"
                }
            }
        
        # Get cloud statistics
        cloud_stats = await cloud_db.get_processing_statistics()
        
        # Get local statistics for comparison
        local_stats = {
            "total_videos": await db.videos.count_documents({}),
            "processed_videos": await db.videos.count_documents({"transcript_processed": True}),
            "total_qa_pairs": await db.question_answers.count_documents({})
        }
        
        return {
            "enabled": True,
            "cloud_stats": cloud_stats,
            "local_stats": local_stats,
            "sync_status": {
                "videos_match": cloud_stats.get('total_videos', 0) == local_stats['total_videos'],
                "qa_pairs_match": cloud_stats.get('total_qa_pairs', 0) == local_stats['total_qa_pairs'],
                "last_checked": datetime.utcnow().isoformat()
            },
            "recommendations": get_sync_recommendations(cloud_stats, local_stats)
        }
        
    except Exception as e:
        logger.error(f"Error getting cloud status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_sync_recommendations(cloud_stats: dict, local_stats: dict) -> list:
    """Get recommendations for data synchronization"""
    recommendations = []
    
    cloud_videos = cloud_stats.get('total_videos', 0)
    local_videos = local_stats['total_videos']
    cloud_qa = cloud_stats.get('total_qa_pairs', 0)
    local_qa = local_stats['total_qa_pairs']
    
    if local_videos > cloud_videos:
        recommendations.append({
            "type": "backup_needed",
            "message": f"Local database has {local_videos - cloud_videos} more videos than cloud. Consider backing up.",
            "action": "POST /api/cloud/backup"
        })
    
    if cloud_videos > local_videos:
        recommendations.append({
            "type": "restore_available",
            "message": f"Cloud database has {cloud_videos - local_videos} more videos than local. Consider restoring.",
            "action": "POST /api/cloud/restore"
        })
    
    if local_qa > cloud_qa:
        recommendations.append({
            "type": "qa_backup_needed",
            "message": f"Local database has {local_qa - cloud_qa} more Q&A pairs than cloud.",
            "action": "POST /api/cloud/backup"
        })
    
    if cloud_qa > local_qa:
        recommendations.append({
            "type": "qa_restore_available",
            "message": f"Cloud database has {cloud_qa - local_qa} more Q&A pairs than local.",
            "action": "POST /api/cloud/restore"
        })
    
    if cloud_videos == local_videos and cloud_qa == local_qa:
        recommendations.append({
            "type": "in_sync",
            "message": "Local and cloud databases are in sync.",
            "action": "none"
        })
    
    return recommendations

@api_router.post("/cloud/sync")
async def sync_with_cloud():
    """Smart synchronization with cloud database"""
    try:
        # Import conditionally to handle missing module gracefully
        try:
            from backend.services.cloud_database_service import cloud_db
        except ImportError:
            return {
                "success": False,
                "error": "Cloud database module not found. Please install google-cloud-firestore package."
            }
        
        if not hasattr(cloud_db, 'enabled') or not cloud_db.enabled:
            return {
                "success": False,
                "error": "Cloud database not configured"
            }
        
        sync_results = {
            "videos_synced": 0,
            "qa_pairs_synced": 0,
            "errors": []
        }
        
        # Get unprocessed videos from cloud to avoid reprocessing
        cloud_processed_ids = await cloud_db.get_processed_video_ids()
        
        # Mark videos as processed in local DB if they're processed in cloud
        if cloud_processed_ids:
            result = await db.videos.update_many(
                {
                    "video_id": {"$in": cloud_processed_ids},
                    "transcript_processed": {"$ne": True}
                },
                {"$set": {"transcript_processed": True}}
            )
            sync_results["videos_synced"] = result.modified_count
        
        # Sync any new local videos to cloud
        local_videos = await db.videos.find({"transcript_processed": True}).to_list(None)
        for video in local_videos:
            if video['video_id'] not in cloud_processed_ids:
                video_data = {
                    'video_id': video['video_id'],
                    'title': video['title'],
                    'description': video.get('description', ''),
                    'duration': video.get('duration', ''),
                    'upload_date': video.get('upload_date'),
                    'view_count': video.get('view_count', 0),
                    'transcript_processed': video.get('transcript_processed', False)
                }
                await cloud_db.sync_video_metadata(video_data)
        
        return {
            "success": True,
            "sync_results": sync_results,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Synchronization completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error during cloud sync: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)