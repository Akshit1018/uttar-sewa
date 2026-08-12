#!/usr/bin/env python3
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid

# Import models and services
from backend.models import (
    VideoModel, TranscriptSegment, QuestionAnswer,
    SearchQuery, SearchResult, ProcessingStatus, RecommendationRequest,
    AskQuery, MalaState, ControlSettingsPatch, PinQaRequest, MalaSyncRequest,
    CompanionQuery, ScrapeRequest, VideoMetaRequest, IngestRequest
)
from backend.services.processing_service import ProcessingService
from backend.services.llm_service import LLMService
from backend.services.youtube_service import YouTubeService
from backend.services.enhanced_search_coordinator import enhanced_search_coordinator
from backend.services.relevance_search import (
    expand_query, rank_answers, related_questions, library_as_qa, recommend_from_history
)
from backend.services.grounded_ask import grounded_ask
from backend.services.mala_counter import (
    ALLOWED_CYCLE_LENGTHS,
    BEADS_PER_CYCLE,
    HOLD_MS,
    apply_tap,
    apply_undo,
    named_malas,
    summarize_day,
)
from backend.services.timestamp_urls import build_watch_url, format_timestamp_display
from backend.services.channel_registry import list_channels, get_channel, topic_for_tags
from backend.services.control_store import (
    dashboard_payload,
    default_settings,
    mala_day_key,
    merge_settings,
    pin_document,
)
from backend.services.database import bootstrap_database
from backend.db_schema import SETTINGS_DOC_ID
from backend.services.public_enrichment import (
    catalog as public_catalog,
    companions_for_query,
    fetch_books,
    fetch_definition,
    fetch_gita,
    fetch_wikipedia,
    fetch_youtube_meta,
    scrape_public_page,
    today_bundle,
    daily_gita_ref,
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=2000)
db = client[os.environ.get('DB_NAME', 'uttar_sewa')]

# Create the main app without a prefix
app = FastAPI(title="Uttar Sewa API", version="2.3.0")

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
        "message": "Uttar Sewa API",
        "status": "running",
        "flutter": True,
        "control_dashboard": "/api/control/dashboard",
        "health": "/api/health",
        "enrich": "/api/enrich/today",
    }


@api_router.get("/health")
async def health():
    mongo_ok = False
    try:
        await db.command("ping")
        mongo_ok = True
    except Exception:
        mongo_ok = False
    return {
        "ok": True,
        "api": True,
        "database": mongo_ok,
        "ready": True,
        "enrichment": True,
    }

@api_router.post("/process/start")
async def start_processing():
    """Start processing all videos from the YouTube channel"""
    settings = await _load_control_settings()
    if not settings.get("processing_enabled"):
        raise HTTPException(status_code=400, detail="Processing is disabled in control settings")
    try:
        status_id = await processing_service.start_channel_processing()
        return {
            "ok": True,
            "message": "Processing started",
            "status_id": status_id,
            "note": "This will process all videos from the channel. Check status using /process/status/{status_id}"
        }
    except Exception as e:
        logger.error(f"Error starting processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/process/ingest")
async def ingest_youtube_library(body: IngestRequest):
    """Fill videos / captions / Q&A from a YouTube payload without the curated fallback."""
    settings = await _load_control_settings()
    if not settings.get("processing_enabled"):
        raise HTTPException(status_code=400, detail="Processing is disabled in control settings")
    videos = list(body.videos or [])
    for video_id in body.video_ids or []:
        videos.append({"video_id": video_id})
    try:
        if body.channel and not videos:
            return await processing_service.ingest_from_channel(body.channel)
        if not videos:
            raise HTTPException(status_code=400, detail="Provide videos, video_ids, or channel")
        return await processing_service.ingest_video_list(videos)
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error ingesting YouTube library: {error}")
        raise HTTPException(status_code=500, detail=str(error))

