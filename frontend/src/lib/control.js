const TOKEN_KEY = 'controlToken';

export function readControlToken() {
  try {
    return String(localStorage.getItem(TOKEN_KEY) || '').trim();
  } catch (error) {
    return '';
  }
}

export function writeControlToken(value) {
  const token = String(value || '').trim();
  try {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  } catch (error) {
    // private mode
  }
  return token;
}

export function controlHeaders(extra = {}) {
  const headers = { 'Content-Type': 'application/json', ...extra };
  const token = readControlToken();
  if (token) {
    headers['X-Control-Token'] = token;
  }
  return headers;
}
