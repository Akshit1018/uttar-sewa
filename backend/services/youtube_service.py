import os
import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional, Any
import logging
from datetime import datetime, timezone
import isodate

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.api_key = os.environ.get('YOUTUBE_API_KEY')
        self.youtube = None
        if self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        else:
            logger.warning("YOUTUBE_API_KEY missing; YouTube ingest disabled")

    def _client(self):
        if self.youtube is None:
            raise RuntimeError("YOUTUBE_API_KEY is not configured")
        return self.youtube
        
    async def get_channel_videos(self, channel_username: str = "bhajanmarg") -> List[Dict[str, Any]]:
        """Get all videos from the channel"""
        try:
            # First get channel ID from username
            channels_response = self._client().channels().list(
                part='id,contentDetails',
                forUsername=channel_username
            ).execute()
            
            if not channels_response.get('items'):
                # Try with channel handle instead
                search_response = self._client().search().list(
                    part='snippet',
                    q=channel_username,
                    type='channel',
                    maxResults=1
                ).execute()
                
                if not search_response.get('items'):
                    raise ValueError(f"Channel {channel_username} not found")
                    
                channel_id = search_response['items'][0]['snippet']['channelId']
                
                channels_response = self._client().channels().list(
                    part='id,contentDetails',
                    id=channel_id
                ).execute()
            
            channel_id = channels_response['items'][0]['id']
            uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            logger.info(f"Found channel ID: {channel_id}")
            
            # Get all videos from uploads playlist
            videos = []
            next_page_token = None
            
            while True:
                playlist_response = self._client().playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
                
                # Get detailed video information
                videos_response = self._client().videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(video_ids)
                ).execute()
                
                for video in videos_response['items']:
                    try:
                        duration = isodate.parse_duration(video['contentDetails']['duration'])
                        upload_date = datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', '+00:00'))
                        
                        video_data = {
                            'video_id': video['id'],
                            'title': video['snippet']['title'],
                            'description': video['snippet']['description'],
                            'duration': str(duration),
                            'upload_date': upload_date,
                            'view_count': int(video['statistics'].get('viewCount', 0)),
                            'transcript_processed': False
                        }
                        videos.append(video_data)
                        
                    except Exception as e:
                        logger.error(f"Error processing video {video['id']}: {str(e)}")
                        continue
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
                    
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            logger.info(f"Found {len(videos)} videos from channel")
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error fetching channel videos: {str(e)}")
            raise
    
    async def get_video_captions(self, video_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get video captions/transcripts"""
        try:
            # Get available caption tracks
            captions_response = self._client().captions().list(
                part='snippet',
                videoId=video_id
            ).execute()
            
            if not captions_response.get('items'):
                logger.warning(f"No captions found for video {video_id}")
                return None
            
            # Priority: Hindi -> English -> Auto-generated
            caption_priorities = ['hi', 'en', 'a.hi', 'a.en']
            selected_caption = None
            
            for priority_lang in caption_priorities:
                for caption in captions_response['items']:
                    if caption['snippet']['language'] == priority_lang:
                        selected_caption = caption
                        break
                if selected_caption:
                    break
            
            if not selected_caption:
                # Take the first available caption
                selected_caption = captions_response['items'][0]
            
            caption_id = selected_caption['id']
            language = selected_caption['snippet']['language']
            
            # Download caption content
            caption_content = self._client().captions().download(
                id=caption_id,
                tfmt='srv3'  # Timed text format with timestamps
            ).execute()
            
            # Parse the caption content to extract segments with timestamps
            segments = self._parse_caption_content(caption_content, language)
            
            logger.info(f"Retrieved {len(segments)} caption segments for video {video_id}")
            return segments
            
        except HttpError as e:
            if e.resp.status == 403:
                logger.warning(f"Captions not accessible for video {video_id} (possibly disabled)")
            else:
                logger.error(f"YouTube API error getting captions for {video_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error getting captions for video {video_id}: {str(e)}")
            return None
    
    def _parse_caption_content(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Parse caption content to extract timestamped segments"""
        segments = []
        
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            
            for text_elem in root.findall('.//text'):
                start = float(text_elem.get('start', 0))
                duration = float(text_elem.get('dur', 3))
                end = start + duration
                text = text_elem.text or ""
                
                if text.strip():
                    segments.append({
                        'start_time': start,
                        'end_time': end,
                        'text': text.strip(),
                        'language': language
                    })
                    
        except Exception as e:
            logger.error(f"Error parsing caption content: {str(e)}")
            # Fallback: treat as plain text
            if content.strip():
                segments.append({
                    'start_time': 0,
                    'end_time': 300,  # Default 5 minutes
                    'text': content.strip(),
                    'language': language
                })
        
        return segments