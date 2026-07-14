from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class VideoModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: str
    title: str
    description: str
    duration: str
    upload_date: datetime
    view_count: int
    transcript_processed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TranscriptSegment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: str
    start_time: float
    end_time: float
    text: str
    language: str = "hi"  # Default Hindi
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuestionAnswer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: str
    question: str
    answer: str
    start_time: float
    end_time: float
    confidence_score: float
    language: str
    tags: List[str] = []
    embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SearchQuery(BaseModel):
    query: str
    language: Optional[str] = "auto"
    limit: int = 5

class SearchResult(BaseModel):
    question: str
    answer: str
    video_id: str
    video_title: str
    start_time: float
    end_time: float
    confidence_score: float
    youtube_url: str
    timestamp_url: str

class ProcessingStatus(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str  # pending, processing, completed, failed
    total_videos: int
    processed_videos: int
    current_video_title: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None