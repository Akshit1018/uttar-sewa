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

export const BACKEND_URL = resolveBackendUrl(process.env.REACT_APP_BACKEND_URL);
export const API = `${BACKEND_URL}/api`;
