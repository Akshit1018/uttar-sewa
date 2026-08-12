import { Play, ExternalLink } from 'lucide-react';
import { Button } from './ui/button';
import { buildWatchUrl, buildYoutubeHomeUrl, formatTimestamp } from '../lib/youtube';

export function VideoTimestampLink({ videoId, startTime, timestampUrl, label, className }) {
  const href = timestampUrl || buildWatchUrl(videoId, startTime);
  if (!href) {
    return null;
  }

  return (
    <Button asChild className={className}>
      <a href={href} target="_blank" rel="noopener noreferrer">
        <Play className="w-4 h-4 mr-2" />
        {label || formatTimestamp(startTime)}
      </a>
    </Button>
  );
}

export function VideoHomeLink({ videoId, youtubeUrl, label, className }) {
  const href = youtubeUrl || buildYoutubeHomeUrl(videoId);
  if (!href) {
    return null;
  }

  return (
    <Button asChild variant="outline" className={className}>
      <a href={href} target="_blank" rel="noopener noreferrer">
        <ExternalLink className="w-4 h-4 mr-2" />
        {label}
      </a>
    </Button>
  );
}