@api_router.get("/process/status/{status_id}")
async def get_processing_status(status_id: str):
    """Get processing status"""
    try:
        status = await processing_service.get_processing_status(status_id)
        return status
    except Exception as e:
        logger.error(f"Error getting processing status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def _normalize_qa_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    tags = doc.get("tags", []) or []
    channel_id = doc.get("channel_id") or topic_for_tags(tags)
    channel = get_channel(channel_id)
    return {
        "question": doc.get("question", ""),
        "answer": doc.get("answer", ""),
        "video_id": doc.get("video_id", "") or "",
        "start_time": doc.get("start_time", 0) or 0,
        "end_time": doc.get("end_time", (doc.get("start_time") or 0) + 60),
        "confidence_score": doc.get("confidence_score", 0.8),
        "tags": tags,
        "language": doc.get("language", "hi"),
        "video_title": doc.get("video_title") or doc.get("title") or "",
        "channel_id": channel_id,
        "channel_name": (channel or {}).get("name") or channel_id,
    }


async def _load_qa_database() -> List[Dict[str, Any]]:
    try:
        qa_docs = await db.question_answers.find().to_list(2000)
        qa_database = [_normalize_qa_doc(doc) for doc in qa_docs if doc.get("question")]
        if qa_database:
            return qa_database
        logger.warning("No Q&A documents found in database; using curated library")
    except Exception as error:
        logger.warning(f"qa load skipped: {error}")
    return library_as_qa()


def _to_search_result(answer: Dict[str, Any], video: Optional[Dict[str, Any]], related: List[str]) -> SearchResult:
    video_id = answer.get("video_id") or ""
    start_time = float(answer.get("start_time") or 0)
    watch_url = build_watch_url(video_id, start_time) if video_id else ""
    home_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""
    video_title = (
        (video or {}).get("title")
        or answer.get("video_title")
        or "Spiritual discourse"
    )
    channel_id = answer.get("channel_id") or (video or {}).get("channel_id")
    channel = get_channel(channel_id)
    return SearchResult(
        question=answer["question"],
        answer=answer["answer"],
        video_id=video_id,
        video_title=video_title,
        start_time=start_time,
        end_time=float(answer.get("end_time") or start_time + 60),
        confidence_score=float(answer.get("confidence_score") or 0.7),
        youtube_url=home_url,
        timestamp_url=watch_url,
        channel_id=channel_id,
        channel_name=(channel or {}).get("name") or answer.get("channel_name"),
        related_questions=related,
        formatted_start_time=format_timestamp_display(start_time) if video_id else None,
    )


@api_router.post("/search", response_model=List[SearchResult])
async def search_questions(query: SearchQuery):
    """Search Q&A with conversation memory, channel filters, and lexical ranking."""
    try:
        if not (query.query or "").strip():
            return []

        logger.info(f"Processing search query: '{query.query}' with limit: {query.limit}")
        qa_database = await _load_qa_database()
        expanded = expand_query(query.query, query.conversation_history)
        relevant_answers = rank_answers(
            expanded,
            qa_database,
            limit=query.limit,
            channel_id=query.channel_id,
        )

        if len(relevant_answers) < query.limit:
            try:
                extra = await enhanced_search_coordinator.search(
                    user_query=expanded,
                    qa_database=qa_database,
                    limit=query.limit,
                    strategy="ultra",
                )
                seen = {(item.get("video_id"), item.get("question")) for item in relevant_answers}
                for item in extra:
                    key = (item.get("video_id"), item.get("question"))
                    if key not in seen:
                        relevant_answers.append(item)
                        seen.add(key)
                    if len(relevant_answers) >= query.limit:
                        break
            except Exception as extra_error:
                logger.warning(f"Optional ultra search skipped: {extra_error}")

        results = []
        for answer in relevant_answers[: query.limit]:
            try:
                video = None
                if answer.get("video_id"):
                    try:
                        video = await db.videos.find_one({"video_id": answer["video_id"]})
                    except Exception:
                        video = None
                related = related_questions(answer, qa_database, limit=3)
                results.append(_to_search_result(answer, video, related))
            except Exception as e:
                logger.error(f"Error processing search result: {str(e)}")
                continue

        logger.info(f"Returning {len(results)} formatted search results")
        return results

    except Exception as e:
        logger.error(f"Error in enhanced search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/channels")
async def get_channels():
    """List searchable channel groups."""
    return {"channels": list_channels()}


@api_router.post("/recommendations")
async def get_recommendations(body: RecommendationRequest):
    """Personalized question suggestions from recent search history."""
    try:
        qa_database = await _load_qa_database()
        ranked = recommend_from_history(
            body.recent_queries,
            qa_database,
            limit=body.limit,
            channel_id=body.channel_id,
        )
        return {
            "recommendations": [item["question"] for item in ranked],
            "count": len(ranked),
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ask")
async def ask_grounded(body: AskQuery):
    """Answer only from the video/Q&A corpus, with citations. Refuses if evidence is weak."""
    try:
        if not (body.query or "").strip():
            language = body.language or "hi"
            return {
                "answer": "कृपया प्रश्न लिखें।" if language == "hi" else "Please enter a question.",
                "refused": True,
                "clips": [],
                "expanded_query": "",
                "top_score": 0,
            }
        qa_database = await _load_qa_database()
        result = grounded_ask(
            body.query,
            corpus=qa_database,
            conversation_history=body.conversation_history,
            language=body.language or "hi",
            limit=body.limit,
            channel_id=body.channel_id,
        )
        result["companions"] = []
        if body.include_companions:
            try:
                result["companions"] = companions_for_query(body.query, body.language or "hi")
            except Exception as enrich_error:
                logger.warning(f"public companions skipped: {enrich_error}")
                result["companions"] = []
        return result
    except Exception as e:
        logger.error(f"Error in grounded ask: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/mala/config")
async def mala_config():
    return {
        "beads_per_cycle": BEADS_PER_CYCLE,
        "allowed_cycle_lengths": list(ALLOWED_CYCLE_LENGTHS),
        "named_malas": named_malas(),
        "hold_ms": HOLD_MS,
        "overlay": "in_app",
        "sandhya": {"morning_hour": 6, "evening_hour": 18},
        "note": "System-wide overlay requires a native Android shell; iOS uses in-app orb + Live Activity later.",
    }


@api_router.post("/mala/tap")
async def mala_tap(body: MalaState):
    return apply_tap(body.model_dump())


@api_router.post("/mala/undo")
async def mala_undo(body: MalaState):
    return apply_undo(body.model_dump())


@api_router.post("/mala/summary")
async def mala_summary(body: MalaState):
    return summarize_day(body.model_dump())


async def _load_control_settings():
    try:
        doc = await db.control_settings.find_one({"_id": SETTINGS_DOC_ID})
        if doc:
            return merge_settings(doc, {})
    except Exception as error:
        logger.warning(f"control settings read skipped: {error}")
    return default_settings()


async def _save_control_settings(settings):
    try:
        await db.control_settings.replace_one({"_id": SETTINGS_DOC_ID}, settings, upsert=True)
    except Exception as error:
        logger.warning(f"control settings write skipped: {error}")
    return settings


@api_router.get("/control/dashboard")
async def control_dashboard():
    stats = {
        "total_videos": 0,
        "processed_videos": 0,
        "unprocessed_videos": 0,
        "total_qa_pairs": 0,
    }
    pinned_count = 0
    api_ok = True
    try:
        total_videos = await db.videos.count_documents({})
        processed = await db.videos.count_documents({"transcript_processed": True})
        qa_count = await db.question_answers.count_documents({})
        pinned_count = await db.pinned_qa.count_documents({})
        stats = {
            "total_videos": total_videos,
            "processed_videos": processed,
            "unprocessed_videos": max(0, total_videos - processed),
            "total_qa_pairs": qa_count,
        }
    except Exception as error:
        logger.warning(f"control dashboard mongo skipped: {error}")
        api_ok = True
    settings = await _load_control_settings()
    return dashboard_payload(stats, settings, pinned_count, api_ok)


@api_router.get("/control/settings")
async def get_control_settings():
    return await _load_control_settings()


@api_router.put("/control/settings")
async def put_control_settings(body: ControlSettingsPatch):
    current = await _load_control_settings()
    patch = {key: value for key, value in body.model_dump().items() if value is not None}
    merged = merge_settings(current, patch)
    return await _save_control_settings(merged)


@api_router.post("/control/qa/pin")
async def pin_qa(body: PinQaRequest):
    doc = pin_document(body.model_dump())
    try:
        await db.pinned_qa.insert_one(dict(doc))
        if doc.get("video_id"):
            await db.question_answers.update_many(
                {"video_id": doc["video_id"], "question": doc["question"]},
                {"$set": {"pinned": True}},
            )
    except Exception as error:
        logger.warning(f"pin persist skipped: {error}")
    return doc


@api_router.get("/control/qa/pinned")
async def list_pinned_qa():
    try:
        rows = await db.pinned_qa.find({}, {"_id": 0}).sort("pinned_at", -1).to_list(50)
        return {"items": rows, "count": len(rows)}
    except Exception as error:
        logger.warning(f"pinned list skipped: {error}")
        return {"items": [], "count": 0}


@api_router.get("/control/library/gaps")
async def library_gaps():
    try:
        unprocessed = await db.videos.find(
            {"transcript_processed": {"$ne": True}},
            {"_id": 0, "video_id": 1, "title": 1, "channel_id": 1},
        ).to_list(50)
        return {"items": unprocessed, "count": len(unprocessed)}
    except Exception as error:
        logger.warning(f"library gaps skipped: {error}")
        return {"items": [], "count": 0}


@api_router.post("/mala/sync")
async def mala_sync(body: MalaSyncRequest):
    key = mala_day_key(body.device_id, body.day, body.mantra_id)
    doc = {**key, **body.model_dump()}
    try:
        await db.mala_days.replace_one(key, doc, upsert=True)
    except Exception as error:
        logger.warning(f"mala sync skipped: {error}")
    return summarize_day(doc)


@api_router.get("/mala/day")
async def mala_day(device_id: str, day: str, mantra_id: str = "ram"):
    key = mala_day_key(device_id, day, mantra_id)
    try:
        doc = await db.mala_days.find_one(key, {"_id": 0})
        if doc:
            return summarize_day(doc)
    except Exception as error:
        logger.warning(f"mala day skipped: {error}")
    return summarize_day({**key, "beads_today": 0, "cycles_today": 0, "current_in_cycle": 0})


@api_router.get("/enrich/catalog")
async def enrich_catalog():
    return {
        "items": public_catalog(),
        "scrapling": "https://github.com/D4Vinci/Scrapling",
        "llm_apps": "https://github.com/Shubhamsaboo/awesome-llm-apps",
        "public_apis": "https://github.com/public-apis/public-apis",
        "note": "Companions are labeled public text. They never replace a video citation.",
    }


@api_router.get("/enrich/today")
async def enrich_today(language: str = "hi"):
    try:
        return today_bundle(language=language if language in ("hi", "en") else "hi")
    except Exception as error:
        logger.warning(f"enrich today skipped: {error}")
        return {"gita": None, "sandhya": None, "catalog": public_catalog(), "error": str(error)}


@api_router.get("/enrich/gita")
async def enrich_gita(chapter: Optional[int] = None, verse: Optional[int] = None, language: str = "hi"):
    try:
        if chapter is None or verse is None:
            chapter, verse = daily_gita_ref()
        return fetch_gita(int(chapter), int(verse), language=language if language in ("hi", "en") else "hi")
    except Exception as error:
        logger.warning(f"gita fetch skipped: {error}")
        raise HTTPException(status_code=502, detail="Gita API unavailable")


@api_router.get("/enrich/define")
async def enrich_define(q: str, language: str = "hi"):
    try:
        return fetch_definition(q)
    except Exception as error:
        logger.warning(f"dictionary skipped: {error}")
        raise HTTPException(status_code=502, detail="Dictionary API unavailable")


@api_router.get("/enrich/wiki")
async def enrich_wiki(q: str, language: str = "hi"):
    try:
        return fetch_wikipedia(q, language=language if language in ("hi", "en") else "hi")
    except Exception as error:
        logger.warning(f"wikipedia skipped: {error}")
        raise HTTPException(status_code=502, detail="Wikipedia API unavailable")


@api_router.get("/enrich/books")
async def enrich_books(q: str):
    try:
        return {"items": fetch_books(q)}
    except Exception as error:
        logger.warning(f"open library skipped: {error}")
        raise HTTPException(status_code=502, detail="Open Library unavailable")


@api_router.post("/enrich/companions")
async def enrich_companions(body: CompanionQuery):
    """Corrective-RAG style public cards. Never mixed into the video answer."""
    try:
        cards = companions_for_query(body.query, body.language or "hi")
        return {"items": cards, "count": len(cards), "source": "public"}
    except Exception as error:
        logger.warning(f"companions skipped: {error}")
        return {"items": [], "count": 0, "source": "public"}


@api_router.post("/control/scrape")
async def control_scrape(body: ScrapeRequest):
    try:
        return scrape_public_page(body.url)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        logger.warning(f"scrape skipped: {error}")
        raise HTTPException(status_code=502, detail="Public scrape failed")


@api_router.post("/control/enrich/video")
async def control_enrich_video(body: VideoMetaRequest):
    try:
        return fetch_youtube_meta(body.video_id)
    except Exception as error:
        logger.warning(f"youtube oembed skipped: {error}")
        raise HTTPException(status_code=502, detail="YouTube oEmbed unavailable")

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
        logger.warning(f"Error getting stats: {str(e)}")
        return {
            "total_videos": 0,
            "processed_videos": 0,
            "total_qa_pairs": 0,
            "total_transcript_segments": 0,
            "processing_progress": "0/0",
            "library": "curated",
        }

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
        logger.warning(f"Error getting suggested questions: {str(e)}")
        defaults = [
            "जीवन का उद्देश्य क्या है?",
            "ध्यान कैसे करें?",
            "मानसिक शांति कैसे पाएं?",
            "आध्यात्मिक जीवन कैसे जिएं?",
            "गुरु की आवश्यकता क्यों है?",
        ]
        return {
            "suggested_questions": defaults,
            "note": "curated library",
            "real_questions_count": 0,
        }

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
        await db.processing_status.delete_many({})
        return {
            "ok": True,
            "message": "Processing status cleared successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.warning(f"Error clearing processing status: {str(e)}")
        return {
            "ok": False,
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

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

@api_router.post("/cloud/backup")
async def backup_to_cloud():
    """Backup local data to Google Cloud Firestore"""
    try:
        from backend.services.cloud_database_service import cloud_db
        
        if not cloud_db.enabled:
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
        from backend.services.cloud_database_service import cloud_db
        
        if not cloud_db.enabled:
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
        from backend.services.cloud_database_service import cloud_db
        
        if not cloud_db.enabled:
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
        from backend.services.cloud_database_service import cloud_db
        
        if not cloud_db.enabled:
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

@app.on_event("startup")
async def startup_database():
    try:
        result = await bootstrap_database(db)
        logger.info(f"database ready: {result}")
    except Exception as error:
        logger.warning(f"database bootstrap skipped: {error}")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
