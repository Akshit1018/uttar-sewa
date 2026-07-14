"""
Video Timestamp Service
Handles proper video redirection with exact timestamp positioning
"""

import logging
from typing import Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

class VideoTimestampService:
    def __init__(self):
        self.youtube_base_url = "https://www.youtube.com/watch"
        self.youtube_mobile_url = "https://m.youtube.com/watch"
        self.youtube_app_url = "youtube://watch"
    
    def generate_timestamp_urls(self, video_id: str, start_time: float, end_time: Optional[float] = None) -> Dict[str, str]:
        """Generate different types of video URLs with timestamps"""
        
        start_seconds = int(start_time)
        
        urls = {
            # Standard web URL with timestamp
            'web_url': f"{self.youtube_base_url}?v={video_id}&t={start_seconds}s",
            
            # Mobile web URL with timestamp  
            'mobile_web_url': f"{self.youtube_mobile_url}?v={video_id}&t={start_seconds}s",
            
            # YouTube app deep link
            'app_url': f"{self.youtube_app_url}?v={video_id}&t={start_seconds}s",
            
            # Basic video URL without timestamp
            'basic_url': f"{self.youtube_base_url}?v={video_id}",
            
            # Embed URL with autoplay and timestamp
            'embed_url': f"https://www.youtube.com/embed/{video_id}?start={start_seconds}&autoplay=1"
        }
        
        # Add end time if provided (for video segments)
        if end_time:
            end_seconds = int(end_time)
            urls['web_url_with_end'] = f"{self.youtube_base_url}?v={video_id}&t={start_seconds}s&end={end_seconds}s"
            urls['embed_url_with_end'] = f"https://www.youtube.com/embed/{video_id}?start={start_seconds}&end={end_seconds}&autoplay=1"
        
        return urls
    
    def generate_mobile_friendly_link(self, video_id: str, start_time: float) -> str:
        """Generate mobile-friendly video link that tries app first, then web"""
        start_seconds = int(start_time)
        
        # This will be handled in the frontend JavaScript
        # Returns the web URL, frontend will handle app detection
        return f"{self.youtube_base_url}?v={video_id}&t={start_seconds}s"
    
    def format_timestamp_display(self, seconds: float) -> str:
        """Format timestamp for display (MM:SS or HH:MM:SS)"""
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def create_video_metadata(self, qa_item: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive video metadata for frontend"""
        
        video_id = qa_item.get('video_id', '')
        start_time = qa_item.get('start_time', 0)
        end_time = qa_item.get('end_time')
        
        if not video_id:
            logger.error("No video_id provided in Q&A item")
            return {}
        
        # Generate all URL variants
        urls = self.generate_timestamp_urls(video_id, start_time, end_time)
        
        # Create metadata
        metadata = {
            'video_id': video_id,
            'start_time': start_time,
            'end_time': end_time,
            'formatted_start_time': self.format_timestamp_display(start_time),
            'urls': urls,
            'primary_url': urls['web_url'],  # Main URL to use
            'mobile_url': urls['mobile_web_url'],
            'app_url': urls['app_url'],
            'embed_url': urls['embed_url'],
            
            # Frontend JavaScript code for mobile handling
            'mobile_redirect_code': self._generate_mobile_redirect_js(video_id, start_time),
            
            # Display information
            'duration_text': self._calculate_duration_text(start_time, end_time),
            'video_segment_info': {
                'start': self.format_timestamp_display(start_time),
                'end': self.format_timestamp_display(end_time) if end_time else None,
                'duration': self.format_timestamp_display(end_time - start_time) if end_time else None
            }
        }
        
        return metadata
    
    def _generate_mobile_redirect_js(self, video_id: str, start_time: float) -> str:
        """Generate JavaScript code for smart mobile redirection"""
        start_seconds = int(start_time)
        
        js_code = f"""
        function openVideoAtTimestamp() {{
            const videoId = '{video_id}';
            const startTime = {start_seconds};
            
            // Try to detect if we're on mobile
            const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
            
            if (isMobile) {{
                // Try YouTube app first
                const appUrl = `youtube://watch?v=${{videoId}}&t=${{startTime}}s`;
                const webUrl = `https://www.youtube.com/watch?v=${{videoId}}&t=${{startTime}}s`;
                
                // Create hidden iframe to trigger app
                const iframe = document.createElement('iframe');
                iframe.style.display = 'none';
                iframe.src = appUrl;
                document.body.appendChild(iframe);
                
                // Fallback to web after delay
                setTimeout(() => {{
                    window.open(webUrl, '_blank');
                    document.body.removeChild(iframe);
                }}, 1000);
            }} else {{
                // Desktop: open in new tab
                const webUrl = `https://www.youtube.com/watch?v=${{videoId}}&t=${{startTime}}s`;
                window.open(webUrl, '_blank', 'noopener,noreferrer');
            }}
        }}
        openVideoAtTimestamp();
        """
        
        return js_code.strip()
    
    def _calculate_duration_text(self, start_time: float, end_time: Optional[float]) -> str:
        """Calculate human-readable duration text"""
        if end_time:
            duration = end_time - start_time
            if duration < 60:
                return f"{int(duration)} seconds"
            elif duration < 3600:
                minutes = int(duration / 60)
                return f"{minutes} minute{'s' if minutes != 1 else ''}"
            else:
                hours = int(duration / 3600)
                return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return "Full segment"
    
    def validate_video_url(self, url: str) -> bool:
        """Validate if the URL is a proper YouTube URL"""
        youtube_patterns = [
            r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'youtu\.be/([a-zA-Z0-9_-]+)',
            r'youtube\.com/embed/([a-zA-Z0-9_-]+)'
        ]
        
        return any(re.search(pattern, url) for pattern in youtube_patterns)
    
    def extract_video_id_from_url(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'youtu\.be/([a-zA-Z0-9_-]+)',
            r'youtube\.com/embed/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

# Global instance
video_timestamp_service = VideoTimestampService()