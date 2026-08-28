export const BACKEND_URL_STORAGE_KEY = 'uttar_sewa_backend_url';

export function readStoredBackendUrl() {
  if (typeof window === 'undefined') {
    return '';
  }
  try {
    return String(window.localStorage.getItem(BACKEND_URL_STORAGE_KEY) || '').trim();
  } catch (error) {
    return '';
  }
}

export function writeStoredBackendUrl(url) {
  const cleaned = String(url || '').trim();
  try {
    if (!cleaned) {
      window.localStorage.removeItem(BACKEND_URL_STORAGE_KEY);
      return '';
    }
    window.localStorage.setItem(BACKEND_URL_STORAGE_KEY, cleaned);
    return cleaned;
  } catch (error) {
    return cleaned;
  }
}

export function resolveBackendUrl(configured, origin) {
  let raw = String(configured || '').trim().replace(/\/$/, '');
  if (raw.endsWith('/api')) {
    raw = raw.slice(0, -4).replace(/\/$/, '');
  }
  if (!raw || raw === 'undefined' || raw === 'null') {
    const page = String(origin || (typeof window !== 'undefined' ? window.location.origin : '')).replace(/\/$/, '');
    if (page && page !== 'null' && page !== 'undefined' && !page.startsWith('file:')) {
      return page;
    }
    return 'http://127.0.0.1:8000';
  }
  return raw;
}

export const BACKEND_URL = resolveBackendUrl(
  readStoredBackendUrl() || process.env.REACT_APP_BACKEND_URL
);
export const API = `${BACKEND_URL}/api`;
