import asyncio
import logging
import os
from typing import Any, Callable, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models import ProcessingStatus, QuestionAnswer, TranscriptSegment, VideoModel
from .llm_service import LLMService
from .transcript_ingest import (
    resolve_video_transcript,
    segments_to_qa,
    to_caption_segments,
    transcribe_with_whisper,
)
from .youtube_service import YouTubeService

logger = logging.getLogger(__name__)

TranscribeFn = Callable[..., List[Dict[str, Any]]]


class ProcessingService:
    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        youtube_service: Optional[YouTubeService] = None,
        llm_service: Optional[LLMService] = None,
        transcribe: Optional[TranscribeFn] = None,
        audio_directory: Optional[str] = None,
    ):
        self.db = db
        self.youtube_service = youtube_service or YouTubeService()
        self.llm_service = llm_service or LLMService()
        self.transcribe = transcribe or transcribe_with_whisper
        self.audio_directory = audio_directory or os.getenv("WHISPER_AUDIO_DIR")
        
    async def start_channel_processing(self, channel_url: str = None) -> str:
        """Start incremental processing of unprocessed videos from the channel"""
        try:
            # Create processing status
            status = ProcessingStatus(
                status="pending",
                total_videos=0,
                processed_videos=0,
                current_video_title="Initializing..."
            )
            
            # Insert status into database
            await self.db.processing_status.insert_one(status.dict())
            status_id = status.id
            
            # Start processing in background
            asyncio.create_task(self._process_channel_videos_incremental(status_id, channel_url))
            
            return status_id
            
        except Exception as e:
            logger.error(f"Error starting channel processing: {str(e)}")
            raise
    
    async def _process_channel_videos_incremental(self, status_id: str, channel_url: str = None):
        """Incremental processing - only process unprocessed videos"""
        try:
            # Update status to processing
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {"status": "processing", "current_video_title": "Fetching video list..."}}
            )
            
            logger.info("Starting incremental video processing...")
            
            # Extract channel info from URL if provided
            channel_username = "bhajanmarg"  # default
            if channel_url:
                channel_username = self._extract_channel_from_url(channel_url)
            
            # Get all videos from YouTube (only if needed)
            existing_video_count = await self.db.videos.count_documents({})
            
            if existing_video_count < 100 or channel_url:  # Fetch videos if we don't have many or custom channel
                logger.info(f"Fetching videos from YouTube channel: {channel_username}")
                try:
                    videos_data = await self.youtube_service.get_channel_videos(channel_username)
                    logger.info(f"Fetched {len(videos_data)} videos from YouTube")
                    
                    # Store videos that don't exist yet
                    new_videos_count = 0
                    for video_data in videos_data:
                        existing = await self.db.videos.find_one({"video_id": video_data['video_id']})
                        if not existing:
                            video = VideoModel(**video_data)
                            await self.db.videos.insert_one(video.dict())
                            new_videos_count += 1
                    
                    logger.info(f"Added {new_videos_count} new videos to database")
                    
                except Exception as e:
                    if "quota" in str(e).lower():
                        logger.warning("YouTube API quota exceeded, using existing videos")
                    else:
                        logger.error(f"Error fetching videos: {str(e)}")
            
            # Get unprocessed videos from database
            unprocessed_videos = await self.db.videos.find({
                "transcript_processed": {"$ne": True}
            }).to_list(None)
            
            total_videos = len(unprocessed_videos)
            processed_count = 0
            
            # Update total count
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {"total_videos": total_videos}}
            )
            
            logger.info(f"Processing {total_videos} unprocessed videos...")
            
            # Process each unprocessed video
            for video in unprocessed_videos:
                try:
                    await self._process_single_video_smart(video, status_id)
                    processed_count += 1
                    
                    # Update progress
                    await self.db.processing_status.update_one(
                        {"id": status_id},
                        {"$set": {
                            "processed_videos": processed_count,
                            "current_video_title": video['title']
                        }}
                    )
                    
                    logger.info(f"Processed video {processed_count}/{total_videos}: {video['title']}")
                    
                    # Add delay to avoid rate limiting (only call APIs when needed)
                    await asyncio.sleep(3)
                    
                except Exception as e:
                    logger.error(f"Error processing video {video['video_id']}: {str(e)}")
                    # Continue with next video instead of stopping
                    continue
            
            # Mark as completed
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {"status": "completed"}}
            )
            
            logger.info(f"Incremental processing completed. Processed {processed_count} videos.")
            
        except Exception as e:
            logger.error(f"Error in incremental processing: {str(e)}")
            
            # Mark as failed
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {
                    "status": "failed",
                    "error_message": str(e)
                }}
            )
    
    def _extract_channel_from_url(self, channel_url: str) -> str:
        """Extract channel username/handle from YouTube URL"""
        try:
            import re
            # Handle different YouTube URL formats
            patterns = [
                r'youtube\.com/@([^/?]+)',  # @username format
                r'youtube\.com/c/([^/?]+)',  # /c/channelname format
                r'youtube\.com/user/([^/?]+)',  # /user/username format
                r'youtube\.com/channel/([^/?]+)',  # /channel/id format
            ]
            
            for pattern in patterns:
                match = re.search(pattern, channel_url)
                if match:
                    return match.group(1)
            
            # If no pattern matches, return the URL as is (let YouTube service handle it)
            return channel_url
            
        except Exception as e:
            logger.error(f"Error extracting channel from URL: {str(e)}")
            return "bhajanmarg"  # fallback
    
    async def _ingest_and_persist(
        self,
        video_id: str,
        title: str,
        captions: Optional[List[Dict[str, Any]]],
    ) -> bool:
        """Store captions or Whisper transcript. Empty result stays unprocessed."""
        ingested = resolve_video_transcript(
            video_id,
            captions=captions,
            transcribe=self.transcribe,
            audio_directory=self.audio_directory,
        )
        storage = to_caption_segments(ingested["segments"])
        if not storage:
            logger.warning(
                f"No captions or audio transcript for video {video_id}; leaving unprocessed"
            )
            return False

        for segment_data in storage:
            segment = TranscriptSegment(video_id=video_id, **segment_data)
            await self.db.transcript_segments.insert_one(segment.dict())

        logger.info(f"Extracting Q&A pairs from {len(storage)} segments...")
        qa_pairs = await self.llm_service.extract_qa_from_transcript(storage, title)
        if not qa_pairs:
            qa_pairs = segments_to_qa(ingested["segments"], video_id, title)

        for qa_data in qa_pairs:
            payload = dict(qa_data)
            payload["video_id"] = video_id
            qa = QuestionAnswer(**payload)
            await self.db.question_answers.insert_one(qa.dict())

        await self.db.videos.update_one(
            {"video_id": video_id},
            {"$set": {"transcript_processed": True}},
        )
        logger.info(
            f"Successfully processed video {video_id}: extracted {len(qa_pairs)} Q&A pairs "
            f"from {ingested['source']}"
        )
        return True

    async def _process_single_video_smart(self, video: Dict[str, Any], status_id: str):
        """Smart processing - only use APIs when absolutely necessary"""
        try:
            video_id = video['video_id']
            
            # Check if already processed
            if video.get('transcript_processed'):
                logger.info(f"Video {video_id} already processed, skipping...")
                return
            
            logger.info(f"Getting captions for video: {video['title']}")
            caption_segments = await self.youtube_service.get_video_captions(video_id)
            await self._ingest_and_persist(video_id, video["title"], caption_segments)
            
        except Exception as e:
            logger.error(f"Error processing video {video.get('video_id', 'unknown')}: {str(e)}")
            raise
    
    async def _process_channel_videos(self, status_id: str):
        """Background task to process all channel videos"""
        try:
            # Update status to processing
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {"status": "processing"}}
            )
            
            # Get all videos from channel
            logger.info("Fetching videos from YouTube channel...")
            videos_data = await self.youtube_service.get_channel_videos()
            
            # Update total count
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {"total_videos": len(videos_data)}}
            )
            
            # Process each video
            processed_count = 0
            
            for video_data in videos_data:
                try:
                    await self._process_single_video(video_data, status_id)
                    processed_count += 1
                    
                    # Update progress
                    await self.db.processing_status.update_one(
                        {"id": status_id},
                        {"$set": {
                            "processed_videos": processed_count,
                            "current_video_title": video_data['title']
                        }}
                    )
                    
                    logger.info(f"Processed video {processed_count}/{len(videos_data)}: {video_data['title']}")
                    
                    # Add delay to avoid rate limiting
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error processing video {video_data['video_id']}: {str(e)}")
                    continue
            
            # Mark as completed
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {"status": "completed"}}
            )
            
            logger.info(f"Channel processing completed. Processed {processed_count} videos.")
            
        except Exception as e:
            logger.error(f"Error in channel processing: {str(e)}")
            
            # Mark as failed
            await self.db.processing_status.update_one(
                {"id": status_id},
                {"$set": {
                    "status": "failed",
                    "error_message": str(e)
                }}
            )
    
    async def _process_single_video(self, video_data: Dict[str, Any], status_id: str):
        """Process a single video"""
        try:
            video_id = video_data['video_id']
            
            # Check if video already exists
            existing_video = await self.db.videos.find_one({"video_id": video_id})
            if existing_video and existing_video.get('transcript_processed'):
                logger.info(f"Video {video_id} already processed, skipping...")
                return
            
            # Create video record
            video = VideoModel(**video_data)
            if existing_video:
                await self.db.videos.update_one(
                    {"video_id": video_id},
                    {"$set": video.dict()}
                )
            else:
                await self.db.videos.insert_one(video.dict())
            
            logger.info(f"Getting captions for video: {video.title}")
            caption_segments = await self.youtube_service.get_video_captions(video_id)
            await self._ingest_and_persist(video_id, video.title, caption_segments)
            
        except Exception as e:
            logger.error(f"Error processing video {video_data.get('video_id', 'unknown')}: {str(e)}")
            raise
    
    async def get_processing_status(self, status_id: str) -> Dict[str, Any]:
        """Get processing status"""
        try:
            status = await self.db.processing_status.find_one({"id": status_id})
            if status:
                # Convert ObjectId to string to make it JSON serializable
                if "_id" in status:
                    status["_id"] = str(status["_id"])
                return status
            else:
                return {"error": "Status not found"}
                
        except Exception as e:
            logger.error(f"Error getting processing status: {str(e)}")
            return {"error": str(e)}