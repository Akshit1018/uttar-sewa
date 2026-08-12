export function normalizeStartSeconds(startTime) {
  const seconds = Math.floor(Number(startTime) || 0);
  return Number.isFinite(seconds) ? Math.max(0, seconds) : 0;
}

export function buildWatchUrl(videoId, startTime) {
  if (!videoId) return '';
  return `https://www.youtube.com/watch?v=${encodeURIComponent(videoId)}&t=${normalizeStartSeconds(startTime)}`;
}

export function buildYoutubeHomeUrl(videoId) {
  if (!videoId) return '';
  return `https://www.youtube.com/watch?v=${encodeURIComponent(videoId)}`;
}

export function formatTimestamp(seconds) {
  const total = normalizeStartSeconds(seconds);
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const secs = total % 60;
  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`;
}
