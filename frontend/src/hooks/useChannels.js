import { useEffect, useState } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const CHANNEL_KEY = 'preferredChannel';

const FALLBACK_CHANNELS = [
  { id: 'all', name: 'All channels', name_hi: 'सभी चैनल' },
  { id: 'bhajanmarg', name: 'Bhajan Marg', name_hi: 'भजन मार्ग' },
  { id: 'meditation', name: 'Meditation', name_hi: 'ध्यान' },
  { id: 'philosophy', name: 'Philosophy', name_hi: 'दर्शन' },
  { id: 'peace', name: 'Peace & Healing', name_hi: 'शांति' },
];

export const useChannels = () => {
  const [channels, setChannels] = useState(FALLBACK_CHANNELS);
  const [channelId, setChannelId] = useState(() => {
    try {
      return localStorage.getItem(CHANNEL_KEY) || 'all';
    } catch (error) {
      return 'all';
    }
  });

  useEffect(() => {
    let cancelled = false;
    fetch(`${API}/channels`)
      .then((response) => response.json())
      .then((data) => {
        if (!cancelled && Array.isArray(data.channels) && data.channels.length > 0) {
          setChannels(data.channels);
        }
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(CHANNEL_KEY, channelId);
    } catch (error) {
      // ignore quota / private mode
    }
  }, [channelId]);

  return { channels, channelId, setChannelId };
};
