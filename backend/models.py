from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from backend.services.query_safety import clamp_limit

class VideoModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: str
    title: str
    description: str
    duration: str
    upload_date: datetime
    view_count: int
    transcript_processed: bool = False
    channel_id: Optional[str] = None
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
    source: Optional[str] = None
    embedding: Optional[List[float]] = None
    channel_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SearchQuery(BaseModel):
    query: str
    language: Optional[str] = "auto"
    limit: int = 5
    conversation_history: List[str] = Field(default_factory=list)
    channel_id: Optional[str] = None

    @field_validator("limit", mode="before")
    @classmethod
    def _clamp_search_limit(cls, value):
        return clamp_limit(value)

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
    channel_id: Optional[str] = None
    channel_name: Optional[str] = None
    related_questions: List[str] = Field(default_factory=list)
    formatted_start_time: Optional[str] = None

class RecommendationRequest(BaseModel):
    recent_queries: List[str] = Field(default_factory=list)
    language: Optional[str] = "hi"
    limit: int = 6
    channel_id: Optional[str] = None

class AskQuery(BaseModel):
    query: str
    language: Optional[str] = "hi"
    limit: int = 3
    conversation_history: List[str] = Field(default_factory=list)
    channel_id: Optional[str] = None
    include_companions: bool = False

    @field_validator("limit", mode="before")
    @classmethod
    def _clamp_ask_limit(cls, value):
        return clamp_limit(value, high=20)

class MalaState(BaseModel):
    beads_today: int = 0
    cycles_today: int = 0
    current_in_cycle: int = 0
    questions_today: int = 0
    completed_cycle: bool = False
    beads_per_cycle: int = 108
    mantra_id: str = "ram"

class ControlSettingsPatch(BaseModel):
    language: Optional[str] = None
    beads_per_cycle: Optional[int] = None
    mantra_id: Optional[str] = None
    sandhya: Optional[bool] = None
    japa_focus: Optional[bool] = None
    notifications: Optional[bool] = None
    processing_enabled: Optional[bool] = None
    default_channel_id: Optional[str] = None
    public_companions: Optional[bool] = None


class ByokKeysPatch(BaseModel):
    youtube: Optional[str] = None
    gemini: Optional[str] = None
    mistral: Optional[str] = None
    google_translate: Optional[str] = None


class PinQaRequest(BaseModel):
    question: str
    answer: str
    video_id: Optional[str] = ""
    video_title: Optional[str] = ""
    start_time: float = 0
    timestamp_url: Optional[str] = ""
    channel_id: Optional[str] = None


class UnpinQaRequest(BaseModel):
    video_id: Optional[str] = ""
    question: str = ""


class MalaSyncRequest(BaseModel):
    device_id: str
    day: str
    mantra_id: str = "ram"
    beads_today: int = 0
    cycles_today: int = 0
    current_in_cycle: int = 0
    questions_today: int = 0
    beads_per_cycle: int = 108
    completed_cycle: bool = False


class CompanionQuery(BaseModel):
    query: str
    language: Optional[str] = "hi"


class ScrapeRequest(BaseModel):
    url: str


class VideoMetaRequest(BaseModel):
    video_id: str


class FeedbackRequest(BaseModel):
    type: Optional[str] = "general"
    rating: Optional[int] = None
    message: str = ""
    user_agent: Optional[str] = ""
    page: Optional[str] = ""
    language: Optional[str] = "en"

    @field_validator("message", mode="before")
    @classmethod
    def _message_len(cls, value):
        text = str(value or "")
        if len(text) > 4000:
            raise ValueError("message too long")
        return text


class IngestRequest(BaseModel):
    videos: List[Dict[str, Any]] = []
    video_ids: List[str] = []
    channel: Optional[str] = None


class ProcessStartRequest(BaseModel):
    channel_url: Optional[str] = None


class IngestUrlRequest(BaseModel):
    url: str = ""

class ProcessingStatus(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str  # pending, processing, completed, failed
    total_videos: int
    processed_videos: int
    current_video_title: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None